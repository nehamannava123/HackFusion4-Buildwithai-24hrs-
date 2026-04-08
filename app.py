# app.py
from flask import Flask, render_template, request, jsonify
from pathlib import Path
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from codenav.analyzer import RepoAnalyzer
from codenav.detector import EntryPointDetector
from codenav.visualizer import FlowVisualizer
from codenav.qa import CodebaseQA

app = Flask(__name__)

# Global variables to store analysis results
current_repo_info = None
current_qa = None
current_flow_viz = None
current_detector = None
current_analyzer = None

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_repository():
    """Analyze a repository path"""
    global current_repo_info, current_qa, current_flow_viz, current_detector, current_analyzer
    
    data = request.get_json()
    repo_path = data.get('path', '')
    
    if not repo_path:
        return jsonify({'error': 'No path provided'}), 400
    
    # Check if path exists
    if not os.path.exists(repo_path):
        return jsonify({'error': f'Path "{repo_path}" does not exist'}), 404
    
    try:
        # Analyze the repository
        current_analyzer = RepoAnalyzer(repo_path)
        current_repo_info = current_analyzer.analyze()
        
        # Extract architecture patterns
        arch_patterns = {
            'controllers': [f.path for f in current_repo_info.files if 'controller' in f.path.lower()],
            'services': [f.path for f in current_repo_info.files if 'service' in f.path.lower()],
            'models': [f.path for f in current_repo_info.files if 'model' in f.path.lower()],
            'routes': [f.path for f in current_repo_info.files if 'route' in f.path.lower() or 'urls' in f.path.lower()],
            'config': [f.path for f in current_repo_info.files if 'config' in f.path.lower()],
        }
        
        # Initialize components
        current_detector = EntryPointDetector(current_repo_info, arch_patterns)
        current_flow_viz = FlowVisualizer(current_repo_info, current_repo_info.dependencies)
        current_qa = CodebaseQA(current_repo_info, arch_patterns, current_repo_info.dependencies)
        
        # Prepare response
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
            'entry_points': current_repo_info.entry_points[:3]
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    """Answer a question about the codebase"""
    global current_qa
    
    if not current_qa:
        return jsonify({'error': 'No repository analyzed yet. Please analyze a repository first.'}), 400
    
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    # Get answer from QA system
    result = current_qa.ask(question)
    
    return jsonify({
        'question': question,
        'answer': result['answer'],
        'type': result.get('type', 'general')
    })

@app.route('/flow', methods=['POST'])
def simulate_flow():
    """Simulate execution flow for a feature"""
    global current_flow_viz
    
    if not current_flow_viz:
        return jsonify({'error': 'No repository analyzed yet'}), 400
    
    data = request.get_json()
    feature = data.get('feature', '')
    
    if not feature:
        return jsonify({'error': 'No feature specified'}), 400
    
    result = current_flow_viz.simulate_flow(feature)
    
    return jsonify({
        'success': result['success'],
        'flow_type': result.get('flow_type', 'unknown'),
        'description': result.get('description', ''),
        'steps': result.get('steps', []),
        'visualization': result.get('visualization', ''),
        'relevant_files': result.get('relevant_files', [])
    })

@app.route('/navigation-path', methods=['GET'])
def get_navigation_path():
    """Get the navigation path"""
    global current_detector
    
    if not current_detector:
        return jsonify({'error': 'No repository analyzed yet'}), 400
    
    start_point = current_detector.get_best_starting_point()
    path = current_detector.generate_navigation_path(start_point)
    
    return jsonify({
        'start_point': start_point,
        'steps': path
    })

@app.route('/learning-path', methods=['POST'])
def get_learning_path():
    """Get learning path based on experience level"""
    global current_detector
    
    if not current_detector:
        return jsonify({'error': 'No repository analyzed yet'}), 400
    
    data = request.get_json()
    level = data.get('level', 'beginner')
    
    path = current_detector.get_learning_path(level)
    
    return jsonify(path)

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║   🚀 CodeNav AI Web Interface Starting...                    ║
    ║                                                              ║
    ║   Open your browser and go to: http://localhost:5000        ║
    ║                                                              ║
    ║   Press Ctrl+C to stop the server                           ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    app.run(debug=True, host='0.0.0.0', port=5000)