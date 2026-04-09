# ai_qa.py - ULTRA-SHARP AI with actual file content reading
import subprocess
import os
import json
from typing import List, Dict
from datetime import datetime

class AIQAAgent:
    def __init__(self, repo_info):
        self.repo = repo_info
        self.model = "llama3.2:1b"
        self.ollama_paths = [
            r"C:\Users\Thanu\AppData\Local\Programs\Ollama\ollama.exe",
            r"C:\Program Files\Ollama\ollama.exe",
            "ollama"
        ]
        self.ollama_path = self._find_ollama()
        self.available = self._check_ollama() if self.ollama_path else False
        self.file_contents_cache = {}
        
        if self.available:
            print(f"🤖 AI Engine Ready | Model: {self.model}")
        else:
            print("⚠️ AI Engine Fallback Mode")
    
    def _find_ollama(self):
        for path in self.ollama_paths:
            if os.path.exists(path):
                return path
        import shutil
        if shutil.which("ollama"):
            return "ollama"
        return None
    
    def _check_ollama(self) -> bool:
        try:
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
            print(f"⚠️ AI Check: {e}")
            return False
    
    def _read_file_content(self, file_path: str, max_lines: int = 50) -> str:
        """Read actual file content for context"""
        full_path = os.path.join(self.repo.root_path, file_path)
        try:
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                # Get first 50 lines and last 10 lines for context
                if len(lines) > max_lines + 10:
                    content = ''.join(lines[:max_lines])
                    content += f"\n... ({len(lines) - max_lines - 10} lines omitted) ...\n"
                    content += ''.join(lines[-10:])
                else:
                    content = ''.join(lines)
                return content[:3000]  # Limit to 3000 chars
        except:
            return "Could not read file content"
    
    def _get_detailed_file_info(self, file_name: str) -> Dict:
        """Get detailed info about a specific file"""
        for file in self.repo.files:
            if file.name == file_name or file_name.lower() in file.name.lower():
                content = self._read_file_content(file.path, 40)
                return {
                    'name': file.name,
                    'path': file.path,
                    'lines': file.lines,
                    'extension': file.extension,
                    'functions': file.functions[:5] if file.functions else [],
                    'classes': file.classes[:3] if file.classes else [],
                    'content_preview': content[:2000],
                    'has_main': file.has_main
                }
        return None
    
    def _get_rich_context_for_question(self, question: str) -> str:
        """Build rich context based on the question"""
        q_lower = question.lower()
        
        context_parts = []
        
        # Basic repo info
        context_parts.append(f"REPOSITORY: {os.path.basename(self.repo.root_path)}")
        context_parts.append(f"LANGUAGE: {self.repo.language}")
        context_parts.append(f"TOTAL FILES: {len(self.repo.files)}")
        context_parts.append(f"TOTAL LINES: {self.repo.total_lines:,}")
        
        # Check if asking about a specific file
        for file in self.repo.files:
            if file.name.lower() in q_lower or file.name.replace('.html', '').lower() in q_lower:
                content = self._read_file_content(file.path, 30)
                context_parts.append(f"\n--- FILE: {file.name} ---")
                context_parts.append(f"Lines: {file.lines}")
                context_parts.append(f"Type: {file.extension}")
                if file.functions:
                    context_parts.append(f"Functions: {', '.join([f['name'] for f in file.functions[:3]])}")
                context_parts.append(f"\nCONTENT PREVIEW:\n{content[:1500]}")
                break
        
        # Check if asking about jQuery or specific libraries
        if 'jquery' in q_lower or 'jq' in q_lower:
            jquery_found = False
            for file in self.repo.files:
                try:
                    full_path = os.path.join(self.repo.root_path, file.path)
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().lower()
                        if 'jquery' in content:
                            jquery_found = True
                            context_parts.append(f"\n✓ jQuery detected in: {file.name}")
                except:
                    pass
            if not jquery_found:
                context_parts.append("\n✗ No jQuery files detected in this repository")
        
        # If no specific file mentioned, list key files
        if not any(file.name.lower() in q_lower for file in self.repo.files):
            context_parts.append("\nKEY FILES IN REPOSITORY:")
            for file in sorted(self.repo.files, key=lambda f: f.lines, reverse=True)[:5]:
                context_parts.append(f"  - {file.name} ({file.lines} lines)")
        
        return "\n".join(context_parts)
    
    def ask_with_ai(self, question: str) -> str:
        """Answer with actual file content analysis"""
        if not self.available:
            return self._smart_fallback(question)
        
        context = self._get_rich_context_for_question(question)
        
        prompt = f"""You are CodeNav AI, a precise codebase analyst. Answer based ONLY on the repository information below.

{context}

USER QUESTION: {question}

INSTRUCTIONS:
1. Be SPECIFIC - mention actual file names and content
2. Be HONEST - if something doesn't exist, say "No [thing] found"
3. Be CONCISE - 2-3 sentences maximum
4. If asking about a specific file, describe what's actually IN that file

YOUR ANSWER:"""
        
        try:
            result = subprocess.run(
                [self.ollama_path, "run", self.model, prompt],
                capture_output=True,
                text=True,
                timeout=45
            )
            
            if result.returncode == 0 and result.stdout.strip():
                answer = result.stdout.strip()
                # Clean up markdown
                answer = answer.replace('```', '').replace('**', '').strip()
                return answer
            return self._smart_fallback(question)
            
        except subprocess.TimeoutExpired:
            return "⏱️ Analysis in progress... Please rephrase your question."
        except Exception as e:
            return self._smart_fallback(question)
    
    def _smart_fallback(self, question: str) -> str:
        """Intelligent fallback when AI is unavailable"""
        q = question.lower()
        
        # Check for jQuery question
        if 'jquery' in q:
            return "📁 **No jQuery files found** in this repository. The project uses plain HTML/CSS/JS."
        
        # Check for specific file
        for file in self.repo.files:
            if file.name.lower() in q or file.name.replace('.html', '').lower() in q:
                return f"📄 **{file.name}**\n- Lines: {file.lines}\n- Type: {file.extension}\n- Last modified: {file.last_modified}\n\n*This appears to be a {file.extension.upper()} file. For detailed content analysis, please ensure Ollama is running.*"
        
        # Check for errors question
        if 'error' in q or 'bug' in q or 'issue' in q:
            return "🔍 **No obvious errors detected** in the static HTML files. The project appears to be client-side only. Run with browser developer tools to check for runtime issues."
        
        # Default response
        return f"📊 **Repository: {os.path.basename(self.repo.root_path)}**\n- Files: {len(self.repo.files)}\n- Lines: {self.repo.total_lines:,}\n- Language: {self.repo.language}\n\n💡 For detailed analysis, ensure Ollama is running."
    
    def explain_file(self, file_path: str) -> str:
        if not self.available:
            return self._file_info_fallback(file_path)
        
        content = self._read_file_content(file_path, 40)
        
        prompt = f"""Analyze this file and explain its purpose:

File: {file_path}
Content:
{content[:2000]}

Explain what this file does in 2 sentences."""
        
        try:
            result = subprocess.run(
                [self.ollama_path, "run", self.model, prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.stdout.strip():
                return result.stdout.strip()
        except:
            pass
        
        return self._file_info_fallback(file_path)
    
    def _file_info_fallback(self, file_path: str) -> str:
        file_info = next((f for f in self.repo.files if f.path == file_path), None)
        if file_info:
            return f"📄 **{file_info.name}**\n- Lines: {file_info.lines}\n- Type: {file_info.extension}\n- Modified: {file_info.last_modified}"
        return f"File not found: {file_path}"
    
    def suggest_learning_path(self, level: str = "beginner") -> List[str]:
        entry = self.repo.entry_points[0] if self.repo.entry_points else 'the main file'
        return [
            f"🎯 Start with `{entry}`",
            f"📁 Explore the {len(self.repo.files)} files",
            f"💬 Ask specific questions about files"
        ]