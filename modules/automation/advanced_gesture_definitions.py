"""
Advanced Gesture Definitions for VATSAL AI
Comprehensive gesture system with system controls, interactions, and combinations
"""

from enum import Enum
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


class GestureType(Enum):
    """Types of gesture detection"""
    STATIC = "static"  # Single hand pose
    DYNAMIC = "dynamic"  # Motion-based
    COMBINATION = "combination"  # Sequential gestures
    FACIAL_FUSION = "facial_fusion"  # Face + gesture


class GestureCategory(Enum):
    """Gesture categories"""
    SYSTEM_CONTROL = "system_control"
    INTERACTION = "interaction"
    NAVIGATION = "navigation"
    CONFIRMATION = "confirmation"
    SECURITY = "security"


@dataclass
class GestureDefinition:
    """Definition of a single gesture"""
    name: str
    emoji: str
    function: str
    category: GestureCategory
    gesture_type: GestureType
    description: str
    mediapipe_mapping: Optional[str] = None  # MediaPipe gesture name if available
    hand_landmarks_required: bool = True


# =============================================================================
# 🧠 1. SYSTEM-LEVEL CONTROLS
# =============================================================================

SYSTEM_GESTURES = {
    "SPOCK": GestureDefinition(
        name="SPOCK",
        emoji="🖖",
        function="activate_listening",
        category=GestureCategory.SYSTEM_CONTROL,
        gesture_type=GestureType.STATIC,
        description="Split fingers - Activate Listening Mode",
        mediapipe_mapping=None  # Custom detection needed
    ),
    
    "ROCK_SIGN": GestureDefinition(
        name="ROCK_SIGN",
        emoji="🤟",
        function="identify_owner",
        category=GestureCategory.SECURITY,
        gesture_type=GestureType.STATIC,
        description="Index + Pinky - Identify Owner / Vatsal Arrived",
        mediapipe_mapping="ILoveYou"
    ),
    
    "OPEN_PALM": GestureDefinition(
        name="OPEN_PALM",
        emoji="✋",
        function="pause_stop",
        category=GestureCategory.SYSTEM_CONTROL,
        gesture_type=GestureType.STATIC,
        description="Open Palm - Pause / Stop / Sleep AI",
        mediapipe_mapping="Open_Palm"
    ),
    
    "FIST": GestureDefinition(
        name="FIST",
        emoji="👊",
        function="wake_resume",
        category=GestureCategory.SYSTEM_CONTROL,
        gesture_type=GestureType.STATIC,
        description="Fist - Wake / Resume AI",
        mediapipe_mapping="Closed_Fist"
    ),
    
    "HEART_HANDS": GestureDefinition(
        name="HEART_HANDS",
        emoji="🫶",
        function="acknowledge",
        category=GestureCategory.INTERACTION,
        gesture_type=GestureType.STATIC,
        description="Heart shape - Acknowledge / Thank You",
        mediapipe_mapping=None  # Custom detection needed
    ),
}

# =============================================================================
# 🧩 2. INTERACTION & COMMAND CONTROL
# =============================================================================

INTERACTION_GESTURES = {
    "ONE_FINGER_UP": GestureDefinition(
        name="ONE_FINGER_UP",
        emoji="👆",
        function="cursor_control",
        category=GestureCategory.INTERACTION,
        gesture_type=GestureType.STATIC,
        description="One finger pointing up - Cursor/Selection mode",
        mediapipe_mapping="Pointing_Up"
    ),
    
    "TWO_FINGERS_UP": GestureDefinition(
        name="TWO_FINGERS_UP",
        emoji="✌️",
        function="drag_scroll",
        category=GestureCategory.INTERACTION,
        gesture_type=GestureType.STATIC,
        description="Peace sign - Drag/Scroll/Camera move",
        mediapipe_mapping="Victory"
    ),
    
    "OK_CIRCLE": GestureDefinition(
        name="OK_CIRCLE",
        emoji="👌",
        function="confirm_execute",
        category=GestureCategory.CONFIRMATION,
        gesture_type=GestureType.STATIC,
        description="Thumb + Index circle - Confirm/OK/Execute",
        mediapipe_mapping=None  # Custom detection needed
    ),
    
    "PINCH": GestureDefinition(
        name="PINCH",
        emoji="🫰",
        function="grab_zoom",
        category=GestureCategory.INTERACTION,
        gesture_type=GestureType.STATIC,
        description="Pinch gesture - Grab/Zoom/Adjust",
        mediapipe_mapping=None  # Custom detection needed
    ),
    
    "THUMBS_UP": GestureDefinition(
        name="THUMBS_UP",
        emoji="👍",
        function="approve",
        category=GestureCategory.CONFIRMATION,
        gesture_type=GestureType.STATIC,
        description="Thumbs up - Approval",
        mediapipe_mapping="Thumb_Up"
    ),
    
    "THUMBS_DOWN": GestureDefinition(
        name="THUMBS_DOWN",
        emoji="👎",
        function="reject",
        category=GestureCategory.CONFIRMATION,
        gesture_type=GestureType.STATIC,
        description="Thumbs down - Rejection",
        mediapipe_mapping="Thumb_Down"
    ),
}

