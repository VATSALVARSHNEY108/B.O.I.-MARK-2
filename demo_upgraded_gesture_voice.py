#!/usr/bin/env python3
"""
Demo: Upgraded Gesture Voice Activator with Android Camera Support
Tests the new auto-detection and Android/DroidCam compatibility
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modules'))

from modules.automation.gesture_voice_activator import create_gesture_voice_activator


def on_speech_detected(text: str):
    """Callback when speech is recognized"""
    print(f"\n{'='*60}")
    print(f"🎤 SPEECH RECOGNIZED: {text}")
    print(f"{'='*60}\n")


def main():
    print("=" * 70)
    print("🚀 UPGRADED GESTURE VOICE ACTIVATOR DEMO")
    print("=" * 70)
    print()
    print("✨ NEW FEATURES:")
    print("   ✅ Auto-detects Android/DroidCam camera")
    print("   ✅ Fixes black screen issues")
    print("   ✅ Proper camera warm-up (2 seconds)")
    print("   ✅ Discards initial black frames")
    print("   ✅ Works with camera index 0, 1, 2, or 3")
    print()
    print("Choose mode:")
    print("   1. Auto-detect camera (recommended)")
    print("   2. Manually specify camera index")
    print()
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        camera_index = int(input("Enter camera index (0-3): ").strip())
        print(f"\n🎥 Using camera index: {camera_index}")
        activator = create_gesture_voice_activator(
            on_speech_callback=on_speech_detected,
            camera_index=camera_index
        )
    else:
        print("\n🔍 Auto-detecting camera...")
        activator = create_gesture_voice_activator(
            on_speech_callback=on_speech_detected
        )
    
    print()
    print("Starting gesture voice activator...")
    print()
    
    activator.run()
    
    print("\n✅ Demo completed!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
