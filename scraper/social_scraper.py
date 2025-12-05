"""
Social Media Scraper Module
Supports Instagram, Facebook (public pages), and more
"""

import os
import time
import json
import re
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse
from dataclasses import dataclass, asdict
from datetime import datetime

from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

# Instagram credentials (optional, for private accounts)
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")


@dataclass
class SocialPost:
    """Represents a social media post"""
    platform: str
    post_id: str
    url: str
    author: str
    content: str
    timestamp: Optional[str]
    likes: int = 0
    comments: int = 0
    shares: int = 0
    media_urls: List[str] = None
    hashtags: List[str] = None
    mentions: List[str] = None
    raw_data: Dict = None
    
    def __post_init__(self):
        if self.media_urls is None:
            self.media_urls = []
        if self.hashtags is None:
            self.hashtags = []
        if self.mentions is None:
            self.mentions = []
        if self.raw_data is None:
            self.raw_data = {}
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def to_text(self) -> str:
        """Convert post to readable text format"""
        lines = [
            f"Platform: {self.platform}",
            f"Author: {self.author}",
            f"Posted: {self.timestamp or 'Unknown'}",
            f"URL: {self.url}",
            "",
            f"Content:",
            self.content,
            "",
            f"Engagement: {self.likes} likes, {self.comments} comments, {self.shares} shares",
        ]
        
        if self.hashtags:
            lines.append(f"Hashtags: {', '.join(self.hashtags)}")
        
        if self.mentions:
            lines.append(f"Mentions: {', '.join(self.mentions)}")
        
        return "\n".join(lines)


@dataclass
class SocialProfile:
    """Represents a social media profile"""
    platform: str
    username: str
    display_name: str
    bio: str
    url: str
    followers: int = 0
    following: int = 0
    posts_count: int = 0
    profile_pic_url: str = ""
    is_verified: bool = False
    external_url: str = ""
    raw_data: Dict = None
    
    def __post_init__(self):
        if self.raw_data is None:
            self.raw_data = {}
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def to_text(self) -> str:
        """Convert profile to readable text format"""
        verified = " ✓" if self.is_verified else ""
        lines = [
            f"Platform: {self.platform}",
            f"Username: @{self.username}{verified}",
            f"Display Name: {self.display_name}",
            f"URL: {self.url}",
            "",
            f"Bio:",
            self.bio,
            "",
            f"Stats: {self.followers} followers, {self.following} following, {self.posts_count} posts",
        ]
        
        if self.external_url:
            lines.append(f"Website: {self.external_url}")
        
        return "\n".join(lines)


