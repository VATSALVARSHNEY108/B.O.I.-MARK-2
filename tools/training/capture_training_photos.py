#!/usr/bin/env python3
"""
Capture Training Photos from Camera
Shows live camera preview and captures photos for face recognition training
"""

import cv2
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def capture_training_photos(person_name: str = "boi", num_photos: int = 20):
    """
    Capture training photos from camera with live preview
    
    Args:
        person_name: Name of the person being photographed
        num_photos: Number of photos to capture
    """
    
    print("=" * 70)
    print("📸 CAMERA PHOTO CAPTURE FOR TRAINING")
    print("=" * 70)
    print(f"\n👤 Capturing photos for: {person_name.upper()}")
    print(f"📊 Target: {num_photos} photos")
    print()
    print("🎯 Instructions:")
    print("  • Look at the camera")
    print("  • Press SPACE to capture a photo")
    print("  • Try different angles, expressions, and lighting")
    print("  • Press 'q' to quit")
    print()
    print("=" * 70)
    print()
    
    # Create folder for this person
    save_folder = os.path.join("biometric_data", "faces", person_name.lower(), "training")
    os.makedirs(save_folder, exist_ok=True)
    
    # Initialize camera
    print("🎥 Opening camera...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open camera!")
        print("💡 Make sure your camera is connected and not being used by another app")
        return
    
    # Set camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Load face detector
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    
    photo_count = 0
    print("✅ Camera ready! Press SPACE to capture photos\n")
    
    while photo_count < num_photos:
        ret, frame = cap.read()
        
        if not ret:
            print("❌ Error: Failed to grab frame")
            break
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(100, 100)
        )
        
        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            # Draw green rectangle around face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Add label
            cv2.putText(frame, "Face Detected", (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Display info on screen
        info_text = f"Photos: {photo_count}/{num_photos} | Press SPACE to capture | Q to quit"
        cv2.putText(frame, info_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Show face count
        face_count_text = f"Faces detected: {len(faces)}"
        cv2.putText(frame, face_count_text, (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        # Show the frame
        cv2.imshow(f'Capture Training Photos - {person_name.upper()}', frame)
        
        # Check for key press
        key = cv2.waitKey(1) & 0xFF
        
        # Press SPACE to capture photo
        if key == ord(' '):
            if len(faces) > 0:
                # Save the photo
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                filename = f"{person_name}_{timestamp}.jpg"
                filepath = os.path.join(save_folder, filename)
                
                cv2.imwrite(filepath, frame)
                photo_count += 1
                
                print(f"✅ Photo {photo_count}/{num_photos} saved: {filename}")
                
                # Flash effect (brief white screen)
                white_frame = frame.copy()
                white_frame[:] = (255, 255, 255)
                cv2.imshow(f'Capture Training Photos - {person_name.upper()}', white_frame)
                cv2.waitKey(100)
            else:
                print("⚠️  No face detected! Move closer to the camera")
        
        # Press 'q' to quit
        elif key == ord('q'):
            print("\n⏹️  Capture stopped by user")
            break
    
    # Release camera and close windows
    cap.release()
    cv2.destroyAllWindows()
    
    print()
    print("=" * 70)
    if photo_count > 0:
        print(f"🎉 SUCCESS! Captured {photo_count} photos")
        print(f"📂 Saved to: {save_folder}")
        print()
        print("✅ Next Steps:")
        print("  1. Run: python train_boi_face.py")
        print("  2. Then test: python test_face_recognition.py")
    else:
        print("❌ No photos captured")
    print("=" * 70)


if __name__ == "__main__":
    # Get person name from command line or use default
    person_name = sys.argv[1] if len(sys.argv) > 1 else "boi"
    num_photos = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    
    capture_training_photos(person_name, num_photos)
