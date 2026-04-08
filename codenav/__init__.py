"""CodeNav AI - AI-powered codebase navigation assistant"""

__version__ = "1.0.0"
__author__ = "CodeNav AI"

from .analyzer import RepoAnalyzer, RepoInfo, FileInfo
from .detector import EntryPointDetector
from .visualizer import FlowVisualizer
from .qa import CodebaseQA
from .cli import main

__all__ = [
    'RepoAnalyzer',
    'RepoInfo', 
    'FileInfo',
    'EntryPointDetector',
    'FlowVisualizer',
    'CodebaseQA',
    'main'
]