class InstagramScraper:
    """Instagram public profile and post scraper"""
    
    def __init__(self, use_login: bool = False):
        self.use_login = use_login
        self.loader = None
        self._init_loader()
    
    def _init_loader(self):
        """Initialize Instaloader"""
        try:
            import instaloader
            self.loader = instaloader.Instaloader(
                download_pictures=False,
                download_videos=False,
                download_video_thumbnails=False,
                download_geotags=False,
                download_comments=False,
                save_metadata=False,
                compress_json=False,
            )
            
            if self.use_login and INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD:
                try:
                    self.loader.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
                except Exception as e:
                    print(f"Instagram login failed: {e}")
        except ImportError:
            print("Instaloader not installed. Run: pip install instaloader")
            self.loader = None
    
    def get_profile(self, username: str) -> Optional[SocialProfile]:
        """Get Instagram profile information"""
        if not self.loader:
            return None
        
        try:
            import instaloader
            profile = instaloader.Profile.from_username(self.loader.context, username)
            
            return SocialProfile(
                platform="instagram",
                username=profile.username,
                display_name=profile.full_name,
                bio=profile.biography or "",
                url=f"https://www.instagram.com/{profile.username}/",
                followers=profile.followers,
                following=profile.followees,
                posts_count=profile.mediacount,
                profile_pic_url=profile.profile_pic_url,
                is_verified=profile.is_verified,
                external_url=profile.external_url or "",
                raw_data={
                    "is_private": profile.is_private,
                    "is_business": profile.is_business_account,
                    "business_category": getattr(profile, 'business_category_name', None),
                }
            )
        except Exception as e:
            print(f"Error fetching Instagram profile: {e}")
            return None
    
    def get_posts(self, username: str, max_posts: int = 10) -> List[SocialPost]:
        """Get recent posts from an Instagram profile"""
        if not self.loader:
            return []
        
        try:
            import instaloader
            profile = instaloader.Profile.from_username(self.loader.context, username)
            
            if profile.is_private:
                print(f"Profile @{username} is private")
                return []
            
            posts = []
            for i, post in enumerate(profile.get_posts()):
                if i >= max_posts:
                    break
                
                # Extract hashtags and mentions from caption
                caption = post.caption or ""
                hashtags = re.findall(r'#(\w+)', caption)
                mentions = re.findall(r'@(\w+)', caption)
                
                social_post = SocialPost(
                    platform="instagram",
                    post_id=post.shortcode,
                    url=f"https://www.instagram.com/p/{post.shortcode}/",
                    author=username,
                    content=caption,
                    timestamp=post.date_utc.isoformat() if post.date_utc else None,
                    likes=post.likes,
                    comments=post.comments,
                    media_urls=[post.url] if post.url else [],
                    hashtags=hashtags,
                    mentions=mentions,
                    raw_data={
                        "is_video": post.is_video,
                        "video_view_count": post.video_view_count if post.is_video else 0,
                        "location": str(post.location) if post.location else None,
                    }
                )
                posts.append(social_post)
                
                # Rate limiting
                time.sleep(0.5)
            
            return posts
            
        except Exception as e:
            print(f"Error fetching Instagram posts: {e}")
            return []


