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