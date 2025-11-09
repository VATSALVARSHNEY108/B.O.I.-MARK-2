"""
VATSAL AI - Gesture-Activated Voice Listener
Detects TWO V signs (both hands) to trigger VATSAL greeting
UPGRADED: Android camera support with auto-detection
"""

import cv2
import mediapipe as mp
import speech_recognition as sr
import threading
import time
from typing import Callable, Optional
from modules.automation.audio_feedback import get_audio_feedback


class GestureVoiceActivator:
    """Gesture-based voice activation system with dual V sign detection"""
    
    def __init__(self, on_speech_callback: Optional[Callable[[str], None]] = None, camera_index: int = None):
        """
        Initialize gesture voice activator
        
        Args:
            on_speech_callback: Function to call when speech is recognized
            camera_index: Camera index to use (None = auto-detect)
        """
        self.mp_hands = mp.solutions.hands
        self.hands = None
        self.mp_draw = mp.solutions.drawing_utils
        
        self.recognizer = sr.Recognizer()
        self.listening = False
        self.last_text = ""
        self.running = False
        self.on_speech_callback = on_speech_callback
        self.on_stop_callback = None
        self.camera_index = camera_index
        
        self.greeting_cooldown = 0
        
    def is_v_sign(self, hand_landmarks):
        """
        Detect V sign gesture
        V sign: Index and Middle fingers up, other fingers down
        """
        landmarks = hand_landmarks.landmark
        
        index_tip = landmarks[8].y
        index_pip = landmarks[6].y
        
        middle_tip = landmarks[12].y
        middle_pip = landmarks[10].y
        
        ring_tip = landmarks[16].y
        ring_pip = landmarks[14].y
        
        pinky_tip = landmarks[20].y
        pinky_pip = landmarks[18].y
        
        index_up = index_tip < index_pip
        middle_up = middle_tip < middle_pip
        
        ring_down = ring_tip > ring_pip
        pinky_down = pinky_tip > pinky_pip
        
        is_v = index_up and middle_up and ring_down and pinky_down
        
        return is_v
    
    def listen_audio(self):
        """Listen to audio and convert to text"""
        self.listening = True
        print("\n🎤 Listening... Speak now!")
        
        # Play audio signal when listening starts
        audio = get_audio_feedback()
        audio.play_listening_start()
        
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("🔄 Processing speech...")
            text = self.recognizer.recognize_google(audio)
            self.last_text = text
            print(f"✅ You said: '{text}'")
            
            if self.on_speech_callback:
                self.on_speech_callback(text)
            
        except sr.WaitTimeoutError:
            print("⏱️  No speech detected")
            self.last_text = ""
        except sr.UnknownValueError:
            print("❓ Could not understand audio")
            self.last_text = ""
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            self.last_text = ""
        except Exception as e:
            print(f"❌ Error: {e}")
            self.last_text = ""
        finally:
            self.listening = False
    
    def start_listening_thread(self):
        """Start listening in a separate thread"""
        if not self.listening:
            thread = threading.Thread(target=self.listen_audio, daemon=True)
            thread.start()
    
    def trigger_vatsal_greeting(self):
        """Greet VATSAL when both hands show V sign"""
        print("\n" + "=" * 70)
        print("👋 VATSAL DETECTED! Both hands showing V sign!")
        print("🎉 Hello VATSAL! Welcome!")
        print("=" * 70 + "\n")
        self.greeting_cooldown = 100
    
    def stop(self):
        """Stop the gesture activator"""
        self.running = False
        if self.hands:
            self.hands.close()
            self.hands = None
    
    def set_stop_callback(self, callback: Callable[[], None]):
        """Set callback to be called when activator stops"""
        self.on_stop_callback = callback
    
    def detect_working_camera(self):
        """Simple camera detection - just returns the default camera index"""
        # No loop - just use the camera index directly
        return self.camera_index if self.camera_index is not None else 1
    
    def initialize_camera(self, camera_index):
        """Initialize camera with Android/DroidCam support (fixes black screen)"""
        print(f"📹 Opening camera {camera_index}...")
        
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            print(f"❌ Could not open camera {camera_index}!")
            print("💡 Try changing camera_index on line 200:")
            print("   - For camera 0: self.camera_index = 0")
            print("   - For camera 1: self.camera_index = 1")
            print("   - For camera 2: self.camera_index = 2")
            return None
        
        # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer for real-time
        
        print("⏳ Warming up camera (4 seconds for Android/DroidCam)...")
        time.sleep(4)  # Increased from 2 to 4 seconds
        
        print("🔄 Discarding initial black frames (15 frames)...")
        black_count = 0
        for i in range(15):  # Increased from 5 to 15 frames
            ret, frame = cap.read()
            if ret and frame is not None:
                brightness = frame.mean()
                is_black = brightness < 15
                black_count += 1 if is_black else 0
                status = "⚫ BLACK" if is_black else "✅ OK"
                print(f"   Frame {i+1}: Brightness {brightness:.1f} {status}")
            time.sleep(0.15)  # Increased delay between frames
        
        # Test final frame
        print("\n🧪 Testing camera feed...")
        ret, test_frame = cap.read()
        if ret and test_frame is not None:
            final_brightness = test_frame.mean()
            print(f"   Final test brightness: {final_brightness:.1f}")
            if final_brightness < 15:
                print("\n⚠️  WARNING: Camera still showing black screen!")
                print("💡 Solutions:")
                print("   1. Try a different camera index (0, 2, or 3)")
                print("   2. Close other apps using the camera")
                print("   3. Restart DroidCam on phone and computer")
                print("   4. Check DroidCam client shows video feed")
            else:
                print("   ✅ Camera feed is working!")
        
        print("\n✅ Camera initialization complete!")
        return cap
    
    def run(self):
        """Main loop for gesture detection"""
        print("=" * 70)
        print("🎯 VATSAL AI - Gesture-Activated Voice Listener (UPGRADED)")
        print("=" * 70)
        print()
        
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        # Set camera index directly (no auto-detection loop)
        if self.camera_index is None:
            self.camera_index = 1  # Change this: 0=default, 1=Android/DroidCam, 2=camera2, 3=camera3
        
        print(f"🎥 Using camera index: {self.camera_index}")
        print()
        
        cap = self.initialize_camera(self.camera_index)
        
        if cap is None:
            print("❌ Camera initialization failed!")
            return
        
        print()
        print("🎯 Instructions:")
        print("   • Show TWO V signs (both hands ✌️✌️) to get VATSAL greeting")
        print("   • Show ONE V sign (1 second) to activate voice listening")
        print("   • Speak your command when microphone icon appears")
        print("   • Press 'q' to quit")
        print()
        print("=" * 70)
        print()
        
        self.running = True
        single_v_detected = False
        single_v_timer = 0
        single_v_cooldown = 0
        
        try:
            while self.running:
                ret, frame = cap.read()
                
                if not ret:
                    print("❌ Failed to read from camera")
                    break
                
                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                results = self.hands.process(rgb_frame)
                
                h, w, _ = frame.shape
                
                v_sign_count = 0
                
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.mp_draw.draw_landmarks(
                            frame, 
                            hand_landmarks, 
                            self.mp_hands.HAND_CONNECTIONS
                        )
                        
                        if self.is_v_sign(hand_landmarks):
                            v_sign_count += 1
                
                if v_sign_count == 2:
                    cv2.putText(frame, "VATSAL DETECTED!", (50, 100),
                               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
                    cv2.putText(frame, "Both Hands V Sign!", (50, 150),
                               cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)
                    
                    if self.greeting_cooldown == 0:
                        self.trigger_vatsal_greeting()
                        
                elif v_sign_count == 1:
                    cv2.putText(frame, "One V Sign Detected", (50, 100),
                               cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 200, 255), 2)
                    
                    if not single_v_detected and single_v_cooldown == 0:
                        single_v_detected = True
                        single_v_timer = time.time()
                
                if v_sign_count == 1 and single_v_detected:
                    if time.time() - single_v_timer > 1.0 and not self.listening:
                        self.start_listening_thread()
                        single_v_detected = False
                        single_v_cooldown = 60
                elif v_sign_count != 1:
                    single_v_detected = False
                
                if single_v_cooldown > 0:
                    single_v_cooldown -= 1
                
                if self.greeting_cooldown > 0:
                    self.greeting_cooldown -= 1
                
                if self.listening:
                    cv2.circle(frame, (w - 50, 50), 30, (0, 0, 255), -1)
                    cv2.putText(frame, "LISTENING...", (w - 200, 100),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                if self.last_text:
                    cv2.putText(frame, f"Last: {self.last_text[:40]}", (10, h - 20),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                status_text = f"Camera {self.camera_index} | 2 V signs=greeting | 1 V sign=listen | q=quit"
                cv2.putText(frame, status_text, (10, h - 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                camera_info = f"Android Camera Support Enabled"
                cv2.putText(frame, camera_info, (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                
                cv2.imshow('VATSAL AI - Gesture Listener (UPGRADED)', frame)
                
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    print("\n⏹️  Stopping...")
                    break
        
        except KeyboardInterrupt:
            print("\n⏹️  Interrupted by user")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            cap.release()
            cv2.destroyAllWindows()
            if self.hands:
                self.hands.close()
                self.hands = None
            
            if self.on_stop_callback:
                self.on_stop_callback()
        
        print("\n" + "=" * 70)
        print("✅ Gesture Listener closed!")
        print("=" * 70)


def create_gesture_voice_activator(on_speech_callback: Optional[Callable[[str], None]] = None, camera_index: int = None):
    """
    Factory function to create gesture voice activator
    
    Args:
        on_speech_callback: Function to call when speech is recognized
        camera_index: Camera index to use (None = auto-detect, 0 = first camera, 1 = Android/DroidCam, etc.)
    
    Usage:
        # Auto-detect camera (recommended for Android/DroidCam)
        activator = create_gesture_voice_activator()
        
        # Use specific camera (if you know the index)
        activator = create_gesture_voice_activator(camera_index=1)
    """
    return GestureVoiceActivator(on_speech_callback, camera_index)
