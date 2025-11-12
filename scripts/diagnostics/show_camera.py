#!/usr/bin/env python3
"""
Show Camera with Face Recognition
Opens a window to display what the camera sees with face recognition
"""

import cv2
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modules'))

from modules.automation.face_trainer import FaceRecognizer


def main():
    print("=" * 70)
    print("📹 VATSAL AI - Face Recognition Camera")
    print("=" * 70)
    print()
    
    model_path = "biometric_data/faces/models/face_model.yml"
    recognizer = None
    
    if os.path.exists(model_path):
        print("🧠 Loading face recognition model...")
        recognizer = FaceRecognizer(model_path)
        if recognizer.load_model():
            print(f"✅ Ready to recognize: {list(recognizer.labels.keys())}")
            print(f"📊 Distance threshold: {recognizer.distance_threshold}")
        else:
            print("⚠️  Model failed to load - face detection only")
            recognizer = None
    else:
        print("⚠️  No trained model found")
        print("   Run: python train_vatsal_face.py")
    
    print()
    print("📹 Opening camera...")
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Could not open camera!")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("✅ Camera ready!")
    print()
    print("🎯 Controls:")
    print("   Press 'q' to quit")
    print("   Press 's' to save snapshot")
    print("   Press '+' to increase threshold")
    print("   Press '-' to decrease threshold")
    print()
    print("=" * 70)
    print()
    
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
            
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(100, 100)
            )
            
            for (x, y, w, h) in faces:
                if recognizer and recognizer.model_loaded:
                    name, confidence, distance = recognizer.recognize_face(gray, (x, y, w, h))
                    
                    if name == "Unknown":
                        color = (0, 0, 255)
                        name_text = "UNKNOWN"
                        confidence_text = f"Distance: {distance:.1f}"
                        status_text = "ACCESS DENIED"
                    elif confidence > 75:
                        color = (0, 255, 0)
                        name_text = name.upper()
                        confidence_text = f"{confidence:.1f}%"
                        status_text = f"Distance: {distance:.1f}"
                    elif confidence > 60:
                        color = (0, 255, 255)
                        name_text = name.upper()
                        confidence_text = f"{confidence:.1f}%"
                        status_text = f"Distance: {distance:.1f}"
                    else:
                        color = (0, 165, 255)
                        name_text = name.upper()
                        confidence_text = f"{confidence:.1f}%"
                        status_text = f"Distance: {distance:.1f}"
                else:
                    color = (255, 0, 0)
                    name_text = "Face Detected"
                    confidence_text = "No Model"
                    status_text = "Training Required"
                
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 3)
                
                overlay = frame.copy()
                cv2.rectangle(overlay, (x, y - 80), (x + w, y), (0, 0, 0), -1)
                cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
                
                cv2.putText(frame, name_text, (x + 5, y - 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                
                cv2.putText(frame, confidence_text, (x + 5, y - 25),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)
                
                cv2.putText(frame, status_text, (x + 5, y - 5),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
            
            info_text = f"Faces: {len(faces)}"
            if recognizer and recognizer.model_loaded:
                info_text += f" | Threshold: {recognizer.distance_threshold:.0f}"
            info_text += " | q=quit s=save +/- adjust"
            
            cv2.putText(frame, info_text, (10, frame.shape[0] - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            cv2.imshow('VATSAL AI - Face Recognition', frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("\n⏹️  Stopping camera...")
                break
            elif key == ord('s'):
                snapshot_count += 1
                filename = f"snapshot_{snapshot_count}.jpg"
                cv2.imwrite(filename, frame)
                print(f"📸 Saved: {filename}")
            elif key == ord('+') or key == ord('='):
                if recognizer:
                    recognizer.set_threshold(recognizer.distance_threshold + 2)
            elif key == ord('-') or key == ord('_'):
                if recognizer:
                    recognizer.set_threshold(max(10, recognizer.distance_threshold - 2))
    
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
