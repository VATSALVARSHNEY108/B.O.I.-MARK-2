#!/usr/bin/env python3

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import os
import sys
from dotenv import load_dotenv
from datetime import datetime
import threading

load_dotenv()

app = Flask(__name__, 
            template_folder='../../templates',
            static_folder='../../static')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

executor = None
vatsal = None

# Try to import and initialize executor (may fail due to X11 dependencies)
try:
    os.environ.setdefault('DISPLAY', ':0')
    from modules.core.command_executor import CommandExecutor
    executor = CommandExecutor()
    print("✅ Command executor initialized successfully")
except Exception as e:
    print(f"⚠️ Running in demo mode (executor unavailable): {e}")
    executor = None

# Try to import vatsal assistant
try:
    from modules.core.vatsal_assistant import create_vatsal_assistant
    vatsal = create_vatsal_assistant()
    print("✅ VATSAL assistant initialized successfully")
except Exception as e:
    print(f"⚠️ VATSAL assistant unavailable: {e}")
    vatsal = None

command_history = []
stats = {
    "commands_run": 0,
    "success_rate": 100,
    "active_time": 0
}


@app.route('/')
def index():
    """Render the main GUI"""
    return render_template('modern_gui.html')


@app.route('/api/execute', methods=['POST'])
def execute_command():
    """Execute a command"""
    data = request.json
    command = data.get('command', '').strip()
    
    if not command:
        return jsonify({"success": False, "message": "No command provided"})
    
    command_history.append({
        "command": command,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    
    stats["commands_run"] += 1
    
    try:
        if executor:
            result = executor.execute(command)
            return jsonify({
                "success": True,
                "message": result,
                "stats": stats,
                "history": command_history[-10:]
            })
        else:
            return jsonify({
                "success": False,
                "message": "Executor not initialized. Please set GEMINI_API_KEY.",
                "stats": stats,
                "history": command_history[-10:]
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}",
            "stats": stats,
            "history": command_history[-10:]
        })


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get current statistics"""
    return jsonify({
        "stats": stats,
        "history": command_history[-10:]
    })


@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('status', {'status': 'connected'})


@socketio.on('execute_command')
def handle_command(data):
    """Handle command execution via WebSocket"""
    command = data.get('command', '').strip()
    
    if not command:
        emit('command_result', {"success": False, "message": "No command provided"})
        return
    
    command_history.append({
        "command": command,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    
    stats["commands_run"] += 1
    
    emit('command_started', {'command': command})
    
    def run_command():
        try:
            if executor:
                result = executor.execute(command)
                socketio.emit('command_result', {
                    "success": True,
                    "message": result,
                    "stats": stats,
                    "history": command_history[-10:]
                })
            else:
                socketio.emit('command_result', {
                    "success": False,
                    "message": "Executor not initialized. Please set GEMINI_API_KEY.",
                    "stats": stats,
                    "history": command_history[-10:]
                })
        except Exception as e:
            socketio.emit('command_result', {
                "success": False,
                "message": f"Error: {str(e)}",
                "stats": stats,
                "history": command_history[-10:]
            })
    
    thread = threading.Thread(target=run_command)
    thread.daemon = True
    thread.start()


def main():
    """Start the web GUI server"""
    print("✨ Starting Modern VATSAL Web GUI...")
    print("=" * 60)
    print("🎨 Eye-Comforting Design | 3D Blocks | Beautiful Interface")
    print("=" * 60)
    print("\n🌐 Access the GUI at: http://0.0.0.0:5000")
    print("📱 Or use your Replit webview URL\n")
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)


if __name__ == "__main__":
    main()
