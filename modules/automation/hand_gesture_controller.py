"""
Hand Gesture Mouse Controller
Control your mouse using hand gestures via webcam
"""

import time
import numpy as np
from typing import Dict, List, Optional, Tuple, Any

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    cv2 = None

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    mp = None

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except Exception:
    # Catch all exceptions including Xlib.error.XauthError in headless environments
    PYAUTOGUI_AVAILABLE = False
    pyautogui = None


class HandGestureController:
    """Control mouse and system with hand gestures using webcam"""
    
    def __init__(self):
        self.cv2_available = CV2_AVAILABLE
        self.mediapipe_available = MEDIAPIPE_AVAILABLE
        self.pyautogui_available = PYAUTOGUI_AVAILABLE
        
        self.cap = None
        self.hands = None
        self.mp_hands = None
        self.mp_drawing = None
        
        self.running = False
        self.screen_width = 1920
        self.screen_height = 1080
        
        self.prev_x = 0
        self.prev_y = 0
        self.smoothing = 5
        
        self.click_cooldown = 0
        self.cooldown_frames = 10
        
        self.gesture_mode = "cursor"
        
        self.stats = {
            "total_gestures": 0,
            "clicks": 0,
            "scrolls": 0,
            "drags": 0
        }
    
    def check_dependencies(self) -> Dict[str, bool]:
        """Check which dependencies are available"""
        return {
            'opencv': self.cv2_available,
            'mediapipe': self.mediapipe_available,
            'pyautogui': self.pyautogui_available
        }
    
    def get_missing_dependencies_message(self) -> str:
        """Get helpful message about missing dependencies"""
        deps = self.check_dependencies()
        missing = [name for name, available in deps.items() if not available]
        
        if not missing:
            return ""
        
        install_commands = {
            'opencv': 'pip install opencv-python',
            'mediapipe': 'pip install mediapipe',
            'pyautogui': 'pip install pyautogui'
        }
        
        msg = f"Missing required dependencies: {', '.join(missing)}\n"
        msg += "Install all with:\n"
        msg += "  pip install opencv-python mediapipe pyautogui numpy\n"
        
        return msg
    
    def initialize(self, camera_id: int = 0, detection_confidence: float = 0.7, 
                   tracking_confidence: float = 0.7) -> Dict:
        """Initialize the hand gesture controller"""
        if not all([self.cv2_available, self.mediapipe_available, self.pyautogui_available]):
            return {
                "success": False,
                "error": "Missing dependencies",
                "help": self.get_missing_dependencies_message()
            }
        
        try:
            self.mp_hands = mp.solutions.hands
            self.mp_drawing = mp.solutions.drawing_utils
            
            self.hands = self.mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=1,
                model_complexity=1,
                min_detection_confidence=detection_confidence,
                min_tracking_confidence=tracking_confidence
            )
            
            self.cap = cv2.VideoCapture(camera_id)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            if not self.cap.isOpened():
                return {
                    "success": False,
                    "error": "Cannot access webcam",
                    "help": "Make sure your webcam is connected and not in use by another application"
                }
            
            self.screen_width, self.screen_height = pyautogui.size()
            
            pyautogui.FAILSAFE = False
            
            return {
                "success": True,
                "message": "Hand gesture controller initialized",
                "screen_size": f"{self.screen_width}x{self.screen_height}",
                "camera": f"Camera {camera_id} opened successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Initialization failed: {str(e)}"
            }
    
    def count_fingers(self, hand_landmarks) -> int:
        """Count how many fingers are extended"""
        if not hand_landmarks:
            return 0
        
        fingers = []
        landmarks = hand_landmarks.landmark
        
        if landmarks[4].x < landmarks[3].x:
            fingers.append(1)
        else:
            fingers.append(0)
        
        finger_tips = [8, 12, 16, 20]
        finger_pips = [6, 10, 14, 18]
        
        for tip, pip in zip(finger_tips, finger_pips):
            if landmarks[tip].y < landmarks[pip].y:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return sum(fingers)
    
    def get_finger_status(self, hand_landmarks) -> List[int]:
        """Get status of each finger (0=down, 1=up)"""
        if not hand_landmarks:
            return [0, 0, 0, 0, 0]
        
        fingers = []
        landmarks = hand_landmarks.landmark
        
        if landmarks[4].x < landmarks[3].x:
            fingers.append(1)
        else:
            fingers.append(0)
        
        finger_tips = [8, 12, 16, 20]
        finger_pips = [6, 10, 14, 18]
        
        for tip, pip in zip(finger_tips, finger_pips):
            if landmarks[tip].y < landmarks[pip].y:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers
    
    def calculate_distance(self, point1, point2) -> float:
        """Calculate distance between two landmarks"""
        return np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2 + (point1.z - point2.z)**2)
    
    def process_cursor_gesture(self, hand_landmarks, frame) -> str:
        """Process cursor movement gestures"""
        landmarks = hand_landmarks.landmark
        index_tip = landmarks[8]
        thumb_tip = landmarks[4]
        
        frame_height, frame_width, _ = frame.shape
        
        index_x = int(index_tip.x * frame_width)
        index_y = int(index_tip.y * frame_height)
        
        screen_x = np.interp(index_x, [100, frame_width - 100], [0, self.screen_width])
        screen_y = np.interp(index_y, [100, frame_height - 100], [0, self.screen_height])
        
        cursor_x = self.prev_x + (screen_x - self.prev_x) / self.smoothing
        cursor_y = self.prev_y + (screen_y - self.prev_y) / self.smoothing
        self.prev_x, self.prev_y = cursor_x, cursor_y
        
        pyautogui.moveTo(cursor_x, cursor_y)
        
        distance = self.calculate_distance(index_tip, thumb_tip)
        
        if distance < 0.05 and self.click_cooldown == 0:
            pyautogui.click()
            self.click_cooldown = self.cooldown_frames
            self.stats["clicks"] += 1
            return "Click"
        
        if self.click_cooldown > 0:
            self.click_cooldown -= 1
        
        return "Moving"
    
    def process_scroll_gesture(self, hand_landmarks, prev_y_pos) -> Tuple[str, float]:
        """Process scroll gestures"""
        landmarks = hand_landmarks.landmark
        index_tip = landmarks[8]
        
        current_y = index_tip.y
        
        if prev_y_pos is not None:
            diff = prev_y_pos - current_y
            
            if abs(diff) > 0.02:
                scroll_amount = int(diff * 300)
                pyautogui.scroll(scroll_amount)
                self.stats["scrolls"] += 1
                return f"Scroll {'Up' if scroll_amount > 0 else 'Down'}", current_y
        
        return "Scroll Mode", current_y
    
    def process_volume_gesture(self, hand_landmarks) -> str:
        """Process volume control gestures"""
        landmarks = hand_landmarks.landmark
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        
        distance = self.calculate_distance(thumb_tip, index_tip)
        
        volume_level = int(np.interp(distance, [0.02, 0.2], [0, 100]))
        
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            
            vol_db = np.interp(volume_level, [0, 100], [-65, 0])
            volume.SetMasterVolumeLevel(vol_db, None)
            
            return f"Volume: {volume_level}%"
        except:
            return "Volume Control (pycaw not installed)"
    
    def recognize_gesture(self, fingers: List[int]) -> str:
        """Recognize specific gestures based on finger positions"""
        if fingers == [0, 1, 0, 0, 0]:
            return "cursor"
        elif fingers == [0, 1, 1, 0, 0]:
            return "cursor"
        elif fingers == [1, 1, 1, 1, 1]:
            return "scroll"
        elif fingers == [1, 1, 0, 0, 0]:
            return "volume"
        elif fingers == [0, 0, 0, 0, 0]:
            return "drag"
        elif fingers == [0, 0, 0, 0, 1]:
            return "right_click"
        else:
            return "cursor"
    
    def start(self, show_video: bool = True) -> Dict:
        """Start the hand gesture controller"""
        if not self.hands or not self.cap:
            init_result = self.initialize()
            if not init_result["success"]:
                return init_result
        
        self.running = True
        prev_scroll_y = None
        
        print("=" * 60)
        print("HAND GESTURE MOUSE CONTROLLER")
        print("=" * 60)
        print("\n✋ Gestures:")
        print("  • Index finger up           → Move cursor")
        print("  • Index + Middle up         → Move cursor")
        print("  • Pinch (Index + Thumb)     → Left click")
        print("  • All fingers up            → Scroll mode")
        print("  • Thumb + Index up          → Volume control")
        print("  • Closed fist               → Drag mode")
        print("  • Pinky finger only         → Right click")
        print("\n⌨️  Controls:")
        print("  • Press 'q' to quit")
        print("  • Press 's' to toggle stats")
        print("=" * 60)
        
        show_stats = False
        
        try:
            while self.running:
                success, frame = self.cap.read()
                if not success:
                    break
                
                frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                results = self.hands.process(frame_rgb)
                
                gesture_text = "No Hand Detected"
                
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        if show_video:
                            self.mp_drawing.draw_landmarks(
                                frame,
                                hand_landmarks,
                                self.mp_hands.HAND_CONNECTIONS
                            )
                        
                        fingers = self.get_finger_status(hand_landmarks)
                        gesture_mode = self.recognize_gesture(fingers)
                        
                        if gesture_mode == "cursor":
                            gesture_text = self.process_cursor_gesture(hand_landmarks, frame)
                        elif gesture_mode == "scroll":
                            gesture_text, prev_scroll_y = self.process_scroll_gesture(hand_landmarks, prev_scroll_y)
                        elif gesture_mode == "volume":
                            gesture_text = self.process_volume_gesture(hand_landmarks)
                        elif gesture_mode == "drag":
                            pyautogui.mouseDown()
                            gesture_text = "Dragging"
                            self.stats["drags"] += 1
                        elif gesture_mode == "right_click":
                            if self.click_cooldown == 0:
                                pyautogui.rightClick()
                                self.click_cooldown = self.cooldown_frames
                                self.stats["clicks"] += 1
                            gesture_text = "Right Click"
                        
                        self.stats["total_gestures"] += 1
                else:
                    pyautogui.mouseUp()
                
                if show_video:
                    cv2.putText(frame, gesture_text, (10, 50),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    cv2.putText(frame, f"Mode: {gesture_mode.upper()}", (10, 90),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                    
                    if show_stats:
                        y_offset = 130
                        for key, value in self.stats.items():
                            cv2.putText(frame, f"{key}: {value}", (10, y_offset),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                            y_offset += 25
                    
                    cv2.imshow('Hand Gesture Controller', frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    show_stats = not show_stats
            
            return {
                "success": True,
                "message": "Hand gesture controller stopped",
                "stats": self.stats
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Runtime error: {str(e)}"
            }
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.running = False
        
        if self.cap:
            self.cap.release()
        
        if CV2_AVAILABLE:
            cv2.destroyAllWindows()
        
        if self.hands:
            self.hands.close()
    
    def get_stats(self) -> Dict:
        """Get gesture statistics"""
        return self.stats.copy()


if __name__ == "__main__":
    controller = HandGestureController()
    
    deps = controller.check_dependencies()
    print("\n📦 Dependency Check:")
    for dep, available in deps.items():
        status = "✓" if available else "✗"
        print(f"  {status} {dep}")
    
    if not all(deps.values()):
        print("\n" + controller.get_missing_dependencies_message())
    else:
        print("\n✅ All dependencies available!")
        print("\nStarting hand gesture controller...")
        result = controller.start(show_video=True)
        print(f"\n{result}")
