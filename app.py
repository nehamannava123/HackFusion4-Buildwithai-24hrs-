# app.py - Flask web server
from flask import Flask, render_template_string, request, jsonify
import os

from codenav.analyzer import RepoAnalyzer
from codenav.hybrid_qa import HybridQAAgent
from codenav.visualizer import FlowVisualizer

app = Flask(__name__)

current_repo = None
current_qa = None
current_viz = None

# Simple HTML template (no external files needed)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>CodeNav AI</title>
    <meta charset="UTF-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #fff;
            padding: 20px;
        }
        .container { max-width: 1000px; margin: 0 auto; }
        .header {
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            margin-bottom: 30px;
        }
        .header h1 { font-size: 48px; margin-bottom: 10px; }
        .ai-badge {
            display: inline-block;
            background: #4caf50;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
            margin-top: 10px;
        }
        .ai-badge.off { background: #ff9800; }
        .repo-box {
            background: rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 30px;
            display: flex;
            gap: 15px;
        }
        .repo-input {
            flex: 1;
            background: rgba(255,255,255,0.2);
            border: none;
            padding: 15px;
            border-radius: 8px;
            color: white;
            font-size: 16px;
        }
        .repo-input::placeholder { color: rgba(255,255,255,0.6); }
        .btn {
            background: #4caf50;
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
        }
        .stat-number { font-size: 36px; font-weight: bold; color: #667eea; }
        .stat-label { margin-top: 8px; color: rgba(255,255,255,0.7); }
        .chat {
            background: rgba(255,255,255,0.1);
            border-radius: 12px;
            height: 400px;
            display: flex;
            flex-direction: column;
        }
        .messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
        }
        .message {
            margin-bottom: 15px;
            padding: 10px 15px;
            border-radius: 10px;
            max-width: 80%;
        }
        .user {
            background: #667eea;
            margin-left: auto;
            text-align: right;
        }
        .bot {
            background: #764ba2;
        }
        .chat-input {
            display: flex;
            padding: 15px;
            gap: 10px;
            border-top: 1px solid rgba(255,255,255,0.2);
        }
        .chat-input input {
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 8px;
            background: rgba(255,255,255,0.2);
            color: white;
        }
        .quick-buttons {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            padding: 10px 15px;
        }
        .quick-btn {
            background: rgba(255,255,255,0.15);
            border: none;
            padding: 8px 15px;
            border-radius: 20px;
            color: white;
            cursor: pointer;
        }
        .loading {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.8);
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        .spinner {
            width: 50px;
            height: 50px;
            border: 3px solid #fff;
            border-top-color: #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 CodeNav AI</h1>
            <p>Understand any codebase in seconds</p>
            <div class="ai-badge" id="aiBadge">⚡ Checking...</div>
        </div>

        <div class="repo-box">
            <input type="text" id="repoPath" class="repo-input" placeholder="Enter folder path (e.g., C:\my-project)">
            <button class="btn" onclick="analyze()">Analyze</button>
        </div>

        <div id="statsPanel" style="display: none;">
            <div class="stats" id="stats"></div>
        </div>

        <div class="chat">
            <div class="messages" id="messages">
                <div class="message bot">👋 Welcome! Enter a folder path and click Analyze to start.</div>
            </div>
            <div class="chat-input">
                <input type="text" id="question" placeholder="Ask about the codebase...">
                <button class="btn" onclick="ask()" style="padding: 12px 20px;">Send</button>
            </div>
            <div class="quick-buttons">
                <button class="quick-btn" onclick="askQuick('How many files?')">📊 Count</button>
                <button class="quick-btn" onclick="askQuick('What language?')">🛠 Language</button>
                <button class="quick-btn" onclick="askQuick('Where to start?')">📍 Start</button>
                <button class="quick-btn" onclick="askQuick('Explain what this project does')">🤖 Explain</button>
            </div>
        </div>
    </div>

    <div class="loading" id="loading"><div class="spinner"></div></div>

    <script>
        let repoData = null;

        async function analyze() {
            const path = document.getElementById('repoPath').value;
            if (!path) { addMessage('Please enter a folder path!', 'bot'); return; }

            document.getElementById('loading').style.display = 'flex';
            addMessage(`Analyzing ${path}...`, 'bot');

            try {
                const res = await fetch('/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ path: path })
                });
                repoData = await res.json();

                if (repoData.error) { addMessage(`Error: ${repoData.error}`, 'bot'); return; }

                document.getElementById('statsPanel').style.display = 'block';
                document.getElementById('stats').innerHTML = `
                    <div class="stat-card"><div class="stat-number">${repoData.files}</div><div class="stat-label">Files</div></div>
                    <div class="stat-card"><div class="stat-number">${repoData.lines.toLocaleString()}</div><div class="stat-label">Lines</div></div>
                    <div class="stat-card"><div class="stat-number">${repoData.language}</div><div class="stat-label">Language</div></div>
                    <div class="stat-card"><div class="stat-number">${repoData.entry_point || '?'}</div><div class="stat-label">Entry Point</div></div>
                `;

                const badge = document.getElementById('aiBadge');
                if (repoData.ai_available) {
                    badge.textContent = '🤖 AI Ready';
                    badge.classList.remove('off');
                    addMessage(`✅ Analysis complete! AI is ready. Ask "Explain what this project does"`, 'bot');
                } else {
                    badge.textContent = '⚡ Rule Mode';
                    badge.classList.add('off');
                    addMessage(`✅ Analysis complete! Found ${repoData.files} files. (AI not available)`, 'bot');
                }
            } catch(err) { addMessage(`Error: ${err.message}`, 'bot'); }
            finally { document.getElementById('loading').style.display = 'none'; }
        }

        async function ask() {
            const question = document.getElementById('question').value;
            if (!question || !repoData) return;

            addMessage(question, 'user');
            document.getElementById('question').value = '';

            const res = await fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: question })
            });
            const result = await res.json();
            addMessage(result.answer, 'bot', result.ai_used);
        }

        function askQuick(q) { document.getElementById('question').value = q; ask(); }

        function addMessage(text, sender, isAI = false) {
            const messages = document.getElementById('messages');
            const div = document.createElement('div');
            div.className = `message ${sender}`;
            const aiTag = isAI ? ' [AI]' : '';
            div.innerHTML = `<div>${text.replace(/\\n/g, '<br>')}</div><small style="opacity:0.6;">Just now${aiTag}</small>`;
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    folder = data.get('path', '')
    
    if not os.path.exists(folder):
        return jsonify({'error': 'Path not found'})
    
    analyzer = RepoAnalyzer(folder)
    repo = analyzer.analyze()
    
    global current_repo, current_qa, current_viz
    current_repo = repo
    current_qa = HybridQAAgent(repo)
    current_viz = FlowVisualizer(repo, {})
    
    ai_status = current_qa.get_ai_status()
    
    return jsonify({
        'files': len(repo.files),
        'lines': repo.total_lines,
        'language': repo.language.upper(),
        'entry_point': repo.entry_points[0] if repo.entry_points else None,
        'ai_available': ai_status.get('available', False)
    })

@app.route('/ask', methods=['POST'])
def ask():
    global current_qa
    if not current_qa:
        return jsonify({'answer': 'Please analyze a folder first!'})
    
    data = request.get_json()
    question = data.get('question', '')
    result = current_qa.ask(question)
    
    return jsonify({
        'answer': result['answer'],
        'ai_used': result.get('ai_used', False)
    })

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║   🚀 CodeNav AI Starting...                                  ║
    ║                                                              ║
    ║   Open: http://localhost:5000                               ║
    ║                                                              ║
    ║   Press Ctrl+C to stop                                       ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    app.run(debug=True, host='0.0.0.0', port=5000)