#!/usr/bin/env python3
"""
Modern Web GUI for VATSAL AI Desktop Automation
Beautiful eye-comforting interface with cyber aesthetic
"""

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import sys
import os
from datetime import datetime
import threading
import time

workspace_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, workspace_dir)
sys.path.insert(0, os.path.join(workspace_dir, 'modules'))

app = Flask(__name__, 
            template_folder=os.path.join(workspace_dir, 'templates'),
            static_folder=os.path.join(workspace_dir, 'static'))
app.config['SECRET_KEY'] = 'vatsal-ai-secret-key-2025'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

command_history = []
stats = {
    'commands_executed': 0,
    'success_count': 0,
    'start_time': datetime.now()
}

@app.route('/')
def index():
    return render_template('modern_gui.html')

@socketio.on('connect')
def handle_connect():
    print(f"✅ Client connected: {request.sid}")
    emit('status', {'message': 'Connected to VATSAL AI', 'type': 'success'})
    emit('stats_update', get_stats())

@socketio.on('disconnect')
def handle_disconnect():
    print(f"❌ Client disconnected: {request.sid}")

@socketio.on('execute_command')
def handle_command(data):
    command = data.get('command', '').strip()
    
    if not command:
        emit('command_result', {
            'success': False,
            'output': 'Please enter a command',
            'timestamp': datetime.now().isoformat()
        })
        return
    
    try:
        from modules.core.ai_processor import VatsalAIProcessor
        
        ai_processor = VatsalAIProcessor()
        
        emit('command_status', {'message': f'Processing: {command}', 'type': 'info'})
        
        result = ai_processor.process_command(command)
        
        stats['commands_executed'] += 1
        if result and result.get('success', True):
            stats['success_count'] += 1
        
        command_history.insert(0, {
            'command': command,
            'timestamp': datetime.now().isoformat(),
            'success': result.get('success', True) if result else False
        })
        
        if len(command_history) > 50:
            command_history.pop()
        
        emit('command_result', {
            'success': result.get('success', True) if result else True,
            'output': result.get('message', 'Command executed') if result else 'Command executed',
            'timestamp': datetime.now().isoformat()
        })
        
        emit('stats_update', get_stats())
        emit('history_update', command_history[:10])
        
    except Exception as e:
        print(f"❌ Error processing command: {e}")
        import traceback
        traceback.print_exc()
        
        emit('command_result', {
            'success': False,
            'output': f'Error: {str(e)}',
            'timestamp': datetime.now().isoformat()
        })

@socketio.on('get_stats')
def handle_get_stats():
    emit('stats_update', get_stats())

@socketio.on('get_history')
def handle_get_history():
    emit('history_update', command_history[:10])

def get_stats():
    uptime = datetime.now() - stats['start_time']
    hours = int(uptime.total_seconds() // 3600)
    minutes = int((uptime.total_seconds() % 3600) // 60)
    
    success_rate = 0
    if stats['commands_executed'] > 0:
        success_rate = int((stats['success_count'] / stats['commands_executed']) * 100)
    
    return {
        'commands_executed': stats['commands_executed'],
        'success_rate': success_rate,
        'uptime': f"{hours}h {minutes}m"
    }

def send_time_updates():
    while True:
        time.sleep(1)
        socketio.emit('time_update', {'time': datetime.now().strftime('%I:%M:%S %p')})

def main():
    print("=" * 70)
    print("🚀 Starting VATSAL AI Modern Web GUI")
    print("=" * 70)
    print(f"📡 Server will be available at: http://0.0.0.0:5000")
    print(f"🎨 Modern Cyber Aesthetic UI with Cloud Linen Theme")
    print(f"⚡ Real-time WebSocket enabled")
    print("=" * 70)
    
    threading.Thread(target=send_time_updates, daemon=True).start()
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)

if __name__ == '__main__':
    main()
