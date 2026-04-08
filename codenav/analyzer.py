# analyzer.py - FIXED with better file detection
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
    file_type: str = "unknown"  # New field for file type detection

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
            'dist', 'build', 'target', '.idea', '.vscode', 
            '__pycache__', '.pytest_cache', 'coverage', '.next', '.nuxt'
        }
        
    def analyze(self) -> RepoInfo:
        print(f"📊 Analyzing {self.repo_path}...")
        self._scan_all_files()
        self._calculate_metrics()
        self._detect_entry_points()
        self._detect_language_from_files()  # New: Better language detection
        print(f"   ✅ Found {len(self.repo_info.files)} files")
        print(f"   ✅ {self.repo_info.total_lines:,} lines of code")
        print(f"   ✅ Detected language: {self.repo_info.language.upper()}")
        return self.repo_info
    
    def _scan_all_files(self):
        """Scan ALL files, not just code files"""
        # Now includes MANY more extensions
        text_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs', 
            '.rb', '.php', '.c', '.cpp', '.h', '.hpp', '.cs', '.swift',
            '.kt', '.kts', '.scala', '.clj', '.cljs', '.lisp', '.r', '.m',
            '.sql', '.html', '.htm', '.css', '.scss', '.sass', '.less',
            '.xml', '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg',
            '.conf', '.md', '.markdown', '.txt', '.rst', '.tex', '.latex',
            '.sh', '.bash', '.zsh', '.ps1', '.bat', '.cmd', '.dockerfile',
            '.makefile', '.cmake', '.gradle', '.properties'
        }
        
        # Also include files with NO extension (common in scripts)
        for file_path in self.repo_path.rglob('*'):
            if any(ignore in file_path.parts for ignore in self.ignore_dirs):
                continue
            
            if file_path.is_file():
                # Check if it's a text file (by extension OR content)
                should_scan = False
                
                # Check by extension
                if file_path.suffix.lower() in text_extensions:
                    should_scan = True
                # Check files with no extension (like 'Dockerfile', 'Makefile')
                elif file_path.suffix == '' and file_path.name[0].isalpha():
                    should_scan = True
                # Also check common special files
                elif file_path.name.upper() in ['DOCKERFILE', 'MAKEFILE', 'README', 'LICENSE', 'CONTRIBUTING']:
                    should_scan = True
                
                if should_scan:
                    file_info = self._parse_file(file_path)
                    self.repo_info.files.append(file_info)
                    ext = file_path.suffix[1:] if file_path.suffix else 'no_extension'
                    self.repo_info.file_types[ext] = self.repo_info.file_types.get(ext, 0) + 1
    
    def _parse_file(self, file_path: Path) -> FileInfo:
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
        except:
            content = ""
        
        lines = content.split('\n')
        
        # Determine file type
        file_type = self._detect_file_type(file_path, content)
        
        file_info = FileInfo(
            path=str(file_path.relative_to(self.repo_path)),
            name=file_path.name,
            extension=file_path.suffix[1:] if file_path.suffix else 'no_ext',
            size=file_path.stat().st_size,
            lines=len(lines),
            file_type=file_type
        )
        
        # Parse based on file type
        if file_type == 'python':
            self._parse_python(content, file_info)
        elif file_type in ['javascript', 'typescript']:
            self._parse_javascript(content, file_info)
        elif file_type == 'java':
            self._parse_java(content, file_info)
        elif file_type == 'go':
            self._parse_go(content, file_info)
        elif file_type in ['html', 'css', 'json', 'xml', 'markdown', 'text']:
            self._parse_markup(content, file_info)
        else:
            self._parse_generic(content, file_info)
        
        return file_info
    
    def _detect_file_type(self, file_path: Path, content: str) -> str:
        """Detect file type from extension OR content"""
        ext = file_path.suffix.lower()
        name = file_path.name.lower()
        
        # Extension-based detection
        type_map = {
            '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
            '.jsx': 'javascript', '.tsx': 'typescript', '.java': 'java',
            '.go': 'go', '.rs': 'rust', '.rb': 'ruby', '.php': 'php',
            '.c': 'c', '.cpp': 'cpp', '.h': 'c', '.hpp': 'cpp',
            '.html': 'html', '.htm': 'html', '.css': 'css', '.scss': 'css',
            '.json': 'json', '.xml': 'xml', '.yaml': 'yaml', '.yml': 'yaml',
            '.md': 'markdown', '.markdown': 'markdown', '.txt': 'text',
            '.sh': 'shell', '.bash': 'shell', '.ps1': 'powershell',
            '.sql': 'sql', '.dockerfile': 'docker', '.ini': 'config',
            '.conf': 'config', '.cfg': 'config'
        }
        
        if ext in type_map:
            return type_map[ext]
        
        # Content-based detection for files without extensions
        if '#!/usr/bin/env python' in content or 'def ' in content[:500]:
            return 'python'
        elif '#!/bin/bash' in content or '#!/bin/sh' in content:
            return 'shell'
        elif '<html' in content[:200] or '<!DOCTYPE html' in content[:200]:
            return 'html'
        elif '{' in content[:100] and ':' in content[:100] and '"' in content[:100]:
            return 'json'
        
        return 'unknown'
    
    def _parse_python(self, content: str, file_info: FileInfo):
        lines = content.split('\n')
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
            elif line_stripped.startswith('import ') or line_stripped.startswith('from '):
                file_info.imports.append(line_stripped)
    
    def _parse_javascript(self, content: str, file_info: FileInfo):
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'function ' in line:
                match = re.search(r'function\s+(\w+)', line)
                if match:
                    file_info.functions.append({'name': match.group(1), 'line': i + 1})
            elif 'class ' in line:
                match = re.search(r'class\s+(\w+)', line)
                if match:
                    file_info.classes.append({'name': match.group(1), 'line': i + 1})
    
    def _parse_java(self, content: str, file_info: FileInfo):
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'public static void main' in line:
                file_info.has_main = True
            elif 'class ' in line and '{' in line:
                match = re.search(r'class\s+(\w+)', line)
                if match:
                    file_info.classes.append({'name': match.group(1), 'line': i + 1})
    
    def _parse_go(self, content: str, file_info: FileInfo):
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'func main()' in line:
                file_info.has_main = True
            elif 'func ' in line:
                match = re.search(r'func\s+(\w+)', line)
                if match and match.group(1) != 'main':
                    file_info.functions.append({'name': match.group(1), 'line': i + 1})
    
    def _parse_markup(self, content: str, file_info: FileInfo):
        """Parse markup files like HTML, CSS, JSON, MD"""
        lines = content.split('\n')
        # For markup files, just count structure
        for i, line in enumerate(lines):
            if '<' in line and '>' in line:
                file_info.exports.append(f"Tag at line {i+1}")
    
    def _parse_generic(self, content: str, file_info: FileInfo):
        """Generic parser for unknown file types"""
        lines = content.split('\n')
        # Look for common patterns in any file
        for i, line in enumerate(lines[:50]):  # Check first 50 lines
            if 'main' in line.lower() and ('function' in line.lower() or 'def' in line.lower()):
                file_info.has_main = True
    
    def _calculate_metrics(self):
        total_lines = sum(f.lines for f in self.repo_info.files)
        self.repo_info.total_lines = total_lines
    
    def _detect_entry_points(self):
        """Detect entry points from various file types"""
        entry_names = [
            'main.py', 'app.py', 'run.py', 'index.py', 'cli.py', '__main__.py',
            'index.js', 'app.js', 'server.js', 'main.js', 'index.ts', 'main.ts',
            'Main.java', 'Application.java', 'main.go', 'main.rs', 'main.rb',
            'index.html', 'index.htm', 'default.html', 'Dockerfile', 'Makefile'
        ]
        
        for file_info in self.repo_info.files:
            if file_info.name in entry_names or file_info.has_main:
                self.repo_info.entry_points.append(file_info.path)
        
        # If no entry points found, add the largest file as suggested start
        if not self.repo_info.entry_points and self.repo_info.files:
            largest = max(self.repo_info.files, key=lambda f: f.lines)
            self.repo_info.entry_points.append(largest.path + " (suggested)")
    
    def _detect_language_from_files(self):
        """Detect primary language based on file extensions and content"""
        lang_counts = defaultdict(int)
        
        for file_info in self.repo_info.files:
            if file_info.file_type != 'unknown':
                lang_counts[file_info.file_type] += 1
            elif file_info.extension:
                # Map extensions to languages
                ext_map = {
                    'py': 'python', 'js': 'javascript', 'ts': 'typescript',
                    'java': 'java', 'go': 'go', 'rs': 'rust', 'rb': 'ruby',
                    'php': 'php', 'c': 'c', 'cpp': 'cpp', 'cs': 'csharp',
                    'html': 'html', 'css': 'css', 'json': 'json', 'xml': 'xml',
                    'md': 'markdown', 'txt': 'text', 'sh': 'shell', 'sql': 'sql'
                }
                if file_info.extension in ext_map:
                    lang_counts[ext_map[file_info.extension]] += 1
        
        if lang_counts:
            self.repo_info.language = max(lang_counts, key=lang_counts.get)
        else:
            self.repo_info.language = "text"