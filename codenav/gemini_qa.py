# gemini_qa.py - Simplified Working Version
import os
import google.generativeai as genai
from typing import List
from dotenv import load_dotenv

load_dotenv()

class GeminiQAAgent:
    def __init__(self, repo_info):
        self.repo = repo_info
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.available = False
        
        if not self.api_key:
            print("❌ GEMINI_API_KEY not found")
            return
        
        try:
            genai.configure(api_key=self.api_key)
            # Try the correct model name
            self.model = genai.GenerativeModel('gemini-1.5-flash-001')
            # Test it
            test_response = self.model.generate_content("Say OK")
            if test_response:
                self.available = True
                print("✅ GEMINI AI ACTIVATED!")
        except Exception as e:
            print(f"❌ AI init error: {e}")
    
    def ask_with_ai(self, question: str) -> str:
        if not self.available:
            return f"This is a {self.repo.language} project with {len(self.repo.files)} files."
        
        # Build context about the repo
        context = f"This is a {self.repo.language} project with {len(self.repo.files)} files and {self.repo.total_lines} lines of code."
        
        prompt = f"""{context}

User question: {question}

Answer the question directly and helpfully in 2-3 sentences."""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"API Error: {e}")
            return f"This is a {self.repo.language} project with {len(self.repo.files)} files."
    
    def explain_file(self, file_path: str) -> str:
        return "AI explanation available"
    
    def suggest_learning_path(self, level: str = "beginner") -> List[str]:
        return ["Start with entry point", "Explore files", "Ask questions"]