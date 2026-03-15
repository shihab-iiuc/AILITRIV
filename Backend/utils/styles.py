def get_custom_css():
    """Returns the full premium CSS styling for AILITRIV."""
    return """
    /* ============================================================
       GOOGLE FONT IMPORT
    ============================================================ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&family=Outfit:wght@300;400;500;600;700&display=swap');

    /* ============================================================
       GLOBAL RESETS & BASE
    ============================================================ */
    :root {
        --bg-deep: #030712;
        --bg-card: rgba(17, 24, 39, 0.7);
        --primary: #6366f1;
        --primary-glow: rgba(99, 102, 241, 0.4);
        --secondary: #8b5cf6;
        --accent: #0ea5e9;
        --text-main: #f8fafc;
        --text-muted: #94a3b8;
        --border-subtle: rgba(255, 255, 255, 0.08);
        --glass-border: rgba(255, 255, 255, 0.12);
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        color: var(--text-main);
        font-size: 1.25rem !important; /* Bumped from 1.1rem */
    }

    /* Main app background — deep animated architectural gradient */
    .stApp {
        background: radial-gradient(circle at 0% 0%, #0f172a 0%, #020617 100%) !important;
        background-attachment: fixed !important;
    }

    /* Floating mesh gradient decorative elements */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: 
            radial-gradient(circle at 10% 10%, rgba(99, 102, 241, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 90% 90%, rgba(139, 92, 246, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 50% 50%, rgba(14, 165, 233, 0.03) 0%, transparent 60%);
        pointer-events: none;
        z-index: -1;
    }

    /* ============================================================
       HEADER / TITLE (Glass-Card Hero)
    ============================================================ */
    .hero-title {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 800 !important;
        font-size: 3.5rem !important;
        background: linear-gradient(135deg, #fff 0%, #a5b4fc 50%, #818cf8 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        letter-spacing: -2px;
        margin-bottom: 0px !important;
        text-align: center;
        filter: drop-shadow(0 0 15px rgba(99, 102, 241, 0.3));
    }

    .hero-subtitle {
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.6rem !important; /* Bumped from 1.4rem */
        color: var(--text-muted) !important;
        text-align: center;
        max-width: 900px;
        margin: 0 auto 2.5rem !important;
        line-height: 1.6;
        letter-spacing: 0.5px;
    }

    .hero-subtitle span {
        color: #818cf8;
        font-weight: 600;
        position: relative;
    }

    /* ============================================================
       SIDEBAR (Ultra-Glass)
    ============================================================ */
    [data-testid="stSidebar"] {
        background-color: rgba(3, 7, 18, 0.6) !important;
        backdrop-filter: blur(25px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(25px) saturate(180%) !important;
        border-right: 1px solid var(--glass-border) !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.05) !important;
    }

    /* ============================================================
       CARDS & CONTAINERS
    ============================================================ */
    .active-agent-card {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 1.5rem;
        margin-top: 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }

    .active-agent-card:hover {
        transform: translateY(-3px);
        border-color: var(--primary);
    }

    /* ============================================================
       BUTTONS (Premium Rounded)
    ============================================================ */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-family: 'Outfit', sans-serif !important;
        padding: 0.6rem 1.5rem !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 1.2rem !important; /* Bumped from 1rem */
    }

    .stButton > button:hover {
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 12px 25px rgba(99, 102, 241, 0.6) !important;
    }

    /* Secondary/Clear button */
    .stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid var(--glass-border) !important;
        box-shadow: none !important;
    }

    /* ============================================================
       CHAT INTERFACE
    ============================================================ */
    [data-testid="stChatMessage"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 24px !important;
        padding: 1.2rem 1.5rem !important;
        margin-bottom: 1.2rem !important;
        backdrop-filter: blur(12px) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2) !important;
        animation: slideInUp 0.5s cubic-bezier(0.23, 1, 0.32, 1) both;
    }

    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    [data-testid="stChatMessageAvatarUser"] {
        background: linear-gradient(135deg, #4f46e5, #ec4899) !important;
        border-radius: 12px !important;
    }

    [data-testid="stChatMessageAvatarAssistant"] {
        background: linear-gradient(135deg, #0ea5e9, #8b5cf6) !important;
        border-radius: 12px !important;
    }

    /* Chat Input */
    [data-testid="stChatInput"] {
        background: rgba(17, 24, 39, 0.8) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 20px !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.5) !important;
        margin-bottom: 1rem !important;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }

    /* ============================================================
       BADGES
    ============================================================ */
    .agent-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 12px;
        border-radius: 100px;
        font-size: 1.1rem; /* Bumped from 0.85rem */
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 10px;
        border: 1px solid transparent;
    }

    .badge-search {
        background: rgba(99, 102, 241, 0.15);
        color: #a5b4fc;
        border-color: rgba(99, 102, 241, 0.3);
    }

    .badge-rag {
        background: rgba(16, 185, 129, 0.15);
        color: #6ee7b7;
        border-color: rgba(16, 185, 129, 0.3);
    }

    .badge-ocr {
        background: rgba(236, 72, 153, 0.15);
        color: #f9a8d4;
        border-color: rgba(236, 72, 153, 0.3);
    }

    /* ============================================================
       RELEVANCE CHUNKS (Expander)
    ============================================================ */
    [data-testid="stExpander"] {
        background: rgba(15, 23, 42, 0.4) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 16px !important;
    }

    .chunk-header {
        border-bottom: 1px solid var(--border-subtle);
        padding-bottom: 8px;
        margin-bottom: 10px;
    }

    .relevance-high { color: #34d399; font-weight: 800; }
    .relevance-mid  { color: #fbbf24; font-weight: 700; }
    .relevance-low  { color: #f87171; font-weight: 700; }

    /* ============================================================
       BANNER
    ============================================================ */
    .route-banner {
        background: linear-gradient(90deg, rgba(99, 102, 241, 0.1), transparent);
        border-left: 4px solid var(--primary);
        padding: 12px 20px;
        border-radius: 0 12px 12px 0;
        margin-bottom: 2rem;
    }

    .route-banner-text {
        font-size: 1.1rem; /* Increased from 0.9rem */
        color: var(--text-muted);
    }
    
    .route-banner-text strong {
        color: var(--text-main);
    }

    /* ============================================================
       FILE UPLOADER
    ============================================================ */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px dashed var(--glass-border) !important;
        border-radius: 16px !important;
    }

    /* ================= ===========================================
       SCROLLBAR
    ============================================================ */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { 
        background: rgba(255, 255, 255, 0.1); 
        border-radius: 10px; 
    }
    ::-webkit-scrollbar-thumb:hover { background: var(--primary); }
    
    header { 
        visibility: visible !important; 
        display: block !important;
        background: transparent !important;
    }

    /* ============================================================
       SIDEBAR TOGGLE BUTTON (Ensure Visibility)
    ============================================================ */
    [data-testid="stSidebarCollapseButton"] {
        background-color: var(--primary) !important;
        color: white !important;
        border-radius: 50% !important;
        margin-top: 10px !important;
        margin-left: 10px !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4) !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stSidebarCollapseButton"]:hover {
        transform: scale(1.1) !important;
        background-color: var(--secondary) !important;
    }

    /* Hide redundant Streamlit elements */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    """
