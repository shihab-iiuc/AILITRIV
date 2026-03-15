from typing import Annotated, TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, END
from Backend.utils.llm import (
    get_gemini_2_5_flash, 
    get_gpt_oss_120b,
    get_llama_3_3_70b
)
import os
import re

class AgentState(TypedDict):
    research_topic: str
    chat_history: list
    search_results: str
    rag_results: str
    final_review: str

SYSTEM_PROMPT = (
    "You are a research assistant. Use browser_search for info. "
    "Only answer research queries, else: ' I cannot Answer it.'\n"
    "Format: Paper Title (Year) | Publisher. Summary; Tech (Models/Data); Findings.\n"
    "End with: Sources:\n- [Title](URL)"
)

def clean_chunk(text: str) -> str:
    """Cleans up any remaining citation markers and HTML tags from a chunk."""
    text = re.sub(r"【.*?】", "", text)
    text = text.replace("<br>", "\n")
    return text

class LiteratureReviewAgent:
    def __init__(self):
        # Models for Search
        self.search_primary = get_gemini_2_5_flash().bind(tools=[{"googleSearch": {}}])
        self.search_fallback = get_gpt_oss_120b().bind(tools=[{"googleSearch": {}}])
        
        # Models for Synthesis
        self.rag_primary = get_llama_3_3_70b()
        
        workflow = StateGraph(AgentState)
        workflow.add_node("search_internet", self.search_node)
        
        workflow.set_entry_point("search_internet")
        workflow.add_edge("search_internet", END)
        
        self.retrieval_graph = workflow.compile()

    def search_node(self, state: AgentState):
        topic = state["research_topic"]
        chat_history = state.get("chat_history", [])
        print(f"--- Search Agent (Multi-Fallback): {topic} ---")
        
        messages = [SystemMessage(content=SYSTEM_PROMPT)]

        if chat_history:
            for msg in chat_history[-6:]:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))

        messages.append(HumanMessage(content=topic))  
        
        # Level 1: Primary Gemini Search (Grounding)
        search_data = ""
        try:
            print("Trying Level 1: Gemini 2.5 Flash (Native Search)...")
            response = self.search_primary.invoke(messages)
            search_data = clean_chunk(response.content)
            if not search_data: raise ValueError("Empty output")
            print("[OK] Level 1 Success!")
            
        except Exception as e:
            print(f"[FAIL] Level 1 failed: {e}")
            # Level 2: Try Backup
            try:
                print("Trying Level 2: GPT-OSS-120B (Open Science)...")
                response = self.search_fallback.invoke(messages)
                search_data = "[BACKUP] Backup Search (GPT-OSS-120B):\n" + clean_chunk(response.content)
                if not search_data: raise ValueError("Empty output")
                print("[OK] Level 2 Success!")
            except Exception as backup_e:
                 last_e = backup_e
                 if "tool" in str(backup_e).lower() or "schema" in str(backup_e).lower():
                     try:
                         # Strip .bind() for a raw attempt 
                         raw_llm = self.search_fallback.bound if hasattr(self.search_fallback, 'bound') else self.search_fallback
                         response = raw_llm.invoke(messages)
                         search_data = clean_chunk(response.content)
                     except Exception as inner_e:
                         last_e = inner_e
                 if not search_data:
                     print(f"[FAIL] Level 2 failed: {last_e}")
        
        return {"search_results": search_data}

    def stream_run(self, topic: str, chat_history: list = None):
        """Executes retrieval and then STREAMS the synthesis for ultra-fast UI response."""
        initial_state = {
            "research_topic": topic,
            "chat_history": chat_history or [],
            "search_results": "",
            "rag_results": "",
            "final_review": ""
        }
        
        # 1. Fast Retrieval Pipeline
        state = self.retrieval_graph.invoke(initial_state)
        
        search_data = state.get("search_results", "")
        chat_hist = state.get("chat_history", [])

        # 2. Build Synthesis Context
        system_prompt = """AILITRIV Conversational Synthesizer. 
        You are a high-end research assistant. Your goal is to answer the user's latest query by combining your search findings (internet) and RAG results (internal docs).
        
        RULES:
        1. If the user is just saying 'hi' or general chat, be polite and offer research help.
        2. If research data is present, provide a detailed but conversational explanation.
        3. If search findings have URLs, ALWAYS include them in a '## Sources' section at the end.
        4. Maintain a professional, helpful persona.
        """
        
        messages = [SystemMessage(content=system_prompt)]
        for msg in chat_hist[-4:]:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
        
        user_prompt = f"""
        Current Query: {topic}
        
        Available Research Context:
        - Search Findings: {search_data}
        
        Please synthesize a comprehensive response.
        """
        messages.append(HumanMessage(content=user_prompt))
        
        # 3. Stream Response
        for chunk in self.rag_primary.stream(messages):
            if chunk.content:
                yield chunk.content

    def run(self, topic: str, chat_history: list = None):
        """Legacy synchronous run function (for backwards compatibility)."""
        content = ""
        for chunk in self.stream_run(topic, chat_history):
            content += chunk
        return {"final_review": content}

def search_stream(query: str, chat_history: list = None):
    agent = LiteratureReviewAgent()
    return agent.stream_run(query, chat_history)
