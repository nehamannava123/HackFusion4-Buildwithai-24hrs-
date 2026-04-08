# qa.py - Rule-based Q&A (fallback)
from typing import Dict

class CodebaseQA:
    def __init__(self, repo_info, arch_patterns, dependencies):
        self.repo = repo_info
    
    def ask(self, question: str) -> Dict:
        q = question.lower()
        
        if 'start' in q or 'begin' in q or 'entry' in q:
            entry = self.repo.entry_points[0] if self.repo.entry_points else 'README.md'
            answer = f"🎯 **Start here:** `{entry}`\n\nThis is the main entry point. Open this file first to understand the application flow."
        
        elif 'how many' in q or 'count' in q or 'files' in q:
            answer = f"📊 **Repository Statistics**\n\n- **Files:** {len(self.repo.files)}\n- **Lines of code:** {self.repo.total_lines:,}\n- **Language:** {self.repo.language}\n- **Framework:** {self.repo.framework if self.repo.framework else 'None detected'}"
        
        elif 'language' in q or 'tech' in q:
            answer = f"🛠 **Technology Stack**\n\n- **Primary Language:** {self.repo.language}\n- **Framework:** {self.repo.framework if self.repo.framework else 'None detected'}\n- **File types:** {', '.join([f'{ext}({count})' for ext, count in list(self.repo.file_types.items())[:5]])}"
        
        elif 'largest' in q or 'biggest' in q:
            answer = f"📄 **Largest file:** `{self.repo.largest_file}`" if self.repo.largest_file else "No files found."
        
        elif 'complex' in q:
            answer = f"🔧 **Most complex file:** `{self.repo.most_complex_file}`" if self.repo.most_complex_file else "Complexity analysis complete."
        
        else:
            answer = f"📊 **Repository Overview**\n\n- **Files:** {len(self.repo.files)}\n- **Lines:** {self.repo.total_lines:,}\n- **Language:** {self.repo.language}\n- **Entry point:** {self.repo.entry_points[0] if self.repo.entry_points else 'Auto-detect'}\n\n💡 Try asking:\n- 'Where should I start?'\n- 'What language is this?'\n- 'Explain what this project does' (with AI)"
        
        return {'answer': answer, 'type': 'rule'}