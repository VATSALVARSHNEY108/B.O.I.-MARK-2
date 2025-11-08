"""
Face Recognition Training System for VATSAL AI
Train the system to recognize specific people from their photos
"""

import cv2
import numpy as np
import os
import pickle
from typing import Dict, List, Tuple


class FaceTrainer:
    """Train face recognition model from images"""
    
    def __init__(self, training_data_path: str = "biometric_data/faces"):
        self.training_data_path = training_data_path
        self.model_path = os.path.join(training_data_path, "models", "face_model.yml")
        self.labels_path = os.path.join(training_data_path, "models", "labels.pkl")
        
        # Initialize face detector and recognizer
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Use LBPH (Local Binary Patterns Histograms) recognizer with balanced parameters
        # Optimized for faster loading while maintaining good accuracy
        # Higher threshold = more lenient matching
        self.recognizer = cv2.face.LBPHFaceRecognizer_create(
            radius=1,
            neighbors=8,
            grid_x=8,
            grid_y=8,
            threshold=150.0
        )
        
        self.labels = {}
        self.label_counter = 0
    
    def load_training_images(self) -> Tuple[List[np.ndarray], List[int], Dict]:
        """Load all training images and extract faces"""
        print("📂 Loading training images...")
        
        faces = []
        labels_list = []
        
        # Scan all person folders
        for person_name in os.listdir(self.training_data_path):
            person_folder = os.path.join(self.training_data_path, person_name, "training")
            
            if not os.path.isdir(person_folder):
                continue
            
            # Assign label to this person
            if person_name not in self.labels:
                self.labels[person_name] = self.label_counter
                self.label_counter += 1
            
            person_label = self.labels[person_name]
            print(f"  👤 Processing {person_name} (label: {person_label})")
            
            # Load all images for this person
            image_count = 0
            for image_file in os.listdir(person_folder):
                if not image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    continue
                
                image_path = os.path.join(person_folder, image_file)
                
                try:
                    # Read image
                    img = cv2.imread(image_path)
                    if img is None:
                        continue
                    
                    # Convert to grayscale
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    
                    # Detect faces
                    detected_faces = self.face_cascade.detectMultiScale(
                        gray,
                        scaleFactor=1.1,
                        minNeighbors=5,
                        minSize=(100, 100)
                    )
                    
                    # Extract each face
                    for (x, y, w, h) in detected_faces:
                        face_roi = gray[y:y+h, x:x+w]
                        # Resize to standard size
                        face_roi = cv2.resize(face_roi, (200, 200))
                        
                        # Apply histogram equalization for better contrast
                        face_roi = cv2.equalizeHist(face_roi)
                        
                        # Add original face
                        faces.append(face_roi)
                        labels_list.append(person_label)
                        image_count += 1
                        
                        # Data augmentation: Add horizontally flipped version
                        flipped = cv2.flip(face_roi, 1)
                        faces.append(flipped)
                        labels_list.append(person_label)
                        image_count += 1
                
                except Exception as e:
                    print(f"    ⚠️  Error processing {image_file}: {e}")
            
            print(f"    ✅ Loaded {image_count} face samples")
        
        return faces, labels_list, self.labels
    
    def train(self) -> Dict:
        """Train the face recognition model"""
        print("\n🚀 Starting face recognition training...")
        print("=" * 60)
        
        # Load training data
        faces, labels_list, label_mapping = self.load_training_images()
        
        if len(faces) == 0:
            return {
                'success': False,
                'message': 'No training images found! Add photos first.'
            }
        
        print(f"\n📊 Training Statistics:")
        print(f"  Total face samples: {len(faces)}")
        print(f"  People to recognize: {len(label_mapping)}")
        print(f"  Label mapping: {label_mapping}")
        print()
        
        # Train the model
        print("🧠 Training model...")
        try:
            self.recognizer.train(faces, np.array(labels_list))
            
            # Save the model
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            self.recognizer.save(self.model_path)
            
            # Save the label mapping
            with open(self.labels_path, 'wb') as f:
                pickle.dump(label_mapping, f)
            
            print(f"✅ Model saved to: {self.model_path}")
            print(f"✅ Labels saved to: {self.labels_path}")
            print()
            print("=" * 60)
            print("🎉 Training complete!")
            print()
            print("You can now use the trained model to recognize:")
            for name, label in label_mapping.items():
                print(f"  👤 {name.upper()} (label: {label})")
            
            return {
                'success': True,
                'message': f'Successfully trained on {len(faces)} samples',
                'samples': len(faces),
                'people': len(label_mapping),
                'labels': label_mapping,
                'model_path': self.model_path
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Training failed: {str(e)}'
            }
    
    def add_person_photos(self, person_name: str, photo_paths: List[str]) -> Dict:
        """Add photos for a new person"""
        person_folder = os.path.join(self.training_data_path, person_name, "training")
        os.makedirs(person_folder, exist_ok=True)
        
        copied = 0
        for photo_path in photo_paths:
            if os.path.exists(photo_path):
                filename = os.path.basename(photo_path)
                dest = os.path.join(person_folder, filename)
                
                # Copy file
                import shutil
                shutil.copy2(photo_path, dest)
                copied += 1
        
        return {
            'success': True,
            'message': f'Added {copied} photos for {person_name}',
            'folder': person_folder
        }


