# AI Web Scraper Pro 🌐

A powerful, AI-powered web scraping tool with full website crawling, social media support, and multi-LLM integration.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

### 🚀 Web Scraping
- **Single Page Scraping** - Quick scraping of individual pages
- **Full Website Crawling** - Recursively scrape entire websites with depth control
- **JavaScript Rendering** - Support for dynamic, JavaScript-heavy websites
- **Anti-Bot Bypass** - Optional BrightData integration for bypassing CAPTCHAs

### 📱 Social Media Support
- **Instagram** - Profile info and recent posts
- **Facebook** - Public page information
- **Twitter/X** - Profile scraping

### 🤖 AI Integration
- **Multi-LLM Support** - Choose from Ollama (local), OpenAI, or Groq
- **Smart Extraction** - Extract exactly the data you need
- **Content Summarization** - Get quick summaries of scraped content
- **Q&A** - Ask questions about the scraped data

### 📊 Export Options
- JSON, CSV, Excel, Markdown, Plain Text
- Session saving for resuming later

## 🛠️ Installation

### Prerequisites
- Python 3.9 or higher
- Chrome browser (for Selenium)
- [Ollama](https://ollama.ai) (optional, for local LLM)

### Setup

1. **Clone and navigate to the project**
```bash
cd "custom web scraper"
```

2. **Create a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Install Playwright browsers** (optional, for better JS support)
```bash
playwright install chromium
```

5. **Configure environment variables**
```bash
copy .env.example .env
# Edit .env with your API keys
```

## 🚀 Usage

### Start the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Basic Usage

1. **Select Scraping Mode**
   - 📄 Single Page: Scrape one URL
   - 🌐 Full Website: Crawl entire site
   - 📱 Social Media: Scrape social profiles

2. **Enter URL** and click "Start Scraping"

3. **View Results** in the Raw Content tab

4. **AI Parse** - Describe what you want to extract

5. **Export** in your preferred format

### Command Line Usage

```python
from scraper import scrape_single_page, scrape_website, AIParser

# Single page
html, content = scrape_single_page("https://example.com")

# Full website
pages = scrape_website("https://example.com", max_pages=20, depth=3)

# AI parsing
parser = AIParser(provider="ollama")
result = parser.extract(content, "Extract all product prices")
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SBR_WEBDRIVER` | BrightData Scraping Browser URL | No |
| `OPENAI_API_KEY` | OpenAI API key | No* |
| `GROQ_API_KEY` | Groq API key | No* |
| `DEFAULT_LLM_PROVIDER` | Default AI provider (ollama/openai/groq) | No |
| `OLLAMA_MODEL` | Ollama model name | No |
| `MAX_PAGES_TO_SCRAPE` | Default max pages for website crawling | No |
| `SCRAPE_DELAY_SECONDS` | Delay between requests | No |

*At least one LLM provider should be configured for AI features

### LLM Providers

#### Ollama (Local, Free)
1. Install [Ollama](https://ollama.ai)
2. Pull a model: `ollama pull llama3`
3. Ollama runs at `localhost:11434`

#### OpenAI
1. Get API key from [OpenAI](https://platform.openai.com)
2. Add to `.env`: `OPENAI_API_KEY=sk-...`

#### Groq (Fast, Free tier)
1. Get API key from [Groq Console](https://console.groq.com)
2. Add to `.env`: `GROQ_API_KEY=gsk_...`

## 📁 Project Structure

```
custom web scraper/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Project dependencies
├── .env.example          # Environment variables template
├── .env                  # Your configuration (create this)
├── exports/              # Exported data files
└── scraper/
    ├── __init__.py       # Package initialization
    ├── web_scraper.py    # Web scraping module
    ├── social_scraper.py # Social media scraping
    ├── ai_parser.py      # LLM integration
    └── exporter.py       # Data export utilities
```

## 🔒 Legal & Ethical Use

- Always respect `robots.txt` and website terms of service
- Use appropriate delays between requests
- Don't scrape personal data without consent
- This tool is for educational and legitimate business purposes only

## 🐛 Troubleshooting

### Chrome driver issues
```bash
# Install webdriver-manager for automatic driver management
pip install webdriver-manager
```

### Ollama not connecting
- Ensure Ollama is running: `ollama serve`
- Check if port 11434 is accessible

### Rate limiting
- Increase `SCRAPE_DELAY_SECONDS` in `.env`
- Reduce `MAX_PAGES_TO_SCRAPE`

## ☁️ Cloud Deployment

### Deploy to Streamlit Cloud (Free!)

1. **One-Click Deploy**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select this repository
   - Set main file to `app.py`
   - Add your `GROQ_API_KEY` in the Secrets section

2. **Your app will be live at:** `https://[your-app].streamlit.app`

📖 **Detailed deployment guide:** See [DEPLOYMENT.md](DEPLOYMENT.md) for complete step-by-step instructions.

### Important for Cloud Deployment
- Add your API keys in Streamlit Cloud Secrets (not in `.env`)
- Chromium is automatically installed via `packages.txt`
- Free tier includes 1GB RAM - perfect for web scraping!


## 📄 License

MIT License - feel free to use and modify!

## 🙏 Credits

Inspired by [Tech With Tim's AI Web Scraper](https://github.com/techwithtim/AI-Web-Scraper)

---

**Built with ❤️ using Python, Streamlit, and AI**
