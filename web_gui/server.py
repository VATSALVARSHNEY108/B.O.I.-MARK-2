#!/usr/bin/env python3
"""
VATSAL Web GUI Server
Modern HTML/CSS/JS interface for VATSAL AI System
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sys
import os
from datetime import datetime

workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, workspace_dir)
sys.path.insert(0, os.path.join(workspace_dir, 'modules'))
sys.path.insert(0, os.path.join(workspace_dir, 'modules', 'core'))

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    """Serve the main web GUI"""
    return render_template('index.html')

@app.route('/api/execute', methods=['POST'])
def execute_command():
    """Execute a command through VATSAL"""
    try:
        data = request.get_json()
        command = data.get('command', '')
        
        if not command:
            return jsonify({
                'status': 'error',
                'message': 'No command provided'
            }), 400
        
        try:
            from vatsal_ai import VatsalAI
            
            vatsal = VatsalAI()
            result = vatsal.process_command(command)
            
            return jsonify({
                'status': 'success',
                'response': result.get('response', 'Command executed successfully!'),
                'technical_details': result.get('details', '')
            })
        except ImportError:
            return jsonify({
                'status': 'success',
                'response': f'Command received: "{command}". VATSAL core integration will be established soon.',
                'technical_details': 'This is currently a demo interface. Connect with VATSAL backend for full functionality.'
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get VATSAL system status"""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'features_count': '100+',
        'vatsal_active': True,
        'self_operating': True
    })

@app.route('/api/clear', methods=['POST'])
def clear_console():
    """Clear console history"""
    return jsonify({
        'status': 'success',
        'message': 'Console cleared'
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'VATSAL Web GUI',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Starting VATSAL Web GUI Server")
    print("=" * 60)
    print("🌐 Web Interface: http://0.0.0.0:5000")
    print("📡 API Endpoint: http://0.0.0.0:5000/api/execute")
    print("✨ Status: http://0.0.0.0:5000/api/status")
    print("=" * 60)
    print()
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False
    )
