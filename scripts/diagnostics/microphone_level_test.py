#!/usr/bin/env python3
"""
Real-time Microphone Level Tester
Shows audio input levels to help diagnose microphone issues
"""

import speech_recognition as sr
import time
import sys

def test_microphone_levels():
    """Test microphone and show real-time audio levels"""
    
    print("=" * 70)
    print("🎤 REAL-TIME MICROPHONE LEVEL TEST")
    print("=" * 70)
    
    recognizer = sr.Recognizer()
    
    # List all microphones
    print("\n📋 Available Microphones:")
    mic_list = sr.Microphone.list_microphone_names()
    
    if not mic_list:
        print("❌ No microphones found!")
        return
    
    for idx, name in enumerate(mic_list):
        print(f"   [{idx}] {name}")
    
    # Ask which microphone to use
    print("\n" + "=" * 70)
    mic_index = input("Enter microphone number to test (or press Enter for default): ").strip()
    
    if mic_index:
        try:
            mic_index = int(mic_index)
        except:
            print("Invalid number, using default microphone")
            mic_index = None
    else:
        mic_index = None
    
    print("\n" + "=" * 70)
    print("🔊 TESTING AUDIO LEVELS")
    print("=" * 70)
    
    try:
        # Open microphone
        if mic_index is not None:
            microphone = sr.Microphone(device_index=mic_index)
            print(f"\n✅ Using microphone [{mic_index}]: {mic_list[mic_index]}")
        else:
            microphone = sr.Microphone()
            print("\n✅ Using DEFAULT microphone")
        
        with microphone as source:
            print("\n🔊 Adjusting for ambient noise (2 seconds)...")
            print("   Please be QUIET for 2 seconds...\n")
            
            recognizer.adjust_for_ambient_noise(source, duration=2)
            
            print(f"✅ Baseline energy threshold: {recognizer.energy_threshold:.2f}")
            print("\n" + "=" * 70)
            print("🎤 MONITORING AUDIO LEVELS - SPEAK NOW!")
            print("   (Press Ctrl+C to stop)")
            print("=" * 70)
            print("\nEnergy Level | Visual Bar")
            print("-" * 70)
            
            # Monitor for 30 seconds or until user stops
            for i in range(60):  # 60 iterations of 0.5 seconds each = 30 seconds
                try:
                    # Listen for 0.5 seconds
                    audio = recognizer.listen(source, timeout=0.5, phrase_time_limit=0.5)
                    
                    # Get raw audio data
                    audio_data = audio.get_raw_data()
                    
                    # Calculate simple energy level
                    import array
                    audio_array = array.array('h', audio_data)
                    
                    # Calculate RMS (Root Mean Square) energy
                    if len(audio_array) > 0:
                        sum_squares = sum(x * x for x in audio_array)
                        rms = (sum_squares / len(audio_array)) ** 0.5
                        
                        # Create visual bar
                        bar_length = int(min(50, rms / 100))
                        bar = "█" * bar_length
                        
                        # Determine if this is loud enough
                        if rms > recognizer.energy_threshold:
                            status = "✅ LOUD ENOUGH"
                        elif rms > recognizer.energy_threshold * 0.5:
                            status = "⚠️  TOO QUIET"
                        else:
                            status = "❌ VERY QUIET"
                        
                        print(f"{rms:>10.1f} | {bar:<50} {status}")
                    
                except sr.WaitTimeoutError:
                    # No sound detected
                    print(f"{'0.0':>10} | {'':50} ❌ SILENCE")
                
                except KeyboardInterrupt:
                    print("\n\n⏹️  Stopped by user")
                    break
            
            print("\n" + "=" * 70)
            print("📊 RESULTS ANALYSIS")
            print("=" * 70)
            print(f"\n✅ Energy Threshold: {recognizer.energy_threshold:.2f}")
            print("\n💡 What this means:")
            print(f"   - Sound needs to be ABOVE {recognizer.energy_threshold:.2f} to be detected")
            print("   - If all your bars were below this, microphone is too quiet")
            print("\n🔧 SOLUTIONS:")
            print("   1. Increase microphone volume in system settings")
            print("   2. Speak LOUDER and CLOSER to microphone")
            print("   3. Try a different microphone (if you have multiple)")
            print("   4. Check if microphone is MUTED in system settings")
            print("   5. Select the correct microphone as default input device")
            
            print("\n" + "=" * 70)
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


def test_specific_microphone(mic_index):
    """Quick test of a specific microphone"""
    print(f"\n🎤 Testing microphone {mic_index}...")
    
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 100  # Very sensitive
    
    try:
        with sr.Microphone(device_index=mic_index) as source:
            print("✅ Microphone opened")
            print("🔊 Speak NOW (5 seconds)...")
            
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            print("✅ Audio captured! Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"✅ SUCCESS! You said: '{text}'")
            return True
            
    except sr.WaitTimeoutError:
        print("❌ Timeout - no speech detected")
        return False
    except sr.UnknownValueError:
        print("⚠️  Audio captured but couldn't understand")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    print("\n" + "🎤" * 35)
    print("   MICROPHONE LEVEL DIAGNOSTIC")
    print("🎤" * 35)
    
    print("\n📋 What this tool does:")
    print("   1. Shows you REAL-TIME audio levels from your microphone")
    print("   2. Helps you see if microphone is actually picking up sound")
    print("   3. Tells you if volume is loud enough")
    
    print("\n" + "=" * 70)
    
    test_microphone_levels()
    
    print("\n💡 Want to try a different microphone?")
    retry = input("Enter 'y' to test another microphone, or press Enter to exit: ").strip().lower()
    
    if retry == 'y':
        mic_list = sr.Microphone.list_microphone_names()
        for idx, name in enumerate(mic_list):
            print(f"   [{idx}] {name}")
        
        mic_num = input("\nEnter microphone number to test: ").strip()
        if mic_num:
            try:
                test_specific_microphone(int(mic_num))
            except:
                print("Invalid number")
    
    print("\n" + "=" * 70)
    print("🏁 TEST COMPLETE")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