# =============================================================================
# 🧭 3. GESTURE COMBINATIONS (Sequential)
# =============================================================================

COMBINATION_GESTURES = {
    "VOICE_MODE_ON": {
        "sequence": ["SPOCK", "OPEN_PALM"],
        "function": "enable_voice_mode",
        "description": "Spock → Open Palm: Voice Mode ON",
        "timeout": 3.0  # Max time between gestures
    },
    
    "RESET_INTERFACE": {
        "sequence": ["OPEN_PALM", "FIST"],
        "function": "reset_interface",
        "description": "Open Palm → Fist: Reset/Reboot Interface",
        "timeout": 3.0
    },
    
    "VATSAL_LOGIN": {
        "sequence": ["ROCK_SIGN", "ROCK_SIGN"],
        "function": "vatsal_verified_login",
        "description": "Rock Sign (both hands): Vatsal Login",
        "timeout": 2.0,
        "require_simultaneous": True
    },
    
    "COMMAND_CHAIN_MODE": {
        "sequence": ["OK_CIRCLE", "SPOCK"],
        "function": "enable_command_chain",
        "description": "OK → Spock: Multi-step command mode",
        "timeout": 3.0
    },
    
    "SAVE_CONTEXT": {
        "sequence": ["FIST", "OK_CIRCLE"],
        "function": "save_checkpoint",
        "description": "Fist → OK: Save current context",
        "timeout": 3.0
    },
    
    "SYSTEM_SHUTDOWN": {
        "sequence": ["OPEN_PALM", "OPEN_PALM"],
        "function": "shutdown",
        "description": "Open Palm (two hands): System Shutdown",
        "timeout": 2.0,
        "require_simultaneous": True
    },
}

# =============================================================================
# ⚙️ 4. DYNAMIC GESTURES (Motion + Gesture)
# =============================================================================

DYNAMIC_GESTURES = {
    "SWIPE_NEXT": {
        "gesture": "OPEN_PALM",
        "motion": "left_to_right",
        "function": "next_page",
        "description": "Open palm swipe left→right: Next page",
        "min_movement": 100  # pixels
    },
    
    "SWIPE_PREVIOUS": {
        "gesture": "OPEN_PALM",
        "motion": "right_to_left",
        "function": "previous_page",
        "description": "Open palm swipe right→left: Previous page",
        "min_movement": 100
    },
    
    "VOLUME_UP": {
        "gesture": "OPEN_PALM",
        "motion": "downward_to_upward",
        "function": "increase_volume",
        "description": "Open palm move up: Increase volume/brightness",
        "min_movement": 80
    },
    
    "VOLUME_DOWN": {
        "gesture": "OPEN_PALM",
        "motion": "upward_to_downward",
        "function": "decrease_volume",
        "description": "Open palm move down: Decrease volume/brightness",
        "min_movement": 80
    },
    
    "LOADING_LOOP": {
        "gesture": "ONE_FINGER_UP",
        "motion": "circular",
        "function": "show_processing",
        "description": "Finger move in circle: Loading/Processing",
        "min_movement": 50
    },
    
    "EXECUTE_STRONG": {
        "gesture": "FIST",
        "motion": "double_punch",
        "function": "confirm_strong_command",
        "description": "Double fist punch forward: Strong Execute",
        "min_movement": 50,
        "repetitions": 2
    },
}

# =============================================================================
# 🔮 5. FACIAL + GESTURE FUSION
# =============================================================================

