#!/usr/bin/env python3
"""
Standalone Face Recognition Camera - No Module Imports
This version has all code inline to avoid cache issues
"""

import cv2
import os
import pickle
import numpy as np


def main():
    print("=" * 70)
    print("📹 VATSAL AI - Face Recognition Camera (Standalone)")
    print("=" * 70)
    print()
    
    model_path = "biometric_data/faces/models/face_model.yml"
    labels_path = "biometric_data/faces/models/labels.pkl"
    
    recognizer = None
    labels = {}
    reverse_labels = {}
    model_loaded = False
    distance_threshold = 48
    
    if os.path.exists(model_path):
        print("🧠 Loading face recognition model...")
        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create(
                radius=1,
                neighbors=8,
                grid_x=8,
                grid_y=8
            )
            
            print("   Loading model file...")
            recognizer.read(model_path)
            print("   Model file loaded!")
            
            if not os.path.exists(labels_path):
                labels_path = "biometric_data/faces/models/labels.pkl"
            
            with open(labels_path, 'rb') as f:
                labels = pickle.load(f)
            
            reverse_labels = {v: k for k, v in labels.items()}
            model_loaded = True
            
            print(f"✅ Ready to recognize: {list(labels.keys())}")
            print(f"📊 Distance threshold: {distance_threshold}")
        except Exception as e:
            print(f"⚠️  Model failed to load: {e}")
            model_loaded = False
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
    print("   Press '+' to increase threshold (more lenient)")
    print("   Press '-' to decrease threshold (more strict)")
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
                if model_loaded:
                    face_roi = gray[y:y+h, x:x+w]
                    face_roi = cv2.resize(face_roi, (200, 200))
                    face_roi = cv2.equalizeHist(face_roi)
                    
                    label, distance = recognizer.predict(face_roi)
                    
                    if distance > distance_threshold:
                        name = "Unknown"
                        confidence = 0.0
                    else:
                        name = reverse_labels.get(label, "Unknown")
                        
                        if distance < 30:
                            confidence = 100 - (distance * 0.5)
                        elif distance < 45:
                            confidence = 85 - ((distance - 30) * 0.67)
                        else:
                            confidence = max(50, 75 - ((distance - 45) * 1.5))
                    
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
            if model_loaded:
                info_text += f" | Threshold: {distance_threshold:.0f}"
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
                distance_threshold += 2
                print(f"Threshold increased to: {distance_threshold}")
            elif key == ord('-') or key == ord('_'):
                distance_threshold = max(10, distance_threshold - 2)
                print(f"Threshold decreased to: {distance_threshold}")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
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
