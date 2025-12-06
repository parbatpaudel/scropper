import streamlit as st
import time
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
if os.path.exists('.env.example'):
    load_dotenv('.env.example')

HERO_AVATAR = "https://api.dicebear.com/7.x/shapes/svg?seed=scraper&backgroundColor=667eea"
st.set_page_config(page_title="AI Web Scraper Pro", layout="wide", page_icon=HERO_AVATAR)

from scraper import SmartWebScraper, ScrapedPage, AIChat, is_groq_configured


# CLEAN, MODERN UI WITH WHITE BACKGROUND
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 5rem !important;
        max-width: 1100px !important;
    }
    
    header[data-testid="stHeader"] { display: none !important; }
    #MainMenu, footer { visibility: hidden; }
    
    /* Clean White Background with Subtle Pattern */
    .stApp {
        background: #fafafa;
    }
    
    /* Hero Section - Premium & Clean */
    .hero-section {
        position: relative;
        background: #fff;
        border-radius: 24px;
        padding: 3.5rem 2rem;
        margin-bottom: 2.5rem;
        border: 2px solid transparent;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
        overflow: hidden;
    }
    .hero-section::before {
        content: "";
        position: absolute;
        inset: -2px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899, #f59e0b, #3b82f6);
        background-size: 300% 300%;
        border-radius: 26px;
        animation: gradientShift 4s ease infinite;
        z-index: -1;
    }
    @keyframes gradientShift {
        0%, 100% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
    }
    
    .hero-header {
        display: flex;
        align-items: center;
        gap: 2.5rem;
    }
    
    .hero-avatar {
        width: 90px;
        height: 90px;
        border-radius: 20px;
        flex-shrink: 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transition: transform 0.3s ease;
    }
    
    .hero-avatar:hover {
        transform: scale(1.05);
    }
    
    .hero-avatar img {
        width: 100%;
        height: 100%;
        border-radius: 20px;
    }
    
    .hero-content {
        flex: 1;
    }
    
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        background: linear-gradient(135deg, #dcfce7 0%, #d1fae5 100%);
        border: 1.5px solid #86efac;
        border-radius: 100px;
        font-size: 0.875rem;
        font-weight: 600;
        color: #15803d;
        margin-bottom: 1.25rem;
        box-shadow: 0 2px 8px rgba(34, 197, 94, 0.1);
    }
    
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .input-label {
        font-weight: 600;
        font-size: 0.875rem;
        color: #374151;
        margin-bottom: 0.65rem;
        display: block;
        letter-spacing: 0.01em;
    }
    
    /* Form Elements - Polished */
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        background: #fafafa !important;
        border: 1.5px solid #e5e7eb !important;
        border-radius: 12px !important;
        padding: 13px 18px !important;
        font-size: 0.95rem !important;
        color: #0f172a !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        background: white !important;
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.08) !important;
    }
    
    
    /* Selectbox - Fix visibility issues */
    .stSelectbox > div > div {
        background: #fafafa !important;
        border: 1.5px solid #e5e7eb !important;
        border-radius: 12px !important;
        padding: 10px 16px !important;
        transition: all 0.2s ease !important;
        color: #0f172a !important;
    }
    
    /* Selected value text */
    .stSelectbox div[data-baseweb="select"] > div {
        color: #0f172a !important;
    }
    
    /* Dropdown options */
    .stSelectbox [role="option"] {
        background: #fff !important;
        color: #0f172a !important;
    }
    
    /* Selected option in dropdown */
    .stSelectbox [aria-selected="true"] {
        background: #eff6ff !important;
        color: #1e40af !important;
    }
    
    /* Hover state for options */
    .stSelectbox [role="option"]:hover {
        background: #f0f9ff !important;
        color: #0f172a !important;
    }
    
    .stSelectbox > div > div:hover,
    .stSelectbox > div > div:focus-within {
        background: white !important;
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.08) !important;
    }
    
    /* Premium Button */
    .stButton button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 16px 32px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        width: 100% !important;
        box-shadow: 0 4px 14px rgba(59, 130, 246, 0.3) !important;
        transition: all 0.2s ease !important;
        letter-spacing: 0.01em !important;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
    }
    
    .stButton button:active {
        transform: translateY(0) !important;
    }
    
    /* Stats Grid - Enhanced */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2.5rem;
    }
    
    .stat-card {
        background: white;
        padding: 2rem 1.75rem;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .stat-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.12);
        transform: translateY(-4px);
    }
    
    .stat-card:hover::before {
        opacity: 1;
    }
    
    .stat-emoji {
        font-size: 2rem;
        margin-bottom: 0.75rem;
        display: block;
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.35rem;
        line-height: 1;
    }
    
    .stat-label {
        font-size: 0.875rem;
        font-weight: 600;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Chat Container - Modern */
    .chat-container {
        background: white;
        border-radius: 20px;
        border: 1px solid #e5e7eb;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    
    .chat-header {
        padding: 1.75rem 2rem;
        background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
        border-bottom: 1px solid #e5e7eb;
        display: flex;
        align-items: center;
        gap: 1.25rem;
    }
    
    .chat-avatar {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        flex-shrink: 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    .chat-avatar img {
        width: 100%;
        height: 100%;
        border-radius: 12px;
    }
    
    .chat-info {
        flex: 1;
    }
    
    .chat-title {
        font-weight: 700;
        font-size: 1.1rem;
        color: #0f172a;
        margin-bottom: 2px;
    }
    
    .chat-subtitle {
        font-size: 0.8rem;
        color: #6b7280;
        font-weight: 500;
    }
    
    .chat-messages {
        height: 520px;
        overflow-y: auto;
        padding: 2rem;
        background: #fafafa;
    }
    
    .message {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.75rem;
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .message.user {
        flex-direction: row-reverse;
    }
    
    .message-avatar {
        width: 40px;
        height: 40px;
        border-radius: 12px;
        flex-shrink: 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    .message-avatar img {
        width: 100%;
        height: 100%;
        border-radius: 12px;
    }
    
    .message-bubble {
        max-width: 70%;
        padding: 1.15rem 1.5rem;
        border-radius: 16px;
        font-size: 0.95rem;
        line-height: 1.6;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }
    
    .message.user .message-bubble {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border-bottom-right-radius: 6px;
    }
    
    .message.ai .message-bubble {
        background: white;
        color: #374151;
        border: 1px solid #e5e7eb;
        border-bottom-left-radius: 6px;
    }
    
    /* Empty State - Beautiful */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
    }
    
    .empty-emoji {
        font-size: 4rem;
        margin-bottom: 1.5rem;
        display: block;
        opacity: 0.8;
    }
    
    .empty-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.65rem;
    }
    
    .empty-subtitle {
        font-size: 1rem;
        color: #6b7280;
        line-height: 1.6;
        max-width: 400px;
        margin: 0 auto;
    }
    
    /* Tabs - Polished */
    .stTabs [data-baseweb="tab-list"] {
        background: white;
        padding: 6px;
        border-radius: 14px;
        gap: 6px;
        margin-bottom: 2rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        color: #6b7280;
        background: transparent;
        font-size: 0.9rem;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #f9fafb;
        color: #374151;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }
    
    /* Progress Bar - Smooth */
    .progress-container {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin-top: 2rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    
    .progress-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.25rem;
    }
    
    .progress-label {
        font-weight: 700;
        color: #0f172a;
        font-size: 1rem;
    }
    
    .progress-percent {
        font-weight: 800;
        color: #3b82f6;
        font-size: 1.25rem;
    }
    
    .progress-bar {
        background: #e5e7eb;
        height: 10px;
        border-radius: 10px;
        overflow: hidden;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        height: 100%;
        transition: width 0.4s ease;
        border-radius: 10px;
    }
    
    .progress-url {
        margin-top: 1.25rem;
        font-size: 0.85rem;
        color: #6b7280;
        font-family: 'SF Mono', 'Monaco', 'Courier New', monospace;
        text-align: center;
        padding: 0.75rem 1rem;
        background: #f9fafb;
        border-radius: 10px;
        border: 1px solid #e5e7eb;
        font-weight: 500;
    }
    
    /* Content Expander - Clean */
    .streamlit-expanderHeader {
        background: white !important;
        border-radius: 12px !important;  
        border: 1px solid #e5e7eb !important;
        font-weight: 600 !important;
        padding: 1rem 1.25rem !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #3b82f6 !important;
        background: #f9fafb !important;
    }
    
    /* Scrollbar - Clean */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f3f4f6;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    
    /* Success/Error Messages */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        padding: 1rem 1.25rem !important;
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background: #3b82f6 !important;
    }
</style>
""", unsafe_allow_html=True)

# DiceBear Avatars
HERO_AVATAR = "https://api.dicebear.com/7.x/shapes/svg?seed=scraper&backgroundColor=667eea"
USER_AVATAR = "https://api.dicebear.com/7.x/avataaars/svg?seed=user&backgroundColor=f3f4f6"
AI_AVATAR = "https://api.dicebear.com/7.x/bottts-neutral/svg?seed=ai&backgroundColor=e0e7ff"
LINK_ICON = "https://api.dicebear.com/7.x/icons/svg?seed=link&icon=link"
PAGES_ICON = "https://api.dicebear.com/7.x/icons/svg?seed=pages&icon=document"
WORDS_ICON = "https://api.dicebear.com/7.x/icons/svg?seed=words&icon=text"
TYPES_ICON = "https://api.dicebear.com/7.x/icons/svg?seed=types&icon=category"

# Session State
if "pages" not in st.session_state:
    st.session_state.pages = {}
if "content" not in st.session_state:
    st.session_state.content = ""
if "urls" not in st.session_state:
    st.session_state.urls = []
if "chat" not in st.session_state:
    st.session_state.chat = []
if "ai" not in st.session_state:
    st.session_state.ai = None

groq_ok = is_groq_configured()

# Hero Section
st.markdown(f'''
<div class="hero-section">
    <div class="hero-header">
        <div class="hero-avatar">
            <img src="{HERO_AVATAR}" alt="Avatar">
        </div>
        <div class="hero-content">
            <div class="status-badge">
                <span class="status-dot"></span>
                {'AI Powered & Ready' if groq_ok else 'Configure AI to Continue'}
            </div>
            <h1 class="hero-title">AI Web Scraper Pro</h1>
            <p class="hero-subtitle">Transform any website into structured data with AI-powered intelligence. Extract, analyze, and export content from the web with unprecedented ease.</p>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

# Input Card
st.markdown('<div class="input-card">', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    mode = st.session_state.get('mode_select', "Single Page")
    
    st.markdown('<div class="input-label">🔗 Target URL</div>', unsafe_allow_html=True)
    if mode == "Multiple URLs":
        urls_input = st.text_area(
            "",
            placeholder="https://example.com/page1\nhttps://example.com/page2\nhttps://example.com/page3",
            height=120,
            label_visibility="collapsed"
        )
    else:
        url = st.text_input("", placeholder="https://example.com", label_visibility="collapsed")

with col2:
    st.markdown('<div class="input-label">⚙️ Scraping Mode</div>', unsafe_allow_html=True)
    mode = st.selectbox(
        "",
        ["Single Page", "Full Website", "Multiple URLs", "Quick Scan"],
        key="mode_select",
        label_visibility="collapsed"
    )

if mode == "Full Website":
    st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
    max_pages = st.slider("Maximum Pages to Scrape", 5, 50, 10)

st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)

if st.button("🚀 Start Scraping", use_container_width=True):
    if mode != "Multiple URLs" and not url:
        st.error("Please enter a valid URL")
    elif mode == "Multiple URLs" and not urls_input:
        st.error("Please enter at least one URL")
    else:
        st.session_state.urls = []
        st.session_state.chat = []
        st.session_state.ai = None
        progress_area = st.empty()
        
        def update_progress(curr, count, total):
            progress_area.markdown(f'''
            <div class="progress-container">
                <div class="progress-header">
                    <span class="progress-label">Processing Content...</span>
                    <span class="progress-percent">{int((count/total)*100)}%</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {(count/total)*100}%;"></div>
                </div>
                <div class="progress-url">{curr}</div>
            </div>
            ''', unsafe_allow_html=True)

        if mode == "Full Website":
            try:
                scraper = SmartWebScraper()
                def on_prog(curr, count, q, max_p):
                    st.session_state.urls.append(curr)
                    update_progress(curr, count+1, max_p)
                
                pages = scraper.scrape_website(url, max_pages, on_prog)
                st.session_state.pages = pages
                st.session_state.content = scraper.get_all_content()
                st.session_state.ai = AIChat(st.session_state.content) if groq_ok else None
                progress_area.empty()
                st.success(f"✅ Successfully extracted {len(pages)} pages")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")

        elif mode == "Multiple URLs":
            target_urls = [u.strip() for u in urls_input.split('\n') if u.strip()]
            if not target_urls:
                st.error("No valid URLs found")
            else:
                scraper = SmartWebScraper()
                st.session_state.pages = {}
                for i, target_url in enumerate(target_urls):
                    st.session_state.urls.append(target_url)
                    update_progress(target_url, i+1, len(target_urls))
                    try:
                        page = scraper.scrape_single_page(target_url)
                        if page:
                            st.session_state.pages[target_url] = page
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                
                all_content = [p.content for p in st.session_state.pages.values()]
                st.session_state.content = "\n\n".join(all_content)
                st.session_state.ai = AIChat(st.session_state.content) if groq_ok else None
                progress_area.empty()
                st.success(f"✅ Successfully extracted {len(st.session_state.pages)} pages")
                st.rerun()

        elif mode == "Single Page":
            with st.spinner("Extracting content..."):
                try:
                    scraper = SmartWebScraper()
                    page = scraper.scrape_single_page(url)
                    if page:
                        st.session_state.pages = {url: page}
                        st.session_state.content = page.content
                        st.session_state.ai = AIChat(page.content) if groq_ok else None
                        st.success("✅ Extraction complete")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        else:  # Quick Scan
            with st.spinner("Scanning..."):
                try:
                    import requests
                    from bs4 import BeautifulSoup
                    r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
                    soup = BeautifulSoup(r.text, 'html.parser')
                    for t in soup(['script', 'style']):
                        t.decompose()
                    title = soup.find('title').get_text().strip() if soup.find('title') else "Page"
                    content = soup.get_text("\n", strip=True)
                    page = ScrapedPage(
                        url=url,
                        title=title,
                        content=content,
                        content_type="page",
                        word_count=len(content.split()),
                        links_found=0,
                        scraped_at=str(datetime.now()),
                        value_score=1.0
                    )
                    st.session_state.pages = {url: page}
                    st.session_state.content = content
                    st.session_state.ai = AIChat(content) if groq_ok else None
                    st.success("✅ Scan complete")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

# Results Section
if st.session_state.pages:
    pages = list(st.session_state.pages.values())
    
    # Stats
    st.markdown('<div class="stats-grid">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'''
        <div class="stat-card">
            <span class="stat-emoji">📄</span>
            <div class="stat-value">{len(pages)}</div>
            <div class="stat-label">Pages Extracted</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="stat-card">
            <span class="stat-emoji">📝</span>
            <div class="stat-value">{sum(p.word_count for p in pages):,}</div>
            <div class="stat-label">Total Words</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="stat-card">
            <span class="stat-emoji">🏷️</span>
            <div class="stat-value">{len(set(p.content_type for p in pages))}</div>
            <div class="stat-label">Content Types</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🤖 AI Assistant", "📄 Content Explorer", "💾 Export Data"])
    
    with tab1:
        if groq_ok:
            st.markdown(f'''
            <div class="chat-container">
                <div class="chat-header">
                    <div class="chat-avatar">
                        <img src="{AI_AVATAR}">
                    </div>
                    <div>
                        <div class="chat-title">AI Assistant</div>
                        <div class="chat-subtitle">Powered by {os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")}</div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            
            # Messages
            msgs_html = ""
            if st.session_state.chat:
                for m in st.session_state.chat:
                    if m["role"] == "user":
                        msgs_html += f'''
                        <div class="message user">
                            <div class="message-avatar"><img src="{USER_AVATAR}"></div>
                            <div class="message-bubble">{m["content"]}</div>
                        </div>'''
                    else:
                        msgs_html += f'''
                        <div class="message ai">
                            <div class="message-avatar"><img src="{AI_AVATAR}"></div>
                            <div class="message-bubble">{m["content"]}</div>
                        </div>'''
            else:
                msgs_html = f'''
                <div class="empty-state">
                    <span class="empty-emoji">🤖</span>
                    <div class="empty-title">Ready to Help!</div>
                    <div class="empty-subtitle">Ask me anything about the scraped content. I can analyze, summarize, or extract specific information for you.</div>
                </div>
                '''
            
            st.markdown(f'<div class="chat-messages">{msgs_html}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Input Area
            col1, col2 = st.columns([5, 1])
            
            with col1:
                msg = st.text_input("", placeholder="Ask a question about the content...", label_visibility="collapsed", key="chat_input")
            
            with col2:
                send = st.button("Send", use_container_width=True)
            
            if send and msg:
                if not st.session_state.ai:
                    st.session_state.ai = AIChat(st.session_state.content)
                
                st.session_state.chat.append({"role": "user", "content": msg})
                
                with st.spinner("Thinking..."):
                    resp = st.session_state.ai.chat(msg)
                    st.session_state.chat.append({"role": "assistant", "content": resp})
                
                st.rerun()
            
            if st.button("🧹 Clear Chat", use_container_width=True):
                st.session_state.chat = []
                if st.session_state.ai:
                    st.session_state.ai.clear()
                st.rerun()
                
        else:
            st.warning("⚠️ Configure GROQ_API_KEY in your environment to enable AI features")
    
    with tab2:
        st.subheader("📄 Extracted Content")
        for page in sorted(pages, key=lambda x: x.value_score, reverse=True):
            with st.expander(f"📄 {page.title} ({page.word_count} words)"):
                st.caption(f"🔗 {page.url}")
                st.text_area("", page.content[:3000], height=200, label_visibility="collapsed", key=f"content_{page.url}")
    
    with tab3:
        st.subheader("💾 Export Options")
        col1, col2 = st.columns(2)
        
        with col1:
            fmt = st.selectbox("Format", ["JSON", "Markdown", "Text"])
        
        with col2:
            fname = st.text_input("Filename", "web_scrape_export")
        
        if st.button("📥 Download", use_container_width=True):
            if fmt == "JSON":
                data = {"pages": [{"url": p.url, "title": p.title, "content": p.content, "word_count": p.word_count} for p in pages]}
                st.download_button(
                    "💾 Save JSON",
                    json.dumps(data, indent=2),
                    f"{fname}.json",
                    "application/json",
                    use_container_width=True
                )
            elif fmt == "Markdown":
                md = "\n\n---\n\n".join([f"# {p.title}\n\n**URL:** {p.url}\n\n**Words:** {p.word_count}\n\n{p.content}" for p in pages])
                st.download_button(
                    "💾 Save Markdown",
                    md,
                    f"{fname}.md",
                    "text/markdown",
                    use_container_width=True
                )
            else:
                st.download_button(
                    "💾 Save Text",
                    st.session_state.content,
                    f"{fname}.txt",
                    "text/plain",
                    use_container_width=True
                )