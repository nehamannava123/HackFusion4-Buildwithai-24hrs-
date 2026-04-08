# qa.py
import re
from typing import Dict

class CodebaseQA:
    def __init__(self, repo_info, architecture_patterns: Dict, dependencies: Dict):
        self.repo = repo_info
        self.arch_patterns = architecture_patterns
    
    def ask(self, question: str) -> Dict:
        q_lower = question.lower()
        
        if 'start' in q_lower or 'begin' in q_lower:
            answer = self._answer_start()
        elif 'flow' in q_lower or 'how' in q_lower:
            answer = self._answer_flow()
        elif 'what' in q_lower:
            answer = self._answer_what(question)
        elif 'where' in q_lower:
            answer = self._answer_where(question)
        else:
            answer = self._answer_general()
        
        return {'question': question, 'answer': answer, 'type': 'general'}
    
    def _answer_start(self) -> str:
        if self.repo.entry_points:
            return f"**Start with {self.repo.entry_points[0]}** - This is the main entry point.\n\nNext: Open this file and look for the main() function or initialization code."
        return "Look for main.py, app.py, or index.js as the entry point."
    
    def _answer_flow(self) -> str:
        return """**Typical execution flow:**
1. Entry point loads configuration
2. Dependencies are initialized  
3. Request/command is processed
4. Business logic executes
5. Response is returned"""
    
    def _answer_what(self, question: str) -> str:
        return f"This is a {self.repo.language} project with {len(self.repo.files)} files and {self.repo.total_lines:,} lines of code."
    
    def _answer_where(self, question: str) -> str:
        return f"Check these directories: {', '.join(set([f.path.split('/')[0] for f in self.repo.files[:5]]))}"
    
    def _answer_general(self) -> str:
        return """I can help you understand this codebase. Try asking:
- 'Where should I start?'
- 'How does authentication flow?'
- 'What is the project structure?'
- 'Where are the models?'"""