import streamlit as st
import time
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
if os.path.exists('.env.example'):
    load_dotenv('.env.example')

st.set_page_config(page_title="WebScraper AI Pro", layout="wide")

from scraper import SmartWebScraper, ScrapedPage, AIChat, is_groq_configured

# ENHANCED UI WITH BETTER DROPDOWN HANDLING
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Base Styles */
    .block-container { 
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
        max-width: 1200px !important;
    }
    
    header[data-testid="stHeader"] { display: none !important; }
    #MainMenu, footer { visibility: hidden; }
    
    * { font-family: 'Inter', sans-serif; }
    
    /* Enhanced Background */
    .stApp {
        background: linear-gradient(135deg, #fff7ed 0%, #ffffff 50%, #fef2f2 100%);
        background-attachment: fixed;
    }
    
    /* Hero Section */
    .hero-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        margin-bottom: 3rem;
        padding: 3rem 2rem;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.5);
    }
    
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        background: #fff7ed;
        border: 1px solid #fed7aa;
        border-radius: 100px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 10px rgba(251, 146, 60, 0.1);
    }
    
    .hero-title {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
        line-height: 1.1 !important;
        margin-bottom: 1.5rem !important;
        background: linear-gradient(135deg, #1e293b 0%, #475569 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-title span {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        font-size: 1.25rem !important;
        color: #64748b !important;
        max-width: 700px;
        margin: 0 auto !important;
        line-height: 1.7 !important;
        text-align: center !important;
    }
    
    /* Enhanced Input Card */
    .input-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 15px 35px -5px rgba(0, 0, 0, 0.08);
        margin-bottom: 3rem;
    }
    
    /* Form Elements with Better Dropdown Handling */
    .stTextInput input, .stNumberInput input, .stTextArea textarea {
        background: white !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        font-size: 1rem !important;
        color: #1e293b !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02) !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
        border-color: #f97316 !important;
        box-shadow: 0 0 0 4px rgba(249, 115, 22, 0.1) !important;
    }
    
    /* Spinner Text - Black */
    .stSpinner > div {
        color: #000000 !important;
    }
    
    .stSpinner > div > div {
        border-top-color: #000000 !important;
    }
    
    /* CUSTOM DROPDOWN STYLING */
    .custom-selectbox {
        position: relative;
    }
    
    .custom-selectbox > div {
        background: white !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        font-size: 1rem !important;
        color: #1e293b !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02) !important;
        transition: all 0.2s ease !important;
    }
    
    .custom-selectbox > div:hover {
        border-color: #f97316 !important;
        box-shadow: 0 0 0 4px rgba(249, 115, 22, 0.1) !important;
    }
    
    .custom-selectbox > div:focus-within {
        border-color: #f97316 !important;
        box-shadow: 0 0 0 4px rgba(249, 115, 22, 0.1) !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 16px 32px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        width: 100% !important;
        box-shadow: 0 10px 20px -5px rgba(249, 115, 22, 0.2) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 15px 30px -5px rgba(249, 115, 22, 0.3) !important;
    }
    
    /* Stats Cards */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-bottom: 3rem;
    }
    
    .stat-card {
        background: white;
        padding: 1.75rem;
        border-radius: 20px;
        border: 1px solid #f1f5f9;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
        border-color: #fed7aa;
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 0.25rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Chat Container */
    .chat-container {
        background: white;
        border-radius: 20px;
        border: 1px solid #f1f5f9;
        overflow: hidden;
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05);
    }
    
    .chat-header {
        padding: 1.5rem;
        border-bottom: 1px solid #f1f5f9;
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(10px);
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .chat-messages {
        height: 500px;
        overflow-y: auto;
        padding: 2rem;
        background: #f8fafc;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }
    
    .message {
        display: flex;
        gap: 1rem;
        max-width: 85%;
        animation: slideIn 0.3s ease;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .message.user {
        align-self: flex-end;
        flex-direction: row-reverse;
    }
    
    .message-avatar {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        overflow: hidden;
        flex-shrink: 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        background: white;
        padding: 2px;
    }
    
    .message-avatar img {
        width: 100%;
        height: 100%;
        border-radius: 10px;
    }
    
    .message-bubble {
        padding: 1.25rem 1.5rem;
        border-radius: 18px;
        font-size: 1rem;
        line-height: 1.6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    
    .message.user .message-bubble {
        background: #1e293b;
        color: white;
        border-bottom-right-radius: 6px;
    }
    
    .message.ai .message-bubble {
        background: white;
        color: #475569;
        border: 1px solid #e2e8f0;
        border-bottom-left-radius: 6px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.7);
        padding: 8px;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.3);
        gap: 8px;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        color: #94a3b8;
        background: transparent;
        border: none;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        color: #f97316;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    
    /* Status Dot */
    .status-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
    }
    
    .status-active {
        background: #22c55e;
        box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.1);
    }
    
    .status-inactive {
        background: #ef4444;
        box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.1);
    }
    
    /* Progress Bar */
    .progress-container {
        margin-top: 1.5rem;
        padding: 1.5rem;
        background: #f8fafc;
        border-radius: 16px;
        border: 1px solid #f1f5f9;
    }
