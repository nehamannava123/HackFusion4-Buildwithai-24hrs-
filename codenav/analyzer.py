# analyzer.py - Complete repository analyzer
import os
import re
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class FileInfo:
    path: str
    name: str
    extension: str
    size: int
    lines: int
    functions: List[Dict] = field(default_factory=list)
    classes: List[Dict] = field(default_factory=list)
    has_main: bool = False
    file_type: str = "unknown"

@dataclass
class RepoInfo:
    root_path: str
    files: List[FileInfo] = field(default_factory=list)
    entry_points: List[str] = field(default_factory=list)
    dependencies: Dict[str, List[str]] = field(default_factory=dict)
    language: str = "unknown"
    total_lines: int = 0
    file_types: Dict[str, int] = field(default_factory=dict)

class RepoAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.repo_info = RepoInfo(root_path=str(repo_path))
        self.ignore_dirs = {'node_modules', 'venv', '__pycache__', '.git', 'dist', 'build'}
        
    def analyze(self) -> RepoInfo:
        print(f"📊 Analyzing {self.repo_path}...")
        self._scan_files()
        self._calculate_metrics()
        self._detect_entry_points()
        self._detect_language()
        print(f"   ✅ Found {len(self.repo_info.files)} files")
        print(f"   ✅ {self.repo_info.total_lines:,} lines")
        print(f"   ✅ Language: {self.repo_info.language.upper()}")
        if self.repo_info.entry_points:
            print(f"   ✅ Entry point: {self.repo_info.entry_points[0]}")
        return self.repo_info
    
    def _scan_files(self):
        extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.json', '.md', '.txt', '.java', '.go'}
        
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
        
        file_info = FileInfo(
            path=str(file_path.relative_to(self.repo_path)),
            name=file_path.name,
            extension=file_path.suffix[1:],
            size=file_path.stat().st_size,
            lines=len(lines),
            file_type=file_path.suffix[1:] or 'txt'
        )
        
        # Parse Python
        if file_path.suffix == '.py':
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
                elif 'if __name__ == "__main__"' in line:
                    file_info.has_main = True
        
        # Parse JavaScript
        elif file_path.suffix in ['.js', '.ts']:
            for i, line in enumerate(lines):
                if 'function ' in line:
                    match = re.search(r'function\s+(\w+)', line)
                    if match:
                        file_info.functions.append({'name': match.group(1), 'line': i+1})
        
        return file_info
    
    def _calculate_metrics(self):
        self.repo_info.total_lines = sum(f.lines for f in self.repo_info.files)
        for f in self.repo_info.files:
            ext = f.extension or 'no_ext'
            self.repo_info.file_types[ext] = self.repo_info.file_types.get(ext, 0) + 1
    
    def _detect_entry_points(self):
        entry_names = ['main.py', 'app.py', 'index.js', 'server.js', 'app.js', 'main.js', 'index.html']
        for f in self.repo_info.files:
            if f.name in entry_names or f.has_main:
                self.repo_info.entry_points.append(f.path)
        
        if not self.repo_info.entry_points and self.repo_info.files:
            largest = max(self.repo_info.files, key=lambda f: f.lines)
            self.repo_info.entry_points.append(largest.path)
    
    def _detect_language(self):
        lang_counts = defaultdict(int)
        for f in self.repo_info.files:
            if f.extension:
                lang_counts[f.extension] += 1
        if lang_counts:
            self.repo_info.language = max(lang_counts, key=lang_counts.get)
        else:
            self.repo_info.language = "unknown"