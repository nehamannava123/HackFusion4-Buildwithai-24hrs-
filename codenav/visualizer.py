# visualizer.py - Flow visualization
from typing import Dict, List

class FlowVisualizer:
    def __init__(self, repo_info, dependencies):
        self.repo = repo_info
    
    def simulate_flow(self, query: str) -> Dict:
        query_lower = query.lower()
        
        # Detect flow type from query
        if 'auth' in query_lower or 'login' in query_lower or 'signin' in query_lower:
            flow_type = 'authentication'
            steps = [
                '1. User submits credentials (username/password)',
                '2. Server validates input format',
                '3. Database query checks user existence',
                '4. Password hash comparison',
                '5. JWT token/session generation',
                '6. Token returned to client',
                '7. Client stores token for future requests'
            ]
            description = "🔐 Authentication Flow - How users log in"
            
        elif 'database' in query_lower or 'db' in query_lower or 'query' in query_lower:
            flow_type = 'database'
            steps = [
                '1. Application builds SQL/NoSQL query',
                '2. Database connection established',
                '3. Query executed on database server',
                '4. Result set retrieved',
                '5. Data transformed to objects/models',
                '6. Results returned to caller'
            ]
            description = "🗄️ Database Query Flow - How data is retrieved"
            
        elif 'api' in query_lower or 'request' in query_lower or 'endpoint' in query_lower:
            flow_type = 'api_request'
            steps = [
                '1. HTTP request received by server',
                '2. Router matches URL to handler',
                '3. Middleware processes request (auth, logging)',
                '4. Controller/Action executes business logic',
                '5. Service layer processes data',
                '6. Response formatted (JSON/XML)',
                '7. HTTP response sent to client'
            ]
            description = "🌐 API Request Flow - How endpoints are handled"
            
        else:
            flow_type = 'generic'
            steps = [
                '1. Application starts',
                '2. Configuration loaded',
                '3. Dependencies initialized',
                '4. Main logic executes',
                '5. Results processed',
                '6. Output generated'
            ]
            description = "📊 General Execution Flow"
        
        # Create ASCII diagram
        diagram = "┌" + "─" * 58 + "┐\n"
        diagram += f"│{description.center(58)}│\n"
        diagram += "├" + "─" * 58 + "┤\n"
        
        for i, step in enumerate(steps):
            step_display = step[:55] if len(step) > 55 else step
            diagram += f"│ {step_display:<57} │\n"
            if i < len(steps) - 1:
                diagram += "│" + " " * 28 + "↓" + " " * 29 + "│\n"
        
        diagram += "└" + "─" * 58 + "┘"
        
        return {
            'success': True,
            'flow_type': flow_type,
            'description': description,
            'steps': [{'number': i+1, 'description': s.split('. ')[1] if '. ' in s else s} for i, s in enumerate(steps)],
            'visualization': diagram
        }