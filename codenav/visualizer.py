# visualizer.py
from typing import Dict, List

class FlowVisualizer:
    def __init__(self, repo_info, dependencies: Dict):
        self.repo = repo_info
        self.dependencies = dependencies
    
    def simulate_flow(self, query: str) -> Dict:
        query_lower = query.lower()
        
        if 'auth' in query_lower or 'login' in query_lower:
            flow_type = 'authentication'
            steps = ['Receive credentials', 'Validate input', 'Check database', 'Generate token', 'Return response']
        elif 'database' in query_lower or 'db' in query_lower or 'query' in query_lower:
            flow_type = 'database'
            steps = ['Build query', 'Connect to DB', 'Execute', 'Process results', 'Return data']
        elif 'api' in query_lower or 'request' in query_lower or 'endpoint' in query_lower:
            flow_type = 'api_request'
            steps = ['Receive request', 'Route to handler', 'Process logic', 'Format response', 'Return to client']
        elif 'file' in query_lower or 'upload' in query_lower:
            flow_type = 'file_upload'
            steps = ['Receive file', 'Validate type/size', 'Save to storage', 'Update database', 'Return metadata']
        else:
            flow_type = 'generic'
            steps = ['Start', 'Process input', 'Execute logic', 'Access data', 'Return result']
        
        # Find relevant files
        relevant_files = []
        for file in self.repo.files[:10]:
            if any(keyword in file.name.lower() for keyword in query_lower.split()[:3]):
                relevant_files.append({'path': file.path, 'functions': file.functions[:2]})
        
        return {
            'success': True,
            'flow_type': flow_type,
            'description': f"📊 Simulating {flow_type.replace('_', ' ')} flow",
            'steps': [{'number': i+1, 'description': s} for i, s in enumerate(steps)],
            'visualization': self._create_diagram(steps),
            'relevant_files': relevant_files
        }
    
    def _create_diagram(self, steps: List[str]) -> str:
        lines = ["┌" + "─" * 50 + "┐"]
        lines.append("│" + " " * 15 + "EXECUTION FLOW" + " " * 21 + "│")
        lines.append("├" + "─" * 50 + "┤")
        for i, step in enumerate(steps):
            display_step = step[:40] if len(step) > 40 else step
            lines.append(f"│ Step {i+1}: {display_step:<40} │")
            if i < len(steps) - 1:
                lines.append("│" + " " * 23 + "↓" + " " * 26 + "│")
        lines.append("└" + "─" * 50 + "┘")
        return "\n".join(lines)