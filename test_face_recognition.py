#!/usr/bin/env python3
"""
Test Your Personal Face Recognition
See if the system recognizes you!
"""

import sys
import os
import cv2
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modules'))

from modules.automation.face_trainer import FaceRecognizer


def main():
    print("=" * 70)
    print("VATSAL AI - Personal Face Recognition Test")
    print("=" * 70)
    print()
    print("This will test if the system recognizes YOUR face!")
    print()
    print("📹 Starting webcam...")
    print("💡 Show your face to the camera")
    print("🎯 The system will try to recognize you")
    print()
    print("Press 'q' to quit")
    print("=" * 70)
    print()
    
    # Load recognizer
    recognizer = FaceRecognizer()
    
    if not recognizer.load_model():
        print("❌ No trained model found!")
        print("\n💡 First run: python train_vatsal_face.py")
        return
    
    print(f"✅ Model loaded successfully!")
    print(f"👥 Can recognize: {list(recognizer.labels.keys())}")
    print()
    
    # Open camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Could not open camera!")
        return
    
    print("🎥 Camera ready! Looking for faces...")
    print()
    
    recognition_count = {}
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = recognizer.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(100, 100)
            )
            
            # Recognize each face
            for (x, y, w, h) in faces:
                # Recognize
                name, confidence = recognizer.recognize_face(gray, (x, y, w, h))
                
                # Count recognitions
                if name not in recognition_count:
                    recognition_count[name] = 0
                recognition_count[name] += 1
                
                # Determine color based on confidence
                if confidence > 60:
                    color = (0, 255, 0)  # Green - good match
                    status = "✅ High Confidence"
                elif confidence > 40:
                    color = (0, 255, 255)  # Yellow - medium
                    status = "⚠️  Medium Confidence"
                else:
                    color = (0, 0, 255)  # Red - low
                    status = "❌ Low Confidence"
                
                # Draw rectangle
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 3)
                
                # Draw name
                text = f"{name.upper()} ({confidence:.0f}%)"
                cv2.putText(
                    frame,
                    text,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    color,
                    2
                )
                
                # Draw status
                cv2.putText(
                    frame,
                    status,
                    (x, y + h + 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    color,
                    2
                )
            
            # Show instructions
            cv2.putText(
                frame,
                "Press 'q' to quit",
                (10, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                1
            )
            
            # Display
            cv2.imshow('VATSAL - Face Recognition Test', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
    
    # Show statistics
    print("\n" + "=" * 70)
    print("📊 Recognition Statistics:")
    print("=" * 70)
    for name, count in recognition_count.items():
        print(f"  {name.upper()}: {count} times")
    print("=" * 70)
    print("\n✅ Test complete!")


if __name__ == "__main__":
    main()
