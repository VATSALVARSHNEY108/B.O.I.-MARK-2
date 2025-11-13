#!/usr/bin/env python3
"""
VATSAL Web GUI Server
Modern HTML/CSS/JS interface for VATSAL AI System
Connected to VNC GUI via Bridge
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import sys
import os
from datetime import datetime
import threading
import time

workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, workspace_dir)
sys.path.insert(0, os.path.join(workspace_dir, 'modules'))
sys.path.insert(0, os.path.join(workspace_dir, 'modules', 'core'))
sys.path.insert(0, os.path.join(workspace_dir, 'web_gui'))

from bridge import get_gui_bridge

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

bridge = get_gui_bridge()
bridge.start()

pending_requests = {}

@app.route('/')
def index():
    """Serve the main web GUI"""
    return render_template('index.html')

def handle_vnc_response(response):
    """Callback to handle responses from VNC GUI"""
    request_id = response.get('request_id')
    
    if request_id in pending_requests:
        event = pending_requests[request_id]
        pending_requests[request_id] = response
        event.set()
    
    socketio.emit('vnc_response', response)

bridge.register_web_callback(handle_vnc_response)

@app.route('/api/execute', methods=['POST'])
def execute_command():
    """Execute a command through VATSAL VNC GUI"""
    try:
        data = request.get_json()
        command = data.get('command', '')
        
        if not command:
            return jsonify({
                'status': 'error',
                'message': 'No command provided'
            }), 400
        
        bridge_status = bridge.get_status()
        
        if not bridge_status['vnc_handler_registered']:
            return jsonify({
                'status': 'success',
                'response': f'Command received: "{command}"',
                'technical_details': 'VNC GUI not connected. Start the VNC GUI to enable full functionality.',
                'bridge_status': 'disconnected'
            })
        
        event = threading.Event()
        request_id = f"web_{int(time.time() * 1000)}"
        
        pending_requests[request_id] = event
        
        bridge.send_command_to_vnc(command, {'source': 'web_api', 'request_id': request_id})
        
        if event.wait(timeout=30):
            response = pending_requests.pop(request_id)
            
            if isinstance(response, dict) and 'result' in response:
                return jsonify({
                    'status': 'success',
                    'response': response.get('result', 'Command executed'),
                    'technical_details': response.get('details', ''),
                    'bridge_status': 'connected'
                })
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid response format'
                }), 500
        else:
            pending_requests.pop(request_id, None)
            return jsonify({
                'status': 'error',
                'message': 'Command execution timeout (30s)'
            }), 504
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get VATSAL system status"""
    bridge_status = bridge.get_status()
    
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'features_count': '100+',
        'vatsal_active': True,
        'self_operating': True,
        'vnc_connected': bridge_status['vnc_handler_registered'],
        'bridge': bridge_status
    })

@app.route('/api/bridge/status', methods=['GET'])
def get_bridge_status():
    """Get detailed bridge status"""
    return jsonify(bridge.get_status())

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

@socketio.on('connect')
def handle_connect():
    """Handle web client connection"""
    print(f"🔌 Web client connected")
    emit('connection_status', {
        'status': 'connected',
        'bridge_status': bridge.get_status()
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Handle web client disconnection"""
    print(f"🔌 Web client disconnected")

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Starting VATSAL Web GUI Server with VNC Bridge")
    print("=" * 60)
    print("🌐 Web Interface: http://0.0.0.0:5000")
    print("📡 API Endpoint: http://0.0.0.0:5000/api/execute")
    print("✨ Status: http://0.0.0.0:5000/api/status")
    print("🌉 Bridge Status: http://0.0.0.0:5000/api/bridge/status")
    print("=" * 60)
    print()
    print("💡 Waiting for VNC GUI connection...")
    print("   Start VNC GUI with: python launchers/launch_gui.py")
    print()
    
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False,
        allow_unsafe_werkzeug=True
    )