FACIAL_FUSION_GESTURES = {
    "PERSONAL_LOGIN": {
        "face_required": True,
        "face_recognized": True,
        "gesture": "ROCK_SIGN",
        "function": "personal_login",
        "description": "Face recognized + Rock Sign: Personal login"
    },
    
    "SECURITY_LOCKDOWN": {
        "face_required": True,
        "face_recognized": False,
        "gesture": "OPEN_PALM",
        "function": "security_lockdown",
        "description": "Unknown face + Open Palm: Security lockdown"
    },
    
    "SECRET_COMMAND": {
        "face_required": True,
        "facial_expression": "wink",
        "gesture": "OK_CIRCLE",
        "function": "trigger_easter_egg",
        "description": "Wink + OK: Secret command (Easter Egg)"
    },
    
    "FRIENDLY_ACKNOWLEDGE": {
        "face_required": True,
        "facial_expression": "smile",
        "gesture": "FIST",
        "function": "friendly_acknowledgment",
        "description": "Smile + Fist: AI friendly acknowledgment"
    },
}

# =============================================================================
# GESTURE MAPPINGS & UTILITIES
# =============================================================================

def get_all_static_gestures() -> Dict[str, GestureDefinition]:
    """Get all static gestures"""
    all_gestures = {}
    all_gestures.update(SYSTEM_GESTURES)
    all_gestures.update(INTERACTION_GESTURES)
    return all_gestures


def get_mediapipe_gesture_map() -> Dict[str, str]:
    """Get mapping from MediaPipe gesture names to VATSAL gesture names"""
    mapping = {}
    for gesture_name, gesture_def in get_all_static_gestures().items():
        if gesture_def.mediapipe_mapping:
            mapping[gesture_def.mediapipe_mapping] = gesture_name
    return mapping


def get_gesture_by_function(function: str) -> Optional[GestureDefinition]:
    """Find gesture by its function"""
    for gesture_def in get_all_static_gestures().values():
        if gesture_def.function == function:
            return gesture_def
    return None


def get_gesture_emoji(gesture_name: str) -> str:
    """Get emoji for a gesture"""
    all_gestures = get_all_static_gestures()
    if gesture_name in all_gestures:
        return all_gestures[gesture_name].emoji
    return "🤷"


# =============================================================================
# GESTURE ACTION HANDLERS
# =============================================================================

