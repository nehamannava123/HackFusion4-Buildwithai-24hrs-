# analyzer.py
import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class FileInfo:
    path: str
    name: str
    extension: str
    size: int
    lines: int
    imports: List[str] = field(default_factory=list)
    exports: List[str] = field(default_factory=list)
    functions: List[Dict] = field(default_factory=list)
    classes: List[Dict] = field(default_factory=list)
    docstring: str = ""
    has_main: bool = False

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

class RepoAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.repo_info = RepoInfo(root_path=repo_path)
        self.ignore_dirs = {
            'node_modules', 'venv', 'env', '__pycache__', '.git',
            'dist', 'build', 'target', '.idea', '.vscode'
        }
        
    def analyze(self) -> RepoInfo:
        print(f"📊 Analyzing {self.repo_path}...")
        self._scan_all_files()
        self._calculate_metrics()
        self._detect_entry_points()
        self._extract_imports()
        print(f"   ✅ Found {len(self.repo_info.files)} files")
        print(f"   ✅ {self.repo_info.total_lines:,} lines of code")
        return self.repo_info
    
    def _scan_all_files(self):
        code_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs', '.rb', '.php'}
        
        for file_path in self.repo_path.rglob('*'):
            if any(ignore in file_path.parts for ignore in self.ignore_dirs):
                continue
            
            if file_path.suffix in code_extensions and file_path.is_file():
                file_info = self._parse_file(file_path)
                self.repo_info.files.append(file_info)
                ext = file_path.suffix[1:] or 'no_ext'
                self.repo_info.file_types[ext] = self.repo_info.file_types.get(ext, 0) + 1
    
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
            lines=len(lines)
        )
        
        # Parse Python files
        if file_path.suffix == '.py':
            for i, line in enumerate(lines):
                line_stripped = line.strip()
                if line_stripped.startswith('def '):
                    match = re.search(r'def\s+(\w+)\s*\(', line_stripped)
                    if match:
                        file_info.functions.append({'name': match.group(1), 'line': i + 1})
                elif line_stripped.startswith('class '):
                    match = re.search(r'class\s+(\w+)', line_stripped)
                    if match:
                        file_info.classes.append({'name': match.group(1), 'line': i + 1})
                elif 'if __name__ == "__main__"' in line:
                    file_info.has_main = True
        
        return file_info
    
    def _calculate_metrics(self):
        total_lines = sum(f.lines for f in self.repo_info.files)
        self.repo_info.total_lines = total_lines
    
    def _detect_entry_points(self):
        entry_names = ['main.py', 'app.py', 'run.py', 'index.py', 'cli.py', '__main__.py']
        for file_info in self.repo_info.files:
            if file_info.name in entry_names or file_info.has_main:
                self.repo_info.entry_points.append(file_info.path)
    
    def _extract_imports(self):
        pass