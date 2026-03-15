import streamlit as st
import sys
import os
from pathlib import Path

# Add project root to sys.path for backend imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Backend.agents.search_agent import search_stream
from Backend.agents.rag_agent import build_vector_store, ask_stream, get_retrieved_chunks
from Backend.agents.ocr_agent import get_ocr_stream
from Backend.utils.styles import get_custom_css

# ---- Page Config ----
st.set_page_config(
    page_title="AILITRIV",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---- Premium CSS ----
st.markdown(f"<style>{get_custom_css()}</style>", unsafe_allow_html=True)

# ---- Hero Header ----
st.markdown(
    '<div style="padding-top: 2rem; margin-bottom: 3rem;">'
    '<h1 class="hero-title">AILITRIV</h1>'
    '<p class="hero-subtitle">'
    'Your intelligent co-pilot for academic literature review. '
    '<span>Search</span> the web, <span>Query</span> documents, '
    'or <span>Extract</span> text from images.'
    '</p>'
    '</div>',
    unsafe_allow_html=True,
)

def render_chunks(chunks):
    """Renders retrieved chunks with relevance scores and metadata."""
    for i, chunk in enumerate(chunks, 1):
        relevance = chunk.get("relevance", 0)
        score = chunk.get("score", 0)
        source = chunk.get("source", "Unknown")
        page = chunk.get("page")

        if relevance >= 60:
            color_class = "relevance-high"
        elif relevance >= 40:
            color_class = "relevance-mid"
        else:
            color_class = "relevance-low"

        page_info = f" · Page {page + 1}" if page is not None else ""
        st.markdown(
            f'<div class="chunk-header">'
            f'<strong style="color:var(--primary);">Chunk {i}</strong>'
            f'<span class="chunk-meta">'
            f'<span class="{color_class}">▲ {relevance}%</span>'
            f' · Dist {score:.3f}'
            f'{page_info}'
            f' · {source}'
            f'</span></div>',
            unsafe_allow_html=True,
        )
        st.code(chunk["content"], language=None)
        if i < len(chunks):
            st.divider()

# ---- Sidebar ----
with st.sidebar:
    # Branding
    st.markdown(
        '<div style="text-align:center; padding: 1.5rem 0;">'
        '<div style="font-size:3rem; margin-bottom: 10px;">🔬</div>'
        '<div style="font-family:\'Space Grotesk\',sans-serif; font-size:1.6rem; '
        'font-weight:800; background:linear-gradient(135deg,#818cf8,#a78bfa,#60a5fa); '
        '-webkit-background-clip:text; -webkit-text-fill-color:transparent;">'
        'AILITRIV'
        '</div>'
        '<div style="font-size:0.7rem; color:var(--text-muted); margin-top:4px; letter-spacing:2px; font-weight:600;">'
        'PRECISION RESEARCH'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.divider()
    
    st.markdown(
        '<div style="font-size:1.72rem; font-weight:700; color:var(--text-muted); '
        'letter-spacing:1.2px; text-transform:uppercase; margin-bottom:12px;">'
        '📁 KNOWLEDGE SOURCE'
        '</div>',
        unsafe_allow_html=True,
    )

    # Combined Knowledge Uploader
    all_files = st.file_uploader(
        "Upload Image/PDF/TXT", 
        type=["pdf", "txt", "png", "jpg", "jpeg"], 
        accept_multiple_files=True, 
        label_visibility="collapsed"
    )

    # Categorize files
    image_files = [f for f in all_files if f.type.startswith("image/")]
    doc_files = [f for f in all_files if not f.type.startswith("image/")]

    # ---- Automatic Routing Logic ----
    if image_files:
        agent_choice = "OCR"
        # Take the first image for OCR (as per previous behavior)
        st.session_state.ocr_image = image_files[0].getvalue()
    elif doc_files:
        agent_choice = "RAG"
        
        # Automatic Processing Logic
        current_files_names = [f.name for f in doc_files]
        if "last_indexed_files" not in st.session_state or st.session_state.last_indexed_files != current_files_names:
            with st.spinner("Auto-indexing research papers..."):
                try:
                    st.session_state.vector_store = build_vector_store(doc_files)
                    st.session_state.last_indexed_files = current_files_names
                    st.success("Indexed!")
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        agent_choice = "Search"

    # Active Agent Display
    st.markdown(
        f'<div class="active-agent-card">'
        f'<div style="font-size: 0.65rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px;">System Status</div>'
        f'<div style="font-size: 1.1rem; font-weight: 700; color: var(--primary); margin-top: 4px;">'
        f'{"🔍 Search Agent" if agent_choice == "Search" else "📄 RAG Agent" if agent_choice == "RAG" else "🖼️ OCR Agent"}'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    # Status Indicators
    st.markdown(
        '<div style="font-size:0.72rem; font-weight:700; color:var(--text-muted); '
        'letter-spacing:1.2px; text-transform:uppercase; margin: 20px 0 12px 0;">'
        '📡 SYSTEM STATUS'
        '</div>',
        unsafe_allow_html=True,
    )
    
    if agent_choice == "Search":
        st.info("Web Retrieval Active — Grounding answers in real-world data.")
    elif agent_choice == "RAG":
        if "vector_store" in st.session_state:
            st.success("Knowledge Base Ready — Researching uploaded context.")
        else:
            st.warning("Upload documents to activate RAG.")
    elif agent_choice == "OCR":
        if "ocr_image" in st.session_state:
            st.success("Visual Context Ready — Analyst mode activated.")
        else:
            st.warning("Upload an image to start OCR.")

    st.divider()

    # Actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.search_messages = []
            st.session_state.rag_messages = []
            st.session_state.ocr_messages = []
            st.rerun()

    current_key = (
        "search_messages" if agent_choice == "Search" 
        else "rag_messages" if agent_choice == "RAG" 
        else "ocr_messages"
    )
    
    if current_key in st.session_state and st.session_state[current_key]:
        chat_export = ""
        for msg in st.session_state[current_key]:
            role = "You" if msg["role"] == "user" else f"Assistant ({msg.get('agent', agent_choice)})"
            chat_export += f"**{role}:**\n{msg['content']}\n\n---\n\n"
        with col2:
            st.download_button(
                "📥 Export",
                data=chat_export,
                file_name=f"chat_{agent_choice.lower()}.md",
                mime="text/markdown",
                use_container_width=True
            )

    # Footer
    st.markdown(
        '<div style="margin-top: 2rem; padding-bottom: 1.5rem; font-size: 0.65rem; '
        'color: var(--text-muted); text-align: center; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 1rem;">'
        'ENGINEERED FOR EXCELLENCE<br>'
        'Powered by Gemini · Llama 3.3 · GPT-OSS'
        '</div>',
        unsafe_allow_html=True,
    )

# ---- Initialize Chat History ----
for key in ("search_messages", "rag_messages", "ocr_messages"):
    if key not in st.session_state:
        st.session_state[key] = []

messages = (
    st.session_state.search_messages if agent_choice == "Search" 
    else st.session_state.rag_messages if agent_choice == "RAG"
    else st.session_state.ocr_messages
)

# ---- Display Chat History ----
for message in messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            agent_label = message.get("agent", agent_choice)
            badge_cls = "badge-search" if agent_label == "Search" else "badge-rag" if agent_label == "RAG" else "badge-ocr"
            icon = "🔍" if agent_label == "Search" else "📄" if agent_label == "RAG" else "🖼️"
            st.markdown(
                f'<span class="agent-badge {badge_cls}">{icon} {agent_label}</span>',
                unsafe_allow_html=True,
            )
        st.markdown(message["content"])
        if message.get("chunks"):
            with st.expander("🔎 Retrieved Context Snippets"):
                render_chunks(message["chunks"])

# ---- Handle User Input ----
if prompt := st.chat_input("Connect thoughts..."):
    messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        agent_label = agent_choice
        badge_cls = "badge-search" if agent_label == "Search" else "badge-rag" if agent_label == "RAG" else "badge-ocr"
        icon = "🔍" if agent_label == "Search" else "📄" if agent_label == "RAG" else "🖼️"
        st.markdown(
            f'<span class="agent-badge {badge_cls}">{icon} {agent_label}</span>',
            unsafe_allow_html=True,
        )

        try:
            if agent_choice == "Search":
                response = st.write_stream(search_stream(prompt, messages[:-1]))
                messages.append({"role": "assistant", "content": response, "agent": "Search"})

            elif agent_choice == "RAG":
                if "vector_store" not in st.session_state:
                    response = "⚠️ Please upload and process documents in the sidebar first."
                    st.warning(response)
                    messages.append({"role": "assistant", "content": response, "agent": "RAG"})
                else:
                    chunks = get_retrieved_chunks(prompt, st.session_state.vector_store)
                    response = st.write_stream(ask_stream(prompt, st.session_state.vector_store, messages[:-1]))
                    with st.expander("🔎 Retrieved Context Snippets"):
                        render_chunks(chunks)
                    messages.append({
                        "role": "assistant", 
                        "content": response, 
                        "agent": "RAG",
                        "chunks": chunks
                    })

            elif agent_choice == "OCR":
                if "ocr_image" not in st.session_state:
                    response = "⚠️ Please upload an image in the sidebar first."
                    st.warning(response)
                    messages.append({"role": "assistant", "content": response, "agent": "OCR"})
                else:
                    response = st.write_stream(get_ocr_stream(st.session_state.ocr_image, prompt))
                    messages.append({"role": "assistant", "content": response, "agent": "OCR"})

        except Exception as e:
            st.error(f"❌ System Error: {str(e)}")
