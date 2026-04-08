# ai_qa.py - Real AI integration with Ollama (FIXED)
import subprocess
import os
from typing import List

class AIQAAgent:
    def __init__(self, repo_info):
        self.repo = repo_info
        self.model = "llama3.2:1b"
        # Your correct Ollama path
        self.ollama_path = r"C:\Users\Thanu\AppData\Local\Programs\Ollama\ollama.exe"
        self.available = self._check_ollama()
        
        if self.available:
            print(f"✅ AI READY! Using: {self.ollama_path}")
        else:
            print(f"❌ AI NOT AVAILABLE")
    
    def _check_ollama(self) -> bool:
        """Check if Ollama is working"""
        try:
            if not os.path.exists(self.ollama_path):
                return False
            
            result = subprocess.run(
                [self.ollama_path, "list"], 
                capture_output=True, 
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                return False
            
            if self.model not in result.stdout:
                print(f"📥 Downloading {self.model}...")
                subprocess.run([self.ollama_path, "pull", self.model], timeout=300)
                print(f"✅ Model ready!")
            
            return True
        except Exception as e:
            print(f"Ollama check failed: {e}")
            return False
    
    def ask_with_ai(self, question: str) -> str:
        """Answer using AI"""
        if not self.available:
            return self._fallback()
        
        # Build context
        context = f"Language: {self.repo.language}, Files: {len(self.repo.files)}, Lines: {self.repo.total_lines}"
        entry = self.repo.entry_points[0] if self.repo.entry_points else "None"
        
        prompt = f"""You are CodeNav AI. Answer this question about the codebase:

{context}
Entry point: {entry}

Question: {question}

Answer concisely and helpfully (max 2 sentences):"""
        
        try:
            result = subprocess.run(
                [self.ollama_path, "run", self.model, prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.stdout.strip():
                return result.stdout.strip()
            return self._fallback()
        except Exception as e:
            print(f"AI error: {e}")
            return self._fallback()
    
    def _fallback(self) -> str:
        return f"This is a {self.repo.language} project with {len(self.repo.files)} files and {self.repo.total_lines} lines."
    
    def explain_file(self, file_path: str) -> str:
        if not self.available:
            return "AI unavailable"
        return f"File: {file_path}"
    
    def suggest_learning_path(self, level: str = "beginner") -> List[str]:
        return ["Start with entry point", "Explore files", "Ask questions"]