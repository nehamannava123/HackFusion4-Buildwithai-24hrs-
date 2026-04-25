# detector.py - Entry point detection and navigation
from typing import Dict, List

class EntryPointDetector:
    def __init__(self, repo_info, arch_patterns=None):
        self.repo = repo_info
        self.arch_patterns = arch_patterns or {}
    
    def get_best_starting_point(self) -> Dict:
        if self.repo.entry_points:
            return {
                'path': self.repo.entry_points[0],
                'confidence': 'high',
                'reason': 'Detected as main entry point based on naming convention'
            }
        return {'path': None, 'confidence': 'low', 'reason': 'No clear entry point detected'}
    
    def generate_navigation_path(self, start_point: Dict) -> List[Dict]:
        if not start_point.get('path'):
            return [{
                'step': 1,
                'title': '📁 Explore Files',
                'description': 'Start by browsing the file list',
                'actions': ['Look for README.md', 'Check file extensions']
            }]
        
        return [
            {
                'step': 1,
                'title': '🚀 Entry Point',
                'file': start_point['path'],
                'description': 'Start here - this is the main entry point',
                'actions': ['Open this file', 'Look for initialization code']
            },
            {
                'step': 2,
                'title': '📂 Core Modules',
                'description': 'Explore imported modules and dependencies',
                'actions': ['Check import statements', 'Follow key dependencies']
            },
            {
                'step': 3,
                'title': '💬 Ask Questions',
                'description': 'Use chat to learn about specific files',
                'actions': ['Ask "What is [filename]?"', 'Try "flow authentication"']
            }
        ]
    
    def get_learning_path(self, level: str = 'beginner') -> Dict:
        entry = self.repo.entry_points[0] if self.repo.entry_points else 'the main file'
        
        paths = {
            'beginner': {
                'title': '🌱 Beginner Learning Path',
                'estimated_time': '20-30 minutes',
                'modules': [
                    {'name': 'Project Overview', 'tasks': [f'Review file structure', f'Note: {len(self.repo.files)} files total']},
                    {'name': 'Entry Point', 'tasks': [f'Open {entry}', 'Understand initialization']},
                    {'name': 'Ask Questions', 'tasks': ['Use chat to explore specific files']}
                ]
            },
            'intermediate': {
                'title': '⚡ Intermediate Learning Path',
                'estimated_time': '15-20 minutes',
                'modules': [
                    {'name': 'Architecture', 'tasks': ['Identify design patterns', 'Map dependencies']},
                    {'name': 'Key Functions', 'tasks': ['Review main functions', 'Understand data flow']}
                ]
            },
            'advanced': {
                'title': '🔧 Advanced Learning Path',
                'estimated_time': '10-15 minutes',
                'modules': [
                    {'name': 'Deep Dive', 'tasks': ['Analyze complex functions', 'Review error handling']},
                    {'name': 'Extensions', 'tasks': ['Find extension points', 'Understand plugin system']}
                ]
            }
        }
        return paths.get(level, paths['beginner'])