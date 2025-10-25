#!/usr/bin/env python3
"""Test JARVIS AI System"""

import asyncio
from jarvis_ai import create_jarvis_ai

async def test_jarvis():
    print("\n" + "="*60)
    print("🤖 Testing JARVIS AI System")
    print("="*60)
    
    # Initialize JARVIS
    jarvis = create_jarvis_ai()
    print("✅ JARVIS initialized successfully")
    print(f"👤 User name: {jarvis.user_name}")
    print(f"🤖 Assistant name: {jarvis.name}")
    
    # Test greeting
    print("\n" + "-"*60)
    print("🎯 Initial Greeting:")
    print("-"*60)
    greeting = jarvis.initiate_conversation()
    print(greeting)
    
    # Test conversation
    print("\n" + "-"*60)
    print("💬 Test Conversation:")
    print("-"*60)
    
    test_messages = [
        "What can you do?",
        "Help me with something",
        "Thank you"
    ]
    
    for msg in test_messages:
        print(f"\n👤 USER: {msg}")
        response = await jarvis.process_message(msg)
        print(f"🤖 JARVIS: {response}")
    
    # Test proactive suggestion
    print("\n" + "-"*60)
    print("💡 Proactive Suggestion:")
    print("-"*60)
    suggestion = jarvis.get_proactive_suggestion()
    if suggestion:
        print(suggestion)
    else:
        print("No suggestions at this time")
    
    # Show stats
    print("\n" + "-"*60)
    print("📊 JARVIS Statistics:")
    print("-"*60)
    stats = jarvis.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*60)
    print("✅ All tests completed successfully!")
    print("="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(test_jarvis())
