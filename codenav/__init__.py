"""CodeNav AI - Professional Codebase Navigation Assistant"""

__version__ = "4.0.0"
__author__ = "CodeNav AI Team"

from .analyzer import RepoAnalyzer, RepoInfo, FileInfo
from .detector import EntryPointDetector
from .visualizer import FlowVisualizer
from .qa import CodebaseQA
from .ai_qa import AIQAAgent
from .hybrid_qa import HybridQAAgent

__all__ = [
    'RepoAnalyzer', 'RepoInfo', 'FileInfo',
    'EntryPointDetector', 'FlowVisualizer',
    'CodebaseQA', 'AIQAAgent', 'HybridQAAgent'
]