# app.py - COMPLETE WORKING VERSION WITH FILE LIST
import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, jsonify
import tempfile
import git
import shutil

from codenav.analyzer import RepoAnalyzer
from codenav.direct_ai import DirectAIAgent
from codenav.visualizer import FlowVisualizer

app = Flask(__name__)

current_repo = None
current_ai = None
current_viz = None

# HTML Template
HTML_TEMPLATE = '''[Your existing HTML template here]'''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    global current_repo, current_ai, current_viz
    
    data = request.get_json()
    github_url = data.get('url', '')
    
    if not github_url:
        return jsonify({'error': 'No URL provided'}), 400
    
    temp_dir = None
    try:
        temp_dir = tempfile.mkdtemp()
        print(f"📦 Cloning: {github_url}")
        git.Repo.clone_from(github_url, temp_dir)
        
        analyzer = RepoAnalyzer(temp_dir)
        current_repo = analyzer.analyze()
        current_ai = DirectAIAgent(current_repo)
        current_viz = FlowVisualizer(current_repo, {})
        
        # Create files_list for frontend
        sorted_files = sorted(current_repo.files, key=lambda f: f.lines, reverse=True)[:20]
        files_list = [{
            'name': f.name,
            'lines': f.lines,
            'modified': f.last_modified,
            'path': f.path
        } for f in sorted_files]
        
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
            'ai_status': {'available': current_ai.available, 'message': 'Gemini AI Ready!' if current_ai.available else 'AI not available'}
        })
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if temp_dir:
            shutil.rmtree(temp_dir, ignore_errors=True)

@app.route('/ask', methods=['POST'])
def ask():
    global current_ai
    
    if not current_ai:
        return jsonify({'answer': 'Please analyze a repository first'})
    
    data = request.get_json()
    question = data.get('question', '')
    
    answer = current_ai.answer(question)
    
    return jsonify({
        'answer': answer,
        'type': 'ai',
        'ai_used': current_ai.available
    })

@app.route('/flow', methods=['POST'])
def flow():
    global current_viz
    if not current_viz:
        return jsonify({'error': 'No repository analyzed'})
    
    data = request.get_json()
    result = current_viz.simulate_flow(data.get('feature', ''))
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║   🚀 CodeNav AI Starting at http://localhost:{port}           ║
    ║   🤖 AI Powered by Google Gemini                             ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    app.run(debug=False, host='0.0.0.0', port=port)