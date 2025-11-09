"""
Gesture Action Dispatcher
Routes detected gestures to their configured actions
"""

import json
import time
import os
from typing import Dict, Optional, Callable
from modules.automation.window_control_helper import WindowControlHelper
from modules.automation.media_control_helper import MediaControlHelper


class GestureActionDispatcher:
    """
    Dispatches detected gestures to their configured actions.
    Handles cooldowns, priorities, and voice feedback.
    """
    
    def __init__(self, system_controller=None, voice_commander=None):
        self.system_controller = system_controller
        self.voice_commander = voice_commander
        
        # Helper modules
        self.window_control = WindowControlHelper()
        self.media_control = MediaControlHelper()
        
        # Load configuration
        self.config_path = "config/gesture_actions.json"
        self.config = self._load_config()
        
        # Cooldown tracking
        self.last_gesture_times = {}
        
        # Action callbacks
        self.custom_callbacks = {}
        
        # Statistics
        self.stats = {
            'total_gestures': 0,
            'gestures_by_type': {},
            'actions_executed': 0,
            'cooldown_blocked': 0
        }
    
    def _load_config(self) -> Dict:
        """Load gesture configuration from JSON file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            else:
                print(f"⚠️  Config file not found: {self.config_path}")
                return {"gestures": {}, "actions": {}, "settings": {}}
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            return {"gestures": {}, "actions": {}, "settings": {}}
    
    def register_custom_callback(self, action_name: str, callback: Callable):
        """Register a custom callback for an action"""
        self.custom_callbacks[action_name] = callback
    
    def dispatch(self, gesture_id: str, confidence: float = 1.0, metadata: Optional[Dict] = None) -> Dict:
        """
        Dispatch a detected gesture to its configured action.
        
        Args:
            gesture_id: The gesture identifier (e.g., "OPEN_PALM", "THUMBS_UP")
            confidence: Detection confidence (0.0-1.0)
            metadata: Optional additional data about the gesture
        
        Returns:
            dict with 'success', 'message', and optional action result
        """
        self.stats['total_gestures'] += 1
        self.stats['gestures_by_type'][gesture_id] = self.stats['gestures_by_type'].get(gesture_id, 0) + 1
        
        # Get gesture configuration
        gesture_config = self.config.get('gestures', {}).get(gesture_id)
        
        if not gesture_config:
            return {
                'success': False,
                'message': f"Unknown gesture: {gesture_id}",
                'blocked': False
            }
        
        # Check if gesture is enabled
        if not gesture_config.get('enabled', True):
            return {
                'success': False,
                'message': f"Gesture {gesture_id} is disabled",
                'blocked': True
            }
        
        # Check confidence threshold
        settings = self.config.get('settings', {})
        min_confidence = settings.get('confidence_threshold', 0.7)
        if confidence < min_confidence:
            return {
                'success': False,
                'message': f"Low confidence: {confidence:.2f} < {min_confidence:.2f}",
                'blocked': True
            }
        
        # Check cooldown
        cooldown = gesture_config.get('cooldown', 1.0)
        current_time = time.time()
        last_time = self.last_gesture_times.get(gesture_id, 0)
        
        if current_time - last_time < cooldown:
            self.stats['cooldown_blocked'] += 1
            return {
                'success': False,
                'message': f"Cooldown active ({current_time - last_time:.1f}s/{cooldown}s)",
                'blocked': True
            }
        
        # Update last gesture time
        self.last_gesture_times[gesture_id] = current_time
        
        # Get action name
        action_name = gesture_config.get('action')
        if not action_name:
            return {
                'success': False,
                'message': f"No action configured for {gesture_id}"
            }
        
        # Execute action
        result = self._execute_action(action_name, gesture_id, gesture_config)
        
        if result.get('success'):
            self.stats['actions_executed'] += 1
            
            # Voice feedback if enabled
            if settings.get('enable_voice_feedback', True) and self.voice_commander:
                feedback = gesture_config.get('voice_feedback')
                if feedback:
                    self.voice_commander.speak(feedback)
        
        return result
    
    def _execute_action(self, action_name: str, gesture_id: str, gesture_config: Dict) -> Dict:
        """Execute the specified action"""
        
        # Check for custom callback first
        if action_name in self.custom_callbacks:
            try:
                return self.custom_callbacks[action_name](gesture_id, gesture_config)
            except Exception as e:
                return {'success': False, 'message': f"Callback error: {e}"}
        
        # Get action configuration
        action_config = self.config.get('actions', {}).get(action_name, {})
        module = action_config.get('module')
        method = action_config.get('method')
        params = action_config.get('params', {})
        
        if not module or not method:
            return {'success': False, 'message': f"Invalid action config: {action_name}"}
        
        # Route to appropriate module
        try:
            if module == 'system_control' and self.system_controller:
                return self._execute_system_action(method, params)
            elif module == 'window_control':
                return self._execute_window_action(method, params)
            elif module == 'media_control':
                return self._execute_media_action(method, params)
            elif module == 'voice_commander' and self.voice_commander:
                return self._execute_voice_action(method, params)
            elif module == 'gesture_detector':
                # Special internal actions
                return self._execute_internal_action(method, gesture_id)
            else:
                return {'success': False, 'message': f"Unknown module: {module}"}
        except Exception as e:
            return {'success': False, 'message': f"Action execution error: {e}"}
    
    def _execute_system_action(self, method: str, params: Dict) -> Dict:
        """Execute system control action"""
        if not self.system_controller:
            return {'success': False, 'message': "System controller not available"}
        
        try:
            if method == 'lock_screen':
                result = self.system_controller.lock_screen()
            elif method == 'increase_volume':
                amount = params.get('amount', 10)
                result = self.system_controller.increase_volume(amount)
            elif method == 'decrease_volume':
                amount = params.get('amount', 10)
                result = self.system_controller.decrease_volume(amount)
            elif method == 'take_screenshot':
                import pyautogui
                filename = f"screenshot_{int(time.time())}.png"
                pyautogui.screenshot(filename)
                result = f"Screenshot saved: {filename}"
            elif method == 'toggle_screen_recording':
                result = "Screen recording toggle not yet implemented"
            else:
                result = f"Unknown system method: {method}"
            
            return {'success': True, 'message': result}
        except Exception as e:
            return {'success': False, 'message': f"System action error: {e}"}
    
    def _execute_window_action(self, method: str, params: Dict) -> Dict:
        """Execute window control action"""
        try:
            if method == 'minimize_active_window':
                return self.window_control.minimize_active_window()
            elif method == 'maximize_active_window':
                return self.window_control.maximize_active_window()
            elif method == 'close_active_window':
                return self.window_control.close_active_window()
            elif method == 'switch_desktop':
                direction = params.get('direction', 'right')
                return self.window_control.switch_desktop(direction)
            elif method == 'show_desktop':
                return self.window_control.show_desktop()
            else:
                return {'success': False, 'message': f"Unknown window method: {method}"}
        except Exception as e:
            return {'success': False, 'message': f"Window action error: {e}"}
    
    def _execute_media_action(self, method: str, params: Dict) -> Dict:
        """Execute media control action"""
        try:
            if method == 'play_pause':
                return self.media_control.play_pause()
            elif method == 'next_track':
                return self.media_control.next_track()
            elif method == 'previous_track':
                return self.media_control.previous_track()
            elif method == 'stop':
                return self.media_control.stop()
            else:
                return {'success': False, 'message': f"Unknown media method: {method}"}
        except Exception as e:
            return {'success': False, 'message': f"Media action error: {e}"}
    
    def _execute_voice_action(self, method: str, params: Dict) -> Dict:
        """Execute voice commander action"""
        if not self.voice_commander:
            return {'success': False, 'message': "Voice commander not available"}
        
        try:
            # Dynamically call the voice commander method
            if hasattr(self.voice_commander, method):
                method_func = getattr(self.voice_commander, method)
                result = method_func(**params) if params else method_func()
                
                # Handle different return types
                if isinstance(result, dict):
                    return result
                else:
                    return {'success': True, 'message': f"Voice action executed: {method}"}
            else:
                return {'success': False, 'message': f"Unknown voice method: {method}"}
        except Exception as e:
            return {'success': False, 'message': f"Voice action error: {e}"}
    
    def _execute_internal_action(self, method: str, gesture_id: str) -> Dict:
        """Execute internal gesture detector actions"""
        # These are handled by the detector itself via callbacks
        return {'success': True, 'message': f"Internal action: {method}"}
    
    def get_stats(self) -> Dict:
        """Get dispatcher statistics"""
        return self.stats.copy()
    
    def reset_stats(self):
        """Reset statistics"""
        self.stats = {
            'total_gestures': 0,
            'gestures_by_type': {},
            'actions_executed': 0,
            'cooldown_blocked': 0
        }
    
    def get_gesture_list(self) -> list:
        """Get list of all configured gestures"""
        gestures = []
        for gesture_id, config in self.config.get('gestures', {}).items():
            gestures.append({
                'id': gesture_id,
                'action': config.get('action'),
                'description': config.get('description'),
                'enabled': config.get('enabled', True),
                'cooldown': config.get('cooldown', 1.0)
            })
        return gestures
