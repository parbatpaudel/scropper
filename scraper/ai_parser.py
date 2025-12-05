"""
AI Parser with Chat - Fixed Model
"""

import os
from typing import List, Dict
from dotenv import load_dotenv

# Load env
if os.path.exists('.env'):
    load_dotenv('.env')
elif os.path.exists('.env.example'):
    load_dotenv('.env.example')
else:
    load_dotenv()

# Config - using mixtral which is stable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")
SUPERMEMORY_API_KEY = os.getenv("SUPERMEMORY_API_KEY")


class GroqProvider:
    def __init__(self):
        self.api_key = GROQ_API_KEY
        self.model = GROQ_MODEL
        self.client = None
    
    def _init(self):
        if not self.client:
            from groq import Groq
            self.client = Groq(api_key=self.api_key)
    
    def chat(self, messages: List[Dict], max_tokens: int = 4000) -> str:
        self._init()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    
    def is_available(self) -> bool:
        return bool(self.api_key)


class SuperMemory:
    def __init__(self):
        self.api_key = SUPERMEMORY_API_KEY
        self.memories = []
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def add(self, content: str):
        self.memories.append(content)
    
    def search(self, query: str) -> List[str]:
        results = []
        q = query.lower()
        for m in self.memories:
            if q in m.lower():
                results.append(m)
        return results[:5]
    
    def clear(self):
        self.memories = []


class AIChat:
    def __init__(self, content: str = ""):
        self.provider = GroqProvider()
        self.memory = SuperMemory()
        self.content = content
        self.history: List[Dict] = []
        
        if content:
            self.memory.add(content)
    
    def set_context(self, content: str):
        self.content = content
        self.memory.add(content)
    
    def chat(self, message: str) -> str:
        if not self.provider.is_available():
            return "Error: Add GROQ_API_KEY to .env file"
        
        system = f"""You are a helpful assistant with access to scraped website data.
Answer questions based on this data. Be accurate and helpful.

SCRAPED DATA:
{self.content[:30000]}

Instructions:
- Answer based on the data above
- If not found, say so
- Be conversational and helpful"""

        messages = [{"role": "system", "content": system}]
        messages.extend(self.history[-10:])
        messages.append({"role": "user", "content": message})
        
        try:
            response = self.provider.chat(messages)
            self.history.append({"role": "user", "content": message})
            self.history.append({"role": "assistant", "content": response})
            return response
        except Exception as e:
            return f"Error: {str(e)}"
    
    def clear(self):
        self.history = []


class AIParser:
    def __init__(self):
        self.provider = GroqProvider()
    
    def extract(self, content: str, request: str) -> str:
        prompt = f"Extract from this content:\n\nREQUEST: {request}\n\nCONTENT:\n{content[:25000]}"
        return self.provider.chat([{"role": "user", "content": prompt}])
    
    def summarize(self, content: str) -> str:
        prompt = f"Summarize this content:\n\n{content[:25000]}"
        return self.provider.chat([{"role": "user", "content": prompt}])
    
    def analyze_brand(self, content: str) -> str:
        prompt = f"Analyze this brand:\n\n{content[:25000]}\n\nInclude: Overview, Products, Audience, Values, Contact"
        return self.provider.chat([{"role": "user", "content": prompt}])


def is_groq_configured() -> bool:
    return bool(GROQ_API_KEY)

def is_supermemory_configured() -> bool:
    return bool(SUPERMEMORY_API_KEY)
