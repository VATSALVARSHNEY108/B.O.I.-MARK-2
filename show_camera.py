#!/usr/bin/env python3
"""
Show Camera with Face Detection
Opens a window to display what the camera sees with face detection
"""

import cv2
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modules'))

from modules.automation.face_trainer import FaceRecognizer


def main():
    print("=" * 70)
    print("📹 Camera Display with Face Recognition")
    print("=" * 70)
    print()
    
    # Load model
    model_path = "biometric_data/faces/models/face_model.yml"
    recognizer = None
    
    if os.path.exists(model_path):
        print("🧠 Loading face recognition model...")
        recognizer = FaceRecognizer(model_path)
        if recognizer.load_model():
            print(f"✅ Model loaded! Can recognize: {list(recognizer.labels.keys())}")
        else:
            print("⚠️  Model failed to load - will only show face detection")
            recognizer = None
    else:
        print("⚠️  No trained model found - will only show face detection")
        print("   Run: python train_vatsal_face.py")
    
    print()
    print("📹 Opening camera...")
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Could not open camera!")
        return
    
    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("✅ Camera ready!")
    print()
    print("🎯 Instructions:")
    print("   • Look at the camera")
    print("   • Press 'q' to quit")
    print("   • Press 's' to save a snapshot")
    print()
    print("=" * 70)
    print()
    
    # Face detector
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    
    snapshot_count = 0
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("❌ Failed to read from camera")
                break
            
            # Flip for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Convert to grayscale for detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(100, 100)
            )
            
            # Process each face
            for (x, y, w, h) in faces:
                if recognizer and recognizer.model_loaded:
                    # Recognize the face
                    name, confidence = recognizer.recognize_face(gray, (x, y, w, h))
                    
                    # Color based on confidence
                    if confidence > 60:
                        color = (0, 255, 0)  # Green
                        status = "EXCELLENT"
                    elif confidence > 40:
                        color = (0, 255, 255)  # Yellow
                        status = "GOOD"
                    else:
                        color = (0, 165, 255)  # Orange
                        status = "POOR"
                    
                    name_text = f"{name.upper()}"
                    confidence_text = f"{confidence:.1f}%"
                    status_text = f"Match: {status}"
                else:
                    # Just show face detection
                    color = (255, 0, 0)  # Blue
                    name_text = "Face Detected"
                    confidence_text = "N/A"
                    status_text = "No Model"
                
                # Draw rectangle around face (thick border)
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 4)
                
                # Draw semi-transparent background for text
                overlay = frame.copy()
                cv2.rectangle(overlay, (x, y - 80), (x + w, y), (0, 0, 0), -1)
                cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
                
                # Draw name (large)
                cv2.putText(frame, name_text, (x + 5, y - 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                
                # Draw confidence percentage (LARGE and bold)
                cv2.putText(frame, confidence_text, (x + 5, y - 25),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
                
                # Draw status
                cv2.putText(frame, status_text, (x + 5, y - 5),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # Add instructions at bottom
            info_text = f"Faces: {len(faces)} | Press 'q' to quit, 's' to save snapshot"
            cv2.putText(frame, info_text, (10, frame.shape[0] - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Show frame
            cv2.imshow('VATSAL AI - Face Recognition', frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("\n⏹️  Stopping camera...")
                break
            elif key == ord('s'):
                # Save snapshot
                snapshot_count += 1
                filename = f"snapshot_{snapshot_count}.jpg"
                cv2.imwrite(filename, frame)
                print(f"📸 Saved: {filename}")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
    
    print("\n" + "=" * 70)
    print("✅ Camera closed!")
    if snapshot_count > 0:
        print(f"📸 Saved {snapshot_count} snapshot(s)")
    print("=" * 70)


if __name__ == "__main__":
    main()
