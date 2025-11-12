#!/usr/bin/env python3
"""
Demo: Enhanced Interactive and Humanized AI
Showcases the new personality, empathy, and conversational features
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from modules.intelligence.persona_response_service import create_persona_service
from modules.core.command_executor import CommandExecutor
from modules.voice.voice_assistant import VoiceAssistant

def demo_persona_responses():
    """Demo the PersonaResponseService"""
    print("=" * 70)
    print("🎭 DEMO: PersonaResponseService - Humanized AI Responses")
    print("=" * 70)
    
    persona = create_persona_service()
    
    # Test greeting
    print("\n1. Warm Greeting:")
    print(persona.get_greeting(include_small_talk=True))
    
    # Test processing messages
    print("\n2. Processing Message:")
    print(persona.handle_processing())
    
    # Test wake word acknowledgment
    print("\n3. Wake Word Acknowledgment:")
    print(persona.acknowledge_wake_word())
    
    # Test misunderstanding
    print("\n4. Empathetic Misunderstanding:")
    print(persona.handle_misunderstanding())
    
    # Test humanized success response
    print("\n5. Success Response (Opening App):")
    result = {"success": True, "message": "Opened Chrome"}
    humanized = persona.humanize_response("open_app", result)
    print(humanized)
    
    # Test humanized error response
    print("\n6. Error Response with Empathy:")
    result = {"success": False, "message": "Failed to open application"}
    humanized = persona.humanize_response("open_app", result)
    print(humanized)
    
    # Test helpful tip
    print("\n7. Helpful Tip:")
    print(persona.provide_helpful_tip())
    
    # Test farewell
    print("\n8. Warm Farewell:")
    print(persona.get_farewell())
    
    print("\n" + "=" * 70)

def demo_voice_enhancements():
    """Demo enhanced voice assistant"""
    print("\n" + "=" * 70)
    print("🎤 DEMO: Enhanced Voice Assistant with Empathy")
    print("=" * 70)
    
    print("\nThe Voice Assistant now features:")
    print("✨ Empathetic listening feedback")
    print("💬 Friendly wake word acknowledgments")
    print("🤗 Warm conversational tone")
    print("😊 Helpful error messages with suggestions")
    print("🎯 Context-aware responses")
    
    print("\nExamples of new responses:")
    print("• Instead of '❌ Could not understand audio'")
    print("  Now: '🤔 Sorry, I didn't quite catch that. Could you repeat?'")
    print()
    print("• Instead of '🎤 Listening...'")
    print("  Now: '🎤 I'm all ears! Listening...'")
    print()
    print("• Instead of '✅ Heard: open chrome'")
    print("  Now: '✅ Heard loud and clear: open chrome'")
    
    print("\n" + "=" * 70)

def demo_command_executor():
    """Demo enhanced command executor"""
    print("\n" + "=" * 70)
    print("🚀 DEMO: Command Executor with Personality")
    print("=" * 70)
    
    print("\nAll command responses are now humanized:")
    print("✅ Success messages have celebratory tones")
    print("❌ Error messages show empathy and offer help")
    print("🎯 Milestone celebrations every 10 commands")
    print("💡 Helpful tips every 8 commands")
    print("🧠 Mood detection from user's language")
    print("🌟 Proactive suggestions based on context")
    
    print("\nExample transformations:")
    print("• Before: 'Screenshot saved as screenshot.png'")
    print("  After: 'Perfect! I captured a screenshot and saved it as screenshot.png'")
    print()
    print("• Before: 'Failed to open folder'")
    print("  After: 'Hmm, ran into a small hiccup. I couldn't open folder. Would you like to try a different approach?'")
    print()
    print("• Before: 'Opened Chrome'")
    print("  After: 'Let's make it happen! 🚀 I opened Chrome. What's next on your list?'")
    
    print("\n" + "=" * 70)

def demo_contextual_awareness():
    """Demo contextual awareness and mood tracking"""
    print("\n" + "=" * 70)
    print("🧠 DEMO: Contextual Awareness & Mood Tracking")
    print("=" * 70)
    
    persona = create_persona_service()
    
    print("\nThe AI detects user mood from commands:")
    
    # Test different moods
    moods = [
        ("Can you help me quick? This is urgent!", "busy"),
        ("This is still not working! Fix it!", "frustrated"),
        ("Thanks! That's awesome!", "happy"),
        ("Open Chrome", "neutral")
    ]
    
    for command, expected_mood in moods:
        detected = persona.detect_user_mood(command)
        print(f"\n• Command: '{command}'")
        print(f"  Detected Mood: {detected.upper()}")
        print(f"  Response Style: {persona.mood_responses[detected]['greeting']}")
    
    print("\n" + "=" * 70)

def demo_proactive_suggestions():
    """Demo proactive suggestions"""
    print("\n" + "=" * 70)
    print("💡 DEMO: Proactive Suggestions")
    print("=" * 70)
    
    persona = create_persona_service()
    
    print("\nTime-based suggestions:")
    
    time_periods = ['morning', 'afternoon', 'evening', 'night']
    
    for period in time_periods:
        suggestions = persona.context_suggestions.get(period, [])
        print(f"\n{period.upper()} suggestions:")
        for suggestion in suggestions[:2]:
            print(f"  • {suggestion}")
    
    print("\n" + "=" * 70)

def main():
    """Run all demos"""
    print("\n" + "=" * 70)
    print("🌟 INTERACTIVE & HUMANIZED AI - FEATURE SHOWCASE")
    print("=" * 70)
    print("\nThis demo showcases the new personality and empathy features")
    print("that make the AI more interactive, warm, and human-like!")
    print()
    
    # Run all demos
    demo_persona_responses()
    demo_voice_enhancements()
    demo_command_executor()
    demo_contextual_awareness()
    demo_proactive_suggestions()
    
    print("\n" + "=" * 70)
    print("✨ DEMO COMPLETE!")
    print("=" * 70)
    print("\nThe AI is now:")
    print("✅ More conversational and friendly")
    print("✅ Empathetic and understanding")
    print("✅ Proactive with helpful suggestions")
    print("✅ Context-aware and mood-sensitive")
    print("✅ Celebratory of your accomplishments")
    print("✅ Encouraging and supportive")
    print("\nTry running the main application to experience it yourself!")
    print("Run: python launch_cli.py")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
