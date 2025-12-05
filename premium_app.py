import streamlit as st
import time
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
if os.path.exists('.env.example'):
    load_dotenv('.env.example')

st.set_page_config(page_title="WebScraper AI Premium", layout="wide")

from scraper import SmartWebScraper, ScrapedPage, AIChat, is_groq_configured

# PREMIUM UI WITH APPLE + LINEAR + STRIPE AESTHETIC
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Base Styles - Apple + Linear + Stripe Aesthetic */
    .block-container { 
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
        max-width: 1200px !important;
    }
    
    header[data-testid="stHeader"] { display: none !important; }
    #MainMenu, footer { visibility: hidden; }
    
    * { font-family: 'Inter', sans-serif; }
    
    /* Premium Glassmorphism Background */
    .stApp {
        background: linear-gradient(135deg, #fafafa 0%, #f5f5f5 50%, #f0f0f0 100%);
        background-attachment: fixed;
    }
    
    /* Hero Section with Glass Effect */
    .hero-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        margin-bottom: 3rem;
        padding: 4rem 2rem;
        background: rgba(255, 255, 255, 0.75);
        border-radius: 24px;
        box-shadow: 
            0 10px 30px rgba(0, 0, 0, 0.03),
            inset 0 0 0 1px rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        position: relative;
        overflow: hidden;
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(249, 115, 22, 0.05) 0%, transparent 70%);
        z-index: -1;
    }
    
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 10px 20px;
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.9);
        border-radius: 100px;
        margin-bottom: 2rem;
        box-shadow: 
            0 4px 15px rgba(251, 146, 60, 0.1),
            inset 0 0 0 1px rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
    }
    
    .hero-title {
        font-size: 4rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.04em !important;
        line-height: 1.05 !important;
        margin-bottom: 1.5rem !important;
        background: linear-gradient(135deg, #0f172a 0%, #334155 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        position: relative;
    }
    
    .hero-title span {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        font-size: 1.3rem !important;
        color: #64748b !important;
        max-width: 750px;
        margin: 0 auto !important;
        line-height: 1.7 !important;
        text-align: center !important;
        font-weight: 400;
    }
    
    /* Premium Input Card with Glass Effect */
    .input-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 
            0 20px 50px -10px rgba(0, 0, 0, 0.05),
            inset 0 0 0 1px rgba(255, 255, 255, 0.9);
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
    }
    
    .input-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(249, 115, 22, 0.2), transparent);
    }
    
    /* Form Elements with Premium Styling */
    .stTextInput input, .stNumberInput input, .stTextArea textarea {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 16px 18px !important;
        font-size: 1.05rem !important;
        color: #1e293b !important;
        box-shadow: 
            0 2px 8px rgba(0,0,0,0.02),
            inset 0 1px 2px rgba(0,0,0,0.03) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
        border-color: #f97316 !important;
        box-shadow: 
            0 0 0 4px rgba(249, 115, 22, 0.15),
            inset 0 1px 2px rgba(0,0,0,0.03) !important;
        outline: none;
    }
    
    /* CUSTOM DROPDOWN STYLING - FIXED APPROACH */
    .stSelectbox > div {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        box-shadow: 
            0 2px 8px rgba(0,0,0,0.02),
            inset 0 1px 2px rgba(0,0,0,0.03) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .stSelectbox > div > div {
        padding: 16px 18px !important;
        font-size: 1.05rem !important;
        color: #1e293b !important;
        background: transparent !important;
    }
    
    .stSelectbox > div:hover {
        border-color: #f97316 !important;
        box-shadow: 
            0 0 0 4px rgba(249, 115, 22, 0.15),
            inset 0 1px 2px rgba(0,0,0,0.03) !important;
    }
    
    /* Dropdown Options List */
    [data-baseweb="select"] [role="listbox"] {
        background: white !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 16px !important;
        box-shadow: 
            0 20px 40px -5px rgba(0,0,0,0.1),
            0 0 0 1px rgba(0,0,0,0.02) !important;
        padding: 8px !important;
        backdrop-filter: blur(20px);
    }
    
    [data-baseweb="select"] [role="option"] {
        padding: 14px 18px !important;
        border-radius: 10px !important;
        color: #1e293b !important;
        font-size: 1.05rem !important;
        transition: all 0.2s ease !important;
    }
    
    [data-baseweb="select"] [role="option"]:hover {
        background: #fff7ed !important;
        color: #f97316 !important;
    }
    
    /* Premium Buttons with Gradient */
    .stButton button {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 18px 36px !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        width: 100% !important;
        box-shadow: 
            0 12px 30px -5px rgba(249, 115, 22, 0.3),
            0 2px 8px rgba(249, 115, 22, 0.2) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        letter-spacing: -0.01em;
    }
    
    .stButton button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 
            0 18px 40px -5px rgba(249, 115, 22, 0.4),
            0 4px 15px rgba(249, 115, 22, 0.25) !important;
    }
    
    .stButton button:active {
        transform: translateY(-1px) !important;
    }
    
    /* Stats Cards with Premium Design */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2rem;
        margin-bottom: 3.5rem;
    }
    
    .stat-card {
        background: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.9);
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            0 8px 25px -5px rgba(0, 0, 0, 0.03),
            inset 0 0 0 1px rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(15px);
        position: relative;
        overflow: hidden;
    }
    
    .stat-card:hover {
        transform: translateY(-8px);
        box-shadow: 
            0 15px 40px -5px rgba(0, 0, 0, 0.08),
            inset 0 0 0 1px rgba(255, 255, 255, 0.95);
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #f97316, transparent);
    }
    
    .stat-value {
        font-size: 3rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #0f172a 0%, #334155 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stat-label {
        font-size: 1rem;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    /* Premium Chat Container */
    .chat-container {
        background: rgba(255, 255, 255, 0.85);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.9);
        overflow: hidden;
        box-shadow: 
            0 15px 40px -5px rgba(0,0,0,0.05),
            inset 0 0 0 1px rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(15px);
        margin-bottom: 2rem;
    }
    
    .chat-header {
        padding: 1.75rem;
        border-bottom: 1px solid rgba(241, 245, 249, 0.8);
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        display: flex;
        align-items: center;
        gap: 14px;
    }
    
    .chat-messages {
        height: 550px;
        overflow-y: auto;
        padding: 2.5rem;
        background: #f8fafc;
        display: flex;
        flex-direction: column;
        gap: 1.75rem;
    }
    
    .message {
        display: flex;
        gap: 1.25rem;
        max-width: 90%;
        animation: slideIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .message.user {
        align-self: flex-end;
        flex-direction: row-reverse;
    }
    
    .message-avatar {
        width: 48px;
        height: 48px;
        border-radius: 14px;
        overflow: hidden;
        flex-shrink: 0;
        box-shadow: 0 6px 15px rgba(0,0,0,0.08);
        background: white;
        padding: 3px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .message-avatar img {
        width: 100%;
        height: 100%;
        border-radius: 12px;
    }
    
    .message-bubble {
        padding: 1.5rem 1.75rem;
        border-radius: 20px;
        font-size: 1.05rem;
        line-height: 1.65;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        max-width: 100%;
    }
    
    .message.user .message-bubble {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
        border-bottom-right-radius: 8px;
    }
    
    .message.ai .message-bubble {
        background: white;
        color: #475569;
        border: 1px solid #e2e8f0;
        border-bottom-left-radius: 8px;
    }
    
    /* Premium Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.7);
        padding: 10px;
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.8);
        gap: 10px;
        margin-bottom: 2.5rem;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 14px;
        padding: 14px 28px;
        font-weight: 600;
        color: #94a3b8;
        background: transparent;
        border: none;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        font-size: 1.05rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        color: #f97316;
        box-shadow: 
            0 6px 20px -5px rgba(0,0,0,0.08),
            inset 0 0 0 1px rgba(255, 255, 255, 0.95);
    }
    
    /* Status Indicator */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 8px 18px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 100px;
        font-weight: 600;
        font-size: 0.95rem;
        border: 1px solid rgba(255, 255, 255, 0.9);
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    
    .status-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        display: inline-block;
    }
    
    .status-active {
        background: #22c55e;
        box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.2);
    }
    
    .status-inactive {
        background: #ef4444;
        box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.2);
    }
    
    /* Progress Bar - Premium Style */
    .progress-container {
        margin-top: 2rem;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.9);
        box-shadow: 0 8px 25px -5px rgba(0,0,0,0.05);
        backdrop-filter: blur(15px);
    }
    
    /* Expander Styling */
    .streamlit-expander {
        border-radius: 16px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03) !important;
        margin-bottom: 1.25rem !important;
        transition: all 0.3s ease !important;
    }
    
    .streamlit-expander:hover {
        border-color: #f97316 !important;
        box-shadow: 0 6px 20px rgba(249, 115, 22, 0.1) !important;
    }
    
    .streamlit-expanderHeader {
        padding: 1.25rem 1.5rem !important;
        border-radius: 16px !important;
        background: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Text Areas */
    .stTextArea textarea {
        font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Fira Mono', monospace !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
    }
</style>

<!-- JAVASCRIPT FOR DYNAMIC DROPDOWN STYLING -->
<script>
    // Enhanced dropdown styling with JavaScript
    function styleSelectboxes() {
        const selectBoxes = document.querySelectorAll('.stSelectbox > div');
        selectBoxes.forEach(sb => {
            // Ensure we haven't already processed this element
            if (!sb.dataset.processed) {
                sb.dataset.processed = "true";
                
                // Style the inner div (the actual select box)
                const innerDiv = sb.querySelector('div');
                if (innerDiv) {
                    innerDiv.style.transition = 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)';
                    
                    // Add focus and blur handlers
                    innerDiv.addEventListener('focus', function() {
                        sb.style.borderColor = '#f97316';
                        sb.style.boxShadow = '0 0 0 4px rgba(249, 115, 22, 0.15), inset 0 1px 2px rgba(0,0,0,0.03)';
                    });
                    
                    innerDiv.addEventListener('blur', function() {
                        sb.style.borderColor = '#e2e8f0';
                        sb.style.boxShadow = '0 2px 8px rgba(0,0,0,0.02), inset 0 1px 2px rgba(0,0,0,0.03)';
                    });
                }
            }
        });
    }
    
    // Run immediately and then periodically to catch dynamically added elements
    document.addEventListener('DOMContentLoaded', function() {
        styleSelectboxes();
        const interval = setInterval(styleSelectboxes, 500);
        // Stop after 10 seconds to prevent memory leaks
        setTimeout(() => clearInterval(interval), 10000);
    });
    
    // Also run when Streamlit updates
    window.addEventListener('load', function() {
        setTimeout(styleSelectboxes, 1000);
    });
