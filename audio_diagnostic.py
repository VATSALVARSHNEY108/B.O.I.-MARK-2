#!/usr/bin/env python3
"""
Comprehensive Audio & Microphone Diagnostic Tool
Checks why voice input isn't working
"""

import sys
import os

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def check_pyaudio():
    """Check if PyAudio is available"""
    print_header("🔍 CHECKING PYAUDIO (Required for microphone access)")
    try:
        import pyaudio
        print("✅ PyAudio is installed")
        
        # List audio devices
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        
        print(f"\n📊 Found {num_devices} audio devices:")
        
        for i in range(num_devices):
            device_info = p.get_device_info_by_host_api_device_index(0, i)
            print(f"\n  Device {i}: {device_info.get('name')}")
            print(f"    - Max Input Channels: {device_info.get('maxInputChannels')}")
            print(f"    - Max Output Channels: {device_info.get('maxOutputChannels')}")
            print(f"    - Default Sample Rate: {device_info.get('defaultSampleRate')}")
            
            if device_info.get('maxInputChannels') > 0:
                print(f"    ✅ Can be used as MICROPHONE")
            
        p.terminate()
        return True
        
    except ImportError:
        print("❌ PyAudio is NOT installed")
        print("\n💡 Install with: pip install pyaudio")
        return False
    except Exception as e:
        print(f"⚠️  Error checking PyAudio: {e}")
        return False

def check_speech_recognition():
    """Check SpeechRecognition library"""
    print_header("🔍 CHECKING SPEECH RECOGNITION")
    try:
        import speech_recognition as sr
        print(f"✅ SpeechRecognition is installed (version: {sr.__version__})")
        
        # Try to list microphones
        try:
            print("\n📋 Available Microphones:")
            mic_list = sr.Microphone.list_microphone_names()
            
            if not mic_list:
                print("❌ NO microphones detected!")
                print("\n💡 This usually means:")
                print("   1. You're on a cloud server (like Replit) without physical mic")
                print("   2. PyAudio isn't properly installed")
                print("   3. No audio devices are connected")
            else:
                for idx, name in enumerate(mic_list):
                    print(f"   [{idx}] {name}")
                print(f"\n✅ Found {len(mic_list)} microphone(s)")
                
            return len(mic_list) > 0
            
        except Exception as e:
            print(f"❌ Error listing microphones: {e}")
            return False
            
    except ImportError:
        print("❌ SpeechRecognition is NOT installed")
        print("\n💡 Install with: pip install SpeechRecognition")
        return False

def check_environment():
    """Check the runtime environment"""
    print_header("🔍 CHECKING ENVIRONMENT")
    
    # Check if running on Replit
    is_replit = os.environ.get('REPL_ID') is not None
    print(f"Running on Replit: {'YES ⚠️' if is_replit else 'NO'}")
    
    # Check if X server is available
    has_xauthority = os.path.exists(os.path.expanduser('~/.Xauthority'))
    print(f"X Server Available: {'YES ✅' if has_xauthority else 'NO ⚠️'}")
    
    # Check display
    display = os.environ.get('DISPLAY')
    print(f"DISPLAY variable: {display if display else 'Not set ⚠️'}")
    
    # Check audio devices in /dev
    audio_devices = []
    if os.path.exists('/dev/snd'):
        audio_devices = os.listdir('/dev/snd')
        print(f"\n/dev/snd devices: {audio_devices if audio_devices else 'None ⚠️'}")
    else:
        print("\n/dev/snd: Not found ⚠️")
    
    if is_replit:
        print("\n⚠️  WARNING: You're running on Replit (cloud environment)")
        print("   Replit servers DON'T have access to your laptop's microphone!")
        print("\n💡 SOLUTION: Use browser-based audio input in Streamlit")
        print("   (See streamlit-webrtc or st.audio_input)")
        
    return not is_replit

def test_microphone_recording():
    """Try to actually record from microphone"""
    print_header("🔍 TESTING MICROPHONE RECORDING")
    
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        
        print("Attempting to access default microphone...")
        
        try:
            with sr.Microphone() as source:
                print("✅ Microphone opened successfully!")
                print("\n🔊 Adjusting for ambient noise (1 second)...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                
                energy = recognizer.energy_threshold
                print(f"📊 Energy Threshold: {energy}")
                
                print("\n🎤 Trying to capture 2 seconds of audio...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
                
                print("✅ Audio captured successfully!")
                print(f"📊 Audio data size: {len(audio.get_raw_data())} bytes")
                
                if len(audio.get_raw_data()) > 0:
                    print("\n✅ MICROPHONE IS WORKING!")
                    return True
                else:
                    print("\n⚠️  No audio data captured (silence?)")
                    return False
                    
        except sr.WaitTimeoutError:
            print("❌ TIMEOUT: No audio detected")
            print("\n💡 Possible causes:")
            print("   1. Microphone is muted")
            print("   2. No microphone connected")
            print("   3. Wrong microphone selected")
            print("   4. Running on cloud server without mic access")
            return False
            
        except OSError as e:
            print(f"❌ OS ERROR: {e}")
            print("\n💡 This usually means:")
            print("   1. No audio input devices available")
            print("   2. Running on server/cloud environment")
            print("   3. Audio drivers not installed")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def check_alternative_solutions():
    """Show alternative ways to get voice input"""
    print_header("💡 ALTERNATIVE SOLUTIONS FOR VOICE INPUT")
    
    is_replit = os.environ.get('REPL_ID') is not None
    
    if is_replit:
        print("\n🌐 For Replit/Cloud Environments:")
        print("\n1. Use Streamlit's audio_input widget (RECOMMENDED):")
        print("   >>> audio_file = st.audio_input('Record audio')")
        print("   >>> # Process the uploaded audio file")
        print("\n2. Use streamlit-webrtc for real-time audio:")
        print("   >>> pip install streamlit-webrtc")
        print("\n3. Use browser's Speech Recognition API (JavaScript):")
        print("   >>> # Capture audio in browser, send to server")
        
    else:
        print("\n🖥️  For Local Machines:")
        print("\n1. Check microphone permissions in system settings")
        print("2. Test with: python test_microphone.py")
        print("3. Make sure microphone is not muted")
        print("4. Try selecting different microphone device")

def main():
    print("\n" + "🎤" * 35)
    print("   COMPREHENSIVE AUDIO DIAGNOSTIC TOOL")
    print("🎤" * 35)
    
    results = {}
    
    # Run all checks
    results['pyaudio'] = check_pyaudio()
    results['speech_recognition'] = check_speech_recognition()
    results['environment'] = check_environment()
    results['recording'] = test_microphone_recording()
    
    # Show alternatives
    check_alternative_solutions()
    
    # Summary
    print_header("📊 DIAGNOSTIC SUMMARY")
    
    total_checks = len(results)
    passed_checks = sum(1 for v in results.values() if v)
    
    print(f"\nPassed: {passed_checks}/{total_checks} checks")
    print("\nDetails:")
    for check, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {check.upper()}: {status}")
    
    # Final verdict
    print("\n" + "=" * 70)
    if passed_checks == total_checks:
        print("🎉 ALL CHECKS PASSED - Microphone should be working!")
    elif os.environ.get('REPL_ID'):
        print("⚠️  RUNNING ON CLOUD SERVER (Replit)")
        print("\n🔧 FIX: Use browser-based audio input instead!")
        print("   The streamlit_app.py should use st.audio_input() widget")
        print("   to capture audio directly from YOUR browser/laptop.")
    else:
        print("❌ ISSUES DETECTED - See above for solutions")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
