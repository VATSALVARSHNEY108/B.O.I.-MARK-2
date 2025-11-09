"""
VATSAL AI - Gesture-Activated Voice Listener
Detects TWO V signs (both hands) to trigger VATSAL greeting
"""

import cv2
import mediapipe as mp
import speech_recognition as sr
import threading
import time
from typing import Callable, Optional


class GestureVoiceActivator:
    """Gesture-based voice activation system with dual V sign detection"""
    
    def __init__(self, on_speech_callback: Optional[Callable[[str], None]] = None):
        """
        Initialize gesture voice activator
        
        Args:
            on_speech_callback: Function to call when speech is recognized
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
    
    def run(self):
        """Main loop for gesture detection"""
        print("=" * 70)
        print("🎯 VATSAL AI - Gesture-Activated Voice Listener")
        print("=" * 70)
        print()
        
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        print("📹 Opening camera...")
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Could not open camera!")
            return
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        print("✅ Camera ready!")
        print()
        print("🎯 Instructions:")
        print("   • Show TWO V signs (both hands ✌️✌️) to get VATSAL greeting")
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
                
                status_text = "Show 2 V signs for VATSAL greeting | 1 V sign for listening | Press 'q' to quit"
                cv2.putText(frame, status_text, (10, h - 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                cv2.imshow('VATSAL AI - Gesture Listener', frame)
                
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


def create_gesture_voice_activator(on_speech_callback: Optional[Callable[[str], None]] = None):
    """Factory function to create gesture voice activator"""
    return GestureVoiceActivator(on_speech_callback)
