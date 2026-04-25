import os
import requests
from dotenv import load_dotenv

load_dotenv()

class DirectAIAgent:
    def __init__(self, repo_info):
        self.repo = repo_info
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.available = bool(self.api_key)
        
        if self.available:
            print("✅ DIRECT API MODE ACTIVATED!")
        else:
            print("❌ No API key found")
    
    def answer(self, question: str) -> str:
        if not self.available:
            return "AI not available - please set GEMINI_API_KEY"
        
        # Use the model from your API response
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": question}]
            }]
        }
        
        try:
            response = requests.post(url, json=payload)
            result = response.json()
            
            if response.status_code == 200:
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                error_msg = result.get('error', {}).get('message', 'Unknown error')
                return f"API Error: {error_msg}"
        except Exception as e:
            return f"Error: {e}"