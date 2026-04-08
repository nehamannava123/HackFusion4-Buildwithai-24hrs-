# utils.py
"""Utility functions for CodeNav AI"""

import os
from pathlib import Path
from typing import List, Set

def is_text_file(file_path: str) -> bool:
    """Check if a file is likely a text file"""
    text_extensions = {
        '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs', '.rb', '.php',
        '.c', '.cpp', '.h', '.hpp', '.cs', '.swift', '.kt', '.scala',
        '.html', '.htm', '.css', '.scss', '.sass', '.less', '.xml', '.json',
        '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf', '.md', '.markdown',
        '.txt', '.rst', '.tex', '.sh', '.bash', '.ps1', '.bat', '.cmd',
        '.sql', '.dockerfile', '.makefile', '.gradle', '.properties', '.env'
    }
    return Path(file_path).suffix.lower() in text_extensions

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

def get_file_extension(file_path: str) -> str:
    return Path(file_path).suffix.lower()