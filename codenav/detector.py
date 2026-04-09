<<<<<<< HEAD
# detector.py
from typing import Dict, List, Optional

class EntryPointDetector:
    def __init__(self, repo_info, architecture_patterns: Dict = None):
        self.repo = repo_info
        self.arch_patterns = architecture_patterns or {}
    
    def get_best_starting_point(self) -> Dict:
        if not self.repo.entry_points:
            return {'path': None, 'score': 0, 'reason': 'No entry points found', 'confidence': 'low'}
        
        best = self.repo.entry_points[0]
        return {
            'path': best,
            'score': 25,
            'reason': 'Main entry point detected',
            'confidence': 'high'
        }
    
    def generate_navigation_path(self, start_point: Dict) -> List[Dict]:
        if not start_point or not start_point.get('path'):
            return [{
                'step': 1,
                'title': '📁 Explore Files',
                'description': 'Start by exploring the file structure',
                'actions': ['Browse the file list below', 'Look for README files']
            }]
        
        steps = [
            {
                'step': 1,
                'title': '🚀 Start Here',
                'file': start_point['path'],
                'description': 'This is the suggested starting point',
                'actions': ['Open this file', 'Look for initialization code']
            },
            {
                'step': 2,
                'title': '📦 Explore Structure',
                'description': 'Understand the project organization',
                'actions': ['Review file types', 'Check directory structure']
            },
            {
                'step': 3,
                'title': '💬 Ask Questions',
                'description': 'Use the chat to learn more',
                'actions': ['Ask about specific files', 'Request flow simulation']
            }
        ]
        return steps
    
    def get_learning_path(self, level: str = 'beginner') -> Dict:
        paths = {
            'beginner': {
                'title': '🌱 Beginner Path',
                'estimated_time': '20 min',
                'modules': [
                    {'name': 'Project Overview', 'tasks': ['Review all files', 'Note file types']},
                    {'name': 'Find Entry Points', 'tasks': ['Look for main files', 'Check README']},
                    {'name': 'Ask Questions', 'tasks': ['Use chat to learn', 'Try flow commands']}
                ]
            },
            'intermediate': {
                'title': '⚡ Intermediate Path',
                'estimated_time': '15 min',
                'modules': [
                    {'name': 'Code Analysis', 'tasks': ['Review functions', 'Understand dependencies']},
                    {'name': 'Flow Understanding', 'tasks': ['Simulate flows', 'Trace execution']}
                ]
            },
            'advanced': {
                'title': '🔧 Advanced Path',
                'estimated_time': '10 min',
                'modules': [
                    {'name': 'Architecture', 'tasks': ['Identify patterns', 'Review design']},
                    {'name': 'Extensions', 'tasks': ['Find extension points', 'Contribution guide']}
                ]
            }
        }
        return paths.get(level, paths['beginner'])
=======
# detector.py - Entry point detection
from typing import Dict, List

class EntryPointDetector:
    def __init__(self, repo_info, arch_patterns=None):
        self.repo = repo_info
        self.arch_patterns = arch_patterns or {}
    
    def get_best_starting_point(self) -> Dict:
        if self.repo.entry_points:
            return {'path': self.repo.entry_points[0], 'confidence': 'high'}
        return {'path': None, 'confidence': 'low'}
    
    def generate_navigation_path(self, start_point: Dict) -> List[Dict]:
        return [
            {'step': 1, 'title': 'Entry Point', 'file': start_point.get('path', 'README.md')},
            {'step': 2, 'title': 'Core Modules', 'description': 'Explore dependencies'},
            {'step': 3, 'title': 'Key Functions', 'description': 'Understand main logic'}
        ]
    
    def get_learning_path(self, level: str = 'beginner') -> Dict:
        return {'title': f'{level.capitalize()} Path', 'estimated_time': '20 min', 'modules': []}
>>>>>>> 7db48e7 (Final version: CodeNav AI complete)
