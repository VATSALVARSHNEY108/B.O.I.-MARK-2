#!/usr/bin/env python3
"""
Demo: OpenCV Hand Gesture and Face Detection
Works without MediaPipe - pure OpenCV implementation
"""

import sys
import os

# Add modules to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modules'))

from modules.automation.opencv_hand_gesture_detector import OpenCVHandGestureDetector


def main():
    print("=" * 70)
    print("VATSAL AI - OpenCV Hand Gesture & Face Detection Demo")
    print("=" * 70)
    print()
    print("Features:")
    print("  ✅ Face Detection (Haar Cascade)")
    print("  ✅ Hand Gesture Recognition (Color + Contour Analysis)")
    print("  ✅ Real-time Processing")
    print("  ✅ No MediaPipe Required!")
    print()
    print("Gestures:")
    print("  👋 OPEN PALM - Activate voice listening")
    print("  ✊ FIST - Stop/Cancel")
    print()
    print("Controls:")
    print("  Press 'q' in the video window to quit")
    print("=" * 70)
    print()
    
    # Create detector
    detector = OpenCVHandGestureDetector()
    
    # Set callbacks
    def on_gesture_detected(command):
        print(f"🎯 Gesture callback triggered with command: {command}")
    
    detector.set_gesture_callback(on_gesture_detected)
    
    # Start detection
    print("🚀 Starting detector...")
    result = detector.start(camera_index=0)
    
    if result['success']:
        print(f"✅ {result['message']}")
        print()
        print("👀 Looking for your face and hand gestures...")
        print("💡 TIP: Show your open palm when your face is detected")
        print()
        
        try:
            # Keep running until stopped
            import time
            while detector.is_running():
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
        
        # Stop detector
        detector.stop()
        
        # Show statistics
        stats = detector.get_stats()
        print("\n" + "=" * 70)
        print("📊 Detection Statistics:")
        print("=" * 70)
        for key, value in stats.items():
            print(f"  {key}: {value}")
        print("=" * 70)
    else:
        print(f"❌ {result['message']}")
        print("\n💡 Make sure you have a webcam connected and permissions are granted")
    
    print("\n✅ Demo complete!")


if __name__ == "__main__":
    main()
