"""
Data Export Module
Export scraped data to various formats
"""

import os
import json
import csv
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


class DataExporter:
    """Export scraped data to various formats"""
    
    def __init__(self, output_dir: str = "exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def _generate_filename(self, base_name: str, extension: str) -> Path:
        """Generate unique filename with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in base_name)
        return self.output_dir / f"{safe_name}_{timestamp}.{extension}"
    
    def to_json(self, data: Any, filename: str = "scraped_data") -> str:
        """Export data to JSON file"""
        output_path = self._generate_filename(filename, "json")
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        
        return str(output_path)
    
    def to_csv(self, data: Dict[str, str], filename: str = "scraped_data") -> str:
        """
        Export URL-content mapping to CSV
        
        Args:
            data: Dictionary mapping URLs to content
            filename: Base filename
        """
        output_path = self._generate_filename(filename, "csv")
        
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["URL", "Content"])
            
            for url, content in data.items():
                # Truncate content if too long for CSV
                truncated = content[:32000] if len(content) > 32000 else content
                writer.writerow([url, truncated])
        
        return str(output_path)
    
    def to_excel(self, data: Dict[str, str], filename: str = "scraped_data") -> str:
        """
        Export URL-content mapping to Excel
        
        Args:
            data: Dictionary mapping URLs to content
            filename: Base filename
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("pandas not installed. Run: pip install pandas openpyxl")
        
        output_path = self._generate_filename(filename, "xlsx")
        
        df = pd.DataFrame([
            {"URL": url, "Content": content}
            for url, content in data.items()
        ])
        
        df.to_excel(output_path, index=False, engine="openpyxl")
        
        return str(output_path)
    
    def to_markdown(self, data: Dict[str, str], filename: str = "scraped_data") -> str:
        """Export data to Markdown file"""
        output_path = self._generate_filename(filename, "md")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# Scraped Data\n\n")
            f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            f.write(f"**Total Pages: {len(data)}**\n\n")
            f.write("---\n\n")
            
            for i, (url, content) in enumerate(data.items(), 1):
                f.write(f"## Page {i}\n\n")
                f.write(f"**URL:** {url}\n\n")
                f.write(f"### Content\n\n")
                f.write(f"```\n{content[:5000]}\n```\n\n")
                
                if len(content) > 5000:
                    f.write(f"*Content truncated. Full length: {len(content)} characters*\n\n")
                
                f.write("---\n\n")
        
        return str(output_path)
    
    def to_text(self, data: Dict[str, str], filename: str = "scraped_data") -> str:
        """Export data to plain text file"""
        output_path = self._generate_filename(filename, "txt")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"SCRAPED DATA\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Pages: {len(data)}\n")
            f.write("=" * 80 + "\n\n")
            
            for i, (url, content) in enumerate(data.items(), 1):
                f.write(f"PAGE {i}\n")
                f.write(f"URL: {url}\n")
                f.write("-" * 40 + "\n")
                f.write(content)
                f.write("\n\n" + "=" * 80 + "\n\n")
        
        return str(output_path)
    
    def save_session(
        self,
        scraped_data: Dict[str, str],
        parsed_results: Dict[str, Any] = None,
        metadata: Dict[str, Any] = None,
        filename: str = "scraping_session"
    ) -> str:
        """Save complete scraping session"""
        session_data = {
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
            "scraped_pages": len(scraped_data),
            "urls": list(scraped_data.keys()),
            "content": scraped_data,
            "parsed_results": parsed_results or {},
        }
        
        return self.to_json(session_data, filename)
    
    def load_session(self, filepath: str) -> Dict[str, Any]:
        """Load a saved scraping session"""
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)


class ReportGenerator:
    """Generate reports from scraped data"""
    
    def __init__(self, exporter: DataExporter = None):
        self.exporter = exporter or DataExporter()
    
    def generate_summary_report(
        self,
        scraped_data: Dict[str, str],
        parsed_results: str = None,
        filename: str = "scraping_report"
    ) -> str:
        """Generate a summary report in Markdown"""
        output_path = self.exporter._generate_filename(filename, "md")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# Web Scraping Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Summary stats
            f.write("## Summary\n\n")
            total_chars = sum(len(c) for c in scraped_data.values())
            f.write(f"- **Pages Scraped:** {len(scraped_data)}\n")
            f.write(f"- **Total Content:** {total_chars:,} characters\n")
            f.write(f"- **Average per Page:** {total_chars // len(scraped_data):,} characters\n\n")
            
            # URLs list
            f.write("## Scraped URLs\n\n")
            for i, url in enumerate(scraped_data.keys(), 1):
                f.write(f"{i}. {url}\n")
            f.write("\n")
            
            # Parsed results
            if parsed_results:
                f.write("## AI Parsed Results\n\n")
                f.write(parsed_results)
                f.write("\n\n")
            
            # Content preview
            f.write("## Content Preview\n\n")
            for url, content in scraped_data.items():
                f.write(f"### {url}\n\n")
                preview = content[:500] + "..." if len(content) > 500 else content
                f.write(f"{preview}\n\n")
        
        return str(output_path)


# Convenience functions
def export_to_json(data: Any, filename: str = "data") -> str:
    """Quick export to JSON"""
    exporter = DataExporter()
    return exporter.to_json(data, filename)


def export_to_csv(data: Dict[str, str], filename: str = "data") -> str:
    """Quick export to CSV"""
    exporter = DataExporter()
    return exporter.to_csv(data, filename)


def export_to_excel(data: Dict[str, str], filename: str = "data") -> str:
    """Quick export to Excel"""
    exporter = DataExporter()
    return exporter.to_excel(data, filename)