class FacebookScraper:
    """Facebook public page scraper using Selenium"""
    
    def __init__(self):
        self.driver = None
    
    def _init_driver(self):
        """Initialize Selenium WebDriver"""
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from fake_useragent import UserAgent
        
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"user-agent={UserAgent().random}")
        
        self.driver = webdriver.Chrome(options=options)
    
    def _close_driver(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def get_page_info(self, page_url: str) -> Optional[SocialProfile]:
        """Get Facebook page information"""
        try:
            self._init_driver()
            self.driver.get(page_url)
            time.sleep(3)  # Wait for page to load
            
            html = self.driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            
            # Try to extract basic info (Facebook structure changes frequently)
            title = soup.find("title")
            page_name = title.text.replace(" | Facebook", "").replace(" - Facebook", "") if title else ""
            
            # Extract description/bio
            meta_desc = soup.find("meta", {"name": "description"})
            bio = meta_desc.get("content", "") if meta_desc else ""
            
            return SocialProfile(
                platform="facebook",
                username=urlparse(page_url).path.strip("/"),
                display_name=page_name,
                bio=bio,
                url=page_url,
                raw_data={"html_snippet": str(soup)[:5000]}
            )
            
        except Exception as e:
            print(f"Error fetching Facebook page: {e}")
            return None
        finally:
            self._close_driver()


class TwitterScraper:
    """Twitter/X public profile scraper using Selenium"""
    
    def __init__(self):
        self.driver = None
    
    def _init_driver(self):
        """Initialize Selenium WebDriver"""
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from fake_useragent import UserAgent
        
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"user-agent={UserAgent().random}")
        
        self.driver = webdriver.Chrome(options=options)
    
    def _close_driver(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def get_profile(self, username: str) -> Optional[SocialProfile]:
        """Get Twitter/X profile information"""
        try:
            self._init_driver()
            url = f"https://twitter.com/{username}"
            self.driver.get(url)
            time.sleep(5)  # Twitter needs more time to load
            
            html = self.driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            
            # Extract basic info
            title = soup.find("title")
            title_text = title.text if title else ""
            
            # Parse display name from title
            display_name = title_text.split("(")[0].strip() if "(" in title_text else username
            
            return SocialProfile(
                platform="twitter",
                username=username,
                display_name=display_name,
                bio="",  # Requires more complex parsing
                url=url,
                raw_data={"html_snippet": str(soup)[:5000]}
            )
            
        except Exception as e:
            print(f"Error fetching Twitter profile: {e}")
            return None
        finally:
            self._close_driver()


class SocialMediaScraper:
    """Unified social media scraper"""
    
    def __init__(self):
        self.instagram = InstagramScraper()
        self.facebook = FacebookScraper()
        self.twitter = TwitterScraper()
    
    def detect_platform(self, url: str) -> Optional[str]:
        """Detect social media platform from URL"""
        domain = urlparse(url).netloc.lower()
        
        if "instagram.com" in domain:
            return "instagram"
        elif "facebook.com" in domain or "fb.com" in domain:
            return "facebook"
        elif "twitter.com" in domain or "x.com" in domain:
            return "twitter"
        elif "linkedin.com" in domain:
            return "linkedin"
        elif "tiktok.com" in domain:
            return "tiktok"
        elif "youtube.com" in domain or "youtu.be" in domain:
            return "youtube"
        
        return None
    
    def extract_username(self, url: str, platform: str) -> Optional[str]:
        """Extract username from social media URL"""
        parsed = urlparse(url)
        path = parsed.path.strip("/")
        
        if platform == "instagram":
            # instagram.com/username or instagram.com/username/
            parts = path.split("/")
            return parts[0] if parts else None
        
        elif platform == "twitter":
            # twitter.com/username or x.com/username
            parts = path.split("/")
            return parts[0] if parts else None
        
        elif platform == "facebook":
            # facebook.com/pagename
            parts = path.split("/")
            return parts[0] if parts else None
        
        return None
    
    def scrape(self, url: str, include_posts: bool = True, max_posts: int = 10) -> Dict[str, Any]:
        """
        Scrape social media profile and optionally posts
        
        Returns:
            Dictionary with 'profile' and optionally 'posts' keys
        """
        platform = self.detect_platform(url)
        
        if not platform:
            return {"error": "Unsupported platform or invalid URL"}
        
        username = self.extract_username(url, platform)
        if not username:
            return {"error": "Could not extract username from URL"}
        
        result = {"platform": platform, "username": username}
        
        if platform == "instagram":
            profile = self.instagram.get_profile(username)
            if profile:
                result["profile"] = profile.to_dict()
                result["profile_text"] = profile.to_text()
                
                if include_posts:
                    posts = self.instagram.get_posts(username, max_posts)
                    result["posts"] = [p.to_dict() for p in posts]
                    result["posts_text"] = "\n\n---\n\n".join([p.to_text() for p in posts])
        
        elif platform == "facebook":
            profile = self.facebook.get_page_info(url)
            if profile:
                result["profile"] = profile.to_dict()
                result["profile_text"] = profile.to_text()
        
        elif platform == "twitter":
            profile = self.twitter.get_profile(username)
            if profile:
                result["profile"] = profile.to_dict()
                result["profile_text"] = profile.to_text()
        
        return result
    
    def get_scraped_text(self, result: Dict[str, Any]) -> str:
        """Get all scraped content as text for AI parsing"""
        parts = []
        
        if "profile_text" in result:
            parts.append("=== PROFILE ===")
            parts.append(result["profile_text"])
        
        if "posts_text" in result:
            parts.append("\n=== POSTS ===")
            parts.append(result["posts_text"])
        
        return "\n".join(parts)


# Convenience functions
def scrape_instagram(username: str, include_posts: bool = True, max_posts: int = 10) -> Dict[str, Any]:
    """Scrape Instagram profile"""
    scraper = SocialMediaScraper()
    return scraper.scrape(f"https://instagram.com/{username}", include_posts, max_posts)


def scrape_social_media(url: str, include_posts: bool = True, max_posts: int = 10) -> Dict[str, Any]:
    """Scrape any supported social media platform"""
    scraper = SocialMediaScraper()
    return scraper.scrape(url, include_posts, max_posts)
