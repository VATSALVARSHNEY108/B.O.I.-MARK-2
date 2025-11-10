"""
VATSAL AI - Gesture-Activated Voice Listener
Detects TWO V signs (both hands) to trigger VATSAL greeting
UPGRADED: Smart DroidCam prioritization + brightness-based detection
"""

import cv2
import mediapipe as mp
import speech_recognition as sr
import threading
import time
import subprocess
from typing import Callable, Optional


class GestureVoiceActivator:
    """Gesture-based voice activation system with dual V sign detection"""

    def __init__(self, on_speech_callback: Optional[Callable[[str], None]] = None, camera_index: int = None):
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

    # ------------------------------------------------------
    # 🔍 SMART CAMERA DETECTION (prefers DroidCam 2–4 first)
    # ------------------------------------------------------
    def detect_working_camera(self):
        print("🔎 Detecting available cameras (brightness test, prioritizing DroidCam 2–4)...")

        # Prefer DroidCam if connected
        try:
            result = subprocess.check_output('wmic path win32_pnpentity get name', shell=True).decode(errors='ignore')
            if "DroidCam" in result:
                print("📱 DroidCam detected via USB connection")
        except Exception:
            pass

        # First: check likely DroidCam indexes (2–4)
        for index in [2, 3, 4]:
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    brightness = frame.mean()
                    cap.release()
                    if brightness > 10:  # non-black frame threshold
                        print(f"✅ Using DroidCam camera {index} (brightness {brightness:.1f})")
                        return index
            cap.release()

        # Fallback: local camera (0–1)
        for index in [0, 1]:
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    brightness = frame.mean()
                    cap.release()
                    if brightness > 10:
                        print(f"✅ Using fallback camera {index} (brightness {brightness:.1f})")
                        return index
            cap.release()

        print("❌ No working camera found, defaulting to 0")
        return 0

    # ------------------------------------------------------
    def is_v_sign(self, hand_landmarks):
        """Detect ✌️ V sign gesture"""
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

        return index_up and middle_up and ring_down and pinky_down

    # ------------------------------------------------------
    def listen_audio(self):
        """Capture and process speech input"""
        self.listening = True
        print("\n" + "="*60)
        print("🎤 LISTENING MODE ACTIVATED")
        print("="*60)
        
        try:
            with sr.Microphone() as source:
                print("🔊 Adjusting for background noise (1 second)...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                print("✅ Ready! SPEAK NOW! (You have 10 seconds)")
                print("   Say something like: 'Hello' or 'Testing'")
                print()
                
                # Increased timeout and energy threshold for better detection
                self.recognizer.energy_threshold = 300  # Lower = more sensitive
                audio_data = self.recognizer.listen(source, timeout=10, phrase_time_limit=8)
                
                print("✅ Audio captured! Processing...")

            text = self.recognizer.recognize_google(audio_data)
            self.last_text = text
            print(f"\n🎉 SUCCESS! You said: '{text}'")
            print("="*60 + "\n")

            if self.on_speech_callback:
                self.on_speech_callback(text)

        except sr.WaitTimeoutError:
            print("\n⏱️  TIMEOUT - No speech detected")
            print("💡 Make sure:")
            print("   1. Microphone is not muted")
            print("   2. You speak within 10 seconds")
            print("   3. Speak loudly and clearly")
            print("="*60 + "\n")
        except sr.UnknownValueError:
            print("\n❓ Audio captured but couldn't understand")
            print("💡 Try speaking louder and more clearly")
            print("="*60 + "\n")
        except sr.RequestError as e:
            print(f"\n❌ Speech recognition error: {e}")
            print("💡 Check your internet connection")
            print("="*60 + "\n")
        except OSError as e:
            print(f"\n❌ MICROPHONE ERROR: {e}")
            print("💡 Solutions:")
            print("   1. Run: python test_microphone.py")
            print("   2. Check microphone permissions")
            print("   3. Close other apps using microphone")
            print("="*60 + "\n")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("="*60 + "\n")
        finally:
            self.listening = False

    # ------------------------------------------------------
    def start_listening_thread(self):
        """Start audio listening in a separate thread"""
        if not self.listening:
            thread = threading.Thread(target=self.listen_audio, daemon=True)
            thread.start()

    def trigger_vatsal_greeting(self):
        """Display greeting when both hands are detected"""
        print("\n" + "=" * 70)
        print("👋 VATSAL DETECTED! Both hands showing V sign!")
        print("🎉 Hello VATSAL! Welcome!")
        print("=" * 70 + "\n")
        self.greeting_cooldown = 100

    # ------------------------------------------------------
    def set_stop_callback(self, callback: Callable[[], None]):
        """Allow GUI to register a callback when stopped"""
        self.on_stop_callback = callback

    # ------------------------------------------------------
    def initialize_camera(self, camera_index):
        """Initialize webcam or DroidCam source"""
        print(f"📹 Opening camera {camera_index}...")
        cap = cv2.VideoCapture(camera_index)

        if not cap.isOpened():
            print(f"❌ Could not open camera {camera_index}!")
            print("💡 Try reconnecting DroidCam or changing index (0–4)")
            return None

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        print("⏳ Warming up camera (4s for Android/DroidCam)...")
        time.sleep(4)

        print("🔄 Checking frames...")
        for i in range(10):
            ret, frame = cap.read()
            if not ret or frame is None:
                continue
            brightness = frame.mean()
            print(f"   Frame {i+1}: Brightness={brightness:.1f}")
            time.sleep(0.15)

        print("✅ Camera initialization complete!\n")
        return cap

    # ------------------------------------------------------
    def run(self):
        """Main loop for hand and voice gesture detection"""
        print("=" * 70)
        print("🎯 VATSAL AI - Gesture-Activated Voice Listener (SMART CAMERA PRIORITY)")
        print("=" * 70)

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            model_complexity=0,  # Fixes MediaPipe warning (0=lite, 1=full)
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )

        if self.camera_index is None:
            self.camera_index = self.detect_working_camera()

        print(f"🎥 Using camera index: {self.camera_index}")
        cap = self.initialize_camera(self.camera_index)

        if cap is None:
            print("❌ Camera initialization failed!")
            return

        print("🎯 Show TWO V signs for VATSAL greeting")
        print("🎯 Show ONE V sign to start voice listening\n")

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
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(rgb)
                h, w, _ = frame.shape

                v_sign_count = 0
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                        if self.is_v_sign(hand_landmarks):
                            v_sign_count += 1

                if v_sign_count == 2:
                    cv2.putText(frame, "VATSAL DETECTED!", (50, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
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

                cv2.imshow('VATSAL AI - Gesture Listener (SMART CAMERA)', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("\n⏹️ Stopping...")
                    break

        except KeyboardInterrupt:
            print("\n⏹️ Interrupted by user")
        except Exception as e:
            print(f"\n❌ Error: {e}")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            if self.hands:
                self.hands.close()
            if self.on_stop_callback:
                self.on_stop_callback()
            print("\n✅ Gesture Listener closed!")


# ------------------------------------------------------
def create_gesture_voice_activator(on_speech_callback: Optional[Callable[[str], None]] = None, camera_index: int = None):
    """Factory function to create activator instance"""
    return GestureVoiceActivator(on_speech_callback, camera_index)
