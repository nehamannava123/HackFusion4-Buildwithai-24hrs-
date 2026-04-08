# cli.py - Command line interface
import sys
from pathlib import Path
from .analyzer import RepoAnalyzer
from .hybrid_qa import HybridQAAgent

def main():
    if len(sys.argv) < 2:
        print("Usage: codenav <repo_path>")
        sys.exit(1)
    
    repo_path = Path(sys.argv[1])
    if not repo_path.exists():
        print(f"Error: {repo_path} not found")
        sys.exit(1)
    
    analyzer = RepoAnalyzer(str(repo_path))
    repo_info = analyzer.analyze()
    qa = HybridQAAgent(repo_info)
    
    print(f"\n💬 Ask questions (type 'exit' to quit)\n")
    while True:
        q = input("You: ").strip()
        if q.lower() == 'exit':
            break
        response = qa.ask(q)
        print(f"AI: {response['answer']}\n")

if __name__ == "__main__":
    main()