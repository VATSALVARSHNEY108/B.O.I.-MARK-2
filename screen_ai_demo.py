#!/usr/bin/env python3
"""
Standalone AI Screen Understanding Demo
Works perfectly - no dependencies on other modules
"""

import os
from google import genai
from google.genai import types

def ai_understand_screen(image_path: str, question: str = None):
    """AI analyzes and understands what's on a screenshot"""
    
    # Default question
    if not question:
        question = """Analyze this screenshot in detail and tell me:

1. What application or program is visible?
2. What is displayed on the screen?
3. What is the user doing or what purpose does this serve?
4. Any notable features, buttons, or elements?
5. Overall summary of what this screen shows

Be thorough and describe everything you can see."""
    
    # Get API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not set")
        print("💡 Add your Gemini API key to Secrets")
        return
    
    # Check file exists
    if not os.path.exists(image_path):
        print(f"❌ Error: File not found - {image_path}")
        return
    
    try:
        # Initialize Gemini
        client = genai.Client(api_key=api_key)
        
        # Read image
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        print("\n" + "="*70)
        print("🤖 AI SCREEN UNDERSTANDING")
        print("="*70)
        print(f"📸 Image: {image_path}")
        print(f"❓ Question: {question[:100]}...")
        print("\n🧠 AI is analyzing the screenshot...")
        print()
        
        # Analyze with Gemini Vision
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=[
                types.Part.from_bytes(
                    data=image_data,
                    mime_type='image/png'
                ),
                question
            ]
        )
        
        analysis = response.text
        
        print("="*70)
        print("✅ AI ANALYSIS COMPLETE")
        print("="*70)
        print()
        print(analysis)
        print()
        print("="*70)
        
        return analysis
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None


if __name__ == "__main__":
    print("\n🎯 Testing AI Screen Understanding with Phone Link screenshot...")
    
    # Analyze the Phone Link screenshot
    ai_understand_screen(
        'attached_assets/image_1763465108731.png',
        "What application is this? Describe everything you see on this screen in detail."
    )
