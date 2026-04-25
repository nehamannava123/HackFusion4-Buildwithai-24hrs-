<<<<<<< HEAD
"""CodeNav AI - AI-powered codebase navigation assistant with Gemini"""

__version__ = "5.0.0"
=======
"""CodeNav AI - Professional Codebase Navigation Assistant"""

__version__ = "4.0.0"
>>>>>>> 9db4c5255575581e720a0c6164eb2f30887f30fb
__author__ = "CodeNav AI Team"

from .analyzer import RepoAnalyzer, RepoInfo, FileInfo
from .detector import EntryPointDetector
from .visualizer import FlowVisualizer
from .qa import CodebaseQA
<<<<<<< HEAD
from .gemini_qa import GeminiQAAgent
=======
from .ai_qa import AIQAAgent
>>>>>>> 9db4c5255575581e720a0c6164eb2f30887f30fb
from .hybrid_qa import HybridQAAgent

__all__ = [
    'RepoAnalyzer', 'RepoInfo', 'FileInfo',
    'EntryPointDetector', 'FlowVisualizer',
<<<<<<< HEAD
    'CodebaseQA', 'GeminiQAAgent', 'HybridQAAgent'
=======
    'CodebaseQA', 'AIQAAgent', 'HybridQAAgent'
>>>>>>> 9db4c5255575581e720a0c6164eb2f30887f30fb
]