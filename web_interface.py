#!/usr/bin/env python3
"""
JARVIS Web Interface
Modern web dashboard for interacting with your AI assistant
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from jarvis import JARVIS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Initialize JARVIS
jarvis = JARVIS()

# Store conversation history
conversation_history = []

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('dashboard.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Process user message and return response"""
    data = request.json
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400
    
    # Process command
    response = jarvis.process_command(user_message)
    
    # Store in history
    conversation_history.append({
        'timestamp': datetime.now().isoformat(),
        'user': user_message,
        'jarvis': response
    })
    
    return jsonify({
        'response': response,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/commands', methods=['GET'])
def get_commands():
    """Get list of available commands"""
    commands = {
        'file_operations': [
            {'cmd': 'read <file>', 'desc': 'Read file content'},
            {'cmd': 'write <file> <content>', 'desc': 'Write to file'},
            {'cmd': 'create <file>', 'desc': 'Create new file'},
            {'cmd': 'edit <file> <line> <content>', 'desc': 'Edit specific line'},
            {'cmd': 'delete <file>', 'desc': 'Delete file'},
            {'cmd': 'list [directory]', 'desc': 'List files'},
        ],
        'knowledge': [
            {'cmd': 'search <query>', 'desc': 'Search knowledge base'},
            {'cmd': 'learn <cat> <topic> <content>', 'desc': 'Add to knowledge base'},
            {'cmd': 'analyze <text>', 'desc': 'NLP analysis'},
            {'cmd': 'summarize <text>', 'desc': 'Summarize text'},
        ]
    }
    return jsonify(commands)

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get conversation history"""
    return jsonify(conversation_history)

@app.route('/api/knowledge', methods=['GET'])
def get_knowledge():
    """Get knowledge base stats"""
    import sqlite3
    conn = sqlite3.connect('jarvis_knowledge.db')
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM knowledge')
    total_knowledge = c.fetchone()[0]
    
    c.execute('SELECT DISTINCT category FROM knowledge')
    categories = [row[0] for row in c.fetchall()]
    
    conn.close()
    
    return jsonify({
        'total_items': total_knowledge,
        'categories': categories
    })

@app.route('/api/system/info', methods=['GET'])
def system_info():
    """Get system information"""
    return jsonify({
        'name': 'JARVIS',
        'version': '1.0.0',
        'mode': 'Offline',
        'status': 'Online',
        'startup_time': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🤖 JARVIS Web Interface starting...")
    print("📡 Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
