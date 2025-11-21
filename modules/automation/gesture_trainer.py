"""
Hand Gesture Training System for BOI (Barely Obeys Instructions)
Train the system to recognize custom hand gestures
"""

import cv2
import numpy as np
import os
import pickle
import json
from typing import Dict, List, Tuple
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler


class GestureTrainer:
    """Train custom hand gesture recognition using SVM"""
    
    def __init__(self, training_data_path: str = "biometric_data/hands"):
        self.training_data_path = training_data_path
        self.model_path = os.path.join(training_data_path, "models", "gesture_model.pkl")
        self.scaler_path = os.path.join(training_data_path, "models", "gesture_scaler.pkl")
        self.labels_path = os.path.join(training_data_path, "models", "gesture_labels.pkl")
        self.config_path = os.path.join(training_data_path, "models", "custom_gestures.json")
        
        # Hand detection using skin color
        self.lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        self.upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        self.classifier = None
        self.scaler = None
        self.labels = {}
        self.label_counter = 0
    
    def capture_gesture_samples(self, gesture_name: str, num_samples: int = 50) -> Dict:
        """
        Capture samples of a gesture from the camera
        
        Args:
            gesture_name: Name of the gesture to capture
            num_samples: Number of samples to capture (default: 50)
        
        Returns:
            Dictionary with success status and message
        """
        print(f"\n📸 Capturing samples for gesture: {gesture_name}")
        print("=" * 60)
        print(f"Please show the '{gesture_name}' gesture to the camera")
        print(f"We'll capture {num_samples} samples")
        print("Press SPACE when ready, ESC to cancel")
        print("=" * 60)
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return {'success': False, 'message': 'Could not access camera'}
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        samples = []
        sample_count = 0
        capturing = False
        
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            
            frame = cv2.flip(frame, 1)
            display_frame = frame.copy()
            
            # Detect hand
            hand_roi, hand_contour = self._detect_hand(frame)
            
            if hand_roi is not None:
                # Draw hand contour
                cv2.drawContours(display_frame, [hand_contour], 0, (0, 255, 0), 2)
                
                # If capturing, save the sample
                if capturing:
                    samples.append(hand_roi)
                    sample_count += 1
                    
                    if sample_count >= num_samples:
                        break
            
            # Display status
            status_text = f"Samples: {sample_count}/{num_samples}"
            cv2.putText(display_frame, status_text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            if not capturing:
                cv2.putText(display_frame, "Press SPACE to start capturing", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            else:
                cv2.putText(display_frame, "CAPTURING - Hold your gesture!", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
            cv2.putText(display_frame, "ESC to cancel", (10, frame.shape[0] - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            cv2.imshow(f'Capture Gesture: {gesture_name}', display_frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                cap.release()
                cv2.destroyAllWindows()
                return {'success': False, 'message': 'Capture cancelled by user'}
            elif key == 32:  # SPACE
                if hand_roi is not None:
                    capturing = True
                    print("🎬 Started capturing...")
        
        cap.release()
        cv2.destroyAllWindows()
        
        # Save samples to disk
        gesture_folder = os.path.join(self.training_data_path, gesture_name, "samples")
        os.makedirs(gesture_folder, exist_ok=True)
        
        for i, sample in enumerate(samples):
            sample_path = os.path.join(gesture_folder, f"sample_{i:03d}.png")
            cv2.imwrite(sample_path, sample)
        
        print(f"\n✅ Captured {len(samples)} samples for '{gesture_name}'")
        print(f"📁 Saved to: {gesture_folder}")
        
        return {
            'success': True,
            'message': f'Captured {len(samples)} samples',
            'samples_count': len(samples),
            'save_path': gesture_folder
        }
    
    def _detect_hand(self, frame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Detect hand in frame and return normalized ROI
        
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
            if area < 5000 or area > 50000:
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
    
    def _extract_features(self, roi: np.ndarray) -> np.ndarray:
        """
        Extract feature vector from hand ROI using HOG + Hu moments
        
        Args:
            roi: 128x128 grayscale image of hand
        
        Returns:
            Feature vector
        """
        # HOG features
        hog = cv2.HOGDescriptor(
            _winSize=(128, 128),
            _blockSize=(16, 16),
            _blockStride=(8, 8),
            _cellSize=(8, 8),
            _nbins=9
        )
        hog_features = hog.compute(roi).flatten()
        
        # Hu moments
        moments = cv2.moments(roi)
        hu_moments = cv2.HuMoments(moments).flatten()
        hu_moments = -np.sign(hu_moments) * np.log10(np.abs(hu_moments) + 1e-10)
        
        # Combine features
        features = np.concatenate([hog_features, hu_moments])
        
        return features
    
    def load_training_data(self) -> Tuple[List[np.ndarray], List[int], Dict]:
        """Load all training samples and extract features"""
        print("\n📂 Loading training data...")
        
        features_list = []
        labels_list = []
        
        if not os.path.exists(self.training_data_path):
            return [], [], {}
        
        for gesture_name in os.listdir(self.training_data_path):
            samples_folder = os.path.join(self.training_data_path, gesture_name, "samples")
            
            if not os.path.isdir(samples_folder):
                continue
            
            # Assign label to gesture
            if gesture_name not in self.labels:
                self.labels[gesture_name] = self.label_counter
                self.label_counter += 1
            
            gesture_label = self.labels[gesture_name]
            print(f"  ✋ Processing '{gesture_name}' (label: {gesture_label})")
            
            sample_count = 0
            for sample_file in os.listdir(samples_folder):
                if not sample_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    continue
                
                sample_path = os.path.join(samples_folder, sample_file)
                
                try:
                    roi = cv2.imread(sample_path, cv2.IMREAD_GRAYSCALE)
                    if roi is None:
                        continue
                    
                    # Ensure correct size
                    roi = cv2.resize(roi, (128, 128))
                    
                    # Extract features
                    features = self._extract_features(roi)
                    features_list.append(features)
                    labels_list.append(gesture_label)
                    sample_count += 1
                    
                except Exception as e:
                    print(f"    ⚠️  Error processing {sample_file}: {e}")
            
            print(f"    ✅ Loaded {sample_count} samples")
        
        return features_list, labels_list, self.labels
    
    def train(self) -> Dict:
        """Train the gesture recognition model"""
        print("\n🚀 Starting gesture recognition training...")
        print("=" * 60)
        
        features_list, labels_list, label_mapping = self.load_training_data()
        
        if len(features_list) == 0:
            return {
                'success': False,
                'message': 'No training data found! Capture gesture samples first.'
            }
        
        if len(set(labels_list)) < 2:
            return {
                'success': False,
                'message': 'Need at least 2 different gestures to train!'
            }
        
        print(f"\n📊 Training Statistics:")
        print(f"  Total samples: {len(features_list)}")
        print(f"  Gestures: {len(label_mapping)}")
        print(f"  Label mapping: {label_mapping}")
        print()
        
        # Convert to numpy arrays
        X = np.array(features_list)
        y = np.array(labels_list)
        
        print("🔧 Normalizing features...")
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        print("🧠 Training SVM classifier...")
        self.classifier = SVC(
            kernel='rbf',
            C=10,
            gamma='scale',
            probability=True,
            random_state=42
        )
        self.classifier.fit(X_scaled, y)
        
        # Save model
        print("💾 Saving model...")
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.classifier, f)
        
        with open(self.scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        
        with open(self.labels_path, 'wb') as f:
            pickle.dump(label_mapping, f)
        
        # Save gesture config
        gesture_config = {
            'gestures': {name: {'label': label} for name, label in label_mapping.items()},
            'num_gestures': len(label_mapping),
            'feature_size': X.shape[1],
            'trained_date': str(np.datetime64('now'))
        }
        
        with open(self.config_path, 'w') as f:
            json.dump(gesture_config, f, indent=2)
        
        print("\n✅ Training completed successfully!")
        print(f"📁 Model saved to: {self.model_path}")
        print(f"📁 Config saved to: {self.config_path}")
        
        # Calculate training accuracy
        train_predictions = self.classifier.predict(X_scaled)
        accuracy = np.mean(train_predictions == y) * 100
        
        print(f"\n📈 Training Accuracy: {accuracy:.2f}%")
        
        return {
            'success': True,
            'message': f'Training completed with {accuracy:.2f}% accuracy',
            'accuracy': accuracy,
            'num_samples': len(features_list),
            'num_gestures': len(label_mapping),
            'label_mapping': label_mapping
        }
    
    def predict_gesture(self, hand_roi: np.ndarray, min_confidence: float = 0.6) -> Tuple[str, float]:
        """
        Predict gesture from hand ROI
        
        Args:
            hand_roi: 128x128 grayscale hand image
            min_confidence: Minimum confidence threshold (default: 0.6)
        
        Returns:
            Tuple of (gesture_name, confidence)
        """
        if self.classifier is None:
            return "UNKNOWN", 0.0
        
        try:
            # Extract features
            features = self._extract_features(hand_roi)
            features = features.reshape(1, -1)
            
            # Normalize
            features_scaled = self.scaler.transform(features)
            
            # Predict with probability
            prediction = self.classifier.predict(features_scaled)[0]
            probabilities = self.classifier.predict_proba(features_scaled)[0]
            confidence = np.max(probabilities)
            
            # Check confidence threshold
            if confidence < min_confidence:
                return "UNKNOWN", confidence
            
            # Get gesture name from label
            label_to_name = {v: k for k, v in self.labels.items()}
            gesture_name = label_to_name.get(prediction, "UNKNOWN")
            
            return gesture_name, confidence
            
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            return "UNKNOWN", 0.0
    
    def load_model(self) -> bool:
        """Load trained model from disk"""
        try:
            if not os.path.exists(self.model_path):
                return False
            
            with open(self.model_path, 'rb') as f:
                self.classifier = pickle.load(f)
            
            with open(self.scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            
            with open(self.labels_path, 'rb') as f:
                self.labels = pickle.load(f)
            
            print(f"✅ Loaded gesture model with {len(self.labels)} gestures")
            return True
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