class GestureActionHandler:
    """Handles actions triggered by gestures"""
    
    def __init__(self, voice_commander=None, gui_app=None):
        self.voice_commander = voice_commander
        self.gui_app = gui_app
        self.is_paused = False
        self.command_chain_mode = False
    
    def handle_gesture_action(self, function: str, **kwargs):
        """Execute action based on gesture function"""
        handler_map = {
            # System controls
            "activate_listening": self.activate_listening,
            "identify_owner": self.identify_owner,
            "pause_stop": self.pause_stop,
            "wake_resume": self.wake_resume,
            "acknowledge": self.acknowledge,
            
            # Interactions
            "cursor_control": self.cursor_control,
            "drag_scroll": self.drag_scroll,
            "confirm_execute": self.confirm_execute,
            "grab_zoom": self.grab_zoom,
            "approve": self.approve,
            "reject": self.reject,
            
            # Combinations
            "enable_voice_mode": self.enable_voice_mode,
            "reset_interface": self.reset_interface,
            "vatsal_verified_login": self.vatsal_verified_login,
            "enable_command_chain": self.enable_command_chain,
            "save_checkpoint": self.save_checkpoint,
            "shutdown": self.shutdown,
            
            # Dynamic
            "next_page": self.next_page,
            "previous_page": self.previous_page,
            "increase_volume": self.increase_volume,
            "decrease_volume": self.decrease_volume,
            "show_processing": self.show_processing,
            "confirm_strong_command": self.confirm_strong_command,
        }
        
        handler = handler_map.get(function)
        if handler:
            return handler(**kwargs)
        else:
            print(f"⚠️  No handler for function: {function}")
    
    # System Control Handlers
    def activate_listening(self, **kwargs):
        """Activate voice listening mode"""
        print("🖖 Spock gesture detected - Activating listening mode...")
        if self.voice_commander:
            self.voice_commander.speak("Listening mode activated")
            # Trigger voice listening
        return {"action": "listening_activated", "success": True}
    
    def identify_owner(self, **kwargs):
        """Identify owner / Vatsal arrived"""
        print("🤟 Rock sign detected - Vatsal identified!")
        if self.voice_commander:
            self.voice_commander.speak("Welcome Vatsal, supreme leader!")
        return {"action": "owner_identified", "success": True}
    
    def pause_stop(self, **kwargs):
        """Pause/stop AI"""
        print("✋ Open palm detected - Pausing AI...")
        self.is_paused = True
        if self.voice_commander:
            self.voice_commander.speak("Pausing")
        return {"action": "paused", "success": True}
    
    def wake_resume(self, **kwargs):
        """Wake/resume AI"""
        print("👊 Fist detected - Resuming AI...")
        self.is_paused = False
        if self.voice_commander:
            self.voice_commander.speak("Resuming")
        return {"action": "resumed", "success": True}
    
    def acknowledge(self, **kwargs):
        """Acknowledge / thank you"""
        print("🫶 Heart hands detected - Acknowledgment received!")
        if self.voice_commander:
            self.voice_commander.speak("You're welcome!")
        return {"action": "acknowledged", "success": True}
    
    # Interaction Handlers
    def cursor_control(self, **kwargs):
        """Enable cursor control mode"""
        print("👆 One finger up - Cursor control mode")
        return {"action": "cursor_mode", "success": True}
    
    def drag_scroll(self, **kwargs):
        """Enable drag/scroll mode"""
        print("✌️ Two fingers - Drag/scroll mode")
        return {"action": "drag_mode", "success": True}
    
    def confirm_execute(self, **kwargs):
        """Confirm/execute command"""
        print("👌 OK gesture - Confirming/executing")
        return {"action": "confirmed", "success": True}
    
    def grab_zoom(self, **kwargs):
        """Grab/zoom action"""
        print("🫰 Pinch gesture - Grab/zoom")
        return {"action": "grabbed", "success": True}
    
    def approve(self, **kwargs):
        """Approve action"""
        print("👍 Thumbs up - Approved!")
        if self.voice_commander:
            self.voice_commander.speak("Approved")
        return {"action": "approved", "success": True}
    
    def reject(self, **kwargs):
        """Reject action"""
        print("👎 Thumbs down - Rejected")
        if self.voice_commander:
            self.voice_commander.speak("Rejected")
        return {"action": "rejected", "success": True}
    
    # Combination Handlers
    def enable_voice_mode(self, **kwargs):
        """Enable voice mode"""
        print("🖖✋ Voice mode enabled!")
        return {"action": "voice_mode_enabled", "success": True}
    
    def reset_interface(self, **kwargs):
        """Reset/reboot interface"""
        print("✋👊 Resetting interface...")
        return {"action": "interface_reset", "success": True}
    
    def vatsal_verified_login(self, **kwargs):
        """Vatsal verified login"""
        print("🤟🤟 Vatsal verified login - Both hands detected!")
        if self.voice_commander:
            self.voice_commander.speak("Supreme leader verified. Full access granted.")
        return {"action": "vatsal_login", "success": True}
    
    def enable_command_chain(self, **kwargs):
        """Enable command chain mode"""
        print("👌🖖 Command chain mode enabled")
        self.command_chain_mode = True
        return {"action": "command_chain_enabled", "success": True}
    
    def save_checkpoint(self, **kwargs):
        """Save current context/checkpoint"""
        print("👊👌 Saving checkpoint...")
        return {"action": "checkpoint_saved", "success": True}
    
    def shutdown(self, **kwargs):
        """System shutdown"""
        print("✋✋ System shutdown initiated (both hands)")
        if self.voice_commander:
            self.voice_commander.speak("Shutting down")
        return {"action": "shutdown", "success": True}
    
    # Dynamic Gesture Handlers
    def next_page(self, **kwargs):
        """Next page/swipe right"""
        print("➡️ Swipe next")
        return {"action": "next_page", "success": True}
    
    def previous_page(self, **kwargs):
        """Previous page/swipe left"""
        print("⬅️ Swipe previous")
        return {"action": "previous_page", "success": True}
    
    def increase_volume(self, **kwargs):
        """Increase volume/brightness"""
        print("⬆️ Increasing volume")
        return {"action": "volume_up", "success": True}
    
    def decrease_volume(self, **kwargs):
        """Decrease volume/brightness"""
        print("⬇️ Decreasing volume")
        return {"action": "volume_down", "success": True}
    
    def show_processing(self, **kwargs):
        """Show processing/loading"""
        print("🔄 Processing...")
        return {"action": "processing", "success": True}
    
    def confirm_strong_command(self, **kwargs):
        """Strong confirmation (double punch)"""
        print("👊👊 Strong confirmation!")
        return {"action": "strong_confirm", "success": True}
