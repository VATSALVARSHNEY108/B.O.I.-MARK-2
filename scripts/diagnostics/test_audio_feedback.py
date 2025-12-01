#!/usr/bin/env python3
"""
Test Audio Feedback System
Quick test to verify audio signals work correctly
"""

import time
from modules.automation.audio_feedback import get_audio_feedback, play_listening_signal, play_success_signal

def main():
    print("🔊 Testing Audio Feedback System")
    print("=" * 60)
    
    audio = get_audio_feedback()
    
    print("\n✅ Audio feedback initialized")
    print(f"   Pygame available: {audio.listening_start_sound is not None if hasattr(audio, 'listening_start_sound') else False}")
    print(f"   Enabled: {audio.enabled}")
    print(f"   Volume: {audio.volume}")
    
    print("\n🎵 Playing sounds...")
    
    print("\n1. Listening Start Signal (rising tone)")
    play_listening_signal()
    time.sleep(1)
    
    print("2. Success Signal (high tone)")
    play_success_signal()
    time.sleep(1)
    
    print("3. Listening Stop Signal (falling tone)")
    audio.play_listening_stop()
    time.sleep(1)
    
    print("\n✅ Audio test complete!")
    print("\nIf you heard 3 beeps, the audio feedback is working correctly.")
    print("If not, the system will use fallback beeps on your local machine.")

if __name__ == "__main__":
    main()
