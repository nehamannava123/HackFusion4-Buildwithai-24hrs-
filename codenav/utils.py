# utils.py - Utility functions
import os
from pathlib import Path

def is_code_file(file_path: str) -> bool:
    code_extensions = {'.py', '.js', '.ts', '.html', '.css', '.json', '.md', '.txt', '.java', '.go'}
    return Path(file_path).suffix in code_extensions

def get_file_size(file_path: str) -> int:
    try:
        return os.path.getsize(file_path)
    except:
        return 0

def count_lines(file_path: str) -> int:
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except:
        return 0