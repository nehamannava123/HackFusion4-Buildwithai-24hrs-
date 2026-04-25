# hybrid_qa.py - Force AI for ALL questions
from typing import Dict, List
from .qa import CodebaseQA
from .gemini_qa import GeminiQAAgent

class HybridQAAgent:
    def __init__(self, repo_info):
        self.repo = repo_info
        self.rule_qa = CodebaseQA(repo_info, {}, {})
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
    
    def explain_file(self, file_path: str) -> str:
        return self.ai_agent.explain_file(file_path) if self.ai_agent.available else "AI unavailable"
    
    def get_ai_status(self) -> Dict:
        return {
            'available': self.ai_agent.available,
            'model': 'Google Gemini',
            'message': 'Gemini AI Ready!' if self.ai_agent.available else 'AI not available'
        }
    
    def get_learning_path(self, level: str = 'beginner') -> Dict:
        return {'title': f'{level} Path', 'estimated_time': '15 min', 'modules': []}