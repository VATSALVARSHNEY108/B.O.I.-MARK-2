"""
Face Detection & Gesture Recognition Assistant for BOI
Detects user's face, greets them, and recognizes hand signs to activate voice listening
"""

import cv2
import threading
import time
from typing import Dict, Optional, Callable
import numpy as np
from modules.automation.audio_feedback import get_audio_feedback

# Try to import mediapipe, make it optional for Python 3.13 Windows compatibility
try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    print("⚠️  MediaPipe not available - hand gesture recognition will be disabled")
    print("   Face detection will still work using OpenCV")


class FaceGestureAssistant:
    """Face detection and hand gesture recognition for voice activation"""
    
    def __init__(self, voice_commander=None):
        self.voice_commander = voice_commander
        self.mediapipe_available = MEDIAPIPE_AVAILABLE
        
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Only initialize MediaPipe if available
        if MEDIAPIPE_AVAILABLE:
            self.mp_hands = mp.solutions.hands
            self.hands = self.mp_hands.Hands(
                max_num_hands=1,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.5
            )
            self.mp_drawing = mp.solutions.drawing_utils
        else:
            self.mp_hands = None
            self.hands = None
            self.mp_drawing = None
        
        self.cap = None
        self.running = False
        self.thread = None
        
        self.face_detected = False
        self.last_greeting_time = 0
        self.greeting_cooldown = 10
        
        self.gesture_active = False
        self.last_gesture_time = 0
        self.gesture_cooldown = 3
        
        self.on_face_detected_callback = None
        self.on_gesture_detected_callback = None
        
        self.stats = {
            'faces_detected': 0,
            'gestures_detected': 0,
            'greetings_given': 0
        }
    
    def start(self, camera_index: int = 0) -> Dict:
        """Start face detection and gesture recognition"""
        if self.running:
            return {
                'success': False,
                'message': 'Face & Gesture Assistant already running'
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
                'message': 'Face & Gesture Assistant started successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error starting assistant: {str(e)}'
            }
    
    def stop(self) -> Dict:
        """Stop face detection and gesture recognition"""
        if not self.running:
            return {
                'success': False,
                'message': 'Face & Gesture Assistant not running'
            }
        
        self.running = False
        
        if self.thread:
            self.thread.join(timeout=2)
        
        if self.cap:
            self.cap.release()
        
        if self.hands and MEDIAPIPE_AVAILABLE:
            self.hands.close()
        
        cv2.destroyAllWindows()
        
        return {
            'success': True,
            'message': 'Face & Gesture Assistant stopped'
        }
    
    def _detection_loop(self):
        """Main detection loop running in separate thread"""
        print("🎥 Face & Gesture Detection started")
        
        while self.running:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    print("❌ Failed to read from camera")
                    time.sleep(0.1)
                    continue
                
                frame = cv2.flip(frame, 1)
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(80, 80)
                )
                
                current_time = time.time()
                
                if len(faces) > 0:
                    if not self.face_detected:
                        self.face_detected = True
                        self.stats['faces_detected'] += 1
                        print("👤 Face detected!")
                    
                    if current_time - self.last_greeting_time > self.greeting_cooldown:
                        self._greet_user()
                        self.last_greeting_time = current_time
                    
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        cv2.putText(
                            frame, 
                            "Vatsal", 
                            (x, y-10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            0.9, 
                            (0, 255, 0), 
                            2
                        )
                else:
                    self.face_detected = False
                
                # Hand gesture detection (only if MediaPipe is available)
                if MEDIAPIPE_AVAILABLE and self.hands:
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = self.hands.process(rgb_frame)
                    
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            self.mp_drawing.draw_landmarks(
                                frame,
                                hand_landmarks,
                                self.mp_hands.HAND_CONNECTIONS
                            )
                            
                            gesture = self._recognize_gesture(hand_landmarks)
                            
                            if gesture == "OPEN_PALM" and self.face_detected:
                                if current_time - self.last_gesture_time > self.gesture_cooldown:
                                    self._handle_listening_gesture()
                                    self.last_gesture_time = current_time
                                
                                cv2.putText(
                                    frame,
                                    "Listening Gesture Detected!",
                                    (10, 60),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.7,
                                    (0, 255, 255),
                                    2
                                )
                
                status_text = "Face: Detected" if self.face_detected else "Face: Not Detected"
                cv2.putText(
                    frame,
                    status_text,
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0) if self.face_detected else (0, 0, 255),
                    2
                )
                
                cv2.imshow('BOI - Face & Gesture Detection', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.running = False
                    break
                    
            except Exception as e:
                print(f"❌ Error in detection loop: {str(e)}")
                time.sleep(0.1)
        
        print("🛑 Face & Gesture Detection stopped")
    
    def _recognize_gesture(self, hand_landmarks) -> str:
        """Recognize hand gesture from landmarks"""
        try:
            thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]
            
            wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
            
            fingers_extended = 0
            
            finger_tips = [index_tip, middle_tip, ring_tip, pinky_tip]
            for tip in finger_tips:
                if tip.y < wrist.y:
                    fingers_extended += 1
            
            if thumb_tip.x < wrist.x - 0.05 or thumb_tip.x > wrist.x + 0.05:
                fingers_extended += 1
            
            if fingers_extended >= 4:
                return "OPEN_PALM"
            elif fingers_extended <= 1:
                return "FIST"
            else:
                return "PARTIAL"
                
        except Exception as e:
            print(f"❌ Gesture recognition error: {str(e)}")
            return "UNKNOWN"
    
    def _greet_user(self):
        """Greet the user when face is detected"""
        if self.voice_commander:
            import random
            greetings = [
                "Yes sir",
                "Hello Vatsal",
                "I'm here Vatsal",
                "At your service sir",
                "Ready to assist Vatsal"
            ]
            greeting = random.choice(greetings)
            self.voice_commander.speak(greeting)
            self.stats['greetings_given'] += 1
            print(f"👋 Greeting: {greeting}")
        
        if self.on_face_detected_callback:
            self.on_face_detected_callback()
    
    def _handle_listening_gesture(self):
        """
        Handle the listening activation gesture.
        
        NOTE: This runs in the detection worker thread.
        The callback should handle thread-safety if it needs to update GUI.
        """
        print("✋ Listening gesture detected!")
        self.stats['gestures_detected'] += 1
        
        # Play audio signal when listening starts
        audio = get_audio_feedback()
        audio.play_listening_start()
        
        if self.voice_commander:
            self.voice_commander.speak("I'm listening")
            time.sleep(0.5)
            
            result = self.voice_commander.listen_once(timeout=5)
            
            if result['success'] and result['command']:
                print(f"🎤 Voice command received: {result['command']}")
                
                if self.on_gesture_detected_callback:
                    try:
                        self.on_gesture_detected_callback(result['command'])
                    except Exception as e:
                        print(f"❌ Error in gesture callback: {str(e)}")
            else:
                self.voice_commander.speak("I didn't catch that")
    
    def set_face_callback(self, callback: Callable):
        """Set callback for when face is detected"""
        self.on_face_detected_callback = callback
    
    def set_gesture_callback(self, callback: Callable):
        """Set callback for when gesture is detected"""
        self.on_gesture_detected_callback = callback
    
    def get_stats(self) -> Dict:
        """Get statistics"""
        return {
            'running': self.running,
            'face_detected': self.face_detected,
            **self.stats
        }
    
    def is_running(self) -> bool:
        """Check if assistant is running"""
        return self.running


def test_face_gesture_assistant():
    """Test the face and gesture assistant"""
    print("🧪 Testing Face & Gesture Assistant")
    print("=" * 60)
    
    try:
        from modules.voice.voice_commander import VoiceCommander
        voice = VoiceCommander()
    except Exception as e:
        print(f"⚠️  Voice commander not available: {e}")
        voice = None
    
    assistant = FaceGestureAssistant(voice_commander=voice)
    
    print("\n📋 Instructions:")
    print("1. Position your face in front of the camera")
    print("2. You should see a green rectangle around your face")
    print("3. Show an OPEN PALM (all fingers extended) to activate voice listening")
    print("4. Press 'q' to quit")
    print("\n" + "=" * 60)
    
    result = assistant.start()
    print(f"\n{result['message']}")
    
    if result['success']:
        try:
            while assistant.is_running():
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
    
    assistant.stop()
    
    print("\n📊 Final Statistics:")
    stats = assistant.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    test_face_gesture_assistant()
