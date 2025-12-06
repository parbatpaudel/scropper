import streamlit as st
import time
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI Web Scraper Pro",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

from scraper import SmartWebScraper, ScrapedPage, AIChat, is_groq_configured

# Modern UI Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 24px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
    }
    
    .hero-section {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        opacity: 0.95;
        font-weight: 300;
    }
    
    .status-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 1rem 0;
    }
    
    .status-active {
        background: #10b981;
        color: white;
    }
    
    .status-inactive {
        background: #ef4444;
        color: white;
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.15);
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #667eea;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.5rem;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 16px 32px;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.4);
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    
    .user-message {
        background: #667eea;
        color: white;
        margin-left: 20%;
    }
    
    .ai-message {
        background: #f3f4f6;
        color: #1f2937;
        margin-right: 20%;
    }
    
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        padding: 12px;
        font-size: 1rem;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
</style>
""", unsafe_allow_html=True)

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
scrape_do_token = os.getenv("SCRAPE_DO_TOKEN")

# Hero Section
st.markdown(f"""
<div class="hero-section">
    <div class="hero-title">🌐 AI Web Scraper Pro</div>
    <div class="hero-subtitle">Extract, Analyze, and Understand Web Content with AI</div>
    <div class="status-badge {'status-active' if groq_ok else 'status-inactive'}">
        {'✅ AI Ready' if groq_ok else '⚠️ AI Offline'}
    </div>
    {f'<div class="status-badge status-active">🚀 Scrape.do Active</div>' if scrape_do_token else ''}
</div>
""", unsafe_allow_html=True)

# Main Content
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Input Section
col1, col2 = st.columns([3, 1])

with col1:
    mode = st.selectbox(
        "Scraping Mode",
        ["Single Page", "Full Website", "Multiple URLs", "Quick Scan"],
        help="Choose how you want to scrape"
    )
    
    if mode == "Multiple URLs":
        urls_input = st.text_area(
            "Enter URLs (one per line)",
            placeholder="https://example.com/page1\nhttps://example.com/page2",
            height=120
        )
    else:
        url = st.text_input(
            "Target URL",
            placeholder="https://example.com",
            help="Enter the website URL you want to scrape"
        )

with col2:
    if mode == "Full Website":
        max_pages = st.number_input("Max Pages", min_value=5, max_value=100, value=10)
    
    st.markdown("### Options")
    use_proxy = st.checkbox("Force Proxy", value=False, help="Force use of Scrape.do proxy")

# Scrape Button
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
            progress_area.progress((count/total), text=f"Processing {count}/{total}: {curr}")
        
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
                        st.warning(f"Failed to scrape {target_url}: {str(e)}")
                
                all_content = [p.content for p in st.session_state.pages.values()]
                st.session_state.content = "\n\n".join(all_content)
                st.session_state.ai = AIChat(st.session_state.content) if groq_ok else None
                progress_area.empty()
                st.success(f"✅ Successfully extracted {len(st.session_state.pages)} pages")
        
        elif mode == "Single Page":
            with st.spinner("🔄 Extracting content..."):
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
            with st.spinner("⚡ Quick scanning..."):
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
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

# Results Section
if st.session_state.pages:
    pages = list(st.session_state.pages.values())
    
    # Stats
    st.markdown("## 📊 Scraping Results")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{len(pages)}</div>
            <div class="stat-label">Pages Extracted</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{sum(p.word_count for p in pages):,}</div>
            <div class="stat-label">Total Words</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{len(set(p.content_type for p in pages))}</div>
            <div class="stat-label">Content Types</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["🤖 AI Assistant", "📄 Content Explorer", "💾 Export Data"])
    
    with tab1:
        if groq_ok:
            st.markdown("### 💬 Chat with AI About Your Data")
            
            # Display chat history
            for msg in st.session_state.chat:
                if msg["role"] == "user":
                    st.markdown(f'<div class="chat-message user-message">👤 {msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-message ai-message">🤖 {msg["content"]}</div>', unsafe_allow_html=True)
            
            # Chat input
            col1, col2 = st.columns([5, 1])
            with col1:
                msg = st.text_input("Ask a question about the content...", key="chat_input", label_visibility="collapsed")
            with col2:
                send = st.button("Send", use_container_width=True)
            
            if send and msg:
                if not st.session_state.ai:
                    st.session_state.ai = AIChat(st.session_state.content)
                
                st.session_state.chat.append({"role": "user", "content": msg})
                
                with st.spinner("🤔 Thinking..."):
                    resp = st.session_state.ai.chat(msg)
                    st.session_state.chat.append({"role": "assistant", "content": resp})
                
                st.rerun()
            
            if st.button("🧹 Clear Chat", use_container_width=True):
                st.session_state.chat = []
                if st.session_state.ai:
                    st.session_state.ai.clear()
                st.rerun()
        else:
            st.warning("⚠️ Configure GROQ_API_KEY to enable AI features")
    
    with tab2:
        st.markdown("### 📄 Extracted Content")
        for page in sorted(pages, key=lambda x: x.value_score, reverse=True):
            with st.expander(f"📄 {page.title} ({page.word_count} words)"):
                st.caption(f"🔗 {page.url}")
                st.text_area("", page.content[:3000], height=200, label_visibility="collapsed", key=f"content_{page.url}")
    
    with tab3:
        st.markdown("### 💾 Export Options")
        col1, col2 = st.columns(2)
        
        with col1:
            fmt = st.selectbox("Format", ["JSON", "Markdown", "Text", "CSV"])
        
        with col2:
            fname = st.text_input("Filename", "web_scrape_export")
        
        if st.button("📥 Download", use_container_width=True):
            if fmt == "JSON":
                data = {"pages": [{
                    "url": p.url,
                    "title": p.title,
                    "content": p.content,
                    "word_count": p.word_count
                } for p in pages]}
                st.download_button(
                    "💾 Save JSON",
                    json.dumps(data, indent=2),
                    f"{fname}.json",
                    "application/json",
                    use_container_width=True
                )
            elif fmt == "Markdown":
                md = "\n\n---\n\n".join([
                    f"# {p.title}\n\n**URL:** {p.url}\n\n**Words:** {p.word_count}\n\n{p.content}"
                    for p in pages
                ])
                st.download_button(
                    "💾 Save Markdown",
                    md,
                    f"{fname}.md",
                    "text/markdown",
                    use_container_width=True
                )
            elif fmt == "CSV":
                import pandas as pd
                df = pd.DataFrame([{
                    "URL": p.url,
                    "Title": p.title,
                    "Word Count": p.word_count,
                    "Content": p.content[:500]
                } for p in pages])
                st.download_button(
                    "💾 Save CSV",
                    df.to_csv(index=False),
                    f"{fname}.csv",
                    "text/csv",
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

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 2rem;">
    <p>Built with ❤️ using Streamlit & AI | <a href="https://github.com/parbatpaudel/scropper" target="_blank">GitHub</a></p>
</div>
""", unsafe_allow_html=True)
