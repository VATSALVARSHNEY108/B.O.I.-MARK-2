#!/usr/bin/env python3
"""
Communication Bridge between Web GUI and VNC GUI
Handles bidirectional message passing using threading and queues
"""

import threading
import queue
import time
from typing import Dict, Any, Callable, Optional
from datetime import datetime


class GUIBridge:
    """Singleton bridge for communication between Flask Web GUI and VNC tkinter GUI"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.command_queue = queue.Queue()
        self.response_queue = queue.Queue()
        
        self.vnc_gui_handler: Optional[Callable] = None
        self.web_gui_callbacks = []
        
        self.running = False
        self.monitor_thread = None
        
        self._initialized = True
        print("🌉 GUI Bridge initialized")
    
    def start(self):
        """Start the bridge monitor thread"""
        if self.running:
            return
            
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_responses, daemon=True)
        self.monitor_thread.start()
        print("🌉 GUI Bridge started and monitoring")
    
    def stop(self):
        """Stop the bridge"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        print("🌉 GUI Bridge stopped")
    
    def register_vnc_handler(self, handler: Callable):
        """
        Register the VNC GUI command handler
        Handler should accept: (command: str, metadata: dict) -> dict
        """
        self.vnc_gui_handler = handler
        print("✅ VNC GUI handler registered with bridge")
    
    def register_web_callback(self, callback: Callable):
        """
        Register a callback for web GUI to receive responses
        Callback should accept: (response: dict)
        """
        self.web_gui_callbacks.append(callback)
        print(f"✅ Web GUI callback registered ({len(self.web_gui_callbacks)} total)")
    
    def send_command_to_vnc(self, command: str, metadata: Optional[Dict] = None) -> str:
        """
        Send a command from Web GUI to VNC GUI
        Returns a request ID for tracking
        """
        metadata = metadata or {}
        request_id = metadata.get('request_id', f"web_{int(time.time() * 1000)}")
        
        command_data = {
            'request_id': request_id,
            'command': command,
            'source': 'web_gui',
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata
        }
        
        self.command_queue.put(command_data)
        print(f"📤 Command sent to VNC GUI: {command} (ID: {request_id})")
        
        return request_id
    
    def get_command_from_queue(self, timeout: float = 0.1) -> Optional[Dict]:
        """
        VNC GUI calls this to get commands from the queue
        """
        try:
            command_data = self.command_queue.get(timeout=timeout)
            return command_data
        except queue.Empty:
            return None
    
    def send_response_to_web(self, response: Dict):
        """
        VNC GUI sends response back to Web GUI
        """
        response['timestamp'] = datetime.now().isoformat()
        self.response_queue.put(response)
        print(f"📥 Response sent to Web GUI: {response.get('status', 'unknown')}")
    
    def _monitor_responses(self):
        """Monitor response queue and notify web GUI callbacks"""
        while self.running:
            try:
                response = self.response_queue.get(timeout=0.5)
                
                for callback in self.web_gui_callbacks:
                    try:
                        callback(response)
                    except Exception as e:
                        print(f"❌ Error in web callback: {e}")
                        
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ Error in response monitor: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get bridge status"""
        return {
            'running': self.running,
            'vnc_handler_registered': self.vnc_gui_handler is not None,
            'web_callbacks': len(self.web_gui_callbacks),
            'pending_commands': self.command_queue.qsize(),
            'pending_responses': self.response_queue.qsize()
        }


def get_gui_bridge() -> GUIBridge:
    """Get the singleton GUI bridge instance"""
    return GUIBridge()
