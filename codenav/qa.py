# qa.py - Rule-based Q&A (fallback when AI unavailable)
from typing import Dict

class CodebaseQA:
    def __init__(self, repo_info, arch_patterns, dependencies):
        self.repo = repo_info
    
    def ask(self, question: str) -> Dict:
        q = question.lower()
        
        # File count questions
        if 'how many' in q and 'file' in q:
            answer = f"📊 This repository contains **{len(self.repo.files)} files** with **{self.repo.total_lines:,} lines** of code."
        
        # Language questions
        elif 'language' in q or 'what language' in q:
            answer = f"🛠 Primary language: **{self.repo.language.upper()}**\n\nFile types: {', '.join([f'{ext}({count})' for ext, count in list(self.repo.file_types.items())[:5]])}"
        
        # Starting point
        elif 'start' in q or 'begin' in q or 'entry' in q:
            if self.repo.entry_points:
                answer = f"📍 **Start here:** `{self.repo.entry_points[0]}`\n\nThis is the main entry point. Open this file first to understand how the application works."
            else:
                answer = "📁 No clear entry point detected. Look for: main.py, app.py, index.js, or index.html"
        
        # Largest file
        elif 'largest' in q or 'biggest' in q:
            if self.repo.files:
                largest = max(self.repo.files, key=lambda f: f.lines)
                answer = f"📄 **Largest file:** `{largest.name}`\n- Lines: {largest.lines}\n- Type: {largest.file_type}"
            else:
                answer = "No files found."
        
        # List files
        elif 'list' in q or 'show me' in q:
            files_list = '\n'.join([f"• `{f.name}` ({f.lines} lines, {f.file_type})" for f in self.repo.files[:15]])
            answer = f"📁 **Files in this repository ({len(self.repo.files)} total):**\n\n{files_list}"
            if len(self.repo.files) > 15:
                answer += f"\n\n... and {len(self.repo.files) - 15} more files"
        
        # Specific file question
        elif 'what is' in q:
            for file in self.repo.files:
                if file.name.lower().replace('.py', '').replace('.js', '') in q:
                    answer = f"📄 **{file.name}**\n- Path: `{file.path}`\n- Lines: {file.lines}\n- Type: {file.file_type}\n- Functions: {len(file.functions)}\n- Classes: {len(file.classes)}"
                    break
            else:
                answer = f"📊 This is a **{self.repo.language.upper()}** project with **{len(self.repo.files)} files** and **{self.repo.total_lines:,} lines** of code.\n\nTry asking about specific files by name."
        
        # General info
        else:
            answer = f"""**📊 Repository Overview**

- **Files:** {len(self.repo.files)}
- **Lines of code:** {self.repo.total_lines:,}
- **Primary language:** {self.repo.language.upper()}
- **Entry point:** {self.repo.entry_points[0] if self.repo.entry_points else 'Not detected'}
- **Framework:** {self.repo.framework if self.repo.framework else 'None detected'}

**💡 Try asking:**
- "How many files?"
- "What language is this?"
- "Where should I start?"
- "What is the largest file?"
- "List all files"
- "What is [filename]?" """
        
        return {'answer': answer, 'type': 'rule'}