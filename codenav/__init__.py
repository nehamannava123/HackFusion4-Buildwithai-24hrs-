<<<<<<< HEAD
"""CodeNav AI - AI-powered codebase navigation assistant"""

__version__ = "1.0.0"
__author__ = "CodeNav AI"
=======
"""CodeNav AI - Professional Codebase Navigation Assistant"""

__version__ = "4.0.0"
__author__ = "CodeNav AI Team"
>>>>>>> 7db48e7 (Final version: CodeNav AI complete)

from .analyzer import RepoAnalyzer, RepoInfo, FileInfo
from .detector import EntryPointDetector
from .visualizer import FlowVisualizer
from .qa import CodebaseQA
<<<<<<< HEAD
from .cli import main

__all__ = [
    'RepoAnalyzer',
    'RepoInfo', 
    'FileInfo',
    'EntryPointDetector',
    'FlowVisualizer',
    'CodebaseQA',
    'main'
=======
from .ai_qa import AIQAAgent
from .hybrid_qa import HybridQAAgent

__all__ = [
    'RepoAnalyzer', 'RepoInfo', 'FileInfo',
    'EntryPointDetector', 'FlowVisualizer',
    'CodebaseQA', 'AIQAAgent', 'HybridQAAgent'
>>>>>>> 7db48e7 (Final version: CodeNav AI complete)
]