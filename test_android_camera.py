#!/usr/bin/env python3
"""
Test Android Camera Connection
Helps identify which camera index works and tests the video feed
"""

import cv2
import time
import sys


def test_camera_index(index):
    """Test a specific camera index"""
    print(f"\n{'='*60}")
    print(f"🎥 Testing Camera Index: {index}")
    print('='*60)
    
    cap = cv2.VideoCapture(index)
    
    if not cap.isOpened():
        print(f"❌ Camera {index} could not be opened")
        return False
    
    # Give camera time to warm up (critical for DroidCam)
    print("⏳ Warming up camera (2 seconds)...")
    time.sleep(2)
    
    # Try to set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Get camera properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    print(f"📊 Camera Properties:")
    print(f"   Resolution: {width}x{height}")
    print(f"   FPS: {fps}")
    
    # Try to read a few frames (sometimes first frames are black)
    print("📹 Testing video feed (reading 10 frames)...")
    successful_reads = 0
    black_frames = 0
    
    for i in range(10):
        ret, frame = cap.read()
        if ret:
            successful_reads += 1
            # Check if frame is mostly black
            mean_brightness = frame.mean()
            if mean_brightness < 10:
                black_frames += 1
            print(f"   Frame {i+1}: {'✅ OK' if mean_brightness > 10 else '⚠️  Black'} (brightness: {mean_brightness:.1f})")
        else:
            print(f"   Frame {i+1}: ❌ Failed to read")
        time.sleep(0.1)
    
    cap.release()
    
    if successful_reads > 5 and black_frames < 8:
        print(f"\n✅ Camera {index} WORKS! ({successful_reads}/10 frames OK)")
        return True
    elif successful_reads > 0:
        print(f"\n⚠️  Camera {index} opens but mostly black frames ({black_frames}/10 black)")
        return False
    else:
        print(f"\n❌ Camera {index} NOT WORKING")
        return False


def test_camera_live(index):
    """Open live preview of camera"""
    print(f"\n{'='*60}")
    print(f"📹 Opening Live Preview - Camera {index}")
    print('='*60)
    print("Press 'q' to quit")
    print()
    
    cap = cv2.VideoCapture(index)
    
    if not cap.isOpened():
        print(f"❌ Could not open camera {index}")
        return
    
    # Critical: Wait for camera to warm up
    print("⏳ Warming up camera...")
    time.sleep(2)
    
    # Set properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Discard first few frames (often black with DroidCam)
    print("🔄 Discarding initial frames...")
    for _ in range(5):
        cap.read()
        time.sleep(0.1)
    
    print("✅ Camera ready! Showing live feed...")
    
    frame_count = 0
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("❌ Failed to read frame")
            break
        
        frame_count += 1
        
        # Flip for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Add info overlay
        mean_brightness = frame.mean()
        cv2.putText(frame, f"Camera {index} | Frame: {frame_count}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Brightness: {mean_brightness:.1f} | Press 'q' to quit", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        cv2.imshow(f'Android Camera Test - Index {index}', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print(f"\n✅ Closed camera {index}")


def main():
    print("=" * 60)
    print("📱 ANDROID CAMERA TEST UTILITY")
    print("=" * 60)
    print()
    print("This tool will help you:")
    print("  1. Find which camera index your Android device uses")
    print("  2. Test the video feed quality")
    print("  3. Show you the working camera index")
    print()
    
    # Test cameras 0-3
    print("🔍 Scanning for available cameras...")
    working_cameras = []
    
    for i in range(4):
        if test_camera_index(i):
            working_cameras.append(i)
    
    print("\n" + "=" * 60)
    print("📊 SCAN RESULTS")
    print("=" * 60)
    
    if not working_cameras:
        print("❌ No working cameras found!")
        print("\n💡 Troubleshooting:")
        print("   1. Make sure DroidCam is running on your phone")
        print("   2. Check that DroidCam client is connected on your computer")
        print("   3. Try closing other apps using the camera")
        print("   4. Restart DroidCam on both phone and computer")
    else:
        print(f"✅ Found {len(working_cameras)} working camera(s): {working_cameras}")
        print()
        
        # Ask to show live preview
        camera_to_use = working_cameras[0]
        print(f"🎥 Recommended camera index: {camera_to_use}")
        print()
        
        response = input(f"Show live preview of camera {camera_to_use}? (y/n): ").strip().lower()
        if response == 'y':
            test_camera_live(camera_to_use)
        
        print()
        print("=" * 60)
        print("🎯 NEXT STEPS")
        print("=" * 60)
        print(f"Use camera index: {camera_to_use}")
        print()
        print("In your Python code, change:")
        print(f"  cv2.VideoCapture(0)  →  cv2.VideoCapture({camera_to_use})")
        print()
        print("Important: Add this after opening camera:")
        print("  time.sleep(2)  # Wait for camera to warm up")
        print("  for _ in range(5): cap.read()  # Discard first frames")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
