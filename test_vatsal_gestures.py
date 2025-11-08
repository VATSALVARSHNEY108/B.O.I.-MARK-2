#!/usr/bin/env python3
"""
Test VATSAL's Hand Gesture Detection
Based on Vatsal's own gesture photos!
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modules'))

from modules.automation.opencv_hand_gesture_detector import OpenCVHandGestureDetector
import time

def main():
    print("=" * 70)
    print("VATSAL AI - Personal Gesture Recognition Test")
    print("=" * 70)
    print()
    print("Based on Vatsal's gesture photos!")
    print()
    print("Gestures to try:")
    print("  👍 THUMBS UP - Shows approval, good job!")
    print("  ✌️  PEACE SIGN - Victory, 2 or 3 fingers")
    print("  👋 OPEN PALM - Activate voice listening (spread all 5 fingers)")
    print("  ✊ FIST - Stop/Cancel")
    print()
    print("Tips for best detection:")
    print("  • Wear your yellow bracelet for better hand detection")
    print("  • Keep good lighting (like in your photos)")
    print("  • Show gestures clearly to the camera")
    print("  • Hold each gesture for 1-2 seconds")
    print()
    print("=" * 70)
    print()
    
    detector = OpenCVHandGestureDetector()
    
    def on_gesture(command):
        print(f"🎯 Gesture command received: {command}")
    
    detector.set_gesture_callback(on_gesture)
    
    print("🚀 Starting detector...")
    result = detector.start(camera_index=0)
    
    if result['success']:
        print(f"✅ {result['message']}")
        print()
        print("👀 Looking for Vatsal...")
        print("💡 TIP: Try all the gestures from your photos!")
        print()
        print("Press 'q' in the video window to quit")
        print()
        
        try:
            while detector.is_running():
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
        
        detector.stop()
        
        # Show statistics
        stats = detector.get_stats()
        print("\n" + "=" * 70)
        print("📊 Your Gesture Statistics:")
        print("=" * 70)
        print(f"  👤 Faces detected: {stats['faces_detected']}")
        print(f"  🎯 Total gestures: {stats['gestures_detected']}")
        print(f"  👋 Greetings: {stats['greetings_given']}")
        print(f"  ✋ Open palms: {stats['open_palm_detected']}")
        print(f"  👍 Thumbs up: {stats['thumbs_up_detected']}")
        print(f"  ✌️  Peace signs: {stats['peace_sign_detected']}")
        print(f"  ✊ Fists: {stats['fist_detected']}")
        print("=" * 70)
        
        # Fun message based on stats
        if stats['thumbs_up_detected'] > 0:
            print("\n👍 Great job with the thumbs up!")
        if stats['peace_sign_detected'] > 0:
            print("✌️  Peace and victory!")
        if stats['open_palm_detected'] > 0:
            print("👋 You activated voice listening!")
            
    else:
        print(f"❌ {result['message']}")
        print("\n💡 Make sure your webcam is connected")
    
    print("\n✅ Test complete! Your gesture system is ready!")


if __name__ == "__main__":
    main()