</script>
""", unsafe_allow_html=True)

# Premium Avatars
USER_AVATAR = "https://api.dicebear.com/7.x/notionists/svg?seed=User&backgroundColor=dedede"
AI_AVATAR = "https://api.dicebear.com/7.x/bottts/svg?seed=AI&backgroundColor=fdbbc5"

# Session State Initialization
session_vars = ["pages", "content", "urls", "chat", "ai"]
for var in session_vars:
    if var not in st.session_state:
        st.session_state[var] = {} if var == "pages" else ([] if var == "urls" else "")

if "ai" not in st.session_state:
    st.session_state.ai = None

groq_ok = is_groq_configured()

# Hero Section
st.markdown(f'''
<div class="hero-container">
    <div class="hero-badge">
        <span class="status-dot {'status-active' if groq_ok else 'status-inactive'}"></span>
        <span style="font-weight: 600; font-size: 1rem; color: #9a3412;">
            {'AI System Operational' if groq_ok else 'AI System Offline'}
        </span>
    </div>
    <h1 class="hero-title">Web<span>Scraper</span> AI</h1>
    <p class="hero-subtitle">Transform any website into structured data and intelligent conversations.<br>
    Powered by advanced AI to understand context and meaning with precision.</p>
</div>
''', unsafe_allow_html=True)

# Input Section
st.markdown('<div class="input-card">', unsafe_allow_html=True)

col1, col2 = st.columns([2.2, 1])

with col1:
    mode = st.session_state.get('mode_select', "Single Page")
    
    if mode == "Multiple URLs":
        urls_input = st.text_area(
            "Target URLs (One per line)",
            placeholder="https://example.com/page1\\nhttps://example.com/page2",
            height=140
        )
    else:
        url = st.text_input("Target URL", placeholder="https://example.com")

with col2:
    mode = st.selectbox(
        "Extraction Mode",
        ["Single Page", "Full Website", "Multiple URLs", "Quick Scan"],
        key="mode_select"
    )

if mode == "Full Website":
    st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
    max_pages = st.slider("Maximum Pages", 5, 50, 10)

st.markdown('<div style="margin-top: 2.5rem;"></div>', unsafe_allow_html=True)

if st.button("🚀 Start Intelligent Extraction", use_container_width=True):
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
                <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                    <span style="font-weight: 600; color: #1e293b; font-size: 1.1rem;">Processing Content...</span>
                    <span style="color: #f97316; font-weight: 700; font-size: 1.1rem;">{int((count/total)*100)}%</span>
                </div>
                <div style="background: #e2e8f0; height: 10px; border-radius: 5px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #f97316, #ea580c); height: 100%; width: {(count/total)*100}%; transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);"></div>
                </div>
                <div style="margin-top: 1rem; font-size: 1rem; color: #1e293b; font-family: 'SF Mono', monospace; text-align: center;">{curr}</div>
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
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

        elif mode == "Multiple URLs":
            target_urls = [u.strip() for u in urls_input.split('\\n') if u.strip()]
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
                        st.error(f"❌ Error processing {target_url}: {str(e)}")
                
                all_content = [p.content for p in st.session_state.pages.values()]
                st.session_state.content = "\\n\\n".join(all_content)
                st.session_state.ai = AIChat(st.session_state.content) if groq_ok else None
                progress_area.empty()
                st.success(f"✅ Successfully extracted {len(st.session_state.pages)} pages")

        elif mode == "Single Page":
            with st.spinner("🔍 Extracting content..."):
                try:
                    scraper = SmartWebScraper()
                    page = scraper.scrape_single_page(url)
                    if page:
                        st.session_state.pages = {url: page}
                        st.session_state.content = page.content
                        st.session_state.ai = AIChat(page.content) if groq_ok else None
                        st.success("✅ Extraction complete")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        else:  # Quick Scan
            with st.spinner("⚡ Scanning..."):
                try:
                    import requests
                    from bs4 import BeautifulSoup
                    r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0 (compatible; WebScraperAI/1.0)'})
                    soup = BeautifulSoup(r.text, 'html.parser')
                    for t in soup(['script', 'style']):
                        t.decompose()
                    title = soup.find('title').get_text().strip() if soup.find('title') else "Page"
                    content = soup.get_text("\\n", strip=True)
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
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

# Results Section
if st.session_state.pages:
    pages = list(st.session_state.pages.values())
    
    # Stats Dashboard
    st.markdown('<div class="stats-grid">', unsafe_allow_html=True)
    
    stat_cards = [
        {"value": len(pages), "label": "Pages Extracted"},
        {"value": f"{sum(p.word_count for p in pages):,}", "label": "Total Words"},
        {"value": len(set(p.content_type for p in pages)), "label": "Content Types"},
        {"value": f"{sum(p.links_found for p in pages)}", "label": "Links Found"}
    ]
    
    cols = st.columns(len(stat_cards))
    for i, (col, stat) in enumerate(zip(cols, stat_cards)):
        with col:
            st.markdown(f'''
            <div class="stat-card">
                <div class="stat-value">{stat["value"]}</div>
                <div class="stat-label">{stat["label"]}</div>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tabbed Interface
    tab1, tab2, tab3 = st.tabs(["🤖 AI Assistant", "📄 Content Explorer", "💾 Export Data"])
    
    with tab1:
        if groq_ok:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            
            # Chat Header
            st.markdown(f'''
            <div class="chat-header">
                <div style="width: 14px; height: 14px; background: #22c55e; border-radius: 50%; box-shadow: 0 0 0 3px rgba(34,197,94,0.2);"></div>
                <span style="font-weight: 600; color: #1e293b; font-size: 1.1rem;">🤖 AI Assistant Online</span>
                <span style="margin-left: auto; font-size: 0.9rem; color: #94a3b8; background: #f1f5f9; padding: 6px 14px; border-radius: 100px;">{os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")}</span>
            </div>
            ''', unsafe_allow_html=True)
            
            # Chat Messages
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
                <div style="text-align: center; padding: 5rem 2rem;">
                    <div style="width: 80px; height: 80px; background: #fff7ed; border-radius: 24px; display: flex; align-items: center; justify-content: center; margin: 0 auto 2rem; box-shadow: 0 15px 30px rgba(251, 146, 60, 0.15);">
                        <span style="font-size: 2.8rem;">🤖</span>
                    </div>
                    <h3 style="color: #1e293b; font-weight: 700; margin-bottom: 1rem; font-size: 1.8rem;">AI Assistant Ready</h3>
                    <p style="color: #94a3b8; margin: 0; font-size: 1.2rem; line-height: 1.7;">Ask me anything about the extracted content. I can help analyze, summarize, or extract specific information.</p>
                </div>
                '''
            
            st.markdown(f'<div class="chat-messages">{msgs_html}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Chat Input
            col1, col2 = st.columns([5, 1])
            
            with col1:
                msg = st.text_input("", placeholder="Ask a question about the content...", label_visibility="collapsed")
            
            with col2:
                send = st.button("Send", use_container_width=True)
            
            if send and msg:
                if not st.session_state.ai:
                    st.session_state.ai = AIChat(st.session_state.content)
                
                st.session_state.chat.append({"role": "user", "content": msg})
                
                with st.spinner("🧠 Thinking..."):
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
        st.markdown('<div style="margin-bottom: 2rem;"></div>', unsafe_allow_html=True)
        
        # Sort pages by word count (descending)
        sorted_pages = sorted(pages, key=lambda x: x.word_count, reverse=True)
        
        for i, page in enumerate(sorted_pages):
            with st.expander(f"📄 {page.title} ({page.word_count:,} words)", expanded=i==0):
                st.caption(f"🔗 {page.url}")
                st.text_area("", page.content[:5000], height=250, label_visibility="collapsed")
    
    with tab3:
        st.subheader("Export Options")
        st.markdown('<div style="margin-bottom: 2rem;"></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fmt = st.selectbox("Export Format", ["JSON", "Markdown", "Text"])
        
        with col2:
            fname = st.text_input("Filename", "web_scrape_export")
        
        st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
        
        if st.button("📥 Download Exported Data", use_container_width=True):
            if fmt == "JSON":
                data = {
                    "extraction_date": datetime.now().isoformat(),
                    "pages_extracted": len(pages),
                    "total_words": sum(p.word_count for p in pages),
                    "pages": [
                        {
                            "url": p.url,
                            "title": p.title,
                            "content": p.content,
                            "word_count": p.word_count,
                            "content_type": p.content_type,
                            "links_found": p.links_found
                        } 
                        for p in pages
                    ]
                }
                st.download_button(
                    "💾 Save JSON File",
                    json.dumps(data, indent=2),
                    f"{fname}.json",
                    "application/json",
                    use_container_width=True
                )
            elif fmt == "Markdown":
                md = "# Web Scraping Results\\n\\n"
                md += f"**Extraction Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n"
                md += f"**Pages Extracted:** {len(pages)}\\n"
                md += f"**Total Words:** {sum(p.word_count for p in pages):,}\\n\\n"
                md += "---\\n\\n"
                
                for p in pages:
                    md += f"## {p.title}\\n\\n"
                    md += f"**URL:** [{p.url}]({p.url})\\n\\n"
                    md += f"**Word Count:** {p.word_count:,}\\n\\n"
                    md += f"**Content Type:** {p.content_type}\\n\\n"
                    md += f"### Content\\n\\n{p.content}\\n\\n"
                    md += "---\\n\\n"
                
                st.download_button(
                    "💾 Save Markdown File",
                    md,
                    f"{fname}.md",
                    "text/markdown",
                    use_container_width=True
                )
            else:
                export_content = f"Web Scraping Results\\n"
                export_content += f"====================\\n\\n"
                export_content += f"Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n"
                export_content += f"Pages Extracted: {len(pages)}\\n"
                export_content += f"Total Words: {sum(p.word_count for p in pages):,}\\n\\n"
                export_content += "=" * 50 + "\\n\\n"
                
                for p in pages:
                    export_content += f"PAGE: {p.title}\\n"
                    export_content += f"URL: {p.url}\\n"
                    export_content += f"Words: {p.word_count:,}\\n"
                    export_content += "-" * 30 + "\\n"
                    export_content += f"{p.content}\\n\\n"
                    export_content += "=" * 50 + "\\n\\n"
                
                st.download_button(
                    "💾 Save Text File",
                    export_content,
                    f"{fname}.txt",
                    "text/plain",
                    use_container_width=True
                )