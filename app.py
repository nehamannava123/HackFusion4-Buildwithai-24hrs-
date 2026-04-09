<<<<<<< HEAD
# app.py
from flask import Flask, render_template, request, jsonify
from pathlib import Path
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from codenav.analyzer import RepoAnalyzer
from codenav.detector import EntryPointDetector
from codenav.visualizer import FlowVisualizer
from codenav.qa import CodebaseQA

app = Flask(__name__)

current_repo_info = None
current_qa = None
current_flow_viz = None
current_detector = None
=======
# app.py - Main Flask Application
from flask import Flask, render_template, request, jsonify
import os
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
>>>>>>> 7db48e7 (Final version: CodeNav AI complete)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
<<<<<<< HEAD
def analyze_repository():
    global current_repo_info, current_qa, current_flow_viz, current_detector
=======
def analyze():
    global current_repo, current_qa, current_viz
>>>>>>> 7db48e7 (Final version: CodeNav AI complete)
    
    data = request.get_json()
    repo_path = data.get('path', '')
    
    if not repo_path:
        return jsonify({'error': 'No path provided'}), 400
    
    if not os.path.exists(repo_path):
        return jsonify({'error': f'Path "{repo_path}" does not exist'}), 404
    
    try:
<<<<<<< HEAD
        current_repo_info = RepoAnalyzer(repo_path).analyze()
        
        arch_patterns = {
            'controllers': [f.path for f in current_repo_info.files if 'controller' in f.path.lower()],
            'services': [f.path for f in current_repo_info.files if 'service' in f.path.lower()],
            'models': [f.path for f in current_repo_info.files if 'model' in f.path.lower()],
            'routes': [f.path for f in current_repo_info.files if 'route' in f.path.lower()],
        }
        
        current_detector = EntryPointDetector(current_repo_info, arch_patterns)
        current_flow_viz = FlowVisualizer(current_repo_info, current_repo_info.dependencies)
        current_qa = CodebaseQA(current_repo_info, arch_patterns, current_repo_info.dependencies)
        
        response = {
            'success': True,
            'stats': {
                'files': len(current_repo_info.files),
                'lines': current_repo_info.total_lines,
                'language': current_repo_info.language.upper(),
                'entry_point': current_repo_info.entry_points[0] if current_repo_info.entry_points else 'Not found'
            },
            'architecture': {
                'controllers': len(arch_patterns['controllers']),
                'services': len(arch_patterns['services']),
                'models': len(arch_patterns['models']),
                'routes': len(arch_patterns['routes'])
            },
            'file_types': dict(list(current_repo_info.file_types.items())[:10])
        }
        return jsonify(response)
=======
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
>>>>>>> 7db48e7 (Final version: CodeNav AI complete)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ask', methods=['POST'])
<<<<<<< HEAD
def ask_question():
    global current_qa
    if not current_qa:
        return jsonify({'error': 'No repository analyzed'}), 400
=======
def ask():
    global current_qa
    
    if not current_qa:
        return jsonify({'error': 'No repository analyzed. Please analyze a folder first.'}), 400
>>>>>>> 7db48e7 (Final version: CodeNav AI complete)
    
    data = request.get_json()
    question = data.get('question', '')
    result = current_qa.ask(question)
<<<<<<< HEAD
    return jsonify(result)

@app.route('/flow', methods=['POST'])
def simulate_flow():
    global current_flow_viz
    if not current_flow_viz:
=======
    
    return jsonify({
        'answer': result['answer'],
        'type': result.get('type', 'rule'),
        'ai_used': result.get('ai_used', False)
    })

@app.route('/flow', methods=['POST'])
def flow():
    global current_viz
    
    if not current_viz:
>>>>>>> 7db48e7 (Final version: CodeNav AI complete)
        return jsonify({'error': 'No repository analyzed'}), 400
    
    data = request.get_json()
    feature = data.get('feature', '')
<<<<<<< HEAD
    result = current_flow_viz.simulate_flow(feature)
    return jsonify(result)

@app.route('/files', methods=['GET'])
def list_files():
    global current_repo_info
    if not current_repo_info:
        return jsonify({'error': 'No repository analyzed'}), 400
    
    files = [{'path': f.path, 'lines': f.lines, 'type': f.file_type} for f in current_repo_info.files]
    return jsonify({'files': files[:50]})

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║   🚀 CodeNav AI Web Interface Starting...                    ║
    ║                                                              ║
    ║   Open your browser and go to: http://localhost:5000        ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    app.run(debug=True, host='0.0.0.0', port=5000)
=======
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
>>>>>>> 7db48e7 (Final version: CodeNav AI complete)
