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
        steps = [
            {
                'step': 1,
                'title': '🚀 Start Here',
                'file': start_point['path'],
                'description': 'This is the main entry point',
                'actions': ['Open this file', 'Look for initialization code']
            },
            {
                'step': 2,
                'title': '📦 Check Imports',
                'description': 'See what modules are imported',
                'actions': ['Review import statements', 'Understand dependencies']
            }
        ]
        return steps
    
    def get_learning_path(self, level: str = 'beginner') -> Dict:
        paths = {
            'beginner': {
                'title': '🌱 Beginner Path',
                'estimated_time': '20 min',
                'modules': [{'name': 'Overview', 'tasks': ['Read README', 'Find entry point']}]
            }
        }
        return paths.get(level, paths['beginner'])