class FaceRecognizer:
    """Use trained model to recognize faces in real-time"""
    
    def __init__(self, model_path: str = "biometric_data/faces/models/face_model.yml"):
        self.model_path = model_path
        self.labels_path = model_path.replace('.yml', '_labels.pkl')
        
        # Initialize face detector
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Initialize recognizer with same balanced parameters as training
        # Higher threshold = more lenient matching
        self.recognizer = cv2.face.LBPHFaceRecognizer_create(
            radius=1,
            neighbors=8,
            grid_x=8,
            grid_y=8,
            threshold=150.0
        )
        self.labels = {}
        self.reverse_labels = {}
        
        self.model_loaded = False
    
    def load_model(self) -> bool:
        """Load trained model"""
        try:
            print("   Loading model file... (this may take a moment)")
            import sys
            sys.stdout.flush()
            
            # Load the model
            self.recognizer.read(self.model_path)
            print("   Model file loaded successfully!")
            
            # Load labels
            labels_path = self.model_path.replace('.yml', '_labels.pkl')
            if not os.path.exists(labels_path):
                labels_path = "biometric_data/faces/models/labels.pkl"
            
            with open(labels_path, 'rb') as f:
                self.labels = pickle.load(f)
            
            # Create reverse mapping (label -> name)
            self.reverse_labels = {v: k for k, v in self.labels.items()}
            
            self.model_loaded = True
            print(f"✅ Model loaded: {len(self.labels)} people")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
            return False
    
    def recognize_face(self, gray_frame: np.ndarray, bbox: Tuple[int, int, int, int]) -> Tuple[str, float]:
        """
        Recognize a face from a frame
        Returns: (person_name, confidence)
        """
        if not self.model_loaded:
            return "Unknown", 0.0
        
        x, y, w, h = bbox
        face_roi = gray_frame[y:y+h, x:x+w]
        face_roi = cv2.resize(face_roi, (200, 200))
        
        # Apply histogram equalization (same as training)
        face_roi = cv2.equalizeHist(face_roi)
        
        # Predict
        label, distance = self.recognizer.predict(face_roi)
        
        # IMPORTANT: Reject if distance is too high (not a good match)
        # For this simplified model, distance > 70 means it's likely NOT the trained person
        if distance > 70:
            return "Unknown", 0.0
        
        # Get person name
        person_name = self.reverse_labels.get(label, "Unknown")
        
        # Convert distance to confidence percentage
        # In LBPH, lower distance = better match
        # Only accept distances < 70 for trained person
        if distance < 40:
            confidence_score = 100 - (distance * 0.3)
        elif distance < 55:
            confidence_score = 88 - ((distance - 40) * 1.0)
        elif distance < 70:
            confidence_score = 73 - ((distance - 55) * 1.5)
        else:
            confidence_score = 0.0
        
        return person_name, confidence_score


# Convenience functions
def train_face_model(training_data_path: str = "biometric_data/faces") -> Dict:
    """Quick function to train the model"""
    trainer = FaceTrainer(training_data_path)
    return trainer.train()


def load_face_recognizer(model_path: str = "biometric_data/faces/models/face_model.yml") -> FaceRecognizer:
    """Quick function to load a trained model"""
    recognizer = FaceRecognizer(model_path)
    recognizer.load_model()
    return recognizer
