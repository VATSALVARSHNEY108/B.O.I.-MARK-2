#!/usr/bin/env python3
"""
Quick Microphone Test
Tests if your microphone is working and accessible
"""

import speech_recognition as sr

def test_microphone():
    print("=" * 60)
    print("🎤 MICROPHONE TEST")
    print("=" * 60)
    
    recognizer = sr.Recognizer()
    
    # List all microphones
    print("\n📋 Available Microphones:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"   {index}: {name}")
    
    print("\n" + "=" * 60)
    print("🧪 TESTING DEFAULT MICROPHONE")
    print("=" * 60)
    
    try:
        with sr.Microphone() as source:
            print("\n✅ Microphone accessed successfully!")
            print("🔊 Adjusting for ambient noise (2 seconds)...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            
            print("\n🎤 SPEAK NOW! Say something like 'hello' or 'testing'...")
            print("   (You have 10 seconds)\n")
            
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            
            print("✅ Audio captured! Processing...")
            
            try:
                text = recognizer.recognize_google(audio)
                print(f"\n🎉 SUCCESS! You said: '{text}'")
                print("\n✅ Your microphone is working perfectly!")
                return True
                
            except sr.UnknownValueError:
                print("\n⚠️  Audio captured but could not understand")
                print("💡 Try speaking louder and clearer")
                return False
                
            except sr.RequestError as e:
                print(f"\n❌ Google Speech Recognition error: {e}")
                print("💡 Check your internet connection")
                return False
                
    except sr.WaitTimeoutError:
        print("\n❌ TIMEOUT - No speech detected")
        print("\n💡 Possible issues:")
        print("   1. Microphone is muted")
        print("   2. Wrong microphone selected")
        print("   3. Microphone volume too low")
        print("   4. No microphone connected")
        return False
        
    except OSError as e:
        print(f"\n❌ MICROPHONE ACCESS ERROR: {e}")
        print("\n💡 Solutions:")
        print("   1. Check microphone is plugged in")
        print("   2. Allow microphone permission")
        print("   3. Close other apps using microphone")
        print("   4. Restart your computer")
        return False
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False


def test_specific_microphone(index):
    """Test a specific microphone by index"""
    print(f"\n🎤 Testing microphone {index}...")
    
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone(device_index=index) as source:
            print("✅ Microphone accessed")
            print("🔊 Adjusting for noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            print(f"🎤 Speak now (5 seconds)...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            
            text = recognizer.recognize_google(audio)
            print(f"✅ SUCCESS on mic {index}: '{text}'")
            return True
            
    except Exception as e:
        print(f"❌ Failed on mic {index}: {e}")
        return False


if __name__ == "__main__":
    print("\n🚀 Starting microphone diagnostic...\n")
    
    success = test_microphone()
    
    if not success:
        print("\n" + "=" * 60)
        print("🔍 TRYING ALTERNATIVE MICROPHONES")
        print("=" * 60)
        
        mics = sr.Microphone.list_microphone_names()
        print(f"\nFound {len(mics)} microphones. Testing each...\n")
        
        for i in range(min(5, len(mics))):
            if test_specific_microphone(i):
                print(f"\n✅ Microphone {i} works!")
                print(f"💡 Use this in your code:")
                print(f"   sr.Microphone(device_index={i})")
                break
    
    print("\n" + "=" * 60)
    print("🏁 Test Complete")
    print("=" * 60)
