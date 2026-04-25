<<<<<<< HEAD
# hybrid_qa.py - Force AI for ALL questions
from typing import Dict, List
from .qa import CodebaseQA
from .gemini_qa import GeminiQAAgent
=======
# hybrid_qa.py - Smart router with better file detection
from typing import Dict, List
from .qa import CodebaseQA
from .ai_qa import AIQAAgent
>>>>>>> 9db4c5255575581e720a0c6164eb2f30887f30fb

class HybridQAAgent:
    def __init__(self, repo_info):
        self.repo = repo_info
        self.rule_qa = CodebaseQA(repo_info, {}, {})
<<<<<<< HEAD
        self.ai_agent = GeminiQAAgent(repo_info)
        
        if self.ai_agent.available:
            print("🎯 AI MODE ACTIVE - All questions will use Gemini")
        else:
            print("🎯 FALLBACK MODE - Using rules only")
    
    def ask(self, question: str) -> Dict:
        # FORCE USE AI FOR EVERY QUESTION if available
        if self.ai_agent.available:
            print(f"🧠 AI Processing: {question[:50]}...")
            ai_answer = self.ai_agent.ask_with_ai(question)
            return {
                'answer': ai_answer,
                'type': 'ai',
                'ai_used': True
            }
        
        # Fallback to rules only if AI not available
        response = self.rule_qa.ask(question)
        return {
            'answer': response['answer'],
            'type': 'rule',
            'ai_used': False
        }
=======
        self.ai_agent = AIQAAgent(repo_info)
        print(f"🎯 Hybrid Engine Ready | AI: {self.ai_agent.available}")
    
    def ask(self, question: str) -> Dict:
        q_lower = question.lower()
        
        # Flow command
        if q_lower.startswith('flow'):
            from .visualizer import FlowVisualizer
            viz = FlowVisualizer(self.repo, {})
            result = viz.simulate_flow(question)
            return {'answer': result.get('visualization', ''), 'type': 'flow', 'ai_used': False}
        
        # FORCE AI for file-specific questions
        file_keywords = ['what is', 'explain', 'tell me about', 'describe', 'analyze']
        is_asking_about_file = False
        
        # Check if asking about a specific file in the repo
        for file in self.repo.files:
            if file.name.lower().replace('.html', '').replace('.js', '').replace('.py', '') in q_lower:
                is_asking_about_file = True
                break
        
        # Use AI for file questions or complex questions
        if self.ai_agent.available and (is_asking_about_file or any(k in q_lower for k in ['explain', 'what does', 'how does', 'purpose', 'describe', 'error', 'bug', 'issue', 'jquery'])):
            print(f"🧠 AI Processing: {question[:50]}...")
            ai_answer = self.ai_agent.ask_with_ai(question)
            return {'answer': ai_answer, 'type': 'ai', 'ai_used': True}
        
        # Use rules for simple stats
        response = self.rule_qa.ask(question)
        return {'answer': response['answer'], 'type': 'rule', 'ai_used': False}
>>>>>>> 9db4c5255575581e720a0c6164eb2f30887f30fb
    
    def explain_file(self, file_path: str) -> str:
        return self.ai_agent.explain_file(file_path) if self.ai_agent.available else "AI unavailable"
    
    def get_ai_status(self) -> Dict:
        return {
            'available': self.ai_agent.available,
<<<<<<< HEAD
            'model': 'Google Gemini',
            'message': 'Gemini AI Ready!' if self.ai_agent.available else 'AI not available'
        }
    
    def get_learning_path(self, level: str = 'beginner') -> Dict:
        return {'title': f'{level} Path', 'estimated_time': '15 min', 'modules': []}
=======
            'model': self.ai_agent.model if self.ai_agent.available else None,
            'message': '🧠 AI Engine Active' if self.ai_agent.available else '⚡ Rule Engine Active'
        }
    
    def get_learning_path(self, level: str = 'beginner') -> Dict:
        suggestions = self.ai_agent.suggest_learning_path(level)
        return {
            'title': f'🎯 {level.capitalize()} Learning Path',
            'estimated_time': '15-20 minutes',
            'modules': [{'name': s, 'tasks': ['Follow this guide']} for s in suggestions]
        }
>>>>>>> 9db4c5255575581e720a0c6164eb2f30887f30fb
