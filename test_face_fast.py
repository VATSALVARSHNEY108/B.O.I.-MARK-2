#!/usr/bin/env python3
"""
Fast Face Recognition Test (Console Only)
No video display - just shows recognition results in console
MUCH FASTER than GUI versions
"""

import cv2
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modules'))

from modules.automation.face_trainer import FaceRecognizer


def main():
    print("=" * 70)
    print("⚡ FAST Face Recognition Test (Console Mode)")
    print("=" * 70)
    print()
    
    # Load model
    model_path = "biometric_data/faces/models/face_model.yml"
    
    if not os.path.exists(model_path):
        print("❌ Model not found!")
        print("💡 Train the model first: python train_vatsal_face.py")
        return
    
    print("🧠 Loading model...")
    recognizer = FaceRecognizer(model_path)
    
    if not recognizer.load_model():
        print("❌ Failed to load model!")
        return
    
    print(f"✅ Model loaded! Can recognize: {list(recognizer.labels.keys())}")
    print()
    print("📹 Opening camera...")
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Could not open camera!")
        return
    
    print("✅ Camera ready!")
    print()
    print("🎯 Testing face recognition...")
    print("   Press Ctrl+C to stop")
    print()
    print("=" * 70)
    print()
    
    recognition_count = {}
    frame_count = 0
    last_recognition = {}
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("❌ Failed to read from camera")
                break
            
            frame_count += 1
            
            # Process every 5 frames for speed
            if frame_count % 5 != 0:
                continue
            
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
                name, confidence = recognizer.recognize_face(gray, (x, y, w, h))
                
                # Track recognition
                if name not in recognition_count:
                    recognition_count[name] = 0
                recognition_count[name] += 1
                
                # Determine status
                if confidence > 70:
                    emoji = "✅"
                    status = "EXCELLENT"
                elif confidence > 50:
                    emoji = "👍"
                    status = "GOOD"
                else:
                    emoji = "⚠️"
                    status = "POOR"
                
                # Only print if changed or every 30 frames
                should_print = False
                if name not in last_recognition:
                    should_print = True
                elif abs(confidence - last_recognition[name]) > 5:
                    should_print = True
                elif frame_count % 30 == 0:
                    should_print = True
                
                if should_print:
                    print(f"{emoji} {name.upper()}: {confidence:.1f}% ({status}) - Count: {recognition_count[name]}")
                    last_recognition[name] = confidence
            
            # Show status every 60 frames
            if frame_count % 60 == 0:
                print(f"\n📊 Frame {frame_count} | Faces detected: {len(faces)}")
                if recognition_count:
                    print("Recognition stats:")
                    for name, count in recognition_count.items():
                        print(f"  • {name.upper()}: {count} times")
                print()
    
    except KeyboardInterrupt:
        print("\n\n⏹️ Stopped by user")
    
    finally:
        cap.release()
    
    # Final statistics
    print("\n" + "=" * 70)
    print("📊 FINAL STATISTICS")
    print("=" * 70)
    print(f"\nTotal frames processed: {frame_count}")
    print(f"Total recognitions: {sum(recognition_count.values())}")
    print()
    
    if recognition_count:
        print("Recognition breakdown:")
        for name, count in sorted(recognition_count.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {name.upper()}: {count} times")
    else:
        print("⚠️ No faces recognized")
    
    print("\n" + "=" * 70)
    print("✅ Test complete!")
    print()


if __name__ == "__main__":
    main()
