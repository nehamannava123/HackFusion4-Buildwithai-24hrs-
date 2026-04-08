# hybrid_qa.py - FORCE AI for all questions
from typing import Dict, List
from .qa import CodebaseQA
from .ai_qa import AIQAAgent

class HybridQAAgent:
    def __init__(self, repo_info):
        self.repo = repo_info
        self.rule_qa = CodebaseQA(repo_info, {}, {})
        self.ai_agent = AIQAAgent(repo_info)
        print(f"🤖 HybridQA initialized. AI Available: {self.ai_agent.available}")
    
    def ask(self, question: str) -> Dict:
        # FORCE USE AI FOR ALL QUESTIONS
        if self.ai_agent.available:
            print(f"🤖 USING AI for: {question}")
            ai_answer = self.ai_agent.ask_with_ai(question)
            return {
                'answer': ai_answer,
                'type': 'ai',
                'ai_used': True
            }
        
        # Fallback to rules
        print(f"📋 USING RULES for: {question}")
        response = self.rule_qa.ask(question)
        return {
            'answer': response['answer'],
            'type': 'rule',
            'ai_used': False
        }
    
    def explain_file(self, file_path: str) -> str:
        if self.ai_agent.available:
            return self.ai_agent.explain_file(file_path)
        return "AI unavailable"
    
    def get_ai_status(self) -> Dict:
        return {
            'available': self.ai_agent.available,
            'model': self.ai_agent.model if self.ai_agent.available else None,
            'message': 'AI is ready!' if self.ai_agent.available else 'Install Ollama'
        }
    
    def get_learning_path(self, level: str = 'beginner') -> Dict:
        return {'title': 'Learning Path', 'estimated_time': '20 min', 'modules': []}