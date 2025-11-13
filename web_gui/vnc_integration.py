#!/usr/bin/env python3
"""
VNC GUI Integration Module
Connects the tkinter VNC GUI to the Web GUI Bridge
"""

import threading
import time
from typing import Any, Optional
import sys
import os

workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(workspace_dir, 'web_gui'))

from bridge import get_gui_bridge


class VNCIntegration:
    """
    Integration layer for VNC GUI to communicate with Web GUI
    Polls the bridge for commands and executes them
    """
    
    def __init__(self, gui_instance):
        """
        Initialize VNC integration
        
        Args:
            gui_instance: The AutomationControllerGUI instance
        """
        self.gui = gui_instance
        self.bridge = get_gui_bridge()
        self.bridge.start()
        
        self.running = False
        self.poll_thread = None
        
        print("🌉 VNC GUI Integration initialized")
    
    def start(self):
        """Start listening for commands from Web GUI"""
        if self.running:
            return
        
        self.bridge.register_vnc_handler(self.handle_command)
        
        self.running = True
        self.poll_thread = threading.Thread(target=self._poll_commands, daemon=True)
        self.poll_thread.start()
        
        print("✅ VNC GUI now connected to Web GUI Bridge")
        print("   Commands from Web GUI will be executed here")
    
    def stop(self):
        """Stop listening for commands"""
        self.running = False
        if self.poll_thread:
            self.poll_thread.join(timeout=2)
        print("🛑 VNC GUI disconnected from Web GUI Bridge")
    
    def handle_command(self, command: str, metadata: dict) -> dict:
        """
        Handle a command sent from Web GUI
        This is called by the bridge when a command is received
        
        Args:
            command: The command text
            metadata: Additional metadata about the command
            
        Returns:
            dict: Result of command execution
        """
        try:
            print(f"📨 Received command from Web GUI: {command}")
            
            result = self._execute_in_vnc_gui(command)
            
            return {
                'success': result.get('success', True),
                'result': result.get('message', 'Command executed'),
                'details': result.get('details', '')
            }
        except Exception as e:
            print(f"❌ Error executing command from Web GUI: {e}")
            return {
                'success': False,
                'result': f'Error: {str(e)}',
                'details': ''
            }
    
    def _execute_in_vnc_gui(self, command: str) -> dict:
        """
        Execute command in the VNC GUI's main thread
        
        Args:
            command: Command to execute
            
        Returns:
            dict: Execution result
        """
        result_holder = {'completed': False, 'result': None}
        
        def execute_in_gui_thread():
            try:
                from modules.core.gemini_controller import parse_command
                
                command_dict = parse_command(command)
                
                if command_dict.get("action") == "error":
                    result_holder['result'] = {
                        'success': False,
                        'message': command_dict.get('description', 'Error parsing command'),
                        'details': ''
                    }
                else:
                    executor_result = self.gui.executor.execute(command_dict)
                    result_holder['result'] = executor_result
                
            except Exception as e:
                result_holder['result'] = {
                    'success': False,
                    'message': f'Execution error: {str(e)}',
                    'details': ''
                }
            finally:
                result_holder['completed'] = True
        
        if hasattr(self.gui, 'root'):
            self.gui.root.after(0, execute_in_gui_thread)
            
            timeout = 30
            start_time = time.time()
            while not result_holder['completed'] and (time.time() - start_time) < timeout:
                time.sleep(0.1)
            
            if not result_holder['completed']:
                return {
                    'success': False,
                    'message': 'Command execution timeout',
                    'details': ''
                }
        else:
            execute_in_gui_thread()
        
        return result_holder.get('result', {
            'success': False,
            'message': 'No result',
            'details': ''
        })
    
    def _poll_commands(self):
        """Poll the bridge for commands from Web GUI"""
        print("🔄 Started polling for Web GUI commands...")
        
        while self.running:
            try:
                command_data = self.bridge.get_command_from_queue(timeout=0.5)
                
                if command_data:
                    request_id = command_data.get('request_id')
                    command = command_data.get('command')
                    metadata = command_data.get('metadata', {})
                    
                    print(f"📥 Processing command: {command} (ID: {request_id})")
                    
                    result = self.handle_command(command, metadata)
                    
                    response = {
                        'request_id': request_id,
                        'command': command,
                        'status': 'success' if result.get('success') else 'error',
                        'result': result.get('result', ''),
                        'details': result.get('details', '')
                    }
                    
                    self.bridge.send_response_to_web(response)
                    
                    if hasattr(self.gui, 'update_output'):
                        self.gui.root.after(0, lambda: self.gui.update_output(
                            f"\n🌐 Web GUI Command: {command}\n",
                            "info"
                        ))
                
            except Exception as e:
                if self.running:
                    print(f"❌ Error in command polling: {e}")
                time.sleep(1)
        
        print("🛑 Stopped polling for commands")


def integrate_vnc_with_web_gui(gui_instance):
    """
    Helper function to integrate VNC GUI with Web GUI
    
    Args:
        gui_instance: The AutomationControllerGUI instance
        
    Returns:
        VNCIntegration: The integration instance
    """
    integration = VNCIntegration(gui_instance)
    integration.start()
    return integration
