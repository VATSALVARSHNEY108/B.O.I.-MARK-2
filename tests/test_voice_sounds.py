#!/usr/bin/env python3
"""
Test script for Voice Sound Effects
Demonstrates the dynamic WAV playback feature
"""

from voice_commander import create_voice_commander
import time

def test_callback(command):
    """Simple callback to handle commands"""
    print(f"  📝 Executing command: {command}")
    return "Command executed successfully"

def main():
    print("=" * 60)
    print("🔊 VOICE SOUND EFFECTS TEST")
    print("=" * 60)
    
    # Create voice commander with sound effects
    print("\n1️⃣  Initializing Voice Commander...")
    commander = create_voice_commander(command_callback=test_callback)
    
    # Check if sound effects are available
    if commander.sound_effects:
        print("✅ Sound effects initialized successfully!")
    else:
        print("❌ Sound effects not available")
        return
    
    # List available sounds
    print("\n2️⃣  Listing available sound effects:")
    result = commander.list_sound_effects()
    if result['success']:
        for name, info in result['sounds'].items():
            status = "✅" if info['exists'] else "❌"
            print(f"  {status} {name:12s} - {info['path']}")
    
    # Test each sound effect
    print("\n3️⃣  Testing each sound effect:")
    sounds_to_test = ['wake_word', 'listening', 'processing', 'success', 'error']
    
    for sound_name in sounds_to_test:
        print(f"  🔊 Playing: {sound_name}...")
        commander.sound_effects.play_sound(sound_name, async_play=False)
        time.sleep(0.5)
    
    print("\n✅ All sounds tested!")
    
    # Test volume control
    print("\n4️⃣  Testing volume control:")
    volumes = [1.0, 0.5, 0.8]
    for vol in volumes:
        commander.set_sound_volume(vol)
        print(f"  🔊 Volume set to {int(vol * 100)}%")
        commander.sound_effects.play_sound('success', async_play=False)
        time.sleep(0.5)
    
    # Test enable/disable
    print("\n5️⃣  Testing enable/disable:")
    print("  Disabling sound effects...")
    commander.disable_sound_effects()
    commander.sound_effects.play_sound('wake_word')
    print("  ⏸️  Sound effects disabled (you shouldn't hear anything)")
    time.sleep(1)
    
    print("  Enabling sound effects...")
    commander.enable_sound_effects()
    commander.sound_effects.play_sound('wake_word', async_play=False)
    print("  ▶️  Sound effects enabled (you should hear a beep)")
    time.sleep(0.5)
    
    print("\n6️⃣  Voice Commanding Demo (Optional):")
    print("  To test with actual voice commands:")
    print("  1. Uncomment the code below")
    print("  2. Run this script")
    print("  3. Say a wake word like 'bhai' or 'boi'")
    print("  4. Listen for the sound effects as you speak")
    
    # Uncomment to test with actual voice recognition:
    # print("\n  Starting voice listening...")
    # print("  Say: 'bhai hello' or 'boi test'")
    # commander.start_continuous_listening()
    # try:
    #     time.sleep(30)  # Listen for 30 seconds
    # except KeyboardInterrupt:
    #     print("\n  Interrupted by user")
    # finally:
    #     commander.stop_continuous_listening()
    
    # Cleanup
    print("\n7️⃣  Cleanup:")
    commander.cleanup()
    print("  ✅ Resources cleaned up")
    
    print("\n" + "=" * 60)
    print("🎉 VOICE SOUND EFFECTS TEST COMPLETE!")
    print("=" * 60)
    print("\n📖 For more information, see: VOICE_SOUND_EFFECTS_GUIDE.md")
    print("\n💡 Tips:")
    print("  • Customize sounds by replacing WAV files in voice_sounds/")
    print("  • Adjust volume with commander.set_sound_volume(0.5)")
    print("  • Toggle sounds with commander.toggle_sound_effects()")

if __name__ == "__main__":
    main()
