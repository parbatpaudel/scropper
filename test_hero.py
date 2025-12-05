import streamlit as st

st.set_page_config(page_title="Test Hero Section", layout="wide")

# PREMIUM UI STYLES
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    /* Hero Section */
    .hero-container {
        text-align: center;
        padding: 4rem 2rem;
        background: white;
        border-radius: 32px;
        box-shadow: 
            0 4px 6px -1px rgba(0, 0, 0, 0.01),
            0 2px 4px -1px rgba(0, 0, 0, 0.01),
            0 0 0 1px rgba(0, 0, 0, 0.03);
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
    }
    
    .badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #FFF7ED;
        border: 1px solid #FFEDD5;
        padding: 8px 16px;
        border-radius: 100px;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .badge-icon { font-size: 1.1rem; }
    
    .badge-text {
        color: #9A3412;
        font-weight: 600;
        font-size: 0.9rem;
        letter-spacing: 0.3px;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: #111827;
        margin-bottom: 1rem;
        line-height: 1.1;
        letter-spacing: -0.02em;
    }
    
    .hero-title span {
        background: linear-gradient(135deg, #F97316 0%, #EA580C 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        position: relative;
    }
    
    .hero-desc {
        font-size: 1.15rem;
        color: #6B7280;
        max-width: 600px;
        margin: 0 auto 2rem;
        line-height: 1.6;
    }
    
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 100px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #374151;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    
    .dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        position: relative;
    }
    
    .dot-active { background: #10B981; }
</style>
""", unsafe_allow_html=True)

# HERO SECTION
st.markdown('''
<div class="hero-container">
    <div class="badge-pill">
        <span class="badge-icon">✨</span>
        <span class="badge-text">Intelligent Web Extraction</span>
    </div>
    
    <div class="hero-title">
        Extract. Analyze. <span>Chat.</span>
    </div>
    
    <div class="hero-desc">
        Transform any website into structured data and interactive conversations.
        Powered by advanced AI to understand context and content.
    </div>
    
    <div class="status-indicator">
        <span class="dot dot-active"></span>
        AI System Online
    </div>
</div>
''', unsafe_allow_html=True)