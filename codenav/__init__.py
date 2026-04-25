"""CodeNav AI - AI-powered codebase navigation assistant with Gemini"""

__version__ = "5.0.0"
__author__ = "CodeNav AI Team"

from .analyzer import RepoAnalyzer, RepoInfo, FileInfo
from .detector import EntryPointDetector
from .visualizer import FlowVisualizer
from .qa import CodebaseQA
from .gemini_qa import GeminiQAAgent
from .hybrid_qa import HybridQAAgent

__all__ = [
    'RepoAnalyzer', 'RepoInfo', 'FileInfo',
    'EntryPointDetector', 'FlowVisualizer',
    'CodebaseQA', 'GeminiQAAgent', 'HybridQAAgent'
]