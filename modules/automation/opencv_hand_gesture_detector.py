"""
Enhanced Hand Gesture Detection using OpenCV
Works in all environments without MediaPipe dependency
"""

import cv2
import numpy as np
import threading
import time
from typing import Dict, Optional, Callable, Tuple
import os
from modules.automation.audio_feedback import get_audio_feedback


class OpenCVHandGestureDetector:
    """
    Hand gesture detection using pure OpenCV.
    Works everywhere without MediaPipe dependency.
    Supports both hardcoded gestures and custom trained gestures.
    """
    
    def __init__(self, voice_commander=None, use_trained_model: bool = True, use_mediapipe: bool = True):
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
            'peace_sign_detected': 0,
            'custom_gestures_detected': 0,
            'mediapipe_gestures_detected': 0
        }
        
        # Gesture detection parameters
        self.min_hand_area = 5000
        self.max_hand_area = 50000
        
        # MediaPipe pretrained model support
        self.use_mediapipe = use_mediapipe
        self.mediapipe_recognizer = None
        
        # Custom trained model support
        self.use_trained_model = use_trained_model
        self.gesture_trainer = None
        self.min_confidence = 0.6
        
        # Load MediaPipe pretrained model
        if self.use_mediapipe:
            self._load_mediapipe_model()
        
        # Load custom trained model if enabled
        if self.use_trained_model:
            self._load_trained_model()
        
        # Print comprehensive gesture availability summary
        self._print_gesture_summary()
    
    def _load_mediapipe_model(self):
        """Load Google MediaPipe pretrained gesture model"""
        try:
            import importlib.util
            
            # Check if mediapipe is actually installed and functional
            mediapipe_spec = importlib.util.find_spec("mediapipe")
            if mediapipe_spec is None:
                print("ℹ️  MediaPipe not installed (optional - using fallback methods)")
                self.mediapipe_recognizer = None
                return
            
            # Try to import MediaPipe
            try:
                import mediapipe as mp
            except Exception as mp_error:
                print(f"ℹ️  MediaPipe unavailable in this environment: {str(mp_error)[:60]}")
                print("   Using hardcoded + custom trained gestures instead")
                self.mediapipe_recognizer = None
                return
            
            # MediaPipe is available, try to load recognizer
            from modules.automation.mediapipe_gesture_recognizer import MediaPipeGestureRecognizer
            
            self.mediapipe_recognizer = MediaPipeGestureRecognizer()
            
            if self.mediapipe_recognizer.is_available():
                print("✅ MediaPipe pretrained model loaded")
                print(f"   Gestures: {self.mediapipe_recognizer.list_available_gestures()}")
            else:
                print("⚠️  MediaPipe model file not found, will use other methods")
                self.mediapipe_recognizer = None
        except Exception as e:
            print(f"ℹ️  MediaPipe unavailable: {str(e)[:60]}")
            print("   Using hardcoded + custom trained gestures")
            self.mediapipe_recognizer = None
    
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
        
        # Create window and set it to a specific size and position
        window_name = 'VATSAL - Hand Gesture'
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 320, 240)  # Small size: 320x240
        cv2.moveWindow(window_name, 0, 0)  # Top-left corner position
        
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
                            # Custom gesture detected by ML model
                            self.stats['custom_gestures_detected'] += 1
                            confidence = gesture_info.get('confidence', 0.0)
                            cv2.putText(
                                frame,
                                f"{gesture} ({confidence*100:.1f}%)",
                                (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.7,
                                (255, 0, 255),
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
                
                # Resize frame to smaller size for compact display
                display_frame = cv2.resize(frame, (320, 240))
                cv2.imshow(window_name, display_frame)
                
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
        Returns: List of {'gesture': str, 'contour': np.ndarray, 'confidence': float}
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
            
            # Analyze all valid contours
            gestures = []
            
            if contours:
                for contour in contours:
                    area = cv2.contourArea(contour)
                    
                    # Check if area is reasonable for a hand
                    if area < self.min_hand_area or area > self.max_hand_area:
                        continue
                    
                    # Try hybrid detection (ML + hardcoded)
                    gesture, confidence = self._analyze_contour_with_hybrid(frame, contour)
                    if gesture != "NONE":
                        gestures.append({
                            'gesture': gesture, 
                            'contour': contour,
                            'confidence': confidence
                        })
            
            # FALLBACK: If no contours found, try MediaPipe on full frame
            # This ensures gestures work even without reliable skin detection
            if not gestures and self.mediapipe_recognizer is not None:
                gesture, confidence = self.mediapipe_recognizer.recognize(frame)
                if gesture is not None and confidence >= self.min_confidence:
                    self.stats['mediapipe_gestures_detected'] += 1
                    gestures.append({
                        'gesture': gesture,
                        'contour': None,  # No contour available
                        'confidence': confidence
                    })
            
            return gestures
            
        except Exception as e:
            print(f"❌ Multi-hand detection error: {str(e)}")
            return []
    
    def _analyze_contour_with_hybrid(self, frame, contour) -> Tuple[str, float]:
        """
        Analyze contour using hybrid approach with 3 detection methods:
        1. MediaPipe pretrained (7 gestures, no training needed)
        2. Custom ML (user-trained gestures)  
        3. Hardcoded finger-counting (fallback)
        """
        try:
            # Get bounding box for this contour
            x, y, w, h = cv2.boundingRect(contour)
            
            # Add padding
            padding = 20
            x = max(0, x - padding)
            y = max(0, y - padding)
            w = min(frame.shape[1] - x, w + 2 * padding)
            h = min(frame.shape[0] - y, h + 2 * padding)
            
            # Extract ROI
            roi = frame[y:y+h, x:x+w]
            
            # 1. Try MediaPipe pretrained model first (best accuracy)
            if self.mediapipe_recognizer is not None:
                gesture, confidence = self.mediapipe_recognizer.recognize(roi)
                if gesture is not None and confidence >= self.min_confidence:
                    self.stats['mediapipe_gestures_detected'] += 1
                    return gesture, confidence
            
            # 2. Try custom ML classification
            if self.gesture_trainer is not None:
                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                normalized_roi = cv2.resize(gray_roi, (128, 128))
                normalized_roi = cv2.equalizeHist(normalized_roi)
                
                ml_gesture, confidence = self._classify_gesture_ml(normalized_roi)
                
                if ml_gesture != "UNKNOWN" and confidence >= self.min_confidence:
                    return ml_gesture, confidence
            
            # 3. Fall back to finger counting
            hardcoded_gesture = self._analyze_contour_gesture(contour)
            return hardcoded_gesture, 1.0
            
        except Exception as e:
            # Final fallback
            return self._analyze_contour_gesture(contour), 1.0
    
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
        
        # Play audio signal when listening starts
        audio = get_audio_feedback()
        audio.play_listening_start()
        
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
    
    def _load_trained_model(self):
        """Load trained gesture model if available"""
        try:
            from modules.automation.gesture_trainer import GestureTrainer
            import os
            
            self.gesture_trainer = GestureTrainer()
            
            model_path = self.gesture_trainer.model_path
            scaler_path = self.gesture_trainer.scaler_path
            labels_path = self.gesture_trainer.labels_path
            
            if self.gesture_trainer.load_model():
                print(f"✅ Loaded trained gesture model with {len(self.gesture_trainer.labels)} custom gestures")
                print(f"   Custom gestures: {list(self.gesture_trainer.labels.keys())}")
                print(f"   Model path: {model_path}")
            else:
                print("\n" + "=" * 70)
                print("⚠️  CUSTOM TRAINED GESTURES NOT FOUND")
                print("=" * 70)
                print(f"   Expected model files at:")
                print(f"   - {model_path}")
                print(f"   - {scaler_path}")
                print(f"   - {labels_path}")
                print()
                
                missing_files = []
                if not os.path.exists(model_path):
                    missing_files.append("gesture_model.pkl")
                if not os.path.exists(scaler_path):
                    missing_files.append("gesture_scaler.pkl")
                if not os.path.exists(labels_path):
                    missing_files.append("gesture_labels.pkl")
                
                if missing_files:
                    print(f"   Missing files: {', '.join(missing_files)}")
                print()
                print("   📝 To train custom gestures:")
                print("      1. Run: python train_hand_gestures.py")
                print("      2. Capture samples for each gesture (50+ recommended)")
                print("      3. Train the model")
                print("      4. Restart the gesture detector")
                print()
                print("   ℹ️  Currently using:")
                if self.mediapipe_recognizer:
                    print("      ✅ MediaPipe pretrained gestures (7 gestures)")
                print("      ✅ Hardcoded finger-counting gestures")
                print("=" * 70 + "\n")
                self.gesture_trainer = None
        except Exception as e:
            print(f"⚠️  Could not load trained model: {e}")
            self.gesture_trainer = None
    
    def _print_gesture_summary(self):
        """Print comprehensive summary of available gesture types"""
        print("\n" + "=" * 70)
        print("🎯 GESTURE DETECTION SYSTEM - AVAILABLE GESTURES")
        print("=" * 70)
        
        total_gestures = 0
        
        # MediaPipe pretrained gestures
        if self.mediapipe_recognizer:
            mediapipe_gestures = self.mediapipe_recognizer.list_available_gestures()
            print(f"\n📱 MediaPipe Pretrained Gestures ({len(mediapipe_gestures)} gestures):")
            print("   ✅ NO TRAINING REQUIRED - Works instantly!")
            for gesture in mediapipe_gestures:
                print(f"   • {gesture}")
            total_gestures += len(mediapipe_gestures)
        else:
            # MediaPipe not available, show what it would support
            mediapipe_gestures = ["FIST", "OPEN_PALM", "ONE_FINGER_UP", "THUMBS_DOWN", 
                                  "THUMBS_UP", "PEACE_SIGN", "ROCK_SIGN", "SPOCK", "OK_CIRCLE", "PINCH"]
            print(f"\n📱 MediaPipe Pretrained Gestures ({len(mediapipe_gestures)} gestures):")
            print("   ⚠️  MediaPipe not available in cloud environment")
            print("   ℹ️  Install MediaPipe on local machine for instant gesture recognition")
            print("   📋 Supported gestures:")
            for gesture in mediapipe_gestures:
                print(f"      • {gesture}")
        
        # Custom trained gestures
        if self.gesture_trainer and self.gesture_trainer.classifier:
            custom_gestures = list(self.gesture_trainer.labels.keys())
            print(f"\n🎓 Custom Trained Gestures ({len(custom_gestures)} gestures):")
            print("   ✅ User-trained ML model loaded")
            for gesture in custom_gestures:
                print(f"   • {gesture}")
            total_gestures += len(custom_gestures)
        else:
            print(f"\n🎓 Custom Trained Gestures:")
            print("   ❌ NOT CONFIGURED")
            print("   ℹ️  Run 'python train_hand_gestures.py' on local machine to train")
            print("   📝 Recommended: Train 10+ custom gestures for best accuracy")
        
        # Hardcoded finger-counting gestures
        hardcoded_gestures = ["OPEN_PALM", "FIST", "PEACE_SIGN", "THUMBS_UP"]
        print(f"\n👆 Hardcoded Finger-Counting Gestures ({len(hardcoded_gestures)} gestures):")
        print("   ✅ Always available (fallback method)")
        for gesture in hardcoded_gestures:
            print(f"   • {gesture}")
        total_gestures += len(hardcoded_gestures)
        
        print(f"\n📊 Total Configured Gestures: {total_gestures if self.gesture_trainer else len(hardcoded_gestures)}")
        if not self.mediapipe_recognizer:
            print("\n💡 Note: This is a cloud environment without camera access.")
            print("   Deploy to local machine with webcam for full gesture recognition.")
        print("=" * 70 + "\n")
    
    def _detect_hand_roi(self, frame) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
        """
        Detect hand and return normalized 128x128 ROI for ML model
        
        Returns:
            Tuple of (hand_roi as 128x128 grayscale, hand_contour)
        """
        try:
            # Convert to HSV for skin detection
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Create skin mask
            mask = cv2.inRange(hsv, self.lower_skin, self.upper_skin)
            
            # Morphological operations
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.erode(mask, kernel, iterations=1)
            mask = cv2.dilate(mask, kernel, iterations=2)
            mask = cv2.GaussianBlur(mask, (5, 5), 0)
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                return None, None
            
            # Get largest contour
            max_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(max_contour)
            
            # Check reasonable hand size
            if area < self.min_hand_area or area > self.max_hand_area:
                return None, None
            
            # Get bounding box and extract ROI
            x, y, w, h = cv2.boundingRect(max_contour)
            
            # Add padding
            padding = 20
            x = max(0, x - padding)
            y = max(0, y - padding)
            w = min(frame.shape[1] - x, w + 2 * padding)
            h = min(frame.shape[0] - y, h + 2 * padding)
            
            # Extract and normalize ROI
            roi = frame[y:y+h, x:x+w]
            gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            normalized_roi = cv2.resize(gray_roi, (128, 128))
            normalized_roi = cv2.equalizeHist(normalized_roi)
            
            return normalized_roi, max_contour
            
        except Exception as e:
            return None, None
    
    def _classify_gesture_ml(self, hand_roi: np.ndarray) -> Tuple[str, float]:
        """
        Classify gesture using trained ML model
        
        Args:
            hand_roi: 128x128 grayscale hand image
        
        Returns:
            Tuple of (gesture_name, confidence)
        """
        if self.gesture_trainer is None:
            return "UNKNOWN", 0.0
        
        try:
            gesture_name, confidence = self.gesture_trainer.predict_gesture(
                hand_roi, 
                min_confidence=self.min_confidence
            )
            return gesture_name, confidence
        except Exception as e:
            print(f"❌ ML classification error: {e}")
            return "UNKNOWN", 0.0
    
    def _detect_gesture_hybrid(self, frame) -> Tuple[str, Optional[np.ndarray], float]:
        """
        Hybrid gesture detection: tries ML model first, falls back to hardcoded
        
        Returns:
            Tuple of (gesture_name, hand_contour, confidence)
        """
        # First, try to detect hand and get ROI for ML
        if self.gesture_trainer is not None:
            hand_roi, hand_contour = self._detect_hand_roi(frame)
            
            if hand_roi is not None:
                # Try ML classification
                ml_gesture, confidence = self._classify_gesture_ml(hand_roi)
                
                if ml_gesture != "UNKNOWN" and confidence >= self.min_confidence:
                    # ML model recognized it!
                    return ml_gesture, hand_contour, confidence
        
        # Fall back to hardcoded finger-counting detection
        hardcoded_gesture, hand_contour = self._detect_hand_gesture(frame)
        return hardcoded_gesture, hand_contour, 1.0
