# utils.py - Utility functions
import os
from pathlib import Path

def is_code_file(file_path: str) -> bool:
    """Check if a file is a code file"""
    code_extensions = {
        '.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', 
        '.json', '.md', '.txt', '.java', '.go', '.cpp', '.c', 
        '.rb', '.php', '.rs', '.swift', '.kt'
    }
    return Path(file_path).suffix in code_extensions

def get_file_size(file_path: str) -> int:
    """Get file size in bytes"""
    try:
        return os.path.getsize(file_path)
    except:
        return 0

def count_lines(file_path: str) -> int:
    """Count lines in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except:
        return 0

def format_file_size(bytes_size: int) -> str:
    """Format file size to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.1f} TB"