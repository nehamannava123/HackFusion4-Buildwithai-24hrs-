# analyzer.py - Advanced GitHub repository analyzer
import os
import re
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from collections import defaultdict
from datetime import datetime

@dataclass
class FileInfo:
    path: str
    name: str
    extension: str
    size: int
    lines: int
    functions: List[Dict] = field(default_factory=list)
    classes: List[Dict] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    has_main: bool = False
    file_type: str = "unknown"
    last_modified: str = ""

@dataclass
class RepoInfo:
    root_path: str
    files: List[FileInfo] = field(default_factory=list)
    entry_points: List[str] = field(default_factory=list)
    dependencies: Dict[str, List[str]] = field(default_factory=dict)
    language: str = "unknown"
    framework: str = "unknown"
    total_lines: int = 0
    file_types: Dict[str, int] = field(default_factory=dict)
    largest_file: Optional[str] = None
    most_complex_file: Optional[str] = None

class RepoAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.repo_info = RepoInfo(root_path=str(repo_path))
        self.ignore_dirs = {
            'node_modules', 'venv', 'env', '__pycache__', '.git', 
            'dist', 'build', '.next', '.nuxt', '.cache', '.idea', 
            '.vscode', 'coverage', '.pytest_cache'
        }
        
    def analyze(self) -> RepoInfo:
        print(f"🔍 Analyzing {self.repo_path}...")
        self._scan_files()
        self._calculate_metrics()
        self._detect_entry_points()
        self._detect_language()
        self._detect_framework()
        self._find_largest_file()
        self._calculate_complexity()
        
        print(f"   ✅ {len(self.repo_info.files)} files | {self.repo_info.total_lines:,} lines | {self.repo_info.language.upper()}")
        if self.repo_info.entry_points:
            print(f"   🎯 Entry point: {self.repo_info.entry_points[0]}")
        return self.repo_info
    
    def _scan_files(self):
        extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.htm', 
            '.css', '.scss', '.sass', '.json', '.md', '.txt', 
            '.java', '.go', '.rb', '.php', '.c', '.cpp', '.h', 
            '.hpp', '.cs', '.swift', '.kt', '.rs', '.xml', '.yaml', '.yml'
        }
        
        for file_path in self.repo_path.rglob('*'):
            if any(ignore in file_path.parts for ignore in self.ignore_dirs):
                continue
            if file_path.is_file() and file_path.suffix in extensions:
                self.repo_info.files.append(self._parse_file(file_path))
    
    def _parse_file(self, file_path: Path) -> FileInfo:
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
        except:
            content = ""
        
        lines = content.split('\n')
        modified = datetime.fromtimestamp(file_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        
        file_info = FileInfo(
            path=str(file_path.relative_to(self.repo_path)),
            name=file_path.name,
            extension=file_path.suffix[1:] if file_path.suffix else 'txt',
            size=file_path.stat().st_size,
            lines=len(lines),
            file_type=file_path.suffix[1:] if file_path.suffix else 'txt',
            last_modified=modified
        )
        
        # Parse Python
        if file_path.suffix == '.py':
            self._parse_python(content, file_info)
        elif file_path.suffix in ['.js', '.ts', '.jsx', '.tsx']:
            self._parse_javascript(content, file_info)
        elif file_path.suffix in ['.html', '.htm']:
            self._parse_html(content, file_info)
        elif file_path.suffix == '.java':
            self._parse_java(content, file_info)
        elif file_path.suffix == '.go':
            self._parse_go(content, file_info)
        else:
            self._parse_generic(content, file_info)
        
        return file_info
    
    def _parse_python(self, content: str, file_info: FileInfo):
        lines = content.split('\n')
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            if line_stripped.startswith('def '):
                match = re.search(r'def\s+(\w+)', line)
                if match:
                    file_info.functions.append({'name': match.group(1), 'line': i+1})
            elif line_stripped.startswith('class '):
                match = re.search(r'class\s+(\w+)', line)
                if match:
                    file_info.classes.append({'name': match.group(1), 'line': i+1})
            elif line_stripped.startswith('import ') or line_stripped.startswith('from '):
                file_info.imports.append(line_stripped)
            elif 'if __name__ == "__main__"' in line:
                file_info.has_main = True
    
    def _parse_javascript(self, content: str, file_info: FileInfo):
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'function ' in line:
                match = re.search(r'function\s+(\w+)', line)
                if match:
                    file_info.functions.append({'name': match.group(1), 'line': i+1})
            elif 'class ' in line:
                match = re.search(r'class\s+(\w+)', line)
                if match:
                    file_info.classes.append({'name': match.group(1), 'line': i+1})
            elif 'import ' in line or 'require(' in line:
                file_info.imports.append(line.strip())
    
    def _parse_html(self, content: str, file_info: FileInfo):
        title_match = re.search(r'<title>([^<]+)</title>', content, re.IGNORECASE)
        if title_match:
            file_info.imports.append(f"Title: {title_match.group(1)}")
        
        script_count = len(re.findall(r'<script', content, re.IGNORECASE))
        if script_count > 0:
            file_info.imports.append(f"Contains {script_count} script(s)")
        
        css_count = len(re.findall(r'<link[^>]*stylesheet', content, re.IGNORECASE))
        if css_count > 0:
            file_info.imports.append(f"Links {css_count} CSS file(s)")
    
    def _parse_java(self, content: str, file_info: FileInfo):
        lines = content.split('\n')
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            if 'public static void main' in line_stripped:
                file_info.has_main = True
            elif 'class ' in line_stripped:
                match = re.search(r'class\s+(\w+)', line_stripped)
                if match:
                    file_info.classes.append({'name': match.group(1), 'line': i+1})
            elif line_stripped.startswith('import '):
                file_info.imports.append(line_stripped)
    
    def _parse_go(self, content: str, file_info: FileInfo):
        lines = content.split('\n')
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            if line_stripped == 'func main() {':
                file_info.has_main = True
            elif line_stripped.startswith('func '):
                match = re.search(r'func\s+(\w+)', line_stripped)
                if match and match.group(1) != 'main':
                    file_info.functions.append({'name': match.group(1), 'line': i+1})
            elif line_stripped.startswith('import '):
                file_info.imports.append(line_stripped)
    
    def _parse_generic(self, content: str, file_info: FileInfo):
        lines = content.split('\n')
        for i, line in enumerate(lines[:50]):
            if 'main' in line.lower() and ('function' in line.lower() or 'def' in line.lower()):
                file_info.has_main = True
    
    def _calculate_metrics(self):
        self.repo_info.total_lines = sum(f.lines for f in self.repo_info.files)
        for f in self.repo_info.files:
            ext = f.extension or 'no_ext'
            self.repo_info.file_types[ext] = self.repo_info.file_types.get(ext, 0) + 1
    
    def _detect_entry_points(self):
        entry_names = [
            'main.py', 'app.py', 'index.js', 'server.js', 'app.js', 'main.js', 
            'index.html', 'Main.java', 'Application.java', 'main.go', 'run.py'
        ]
        for f in self.repo_info.files:
            if f.name in entry_names or f.has_main:
                self.repo_info.entry_points.append(f.path)
        
        if not self.repo_info.entry_points and self.repo_info.files:
            largest = max(self.repo_info.files, key=lambda f: f.lines)
            self.repo_info.entry_points.append(largest.path + " (largest file)")
    
    def _detect_language(self):
        lang_counts = defaultdict(int)
        lang_names = {
            'py': 'Python', 'js': 'JavaScript', 'ts': 'TypeScript',
            'html': 'HTML', 'htm': 'HTML', 'css': 'CSS',
            'json': 'JSON', 'md': 'Markdown', 'java': 'Java',
            'go': 'Go', 'rb': 'Ruby', 'php': 'PHP', 'cpp': 'C++'
        }
        
        for f in self.repo_info.files:
            if f.extension in lang_names:
                lang_counts[lang_names[f.extension]] += 1
            elif f.extension:
                lang_counts[f.extension.upper()] += 1
        
        if lang_counts:
            self.repo_info.language = max(lang_counts, key=lang_counts.get)
        else:
            self.repo_info.language = "Unknown"
    
    def _detect_framework(self):
        framework_indicators = {
            'React': ['react', 'React', 'useState', 'useEffect', 'jsx'],
            'Vue': ['vue', 'Vue', '.vue', 'v-bind'],
            'Angular': ['angular', 'Angular', 'ngIf', '@Component'],
            'Flask': ['flask', 'Flask', 'render_template'],
            'Django': ['django', 'Django', 'manage.py', 'settings.py'],
            'Express': ['express', 'Express', 'app.get', 'app.post'],
            'Spring': ['springframework', 'SpringBoot', '@Controller'],
            'FastAPI': ['fastapi', 'FastAPI', '@app.get']
        }
        
        for framework, indicators in framework_indicators.items():
            for file in self.repo_info.files:
                for imp in file.imports:
                    if any(ind.lower() in imp.lower() for ind in indicators):
                        self.repo_info.framework = framework
                        return
                
                if file.extension in ['html', 'htm']:
                    try:
                        with open(self.repo_path / file.path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read().lower()
                            if any(ind.lower() in content for ind in indicators):
                                self.repo_info.framework = framework
                                return
                    except:
                        pass
    
    def _find_largest_file(self):
        if self.repo_info.files:
            largest = max(self.repo_info.files, key=lambda f: f.lines)
            self.repo_info.largest_file = largest.name
    
    def _calculate_complexity(self):
        max_complexity = 0
        complex_file = None
        for file in self.repo_info.files:
            complexity = len(file.functions) * 3 + len(file.classes) * 2 + len(file.imports)
            if complexity > max_complexity:
                max_complexity = complexity
                complex_file = file.name
        self.repo_info.most_complex_file = complex_file