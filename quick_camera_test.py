#!/usr/bin/env python3
"""
Quick Camera Test - Find which camera index works
"""
import cv2
import time

def test_camera(index):
    """Test a single camera with proper Android/DroidCam initialization"""
    print(f"\n{'='*60}")
    print(f"Testing Camera {index}")
    print('='*60)
    
    cap = cv2.VideoCapture(index)
    
    if not cap.isOpened():
        print(f"❌ Camera {index} - Cannot open")
        return False
    
    # Configure camera
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    # Wait for camera
    print("⏳ Warming up (4 seconds)...")
    time.sleep(4)
    
    # Discard initial frames
    print("🔄 Testing frames...")
    working = False
    
    for i in range(15):
        ret, frame = cap.read()
        if ret and frame is not None:
            brightness = frame.mean()
            if brightness > 15:
                working = True
                print(f"   Frame {i+1}: ✅ OK (brightness: {brightness:.1f})")
            else:
                print(f"   Frame {i+1}: ⚫ BLACK (brightness: {brightness:.1f})")
        time.sleep(0.15)
    
    cap.release()
    
    if working:
        print(f"\n✅ Camera {index} WORKS!")
        return True
    else:
        print(f"\n❌ Camera {index} - Black screen")
        return False

# Test cameras 0, 1, 2
print("="*60)
print("🔍 QUICK CAMERA FINDER")
print("="*60)
print("\nTesting cameras 0, 1, 2...")

working_cameras = []

for i in range(3):
    if test_camera(i):
        working_cameras.append(i)

print("\n" + "="*60)
print("RESULTS")
print("="*60)

if working_cameras:
    print(f"✅ Working cameras: {working_cameras}")
    print(f"\n🎯 USE THIS: self.camera_index = {working_cameras[0]}")
    print(f"\nEdit line 200 in gesture_voice_activator.py:")
    print(f"   self.camera_index = {working_cameras[0]}")
else:
    print("❌ No working cameras found!")
    print("\n💡 Troubleshooting:")
    print("   1. Check DroidCam is running on phone")
    print("   2. Check DroidCam client is connected")
    print("   3. Close other apps using camera")
    print("   4. Restart DroidCam")
