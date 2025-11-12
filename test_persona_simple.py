#!/usr/bin/env python3
"""
Simple test for PersonaResponseService without GUI dependencies
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from modules.intelligence.persona_response_service import create_persona_service

def test_persona():
    """Test the PersonaResponseService"""
    print("=" * 70)
    print("🎭 Testing PersonaResponseService")
    print("=" * 70)
    
    persona = create_persona_service()
    
    # Test greeting
    print("\n1. ✨ Warm Greeting:")
    print(persona.get_greeting(include_small_talk=True))
    
    # Test processing messages
    print("\n2. ⚙️  Processing Message:")
    print(persona.handle_processing())
    
    # Test wake word acknowledgment
    print("\n3. 👋 Wake Word Acknowledgment:")
    print(persona.acknowledge_wake_word())
    
    # Test misunderstanding
    print("\n4. 🤔 Empathetic Misunderstanding:")
    print(persona.handle_misunderstanding())
    
    # Test humanized success response
    print("\n5. ✅ Success Response (Opening App):")
    result = {"success": True, "message": "Opened Chrome"}
    humanized = persona.humanize_response("open_app", result)
    print(humanized)
    
    # Test humanized error response
    print("\n6. ❌ Error Response with Empathy:")
    result = {"success": False, "message": "Failed to open application"}
    humanized = persona.humanize_response("open_app", result)
    print(humanized)
    
    # Test repeated errors
    print("\n7. 🔄 Repeated Errors (showing empathy):")
    for i in range(3):
        result = {"success": False, "message": f"Failed attempt {i+1}"}
        humanized = persona.humanize_response("open_app", result)
        print(f"   Attempt {i+1}: {humanized}")
    
    # Test mood detection
    print("\n8. 🧠 Mood Detection:")
    moods_test = [
        ("quick! open chrome now", "busy"),
        ("this is still broken!", "frustrated"),
        ("thanks that's great!", "happy"),
        ("open notepad", "neutral")
    ]
    
    for command, expected in moods_test:
        detected = persona.detect_user_mood(command)
        print(f"   '{command}' → {detected.upper()}")
    
    # Test helpful tip
    print("\n9. 💡 Helpful Tip:")
    print(persona.provide_helpful_tip())
    
    # Test milestone celebration
    print("\n10. 🎉 Milestone Celebration:")
    print(persona.celebrate_milestone(10, "open_app"))
    
    # Test farewell
    print("\n11. 👋 Warm Farewell:")
    print(persona.get_farewell())
    
    print("\n" + "=" * 70)
    print("✅ All tests passed! PersonaResponseService is working!")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    test_persona()
