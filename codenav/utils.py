# utils.py
"""Utility functions for CodeNav AI"""

import os
from pathlib import Path
from typing import List, Set

def is_code_file(file_path: str) -> bool:
    """Check if a file is a code file"""
    code_extensions = {'.py', '.js', '.ts', '.java', '.go', '.rs', '.cpp', '.c', '.rb', '.php'}
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

def is_binary_file(file_path: str) -> bool:
    """Check if file is binary"""
    text_extensions = {'.py', '.js', '.ts', '.json', '.txt', '.md', '.yml', '.yaml', '.xml', '.html', '.css'}
    return Path(file_path).suffix not in text_extensions