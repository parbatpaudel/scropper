"""
Simple Working Web Scraper
"""

import os
import time
from urllib.parse import urljoin, urlparse
from typing import Dict, Optional, Callable, Set
from dataclasses import dataclass
from collections import deque

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv

load_dotenv()

@dataclass
class ScrapedPage:
    url: str
    title: str
    content: str
    content_type: str
    word_count: int
    links_found: int
    scraped_at: str
    value_score: float = 1.0


def get_page_type(url: str) -> tuple:
    """Get page type and score"""
    path = urlparse(url).path.lower()
    
    if path in ['/', '', '/home', '/index.html']:
        return 'homepage', 1.0
    elif '/about' in path or '/team' in path or '/company' in path:
        return 'about', 0.9
    elif '/service' in path or '/solution' in path:
        return 'services', 0.9
    elif '/product' in path or '/feature' in path:
        return 'products', 0.9
    elif '/pricing' in path or '/plan' in path:
        return 'pricing', 0.85
    elif '/contact' in path:
        return 'contact', 0.8
    elif '/blog' in path or '/news' in path:
        return 'blog', 0.6
    else:
        return 'other', 0.5


class SmartWebScraper:
    def __init__(self):
        self.driver = None
        self.scraped_pages: Dict[str, ScrapedPage] = {}
        self.visited: Set[str] = set()
        self.base_domain = ""
    
    def _create_driver(self):
        """Create new browser instance"""
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # For Streamlit Cloud compatibility
        chromium_path = "/usr/bin/chromium"
        if os.path.exists(chromium_path):
            options.binary_location = chromium_path
        
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(30)
        return driver
    
    def _close_driver(self):
        """Close browser"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
    
    def _load_page(self, url: str) -> Optional[str]:
        """Load a page and return HTML"""
        try:
            print(f"  Loading: {url}")
            self.driver.get(url)
            
            # Wait for page
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Wait for content to load
            time.sleep(2)
            
            # Scroll to trigger lazy loading
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.5)
            
            html = self.driver.page_source
            print(f"  Got HTML: {len(html)} chars")
            return html
            
        except Exception as e:
            print(f"  Error loading: {e}")
            return None
    
    def _extract_text(self, html: str, url: str) -> tuple:
        """Extract text from HTML"""
        soup = BeautifulSoup(html, "html.parser")
        
        # Get title
        title_tag = soup.find("title")
        title = title_tag.get_text().strip() if title_tag else "Untitled"
        title = title[:100]  # Limit length
        
        # Remove unwanted elements
        for tag in soup.find_all(['script', 'style', 'nav', 'header', 'footer', 
                                   'noscript', 'iframe', 'svg', 'form']):
            tag.decompose()
        
        # Get text
        body = soup.find('body')
        if body:
            text = body.get_text(separator='\n', strip=True)
        else:
            text = soup.get_text(separator='\n', strip=True)
        
        # Clean text
        lines = []
        for line in text.split('\n'):
            line = line.strip()
            if len(line) > 5:
                lines.append(line)
        
        content = '\n'.join(lines)
        
        # Add page context
        full_content = f"=== {title} ===\nURL: {url}\n\n{content}"
        
        return title, full_content
    
    def _find_links(self, html: str, current_url: str) -> list:
        """Find internal links"""
        soup = BeautifulSoup(html, "html.parser")
        links = []
        
        for a in soup.find_all('a', href=True):
            href = a['href'].strip()
            
            if not href or href.startswith('#') or href.startswith('javascript:'):
                continue
            if href.startswith('mailto:') or href.startswith('tel:'):
                continue
            
            # Make absolute
            full_url = urljoin(current_url, href)
            parsed = urlparse(full_url)
            
            # Same domain only
            if parsed.netloc != self.base_domain:
                continue
            
            # Skip files
            path = parsed.path.lower()
            if any(path.endswith(ext) for ext in ['.pdf', '.jpg', '.png', '.gif', '.css', '.js']):
                continue
            
            # Clean URL
            clean = f"https://{parsed.netloc}{parsed.path.rstrip('/')}"
            if clean and clean not in self.visited and clean not in links:
                links.append(clean)
        
        return links[:20]  # Limit links per page
    
    def scrape_website(self, start_url: str, max_pages: int = 10, 
                       progress_callback: Callable = None) -> Dict[str, ScrapedPage]:
        """Scrape multiple pages from a website"""
        
        # Parse start URL
        parsed = urlparse(start_url)
        self.base_domain = parsed.netloc
        homepage = f"https://{self.base_domain}"
        
        # Initialize
        self.scraped_pages = {}
        self.visited = set()
        queue = deque([homepage])
        
        print(f"\n=== Starting scrape of {self.base_domain} ===")
        print(f"Max pages: {max_pages}\n")
        
        try:
            self.driver = self._create_driver()
            
            page_count = 0
            while queue and page_count < max_pages:
                url = queue.popleft()
                
                if url in self.visited:
                    continue
                
                self.visited.add(url)
                page_count += 1
                
                print(f"\n[{page_count}/{max_pages}] {url}")
                
                if progress_callback:
                    progress_callback(url, page_count - 1, len(queue), max_pages)
                
                # Load page
                html = self._load_page(url)
                if not html:
                    print("  FAILED - skipping")
                    continue
                
                # Extract content
                title, content = self._extract_text(html, url)
                word_count = len(content.split())
                
                print(f"  Title: {title}")
                print(f"  Words: {word_count}")
                
                if word_count < 20:
                    print("  Too short - skipping")
                    continue
                
                # Get page type
                page_type, score = get_page_type(url)
                print(f"  Type: {page_type}")
                
                # Find links
                links = self._find_links(html, url)
                print(f"  Found {len(links)} links")
                
                # Store page
                page = ScrapedPage(
                    url=url,
                    title=title,
                    content=content,
                    content_type=page_type,
                    word_count=word_count,
                    links_found=len(links),
                    scraped_at=time.strftime("%Y-%m-%d %H:%M:%S"),
                    value_score=score
                )
                self.scraped_pages[url] = page
                
                # Add new links to queue
                for link in links:
                    if link not in self.visited:
                        queue.append(link)
                
                # Delay between pages
                time.sleep(1)
            
            print(f"\n=== Scrape complete: {len(self.scraped_pages)} pages ===\n")
            return self.scraped_pages
            
        finally:
            self._close_driver()
    
    def scrape_single_page(self, url: str) -> Optional[ScrapedPage]:
        """Scrape just one page"""
        print(f"\nScraping single page: {url}")
        
        parsed = urlparse(url)
        self.base_domain = parsed.netloc
        
        try:
            self.driver = self._create_driver()
            
            html = self._load_page(url)
            if not html:
                return None
            
            title, content = self._extract_text(html, url)
            page_type, score = get_page_type(url)
            
            print(f"  Title: {title}")
            print(f"  Words: {len(content.split())}")
            
            return ScrapedPage(
                url=url,
                title=title,
                content=content,
                content_type=page_type,
                word_count=len(content.split()),
                links_found=0,
                scraped_at=time.strftime("%Y-%m-%d %H:%M:%S"),
                value_score=score
            )
            
        finally:
            self._close_driver()
    
    def get_all_content(self) -> str:
        """Get all scraped content as one string"""
        parts = []
        for page in sorted(self.scraped_pages.values(), key=lambda x: x.value_score, reverse=True):
            parts.append(page.content)
            parts.append("\n" + "="*60 + "\n")
        return "\n".join(parts)


class QuickScraper:
    """Fast scraper without JavaScript"""
    
    def scrape(self, url: str) -> tuple:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            r = requests.get(url, timeout=10, headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")
            
            title = soup.find("title")
            title_text = title.get_text().strip() if title else ""
            
            for tag in soup(['script', 'style', 'nav', 'footer']):
                tag.decompose()
            
            text = soup.get_text(separator="\n", strip=True)
            return title_text, text
        except:
            return "", ""
