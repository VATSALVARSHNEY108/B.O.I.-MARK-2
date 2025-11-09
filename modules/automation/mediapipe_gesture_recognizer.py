"""
MediaPipe Gesture Recognition Module
Uses Google's pretrained gesture model to recognize hand gestures without training
"""

import os
import cv2
import numpy as np
from typing import Optional, Tuple

try:
    import mediapipe as mp
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    print("⚠️  MediaPipe not available. Install with: pip install mediapipe")


class MediaPipeGestureRecognizer:
    """
    Pretrained gesture recognizer using Google MediaPipe
    
    Recognizes 7 gestures without requiring training:
    - Closed_Fist
    - Open_Palm
    - Pointing_Up  
    - Thumb_Down
    - Thumb_Up
    - Victory
    - ILoveYou
    """
    
    def __init__(self, model_path: str = "models/mediapipe/gesture_recognizer.task",
                 min_confidence: float = 0.6):
        """
        Initialize MediaPipe gesture recognizer
        
        Args:
            model_path: Path to the .task model file
            min_confidence: Minimum confidence threshold (0.0-1.0)
        """
        self.model_path = model_path
        self.min_confidence = min_confidence
        self.recognizer = None
        self.available = False
        
        # Gesture mapping: MediaPipe name → VATSAL gesture name
        self.gesture_mapping = {
            "Closed_Fist": "FIST",
            "Open_Palm": "OPEN_PALM",
            "Pointing_Up": "ONE_FINGER_UP",
            "Thumb_Down": "THUMBS_DOWN",
            "Thumb_Up": "THUMBS_UP",
            "Victory": "PEACE_SIGN",
            "ILoveYou": "ROCK_SIGN"
        }
        
        self._load_model()
    
    def _load_model(self):
        """Load the pretrained MediaPipe model"""
        if not MEDIAPIPE_AVAILABLE:
            print("❌ MediaPipe not installed")
            return
        
        if not os.path.exists(self.model_path):
            print(f"❌ Model not found at: {self.model_path}")
            print("Run: curl -L https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task -o models/mediapipe/gesture_recognizer.task")
            return
        
        try:
            base_options = python.BaseOptions(model_asset_path=self.model_path)
            options = vision.GestureRecognizerOptions(
                base_options=base_options,
                running_mode=vision.RunningMode.IMAGE,
                num_hands=1,
                min_hand_detection_confidence=self.min_confidence,
                min_hand_presence_confidence=self.min_confidence,
                min_tracking_confidence=self.min_confidence
            )
            
            self.recognizer = vision.GestureRecognizer.create_from_options(options)
            self.available = True
            print(f"✅ MediaPipe gesture recognizer loaded")
            print(f"   Available gestures: {list(self.gesture_mapping.values())}")
            
        except Exception as e:
            print(f"❌ Failed to load MediaPipe model: {e}")
            self.available = False
    
    def recognize(self, frame: np.ndarray) -> Tuple[Optional[str], float]:
        """
        Recognize gesture in a frame (MediaPipe + custom gestures)
        
        Args:
            frame: BGR image from OpenCV (numpy array)
        
        Returns:
            Tuple of (gesture_name, confidence) or (None, 0.0) if no gesture
        """
        if not self.available or self.recognizer is None:
            return None, 0.0
        
        try:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Create MediaPipe Image
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            
            # Recognize gestures with MediaPipe
            result = self.recognizer.recognize(mp_image)
            
            # 1. Try MediaPipe gestures first
            if result.gestures and len(result.gestures) > 0:
                gesture = result.gestures[0][0]
                
                if gesture.score >= self.min_confidence:
                    # Map MediaPipe gesture to VATSAL gesture
                    mediapipe_name = gesture.category_name
                    vatsal_name = self.gesture_mapping.get(mediapipe_name, mediapipe_name)
                    
                    return vatsal_name, gesture.score
            
            # 2. If no MediaPipe gesture, try custom gesture detection
            if result.hand_landmarks and len(result.hand_landmarks) > 0:
                landmarks = result.hand_landmarks[0]
                landmarks_list = [(lm.x, lm.y, lm.z) for lm in landmarks]
                
                custom_gesture, custom_conf = self.detect_custom_gestures(landmarks_list)
                if custom_gesture:
                    return custom_gesture, custom_conf
            
            return None, 0.0
            
        except Exception as e:
            print(f"❌ MediaPipe recognition error: {e}")
            return None, 0.0
    
    def get_hand_landmarks(self, frame: np.ndarray) -> Optional[list]:
        """
        Get 21 hand landmarks from the frame
        
        Args:
            frame: BGR image from OpenCV
        
        Returns:
            List of 21 (x, y, z) tuples or None
        """
        if not self.available or self.recognizer is None:
            return None
        
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            
            result = self.recognizer.recognize(mp_image)
            
            if result.hand_landmarks and len(result.hand_landmarks) > 0:
                landmarks = result.hand_landmarks[0]
                return [(lm.x, lm.y, lm.z) for lm in landmarks]
            
            return None
            
        except Exception as e:
            print(f"❌ Landmark extraction error: {e}")
            return None
    
    def draw_results(self, frame: np.ndarray, gesture_name: str, confidence: float) -> np.ndarray:
        """
        Draw gesture recognition results on frame
        
        Args:
            frame: BGR image from OpenCV
            gesture_name: Detected gesture name
            confidence: Confidence score
        
        Returns:
            Frame with overlays
        """
        overlay = frame.copy()
        
        # Draw gesture name and confidence
        text = f"{gesture_name} ({confidence*100:.1f}%)"
        
        # Background rectangle
        (text_width, text_height), _ = cv2.getTextSize(
            text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2
        )
        
        cv2.rectangle(
            overlay,
            (10, 10),
            (20 + text_width, 40 + text_height),
            (0, 128, 255),
            -1
        )
        
        # Text
        cv2.putText(
            overlay,
            text,
            (15, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )
        
        # Blend
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        return frame
    
    def detect_custom_gestures(self, landmarks: list) -> Tuple[Optional[str], float]:
        """
        Detect custom gestures using hand landmark analysis
        Supports: SPOCK, OK_CIRCLE, PINCH, ROCK_SIGN
        
        Args:
            landmarks: List of 21 (x, y, z) hand landmarks
        
        Returns:
            Tuple of (gesture_name, confidence) or (None, 0.0)
        """
        if not landmarks or len(landmarks) < 21:
            return None, 0.0
        
        # 1. SPOCK (Vulcan salute - split fingers)
        if self._is_spock_gesture(landmarks):
            return "SPOCK", 0.9
        
        # 2. OK_CIRCLE (Thumb + Index forming circle)
        elif self._is_ok_circle(landmarks):
            return "OK_CIRCLE", 0.85
        
        # 3. PINCH
        elif self._is_pinch(landmarks):
            return "PINCH", 0.8
        
        return None, 0.0
    
    def _is_spock_gesture(self, landmarks: list) -> bool:
        """Detect Spock/Vulcan salute (split fingers 🖖)"""
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        
        # Distance between index and middle (should be small)
        index_middle_dist = np.linalg.norm(np.array(index_tip[:2]) - np.array(middle_tip[:2]))
        
        # Distance between ring and pinky (should be small)
        ring_pinky_dist = np.linalg.norm(np.array(ring_tip[:2]) - np.array(pinky_tip[:2]))
        
        # Distance between middle and ring (should be large)
        middle_ring_dist = np.linalg.norm(np.array(middle_tip[:2]) - np.array(ring_tip[:2]))
        
        # Spock if middle-ring gap is significantly larger
        return middle_ring_dist > 2 * max(index_middle_dist, ring_pinky_dist)
    
    def _is_ok_circle(self, landmarks: list) -> bool:
        """Detect OK gesture (thumb + index forming circle 👌)"""
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        
        # Distance between thumb tip and index tip
        distance = np.linalg.norm(np.array(thumb_tip[:2]) - np.array(index_tip[:2]))
        
        # OK gesture if distance is very small (forming circle)
        return distance < 0.05
    
    def _is_pinch(self, landmarks: list) -> bool:
        """Detect pinch gesture 🫰"""
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        
        distance = np.linalg.norm(np.array(thumb_tip[:2]) - np.array(index_tip[:2]))
        
        # Pinch if fingers are close but not forming complete circle
        return 0.03 < distance < 0.08
    
    def list_available_gestures(self) -> list:
        """
        Get list of gestures this recognizer can detect
        
        Returns:
            List of gesture names (includes MediaPipe + custom gestures)
        """
        base_gestures = list(self.gesture_mapping.values())
        custom_gestures = ["SPOCK", "OK_CIRCLE", "PINCH"]
        return base_gestures + custom_gestures
    
    def is_available(self) -> bool:
        """Check if recognizer is ready to use"""
        return self.available


def demo():
    """Demo function to test MediaPipe gesture recognition"""
    print("🎥 MediaPipe Gesture Recognition Demo")
    print("=" * 60)
    
    recognizer = MediaPipeGestureRecognizer()
    
    if not recognizer.is_available():
        print("❌ Cannot run demo - recognizer not available")
        return
    
    print(f"✅ Recognizer ready!")
    print(f"📋 Can detect: {recognizer.list_available_gestures()}")
    print("\nPress 'q' to quit")
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Cannot open camera")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Recognize gesture
        gesture, confidence = recognizer.recognize(frame)
        
        # Draw results
        if gesture:
            frame = recognizer.draw_results(frame, gesture, confidence)
        else:
            cv2.putText(
                frame,
                "No gesture detected",
                (15, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (128, 128, 128),
                2
            )
        
        cv2.imshow("MediaPipe Gesture Demo", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("\n✅ Demo complete!")


if __name__ == "__main__":
    demo()
