# cli.py
#!/usr/bin/env python3
import sys
from pathlib import Path
from .analyzer import RepoAnalyzer
from .detector import EntryPointDetector
from .visualizer import FlowVisualizer
from .qa import CodebaseQA

class CodeNavCLI:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.repo_info = None
        self.qa = None
        self.flow_viz = None
    
    def run(self):
        self._print_banner()
        
        if not self.repo_path.exists():
            print(f"❌ Error: '{self.repo_path}' does not exist")
            return
        
        # Analyze
        analyzer = RepoAnalyzer(str(self.repo_path))
        self.repo_info = analyzer.analyze()
        
        # Initialize components
        self.qa = CodebaseQA(self.repo_info, {}, {})
        self.flow_viz = FlowVisualizer(self.repo_info, {})
        
        # Show insights
        self._show_insights()
        
        # Interactive session
        self._interactive_session()
    
    def _print_banner(self):
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ██████╗ ██████╗ ██████╗ ███████╗███╗   ██╗ █████╗ ██╗     ║
║   ██╔════╝██╔══██╗██╔══██╗██╔════╝████╗  ██║██╔══██╗██║     ║
║   ██║     ██║  ██║██║  ██║█████╗  ██╔██╗ ██║███████║██║     ║
║   ██║     ██║  ██║██║  ██║██╔══╝  ██║╚██╗██║██╔══██║╚██╗    ║
║   ╚██████╗██████╔╝██████╔╝███████╗██║ ╚████║██║  ██║ ╚████╗  ║
║    ╚═════╝╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝  ╚═══╝  ║
║                                                              ║
║              CodeNav AI - Codebase Navigator                ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
        print(f"\n📂 Repository: {self.repo_path}\n")
    
    def _show_insights(self):
        print("═" * 60)
        print("📊 Repository Insights")
        print("═" * 60)
        print(f"\n📈 Statistics:")
        print(f"   • Language: {self.repo_info.language.upper()}")
        print(f"   • Files: {len(self.repo_info.files)}")
        print(f"   • Lines: {self.repo_info.total_lines:,}")
        
        if self.repo_info.entry_points:
            print(f"\n🎯 Best Starting Point:")
            print(f"   • {self.repo_info.entry_points[0]}")
        
        print("\n" + "═" * 60)
    
    def _interactive_session(self):
        print("\n💬 Interactive Q&A")
        print("   Type 'help', 'flow', or 'exit'\n")
        
        while True:
            try:
                user_input = input("🔍 You: ").strip()
                
                if user_input.lower() in ['exit', 'quit']:
                    print("\n👋 Goodbye!")
                    break
                elif user_input.lower() == 'help':
                    self._show_help()
                elif user_input.lower().startswith('flow'):
                    result = self.flow_viz.simulate_flow(user_input)
                    print(f"\n{result['visualization']}\n")
                else:
                    response = self.qa.ask(user_input)
                    print(f"\n🤖 CodeNav: {response['answer']}\n")
                
                print("─" * 60)
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
    
    def _show_help(self):
        print("""
📖 Commands:
  • Ask natural language questions
  • 'flow <topic>' - Simulate execution
  • 'exit' - Quit

Examples:
  "Where should I start?"
  "How does authentication work?"
  "flow database"
        """)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='CodeNav AI')
    parser.add_argument('repo_path', help='Path to repository')
    parser.add_argument('--quick', action='store_true', help='Quick analysis')
    args = parser.parse_args()
    
    cli = CodeNavCLI(args.repo_path)
    if args.quick:
        analyzer = RepoAnalyzer(args.repo_path)
        info = analyzer.analyze()
        print(f"\n✅ Found {len(info.files)} files, {info.total_lines} lines")
    else:
        cli.run()

if __name__ == "__main__":
    main()