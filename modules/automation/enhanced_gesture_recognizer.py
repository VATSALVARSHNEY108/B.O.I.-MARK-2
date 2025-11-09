"""
Enhanced Gesture Recognizer for VATSAL AI
Supports static gestures, dynamic gestures, combinations, and facial fusion
Uses MediaPipe + custom hand landmark analysis
"""

import os
import cv2
import numpy as np
import time
from typing import Dict, List, Tuple, Optional, Deque
from collections import deque
from dataclasses import dataclass

try:
    import mediapipe as mp
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False

from modules.automation.advanced_gesture_definitions import (
    SYSTEM_GESTURES, INTERACTION_GESTURES, COMBINATION_GESTURES,
    DYNAMIC_GESTURES, FACIAL_FUSION_GESTURES, get_all_static_gestures, 
    get_gesture_emoji, GestureActionHandler
)


@dataclass
class HandLandmarks:
    """Stores hand landmark positions"""
    landmarks: List[Tuple[float, float, float]]  # (x, y, z) for each landmark
    handedness: str  # "Left" or "Right"
    timestamp: float


@dataclass
class GestureEvent:
    """Represents a detected gesture event"""
    gesture_name: str
    confidence: float
    timestamp: float
    hand_landmarks: Optional[HandLandmarks] = None
    motion_vector: Optional[Tuple[float, float]] = None


