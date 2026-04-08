# visualizer.py
from typing import Dict, List

class FlowVisualizer:
    def __init__(self, repo_info, dependencies: Dict):
        self.repo = repo_info
        self.dependencies = dependencies
    
    def simulate_flow(self, query: str) -> Dict:
        query_lower = query.lower()
        
        if 'auth' in query_lower:
            flow_type = 'authentication'
            steps = ['Receive credentials', 'Validate input', 'Check database', 'Generate token', 'Return response']
        elif 'database' in query_lower:
            flow_type = 'database'
            steps = ['Build query', 'Connect to DB', 'Execute', 'Process results', 'Return data']
        else:
            flow_type = 'generic'
            steps = ['Start', 'Process', 'Handle logic', 'Access data', 'Return result']
        
        return {
            'success': True,
            'flow_type': flow_type,
            'description': f"Simulating {flow_type} flow",
            'steps': [{'number': i+1, 'description': s} for i, s in enumerate(steps)],
            'visualization': self._create_diagram(steps),
            'relevant_files': []
        }
    
    def _create_diagram(self, steps: List[str]) -> str:
        lines = ["┌" + "─" * 50 + "┐"]
        lines.append("│" + " " * 15 + "EXECUTION FLOW" + " " * 21 + "│")
        lines.append("├" + "─" * 50 + "┤")
        for i, step in enumerate(steps):
            lines.append(f"│ Step {i+1}: {step:<40} │")
            if i < len(steps) - 1:
                lines.append("│" + " " * 23 + "↓" + " " * 26 + "│")
        lines.append("└" + "─" * 50 + "┘")
        return "\n".join(lines)