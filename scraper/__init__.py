"""
Scraper module
"""

from .web_scraper import (
    SmartWebScraper,
    QuickScraper,
    ScrapedPage,
)

from .ai_parser import (
    AIParser,
    AIChat,
    GroqProvider,
    SuperMemory,
    is_groq_configured,
    is_supermemory_configured,
)

from .exporter import (
    DataExporter,
    export_to_json,
    export_to_csv,
)

__all__ = [
    "SmartWebScraper",
    "QuickScraper",
    "ScrapedPage",
    "AIParser",
    "AIChat",
    "GroqProvider",
    "SuperMemory",
    "is_groq_configured",
    "is_supermemory_configured",
    "DataExporter",
    "export_to_json",
    "export_to_csv",
]
