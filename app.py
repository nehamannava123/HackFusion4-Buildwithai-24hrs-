# app.py - Main Flask Application
import os
import sys

# For Vercel serverless environment
try:
    from flask import Flask, render_template_string, request, jsonify
except ImportError:
    import flask
    from flask import Flask, render_template_string, request, jsonify

from flask import Flask, render_template, request, jsonify
from pathlib import Path

from codenav.analyzer import RepoAnalyzer
from codenav.hybrid_qa import HybridQAAgent
from codenav.visualizer import FlowVisualizer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'codenav-ai-secret-key'

# Global variables
current_repo = None
current_qa = None
current_viz = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    global current_repo, current_qa, current_viz
    
    data = request.get_json()
    repo_path = data.get('path', '')
    
    if not repo_path:
        return jsonify({'error': 'No path provided'}), 400
    
    if not os.path.exists(repo_path):
        return jsonify({'error': f'Path "{repo_path}" does not exist'}), 404
    
    try:
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
        
        return jsonify({
            'success': True,
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
        return jsonify({'error': str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask():
    global current_qa
    
    if not current_qa:
        return jsonify({'error': 'No repository analyzed. Please analyze a folder first.'}), 400
    
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
    return jsonify({'status': 'healthy', 'version': '4.0.0'})

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
    ║                    CodeNav AI v4.0 - Deployment Ready                        ║
    ║                                                                              ║
    ║   🚀 Server Starting...                                                      ║
    ║   🌐 URL: http://localhost:5000                                              ║
    ║   📁 Path: C:\HackFusion4-Final\codenav-ai                                   ║
    ║                                                                              ║
    ║   Press Ctrl+C to stop                                                       ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    app.run(debug=False, host='0.0.0.0', port=5000)