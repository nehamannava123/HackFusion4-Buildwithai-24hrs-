"""CodeNav AI - AI-powered codebase navigation assistant"""

__version__ = "3.0.0"

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