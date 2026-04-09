<<<<<<< HEAD
# qa.py
import re
from typing import Dict

class CodebaseQA:
    def __init__(self, repo_info, architecture_patterns: Dict, dependencies: Dict):
        self.repo = repo_info
        self.arch_patterns = architecture_patterns
    
    def ask(self, question: str) -> Dict:
        q_lower = question.lower()
        
        # Check for specific question types
        if 'start' in q_lower or 'begin' in q_lower or 'entry' in q_lower:
            answer = self._answer_start()
        elif 'flow' in q_lower or 'how' in q_lower or 'process' in q_lower:
            answer = self._answer_flow(question)
        elif 'what' in q_lower or 'explain' in q_lower or 'tell me about' in q_lower:
            answer = self._answer_what(question)
        elif 'where' in q_lower or 'find' in q_lower or 'location' in q_lower:
            answer = self._answer_where(question)
        elif 'file' in q_lower or 'files' in q_lower:
            answer = self._answer_files()
        elif 'language' in q_lower or 'tech' in q_lower:
            answer = self._answer_language()
        else:
            answer = self._answer_general()
        
        return {'question': question, 'answer': answer, 'type': 'general'}
    
    def _answer_start(self) -> str:
        if self.repo.entry_points:
            entry = self.repo.entry_points[0]
            return f"""**🎯 Start Here: {entry}**

This is the recommended starting point for exploring this codebase.

**Next Steps:**
1. Open this file to see what it contains
2. Look for initialization or main functions
3. Check what other files it references

**💡 Tip:** You can also ask about specific files or request a flow simulation."""
        
        return """**📁 Exploring This Project**

No clear entry point was detected. Here's how to start:

1. **Browse the files** - Look for README, main, or index files
2. **Check file types** - See what kind of project this is
3. **Ask me** - "What files are here?" or "Show me all files"

**Common files to look for:**
- README.md, main.py, app.js, index.html, Dockerfile, Makefile"""
    
    def _answer_flow(self, question: str) -> str:
        return """**🔄 Understanding Code Flow**

To understand how this code works, try:

1. **Use flow simulation:** Type `flow [topic]` where topic is:
   - `authentication` - Login/auth flows
   - `database` - Data access patterns
   - `api_request` - HTTP request handling
   - `file_upload` - File processing

2. **Follow dependencies:** Look at imports to see file relationships

3. **Trace execution:** Start from entry point and follow function calls

**Example:** Try typing `flow authentication` to see a sample flow diagram!"""
    
    def _answer_what(self, question: str) -> str:
        # Try to extract file name from question
        words = question.split()
        for word in words:
            # Check if word might be a filename
            if '.' in word or word.endswith(('py', 'js', 'html', 'css', 'md', 'txt')):
                for file in self.repo.files:
                    if word.lower() in file.name.lower():
                        return self._describe_file(file)
        
        # General what answer
        return f"""**📊 About This Project**

- **Files:** {len(self.repo.files)} files
- **Lines:** {self.repo.total_lines:,} lines of code
- **Language:** {self.repo.language.upper()}
- **File types:** {', '.join(list(self.repo.file_types.keys())[:5])}

**To learn more, ask:**
- "What files are here?"
- "Show me the largest file"
- "What is [filename]?" """
    
    def _describe_file(self, file) -> str:
        desc = f"""**📄 {file.name}**

- **Type:** {file.file_type.upper() if file.file_type != 'unknown' else file.extension.upper()}
- **Lines:** {file.lines}
- **Size:** {file.size} bytes

**Contents:**
"""
        if file.functions:
            desc += f"- Functions: {', '.join([f['name'] for f in file.functions[:5]])}\n"
        if file.classes:
            desc += f"- Classes: {', '.join([c['name'] for c in file.classes[:5]])}\n"
        
        return desc
    
    def _answer_where(self, question: str) -> str:
        # Extract search term
        words = question.split()
        search_term = None
        for word in words:
            if len(word) > 3 and word not in ['where', 'find', 'location', 'the', 'is', 'are']:
                search_term = word.strip('?.,!')
                break
        
        if search_term:
            matches = [f for f in self.repo.files if search_term.lower() in f.name.lower() or search_term.lower() in f.path.lower()]
            if matches:
                result = f"**🔍 Found '{search_term}' in:**\n\n"
                for match in matches[:10]:
                    result += f"• `{match.path}` ({match.lines} lines)\n"
                if len(matches) > 10:
                    result += f"\n... and {len(matches) - 10} more files"
                return result
        
        return f"""**📁 Directory Structure**

Files are organized in this repository. Here are all the file types:

{', '.join([f"{ext}: {count}" for ext, count in list(self.repo.file_types.items())[:10]])}

**To find specific files, ask:**
- "Where is the main file?"
- "Find all Python files"
- "Show me the largest file" """
    
    def _answer_files(self) -> str:
        if not self.repo.files:
            return "No files found in this repository."
        
        result = f"**📁 All Files ({len(self.repo.files)} total)**\n\n"
        
        # Group by type
        by_type = {}
        for file in self.repo.files:
            ext = file.extension if file.extension != 'no_ext' else 'no_extension'
            if ext not in by_type:
                by_type[ext] = []
            by_type[ext].append(file)
        
        for ext, files in sorted(by_type.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
            result += f"**.{ext}** ({len(files)} files)\n"
            for file in files[:3]:
                result += f"  • {file.name}\n"
            if len(files) > 3:
                result += f"  • ... and {len(files) - 3} more\n"
            result += "\n"
        
        return result
    
    def _answer_language(self) -> str:
        return f"""**🛠️ Technology Stack**

- **Primary Language:** {self.repo.language.upper()}
- **Files analyzed:** {len(self.repo.files)}
- **Total lines:** {self.repo.total_lines:,}

**File type breakdown:**
{', '.join([f"{ext}: {count}" for ext, count in list(self.repo.file_types.items())[:8]])}

**Note:** Language detection is based on file extensions and content analysis."""
    
    def _answer_general(self) -> str:
        return """**💡 I can help you explore this codebase!**

**Try asking me:**

📌 **Getting Started:**
- "Where should I start?"
- "What files are here?"

🔄 **Understanding Flow:**
- "How does authentication work?"
- "flow database"

📁 **Finding Things:**
- "What is main.py?"
- "Find all Python files"
- "Show me the largest file"

📊 **Project Info:**
- "What language is this?"
- "Tell me about this project"

**Just type your question naturally - I'll do my best to help!** """
=======
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
>>>>>>> 7db48e7 (Final version: CodeNav AI complete)