class EnhancedGestureRecognizer:
    """
    Enhanced gesture recognizer supporting:
    - Static gestures (hand poses)
    - Dynamic gestures (motion + pose)
    - Gesture combinations (sequences)
    - Facial fusion (face + gesture)
    """
    
    def __init__(self, model_path: str = "models/mediapipe/gesture_recognizer.task",
                 min_confidence: float = 0.6,
                 voice_commander=None):
        """
        Initialize enhanced gesture recognizer
        
        Args:
            model_path: Path to MediaPipe .task model file
            min_confidence: Minimum confidence threshold
            voice_commander: Voice commander for audio feedback
        """
        self.model_path = model_path
        self.min_confidence = min_confidence
        self.recognizer = None
        self.hands_detector = None
        self.available = False
        
        # Action handler
        self.action_handler = GestureActionHandler(voice_commander=voice_commander)
        
        # Gesture history for combinations
        self.gesture_history: Deque[GestureEvent] = deque(maxlen=10)
        
        # Motion tracking
        self.hand_position_history: Deque[Tuple[float, float, float]] = deque(maxlen=30)
        
        # MediaPipe gesture mapping (updated with new gestures)
        self.mediapipe_to_vatsal = {
            "Closed_Fist": "FIST",
            "Open_Palm": "OPEN_PALM",
            "Pointing_Up": "ONE_FINGER_UP",
            "Thumb_Down": "THUMBS_DOWN",
            "Thumb_Up": "THUMBS_UP",
            "Victory": "TWO_FINGERS_UP",
            "ILoveYou": "ROCK_SIGN"
        }
        
        # Custom gesture detection parameters
        self.finger_tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
        
        self._load_model()
    
    def _load_model(self):
        """Load MediaPipe models"""
        if not MEDIAPIPE_AVAILABLE:
            print("❌ MediaPipe not installed")
            return
        
        try:
            # Load gesture recognizer
            if os.path.exists(self.model_path):
                base_options = python.BaseOptions(model_asset_path=self.model_path)
                options = vision.GestureRecognizerOptions(
                    base_options=base_options,
                    running_mode=vision.RunningMode.IMAGE,
                    num_hands=2,  # Support 2 hands for combinations
                    min_hand_detection_confidence=self.min_confidence,
                    min_hand_presence_confidence=self.min_confidence,
                    min_tracking_confidence=self.min_confidence
                )
                self.recognizer = vision.GestureRecognizer.create_from_options(options)
            
            # Load hands detector for landmark analysis
            self.hands_detector = mp.solutions.hands.Hands(
                static_image_mode=False,
                max_num_hands=2,
                min_detection_confidence=self.min_confidence,
                min_tracking_confidence=self.min_confidence
            )
            
            self.available = True
            print("✅ Enhanced gesture recognizer loaded")
            print(f"   Supports {len(get_all_static_gestures())} static gestures")
            print(f"   Supports {len(DYNAMIC_GESTURES)} dynamic gestures")
            print(f"   Supports {len(COMBINATION_GESTURES)} gesture combinations")
            
        except Exception as e:
            print(f"❌ Failed to load enhanced gesture recognizer: {e}")
            self.available = False
    
    def recognize_frame(self, frame: np.ndarray) -> List[GestureEvent]:
        """
        Recognize all gestures in a frame
        
        Args:
            frame: BGR image from OpenCV
        
        Returns:
            List of detected gesture events
        """
        if not self.available:
            return []
        
        detected_gestures = []
        current_time = time.time()
        
        # Convert to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 1. Detect static gestures using MediaPipe
        static_gestures = self._detect_static_gestures(rgb_frame, current_time)
        detected_gestures.extend(static_gestures)
        
        # 2. Detect custom gestures using hand landmarks
        custom_gestures = self._detect_custom_gestures(rgb_frame, current_time)
        detected_gestures.extend(custom_gestures)
        
        # 3. Detect dynamic gestures (motion-based)
        dynamic_gestures = self._detect_dynamic_gestures(detected_gestures, current_time)
        detected_gestures.extend(dynamic_gestures)
        
        # 4. Add to history and check for combinations
        for gesture in detected_gestures:
            self.gesture_history.append(gesture)
        
        combo_gestures = self._detect_gesture_combinations(current_time)
        detected_gestures.extend(combo_gestures)
        
        return detected_gestures
    
    def _detect_static_gestures(self, rgb_frame: np.ndarray, timestamp: float) -> List[GestureEvent]:
        """Detect static gestures using MediaPipe pretrained model"""
        gestures = []
        
        if self.recognizer is None:
            return gestures
        
        try:
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            result = self.recognizer.recognize(mp_image)
            
            if result.gestures and len(result.gestures) > 0:
                for hand_gestures in result.gestures:
                    if len(hand_gestures) > 0:
                        gesture = hand_gestures[0]
                        
                        if gesture.score >= self.min_confidence:
                            mp_name = gesture.category_name
                            vatsal_name = self.mediapipe_to_vatsal.get(mp_name, mp_name)
                            
                            gestures.append(GestureEvent(
                                gesture_name=vatsal_name,
                                confidence=gesture.score,
                                timestamp=timestamp
                            ))
        
        except Exception as e:
            print(f"❌ Static gesture detection error: {e}")
        
        return gestures
    
    def _detect_custom_gestures(self, rgb_frame: np.ndarray, timestamp: float) -> List[GestureEvent]:
        """Detect custom gestures using hand landmark analysis"""
        gestures = []
        
        if self.hands_detector is None:
            return gestures
        
        try:
            results = self.hands_detector.process(rgb_frame)
            
            if results.multi_hand_landmarks:
                for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    handedness = results.multi_handedness[hand_idx].classification[0].label
                    
                    # Extract landmark coordinates
                    landmarks = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
                    
                    hand_data = HandLandmarks(
                        landmarks=landmarks,
                        handedness=handedness,
                        timestamp=timestamp
                    )
                    
                    # Detect custom gestures
                    
                    # 1. SPOCK (Split fingers - Vulcan salute)
                    if self._is_spock_gesture(landmarks):
                        gestures.append(GestureEvent(
                            gesture_name="SPOCK",
                            confidence=0.9,
                            timestamp=timestamp,
                            hand_landmarks=hand_data
                        ))
                    
                    # 2. OK_CIRCLE (Thumb + Index forming circle)
                    elif self._is_ok_circle(landmarks):
                        gestures.append(GestureEvent(
                            gesture_name="OK_CIRCLE",
                            confidence=0.85,
                            timestamp=timestamp,
                            hand_landmarks=hand_data
                        ))
                    
                    # 3. PINCH
                    elif self._is_pinch(landmarks):
                        gestures.append(GestureEvent(
                            gesture_name="PINCH",
                            confidence=0.8,
                            timestamp=timestamp,
                            hand_landmarks=hand_data
                        ))
                    
                    # Track hand position for motion detection
                    palm_center = self._get_palm_center(landmarks)
                    self.hand_position_history.append((*palm_center, timestamp))
                
                # 4. HEART_HANDS (requires two hands together)
                if len(results.multi_hand_landmarks) == 2:
                    hand1_landmarks = [(lm.x, lm.y, lm.z) for lm in results.multi_hand_landmarks[0].landmark]
                    hand2_landmarks = [(lm.x, lm.y, lm.z) for lm in results.multi_hand_landmarks[1].landmark]
                    
                    if self._is_heart_hands(hand1_landmarks, hand2_landmarks):
                        gestures.append(GestureEvent(
                            gesture_name="HEART_HANDS",
                            confidence=0.85,
                            timestamp=timestamp
                        ))
        
        except Exception as e:
            print(f"❌ Custom gesture detection error: {e}")
        
        return gestures
    
    def _is_spock_gesture(self, landmarks: List[Tuple[float, float, float]]) -> bool:
        """Detect Spock/Vulcan salute (split fingers)"""
        # Check if index+middle are together and ring+pinky are together
        # but there's a gap between middle and ring
        
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
        
        # Spock if middle-ring gap is significantly larger than the others
        return middle_ring_dist > 2 * max(index_middle_dist, ring_pinky_dist)
    
    def _is_ok_circle(self, landmarks: List[Tuple[float, float, float]]) -> bool:
        """Detect OK gesture (thumb + index forming circle)"""
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        
        # Distance between thumb tip and index tip
        distance = np.linalg.norm(np.array(thumb_tip[:2]) - np.array(index_tip[:2]))
        
        # OK gesture if distance is very small (forming circle)
        return distance < 0.05
    
    def _is_pinch(self, landmarks: List[Tuple[float, float, float]]) -> bool:
        """Detect pinch gesture"""
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        
        distance = np.linalg.norm(np.array(thumb_tip[:2]) - np.array(index_tip[:2]))
        
        # Pinch if fingers are close but not forming complete circle
        return 0.03 < distance < 0.08
    
    def _get_palm_center(self, landmarks: List[Tuple[float, float, float]]) -> Tuple[float, float]:
        """Calculate palm center from landmarks"""
        # Use landmarks 0, 5, 9, 13, 17 (base of palm and fingers)
        palm_points = [landmarks[i] for i in [0, 5, 9, 13, 17]]
        center_x = sum(p[0] for p in palm_points) / len(palm_points)
        center_y = sum(p[1] for p in palm_points) / len(palm_points)
        return (center_x, center_y)
    
    def _is_heart_hands(self, hand1_landmarks: List[Tuple[float, float, float]], 
                       hand2_landmarks: List[Tuple[float, float, float]]) -> bool:
        """Detect heart shape formed by two hands"""
        # Get thumb and index tips from both hands
        hand1_thumb = hand1_landmarks[4]
        hand1_index = hand1_landmarks[8]
        hand2_thumb = hand2_landmarks[4]
        hand2_index = hand2_landmarks[8]
        
        # Calculate distances between key points
        thumb_distance = np.linalg.norm(np.array(hand1_thumb[:2]) - np.array(hand2_thumb[:2]))
        index_distance = np.linalg.norm(np.array(hand1_index[:2]) - np.array(hand2_index[:2]))
        
        # Heart shape: thumbs and indexes should be close together
        # forming a heart-like shape
        return thumb_distance < 0.15 and index_distance < 0.15
    
    def detect_facial_fusion(self, frame: np.ndarray, face_info: Optional[Dict] = None,
                            detected_gestures: Optional[List[GestureEvent]] = None) -> List[GestureEvent]:
        """
        Detect facial fusion gestures (face + gesture combinations)
        
        Args:
            frame: Current video frame
            face_info: Dictionary with face detection info: {
                'recognized': bool,  # Whether face is recognized
                'name': str,         # Name if recognized
                'expression': str    # Facial expression (smile, wink, etc.)
            }
            If face_info dict is provided, face is assumed detected.
            detected_gestures: List of already detected gestures
        
        Returns:
            List of facial fusion gesture events
        """
        fusion_gestures = []
        
        if face_info is None or detected_gestures is None:
            return fusion_gestures
        
        current_time = time.time()
        
        # If face_info is provided, treat it as face detected
        # (presence of dict means face was detected)
        face_detected = True
        
        # Check each facial fusion definition
        for fusion_name, fusion_def in FACIAL_FUSION_GESTURES.items():
            # Check face requirements
            if fusion_def.get("face_required", False):
                if not face_detected:
                    continue
                
                # Check face recognition status
                if "face_recognized" in fusion_def:
                    if fusion_def["face_recognized"] != face_info.get("recognized", False):
                        continue
                
                # Check facial expression
                if "facial_expression" in fusion_def:
                    if fusion_def["facial_expression"] != face_info.get("expression", ""):
                        continue
                
                # Check if required gesture is detected
                required_gesture = fusion_def.get("gesture")
                if required_gesture:
                    gesture_detected = any(g.gesture_name == required_gesture for g in detected_gestures)
                    
                    if gesture_detected:
                        fusion_gestures.append(GestureEvent(
                            gesture_name=fusion_name,
                            confidence=0.85,
                            timestamp=current_time
                        ))
        
        return fusion_gestures
    
    def _detect_dynamic_gestures(self, static_gestures: List[GestureEvent], 
                                  timestamp: float) -> List[GestureEvent]:
        """Detect dynamic gestures based on motion + static gesture"""
        dynamic = []
        
        if len(self.hand_position_history) < 5:
            return dynamic
        
        # Get recent positions
        recent_positions = list(self.hand_position_history)[-10:]
        
        # Calculate motion vector
        if len(recent_positions) >= 2:
            start_pos = recent_positions[0]
            end_pos = recent_positions[-1]
            
            dx = end_pos[0] - start_pos[0]
            dy = end_pos[1] - start_pos[1]
            
            movement = np.sqrt(dx**2 + dy**2)
            
            # Check if there's significant movement
            if movement > 0.1:  # Threshold for significant movement
                motion_direction = self._classify_motion_direction(dx, dy)
                
                # Check if any static gesture is currently active
                for gesture in static_gestures:
                    # Match motion with gesture
                    dynamic_gesture = self._match_dynamic_gesture(
                        gesture.gesture_name, 
                        motion_direction,
                        movement
                    )
                    
                    if dynamic_gesture:
                        dynamic.append(GestureEvent(
                            gesture_name=dynamic_gesture,
                            confidence=0.8,
                            timestamp=timestamp,
                            motion_vector=(dx, dy)
                        ))
        
        return dynamic
    
    def _classify_motion_direction(self, dx: float, dy: float) -> str:
        """Classify motion direction"""
        angle = np.arctan2(dy, dx)
        
        if abs(dx) > abs(dy):
            return "left_to_right" if dx > 0 else "right_to_left"
        else:
            return "upward_to_downward" if dy > 0 else "downward_to_upward"
    
    def _match_dynamic_gesture(self, static_gesture: str, motion: str, 
                                movement: float) -> Optional[str]:
        """Match static gesture + motion to dynamic gesture"""
        for dynamic_name, dynamic_def in DYNAMIC_GESTURES.items():
            if (dynamic_def["gesture"] == static_gesture and 
                dynamic_def["motion"] == motion and
                movement * 640 >= dynamic_def.get("min_movement", 0)):  # Convert to pixels
                return dynamic_name
        return None
    
    def _detect_gesture_combinations(self, current_time: float) -> List[GestureEvent]:
        """Detect gesture combinations (sequences)"""
        combinations = []
        
        for combo_name, combo_def in COMBINATION_GESTURES.items():
            sequence = combo_def["sequence"]
            timeout = combo_def["timeout"]
            require_simultaneous = combo_def.get("require_simultaneous", False)
            
            if require_simultaneous:
                # Check if both gestures detected at the same time
                recent_gestures = [g for g in self.gesture_history 
                                 if current_time - g.timestamp < 1.0]
                
                gesture_names = [g.gesture_name for g in recent_gestures]
                
                if all(gesture in gesture_names for gesture in sequence):
                    combinations.append(GestureEvent(
                        gesture_name=combo_name,
                        confidence=0.9,
                        timestamp=current_time
                    ))
            else:
                # Check if gestures occurred in sequence within timeout
                if len(sequence) == 2:
                    recent = list(self.gesture_history)[-5:]
                    
                    for i in range(len(recent) - 1):
                        if (recent[i].gesture_name == sequence[0] and
                            recent[i+1].gesture_name == sequence[1] and
                            recent[i+1].timestamp - recent[i].timestamp < timeout):
                            
                            combinations.append(GestureEvent(
                                gesture_name=combo_name,
                                confidence=0.85,
                                timestamp=current_time
                            ))
                            break
        
        return combinations
    
    def handle_gesture_action(self, gesture_event: GestureEvent):
        """Handle action for detected gesture"""
        all_gestures = get_all_static_gestures()
        
        # Check if it's a static gesture
        if gesture_event.gesture_name in all_gestures:
            gesture_def = all_gestures[gesture_event.gesture_name]
            return self.action_handler.handle_gesture_action(
                gesture_def.function,
                gesture_event=gesture_event
            )
        
        # Check if it's a combination
        if gesture_event.gesture_name in COMBINATION_GESTURES:
            combo_def = COMBINATION_GESTURES[gesture_event.gesture_name]
            return self.action_handler.handle_gesture_action(
                combo_def["function"],
                gesture_event=gesture_event
            )
        
        # Check if it's a dynamic gesture
        if gesture_event.gesture_name in DYNAMIC_GESTURES:
            dynamic_def = DYNAMIC_GESTURES[gesture_event.gesture_name]
            return self.action_handler.handle_gesture_action(
                dynamic_def["function"],
                gesture_event=gesture_event
            )
        
        return {"action": "unknown", "success": False}
    
    def is_available(self) -> bool:
        """Check if recognizer is available"""
        return self.available
    
    def list_available_gestures(self) -> Dict[str, List[str]]:
        """List all available gestures by category"""
        return {
            "static": list(get_all_static_gestures().keys()),
            "dynamic": list(DYNAMIC_GESTURES.keys()),
            "combinations": list(COMBINATION_GESTURES.keys())
        }


import os  # Add missing import
