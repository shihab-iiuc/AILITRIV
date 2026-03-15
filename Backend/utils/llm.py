from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

def get_gpt_oss_120b():
    """Returns a ChatOpenAI instance configured for GPT-OSS-120B on Groq."""
    return ChatOpenAI(
        model="openai/gpt-oss-120b",
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
        temperature=0.7,
        max_tokens=1024,
    )

def get_llama_3_3_70b():
    """Returns Llama 3.3 70B configured for RAG."""
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.1,
    )

def get_gemini_2_5_flash():
    """Returns Gemini 2.5 Flash for Search, OCR, and multimodal extraction."""
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.1,
        max_retries=0, # Fail fast onto fallbacks instead of infinitely hanging
    )

def get_llama_4_scout():
    """Returns Llama 4 Scout (or equivalent valid multimodal Groq model for preview)."""
    return ChatGroq(
        model="llama-3.2-11b-vision-instruct", # Updated to non-preview model
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.1,
    )

def get_llama_4_scout_17b():
    """Returns the requested Llama 4 Scout 17B model."""
    return ChatOpenAI(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
        temperature=0.1,
        max_tokens=2048,
    )

def get_fallback_chain(primary, secondaries):
    """Creates a LangChain fallback sequence."""
    chain = primary
    for secondary in secondaries:
        chain = chain.with_fallbacks([secondary])
    return chain

def get_llm():
    """Alias for Llama 3.3 70B used by RAG."""
    return get_llama_3_3_70b()

def get_rag_primary():
    return get_llama_3_3_70b()

def get_rag_fallback():
    return get_gpt_oss_120b()

def invoke_llm_with_fallback(primary_llm, fallback_llm, messages, stream=True):
    llms_to_try = [primary_llm, fallback_llm]
    last_exception = None
    
    for llm in llms_to_try:
        try:
            if stream:
                stream_iter = llm.stream(messages)
                yielded_any = False
                for chunk in stream_iter:
                    if chunk.content:
                        yield chunk
                        yielded_any = True
                if yielded_any:
                    return
            else:
                return llm.invoke(messages)
        except Exception as e:
            last_exception = e
            continue
            
    if isinstance(last_exception, Exception):
        raise last_exception
    elif last_exception:
        raise Exception(str(last_exception))
