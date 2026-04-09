# app.py - CodeNav AI with GitHub Repository Support
import os
import sys
import tempfile
import shutil
from pathlib import Path
from flask import Flask, render_template, request, jsonify
import git

from codenav.analyzer import RepoAnalyzer
from codenav.hybrid_qa import HybridQAAgent
from codenav.visualizer import FlowVisualizer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'codenav-ai-secret-key'

# Global variables
current_repo = None
current_qa = None
current_viz = None
current_temp_dir = None

def clone_github_repo(github_url):
    """Clone a GitHub repository to a temporary directory"""
    global current_temp_dir
    
    # Create temporary directory
    current_temp_dir = tempfile.mkdtemp()
    
    # Clone the repository
    repo = git.Repo.clone_from(github_url, current_temp_dir)
    
    return current_temp_dir

def cleanup_temp_dir():
    """Clean up temporary directory"""
    global current_temp_dir
    if current_temp_dir and os.path.exists(current_temp_dir):
        shutil.rmtree(current_temp_dir, ignore_errors=True)
        current_temp_dir = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    global current_repo, current_qa, current_viz
    
    data = request.get_json()
    github_url = data.get('url', '')
    
    if not github_url:
        return jsonify({'error': 'Please provide a GitHub repository URL'}), 400
    
    # Validate GitHub URL
    if not github_url.startswith('https://github.com/') and not github_url.startswith('http://github.com/'):
        return jsonify({'error': 'Please enter a valid GitHub URL (e.g., https://github.com/user/repo)'}), 400
    
    try:
        # Clean up previous temp directory
        cleanup_temp_dir()
        
        # Clone the repository
        print(f"📦 Cloning repository: {github_url}")
        repo_path = clone_github_repo(github_url)
        
        # Analyze the cloned repository
        analyzer = RepoAnalyzer(repo_path)
        current_repo = analyzer.analyze()
        current_qa = HybridQAAgent(current_repo)
        current_viz = FlowVisualizer(current_repo, {})
        
        # Prepare file list for frontend
        sorted_files = sorted(current_repo.files, key=lambda f: f.lines, reverse=True)[:15]
        files_list = [{
            'name': f.name,
            'lines': f.lines,
            'modified': f.last_modified,
            'path': f.path
        } for f in sorted_files]
        
        # Get repository name from URL
        repo_name = github_url.rstrip('/').split('/')[-1]
        
        return jsonify({
            'success': True,
            'repo_name': repo_name,
            'stats': {
                'files': len(current_repo.files),
                'lines': current_repo.total_lines,
                'language': current_repo.language,
                'entry_point': current_repo.entry_points[0] if current_repo.entry_points else 'Auto-detect'
            },
            'files_list': files_list,
            'ai_status': current_qa.get_ai_status()
        })
        
    except Exception as e:
        cleanup_temp_dir()
        return jsonify({'error': f'Failed to analyze repository: {str(e)}'}), 500

@app.route('/ask', methods=['POST'])
def ask():
    global current_qa
    
    if not current_qa:
        return jsonify({'error': 'No repository analyzed. Please analyze a GitHub repository first.'}), 400
    
    data = request.get_json()
    question = data.get('question', '')
    result = current_qa.ask(question)
    
    return jsonify({
        'answer': result['answer'],
        'type': result.get('type', 'rule'),
        'ai_used': result.get('ai_used', False)
    })

@app.route('/flow', methods=['POST'])
def flow():
    global current_viz
    
    if not current_viz:
        return jsonify({'error': 'No repository analyzed'}), 400
    
    data = request.get_json()
    feature = data.get('feature', '')
    result = current_viz.simulate_flow(feature)
    return jsonify(result)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'version': '5.0.0'})

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                              ║
    ║   ██████╗ ██████╗ ██████╗ ███████╗███╗   ██╗ █████╗ ██╗   ██╗               ║
    ║  ██╔════╝██╔═══██╗██╔══██╗██╔════╝████╗  ██║██╔══██╗██║   ██║               ║
    ║  ██║     ██║   ██║██║  ██║█████╗  ██╔██╗ ██║███████║██║   ██║               ║
    ║  ██║     ██║   ██║██║  ██║██╔══╝  ██║╚██╗██║██╔══██║╚██╗ ██╔╝               ║
    ║  ╚██████╗╚██████╔╝██████╔╝███████╗██║ ╚████║██║  ██║ ╚████╔╝                ║
    ║   ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝  ╚═══╝                 ║
    ║                                                                              ║
    ║              CodeNav AI v5.0 - GitHub Repository Analyzer                    ║
    ║                                                                              ║
    ║   🚀 Server Starting...                                                      ║
    ║   🌐 URL: http://localhost:5000                                              ║
    ║   📦 Now supports GitHub repositories!                                       ║
    ║                                                                              ║
    ║   Press Ctrl+C to stop                                                       ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    app.run(debug=False, host='0.0.0.0', port=5000)