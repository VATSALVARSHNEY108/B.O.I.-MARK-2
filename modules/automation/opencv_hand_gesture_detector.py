"""
Enhanced Hand Gesture Detection using OpenCV
Works in all environments without MediaPipe dependency
"""

import cv2
import numpy as np
import threading
import time
from typing import Dict, Optional, Callable, Tuple


class OpenCVHandGestureDetector:
    """
    Hand gesture detection using pure OpenCV.
    Works everywhere without MediaPipe dependency.
    """
    
    def __init__(self, voice_commander=None):
        self.voice_commander = voice_commander
        
        # Hand detection using skin color detection
        self.lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        self.upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        # State
        self.cap = None
        self.running = False
        self.thread = None
        
        # Detection state
        self.hand_detected = False
        self.last_gesture_time = 0
        self.gesture_cooldown = 2
        self.vatsal_greeting_cooldown = 0
        
        # Callbacks
        self.on_gesture_detected_callback = None
        
        # Statistics
        self.stats = {
            'gestures_detected': 0,
            'vatsal_detected': 0,
            'open_palm_detected': 0,
            'fist_detected': 0,
            'thumbs_up_detected': 0,
            'peace_sign_detected': 0
        }
        
        # Gesture detection parameters
        self.min_hand_area = 5000
        self.max_hand_area = 50000
    
    def start(self, camera_index: int = 0) -> Dict:
        """Start gesture detection"""
        if self.running:
            return {
                'success': False,
                'message': 'Detector already running'
            }
        
        try:
            self.cap = cv2.VideoCapture(camera_index)
            if not self.cap.isOpened():
                return {
                    'success': False,
                    'message': 'Could not access camera'
                }
            
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            self.running = True
            self.thread = threading.Thread(target=self._detection_loop, daemon=True)
            self.thread.start()
            
            return {
                'success': True,
                'message': 'OpenCV Hand Gesture Detector started successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error starting detector: {str(e)}'
            }
    
    def stop(self) -> Dict:
        """Stop detection"""
        if not self.running:
            return {
                'success': False,
                'message': 'Detector not running'
            }
        
        self.running = False
        
        if self.thread:
            self.thread.join(timeout=2)
        
        if self.cap:
            self.cap.release()
        
        cv2.destroyAllWindows()
        
        return {
            'success': True,
            'message': 'Detector stopped'
        }
    
    def _detection_loop(self):
        """Main detection loop"""
        print("🎥 OpenCV Hand Gesture Detection started")
        print("👋 Show your OPEN PALM to activate listening")
        print("✊ Make a FIST to stop listening")
        print("👍 Show THUMBS UP for approval")
        print("✌️✌️  Show TWO PEACE SIGNS (both hands) for VATSAL greeting")
        
        while self.running:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    time.sleep(0.1)
                    continue
                
                frame = cv2.flip(frame, 1)
                current_time = time.time()
                
                # Detect all hand gestures in the frame
                gestures = self._detect_all_hand_gestures(frame)
                
                # Count peace signs in current frame
                peace_sign_count = sum(1 for g in gestures if g['gesture'] == "PEACE_SIGN")
                
                # Check for VATSAL greeting (two peace signs simultaneously)
                if peace_sign_count >= 2 and self.vatsal_greeting_cooldown == 0:
                    self._greet_vatsal()
                    for gesture_info in gestures:
                        if gesture_info['contour'] is not None:
                            cv2.drawContours(frame, [gesture_info['contour']], 0, (0, 255, 0), 3)
                    
                    cv2.putText(
                        frame,
                        "VATSAL DETECTED!",
                        (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.5,
                        (0, 255, 0),
                        3
                    )
                    self.hand_detected = True
                
                elif len(gestures) > 0:
                    # Process first detected gesture
                    gesture_info = gestures[0]
                    gesture = gesture_info['gesture']
                    hand_contour = gesture_info['contour']
                    
                    if gesture != "NONE":
                        self.hand_detected = True
                        
                        # Draw hand contour
                        if hand_contour is not None:
                            cv2.drawContours(frame, [hand_contour], 0, (255, 0, 255), 2)
                        
                        # Handle gestures
                        if gesture == "OPEN_PALM":
                            if current_time - self.last_gesture_time > self.gesture_cooldown:
                                self._handle_listening_gesture()
                                self.last_gesture_time = current_time
                                self.stats['open_palm_detected'] += 1
                            
                            cv2.putText(
                                frame,
                                "OPEN PALM - Listening!",
                                (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.7,
                                (0, 255, 255),
                                2
                            )
                        
                        elif gesture == "FIST":
                            self.stats['fist_detected'] += 1
                            cv2.putText(
                                frame,
                                "FIST - Stop",
                                (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.7,
                                (0, 165, 255),
                                2
                            )
                        
                        elif gesture == "THUMBS_UP":
                            self.stats['thumbs_up_detected'] += 1
                            cv2.putText(
                                frame,
                                "THUMBS UP - Good!",
                                (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.7,
                                (0, 255, 0),
                                2
                            )
                        
                        elif gesture == "PEACE_SIGN":
                            self.stats['peace_sign_detected'] += 1
                            cv2.putText(
                                frame,
                                f"PEACE SIGN ({peace_sign_count}/2 for VATSAL)",
                                (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.7,
                                (255, 255, 0),
                                2
                            )
                    else:
                        self.hand_detected = False
                else:
                    self.hand_detected = False
                
                # Decrement cooldown
                if self.vatsal_greeting_cooldown > 0:
                    self.vatsal_greeting_cooldown -= 1
                
                # Display status
                hand_status = "Hand: Detected" if self.hand_detected else "Hand: Not Detected"
                
                cv2.putText(frame, hand_status, (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                           (0, 255, 0) if self.hand_detected else (0, 0, 255), 2)
                
                # Display help
                cv2.putText(frame, "Press 'q' to quit | Show 2 peace signs for VATSAL", 
                           (10, frame.shape[0] - 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                cv2.imshow('VATSAL - OpenCV Hand Gesture Detection', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.running = False
                    break
                    
            except Exception as e:
                print(f"❌ Error in detection loop: {str(e)}")
                time.sleep(0.1)
        
        print("🛑 Detection stopped")
    
    def _detect_all_hand_gestures(self, frame) -> list:
        """
        Detect all hand gestures in the frame (for multiple hands).
        Returns: List of {'gesture': str, 'contour': np.ndarray}
        """
        try:
            # Convert to HSV for better skin detection
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Create skin mask
            mask = cv2.inRange(hsv, self.lower_skin, self.upper_skin)
            
            # Morphological operations to remove noise
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.erode(mask, kernel, iterations=1)
            mask = cv2.dilate(mask, kernel, iterations=2)
            mask = cv2.GaussianBlur(mask, (5, 5), 0)
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                return []
            
            # Analyze all valid contours
            gestures = []
            for contour in contours:
                area = cv2.contourArea(contour)
                
                # Check if area is reasonable for a hand
                if area < self.min_hand_area or area > self.max_hand_area:
                    continue
                
                # Analyze contour to determine gesture
                gesture = self._analyze_contour_gesture(contour)
                if gesture != "NONE":
                    gestures.append({'gesture': gesture, 'contour': contour})
            
            return gestures
            
        except Exception as e:
            print(f"❌ Multi-hand detection error: {str(e)}")
            return []
    
    def _analyze_contour_gesture(self, contour) -> str:
        """Analyze a single contour to determine gesture type"""
        try:
            hull = cv2.convexHull(contour, returnPoints=False)
            
            if len(hull) > 3:
                defects = cv2.convexityDefects(contour, hull)
                
                if defects is not None:
                    finger_count = 0
                    
                    for i in range(defects.shape[0]):
                        s, e, f, d = defects[i, 0]
                        start = tuple(contour[s][0])
                        end = tuple(contour[e][0])
                        far = tuple(contour[f][0])
                        
                        a = np.linalg.norm(np.array(start) - np.array(far))
                        b = np.linalg.norm(np.array(end) - np.array(far))
                        c = np.linalg.norm(np.array(start) - np.array(end))
                        
                        angle = np.arccos((a**2 + b**2 - c**2) / (2 * a * b))
                        
                        if angle <= np.pi / 2 and d > 10000:
                            finger_count += 1
                    
                    # Determine gesture based on finger count
                    if finger_count >= 4:
                        return "OPEN_PALM"
                    elif finger_count == 2 or finger_count == 3:
                        return "PEACE_SIGN"
                    elif finger_count == 1:
                        return "THUMBS_UP"
                    elif finger_count == 0:
                        return "FIST"
            
            return "NONE"
            
        except Exception as e:
            return "NONE"
    
    def _detect_hand_gesture(self, frame) -> Tuple[str, Optional[np.ndarray]]:
        """
        Detect hand gestures using skin color and contour analysis.
        Returns: (gesture_name, hand_contour)
        """
        try:
            # Convert to HSV for better skin detection
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Create skin mask
            mask = cv2.inRange(hsv, self.lower_skin, self.upper_skin)
            
            # Morphological operations to remove noise
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.erode(mask, kernel, iterations=1)
            mask = cv2.dilate(mask, kernel, iterations=2)
            mask = cv2.GaussianBlur(mask, (5, 5), 0)
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                return "NONE", None
            
            # Find largest contour (likely the hand)
            max_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(max_contour)
            
            # Check if area is reasonable for a hand
            if area < self.min_hand_area or area > self.max_hand_area:
                return "NONE", None
            
            # Analyze contour shape to determine gesture
            hull = cv2.convexHull(max_contour, returnPoints=False)
            
            if len(hull) > 3:
                defects = cv2.convexityDefects(max_contour, hull)
                
                if defects is not None:
                    # Count the number of defects (spaces between fingers)
                    finger_count = 0
                    
                    for i in range(defects.shape[0]):
                        s, e, f, d = defects[i, 0]
                        start = tuple(max_contour[s][0])
                        end = tuple(max_contour[e][0])
                        far = tuple(max_contour[f][0])
                        
                        # Calculate the angle at the defect point
                        a = np.linalg.norm(np.array(start) - np.array(far))
                        b = np.linalg.norm(np.array(end) - np.array(far))
                        c = np.linalg.norm(np.array(start) - np.array(end))
                        
                        angle = np.arccos((a**2 + b**2 - c**2) / (2 * a * b))
                        
                        # If angle is less than 90 degrees, count as finger
                        if angle <= np.pi / 2 and d > 10000:
                            finger_count += 1
                    
                    # Determine gesture based on finger count
                    if finger_count >= 4:
                        return "OPEN_PALM", max_contour
                    elif finger_count == 2 or finger_count == 3:
                        return "PEACE_SIGN", max_contour
                    elif finger_count == 1:
                        return "THUMBS_UP", max_contour
                    elif finger_count == 0:
                        return "FIST", max_contour
                    else:
                        return "PARTIAL", max_contour
            
            return "DETECTED", max_contour
            
        except Exception as e:
            print(f"❌ Gesture detection error: {str(e)}")
            return "NONE", None
    
    def _greet_vatsal(self):
        """Greet VATSAL when two peace signs are detected"""
        print("\n" + "=" * 70)
        print("👋 VATSAL DETECTED! Two peace signs shown!")
        print("🎉 Hello VATSAL! Welcome!")
        print("=" * 70 + "\n")
        
        if self.voice_commander:
            import random
            
            # Expanded greetings list with "supreme leader" style greetings
            greetings = [
                "Supreme leader, welcome!",
                "All hail the supreme leader!",
                "Welcome, supreme leader!",
                "The supreme leader has arrived!",
                "Greetings, supreme leader!",
                "Hello Vatsal! Both hands up!",
                "Welcome Vatsal!",
                "Greetings Vatsal! I see you!",
                "At your service, supreme leader!",
                "Your loyal servant reporting, supreme leader!",
                "The boss is in the house!",
                "Master has arrived!",
                "Welcome back, supreme commander!"
            ]
            
            # Select a random greeting, avoiding the last one if possible
            if not hasattr(self, 'last_greeting'):
                self.last_greeting = None
            
            # Try to pick a different greeting than last time
            available_greetings = [g for g in greetings if g != self.last_greeting]
            if not available_greetings:
                available_greetings = greetings
            
            greeting = random.choice(available_greetings)
            self.last_greeting = greeting
            
            self.voice_commander.speak(greeting)
        
        self.stats['vatsal_detected'] += 1
        self.vatsal_greeting_cooldown = 100
    
    def _handle_listening_gesture(self):
        """Handle the listening activation gesture"""
        print("✋ Listening gesture detected!")
        self.stats['gestures_detected'] += 1
        
        if self.voice_commander:
            self.voice_commander.speak("I'm listening")
            time.sleep(0.5)
            
            result = self.voice_commander.listen_once(timeout=5)
            
            if result and result.get('success'):
                command = result.get('text', '').strip()
                if command:
                    print(f"🎤 Voice command received: {command}")
                    
                    if self.on_gesture_detected_callback:
                        self.on_gesture_detected_callback(command)
                else:
                    self.voice_commander.speak("I didn't catch that")
            else:
                self.voice_commander.speak("Sorry, I couldn't hear you")
    
    def set_gesture_callback(self, callback: Callable):
        """Set callback for gesture detection"""
        self.on_gesture_detected_callback = callback
    
    def get_stats(self) -> Dict:
        """Get detection statistics"""
        return self.stats.copy()
    
    def is_running(self) -> bool:
        """Check if detector is running"""
        return self.running