</style>
""", unsafe_allow_html=True)

# DiceBear Avatars
USER_AVATAR = "https://api.dicebear.com/7.x/lorelei/svg?seed=user&backgroundColor=f3f4f6"
AI_AVATAR = "https://api.dicebear.com/7.x/bottts/svg?seed=ai&backgroundColor=fed7aa"

# Session
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
<div class="hero-container">
    <div class="hero-badge">
        <span class="status-dot {'status-active' if groq_ok else 'status-inactive'}"></span>
        <span style="font-weight: 600; font-size: 0.9rem; color: #9a3412;">
            {'AI System Operational' if groq_ok else 'AI System Offline'}
        </span>
    </div>
    <h1 class="hero-title">Web<span>Scraper</span> AI Pro</h1>
    <p class="hero-subtitle">Transform any website into structured data and intelligent conversations.<br>
    Powered by advanced AI to understand context and meaning.</p>
</div>
''', unsafe_allow_html=True)

# Input Section - No extra card wrapper

col1, col2 = st.columns([2, 1])

with col1:
    mode = st.session_state.get('mode_select', "Single Page")
    
    if mode == "Multiple URLs":
        urls_input = st.text_area(
            "Target URLs (One per line)",
            placeholder="https://example.com/page1\nhttps://example.com/page2",
            height=120
        )
    else:
        url = st.text_input("Target URL", placeholder="https://example.com")

with col2:
    # Using a custom class for better dropdown styling
    st.markdown('<label style="font-weight: 600; font-size: 0.9rem; color: #1e293b; margin-bottom: 0.5rem; display: block;">Extraction Mode</label>', unsafe_allow_html=True)
    mode = st.selectbox(
        "Extraction Mode",
        ["Single Page", "Full Website", "Multiple URLs", "Quick Scan"],
        key="mode_select",
        label_visibility="collapsed"
    )

if mode == "Full Website":
    st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
    max_pages = st.slider("Maximum Pages", 5, 50, 10)

st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)

if st.button("🚀 Start Extraction Process", use_container_width=True):
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
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.75rem;">
                    <span style="font-weight: 600; color: #000000;">Processing Content...</span>
                    <span style="color: #f97316; font-weight: 600;">{int((count/total)*100)}%</span>
                </div>
                <div style="background: #e2e8f0; height: 8px; border-radius: 4px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #f97316, #ea580c); height: 100%; width: {(count/total)*100}%; transition: width 0.5s ease;"></div>
                </div>
                <div style="margin-top: 0.75rem; font-size: 0.9rem; color: #64748b; font-family: monospace; text-align: center;">{curr}</div>
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
                st.success(f"Successfully extracted {len(pages)} pages")
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
                st.success(f"Successfully extracted {len(st.session_state.pages)} pages")

        elif mode == "Single Page":
            with st.spinner("Extracting content..."):
                try:
                    scraper = SmartWebScraper()
                    page = scraper.scrape_single_page(url)
                    if page:
                        st.session_state.pages = {url: page}
                        st.session_state.content = page.content
                        st.session_state.ai = AIChat(page.content) if groq_ok else None
                        st.success("Extraction complete")
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
                    st.success("Scan complete")
                except Exception as e:
                    st.error(f"Error: {str(e)}")



# Results
if st.session_state.pages:
    pages = list(st.session_state.pages.values())
    
    # Stats
    st.markdown('<div class="stats-grid">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'''
        <div class="stat-card">
            <div class="stat-value">{len(pages)}</div>
            <div class="stat-label">Pages Extracted</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="stat-card">
            <div class="stat-value">{sum(p.word_count for p in pages):,}</div>
            <div class="stat-label">Total Words</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="stat-card">
            <div class="stat-value">{len(set(p.content_type for p in pages))}</div>
            <div class="stat-label">Content Types</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🤖 AI Assistant", "📄 Content Explorer", "💾 Export Data"])
    
    with tab1:
        if groq_ok:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            
            # Chat Header
            st.markdown(f'''
            <div class="chat-header">
                <div style="width: 12px; height: 12px; background: #22c55e; border-radius: 50%; box-shadow: 0 0 0 3px rgba(34,197,94,0.2);"></div>
                <span style="font-weight: 600; color: #1e293b;">AI Assistant Online</span>
        <img src="{AI_AVATAR}" style="width:24px;height:24px;border-radius:50%;margin-left:8px;" alt="AI Avatar"/>
                <span style="margin-left: auto; font-size: 0.85rem; color: #94a3b8; background: #f1f5f9; padding: 4px 12px; border-radius: 100px;">{os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")}</span>
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
                <div style="text-align: center; padding: 4rem 2rem;">
                    <div style="width: 72px; height: 72px; background: #fff7ed; border-radius: 24px; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem; box-shadow: 0 10px 25px rgba(251, 146, 60, 0.1);">
                        <span style="font-size: 2.5rem;">🤖</span>
                    </div>
                    <h3 style="color: #1e293b; font-weight: 700; margin-bottom: 0.75rem;">AI Assistant Ready</h3>
                    <p style="color: #94a3b8; margin: 0; font-size: 1.1rem;">Ask me anything about the extracted content.</p>
                </div>
                '''
            
            st.markdown(f'<div class="chat-messages">{msgs_html}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Input Area
            col1, col2 = st.columns([5, 1])
            
            with col1:
                msg = st.text_input("", placeholder="Ask a question about the content...", label_visibility="collapsed")
            
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
            
            if st.button("🧹 Clear Chat History", use_container_width=True):
                st.session_state.chat = []
                if st.session_state.ai:
                    st.session_state.ai.clear()
                st.rerun()
                
        else:
            st.warning("⚠️ Configure GROQ_API_KEY in your .env file to enable AI features")
    
    with tab2:
        st.subheader("Extracted Content")
        for page in sorted(pages, key=lambda x: x.value_score, reverse=True):
            with st.expander(f"📄 {page.title} ({page.word_count} words)"):
                st.caption(f"🔗 {page.url}")
                st.text_area("", page.content[:3000], height=200, label_visibility="collapsed")
    
    with tab3:
        st.subheader("Export Options")
        col1, col2 = st.columns(2)
        
        with col1:
            fmt = st.selectbox("Format", ["JSON", "Markdown", "Text"])
        
        with col2:
            fname = st.text_input("Filename", "web_scrape_export")
        
        if st.button("📥 Download Exported Data", use_container_width=True):
            if fmt == "JSON":
                data = {"pages": [{"url": p.url, "title": p.title, "content": p.content, "word_count": p.word_count} for p in pages]}
                st.download_button(
                    "💾 Save JSON File",
                    json.dumps(data, indent=2),
                    f"{fname}.json",
                    "application/json",
                    use_container_width=True
                )
            elif fmt == "Markdown":
                md = "\n\n---\n\n".join([f"# {p.title}\n\n**URL:** {p.url}\n\n**Word Count:** {p.word_count}\n\n{p.content}" for p in pages])
                st.download_button(
                    "💾 Save Markdown File",
                    md,
                    f"{fname}.md",
                    "text/markdown",
                    use_container_width=True
                )
            else:
                st.download_button(
                    "💾 Save Text File",
                    st.session_state.content,
                    f"{fname}.txt",
                    "text/plain",
                    use_container_width=True
                )