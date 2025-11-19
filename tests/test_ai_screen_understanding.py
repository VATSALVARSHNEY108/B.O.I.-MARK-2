#!/usr/bin/env python3
"""
AI Screen Understanding Demo
Upload any screenshot and AI will analyze it!
"""

import os
from google import genai
from google.genai import types
import base64

def analyze_screenshot_with_ai(image_path: str, question: str = "What do you see on this screen?") -> str:
    """
    Analyze a screenshot using Gemini Vision AI
    
    Args:
        image_path: Path to screenshot image
        question: What to ask about the screenshot
    
    Returns:
        AI's analysis of the screenshot
    """
    
    # Check if API key exists
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return "❌ GEMINI_API_KEY not set. Please set it in Secrets."
    
    # Check if image exists
    if not os.path.exists(image_path):
        return f"❌ Image not found: {image_path}"
    
    try:
        # Initialize Gemini client
        client = genai.Client(api_key=api_key)
        
        # Read and encode image
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        print(f"\n📸 Analyzing screenshot: {image_path}")
        print(f"❓ Question: {question}")
        print("\n🤖 AI is analyzing...")
        
        # Create the prompt with image
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
        
        print("\n" + "="*70)
        print("🧠 AI ANALYSIS:")
        print("="*70)
        print(analysis)
        print("="*70)
        
        return analysis
        
    except Exception as e:
        error_msg = f"❌ Error analyzing screenshot: {str(e)}"
        print(error_msg)
        return error_msg


def demo_screen_understanding():
    """Run demo of AI screen understanding"""
    
    print("="*70)
    print("🤖 AI SCREEN UNDERSTANDING DEMO")
    print("="*70)
    print()
    print("This AI can understand ANYTHING on your screen:")
    print("  ✅ Read text and documents")
    print("  ✅ Identify apps and programs")
    print("  ✅ Detect errors and issues")
    print("  ✅ Analyze code")
    print("  ✅ Understand UI/design")
    print("  ✅ Summarize content")
    print("  ✅ Extract information")
    print("  ✅ And much more!")
    print()
    print("="*70)
    print()
    
    # Check for existing screenshots
    screenshot_dir = "screenshots"
    if os.path.exists(screenshot_dir):
        screenshots = [f for f in os.listdir(screenshot_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        if screenshots:
            print("📁 Found existing screenshots:")
            for i, img in enumerate(screenshots, 1):
                print(f"   {i}. {img}")
            print()
    
    # Example questions you can ask
    print("💡 EXAMPLE QUESTIONS YOU CAN ASK:")
    print("   1. 'What do you see on this screen?'")
    print("   2. 'What app is open and what is the user doing?'")
    print("   3. 'Are there any errors or warnings visible?'")
    print("   4. 'What is this code doing?'")
    print("   5. 'Summarize the text visible on screen'")
    print("   6. 'What website is this and what's on it?'")
    print()
    print("="*70)
    print()
    
    # Get image path
    image_path = input("📸 Enter path to screenshot (or drag & drop image here): ").strip()
    
    if not image_path:
        print("\n⚠️  No image provided. Using demo mode...")
        print("\n💡 HOW TO USE:")
        print("   1. Upload a screenshot to the project")
        print("   2. Run this script again")
        print("   3. Enter the path to your screenshot")
        print("   4. Ask any question about it!")
        return
    
    # Remove quotes if present
    image_path = image_path.strip('"').strip("'")
    
    # Get question
    print()
    question = input("❓ What do you want to know about this screen? (press Enter for general analysis): ").strip()
    
    if not question:
        question = """Analyze this screenshot in detail:

1. What application/program is visible?
2. What is the user currently doing?
3. What is the main content on screen?
4. Are there any errors, warnings, or issues visible?
5. What is the overall context and purpose?

Provide a comprehensive analysis."""
    
    # Analyze the screenshot
    result = analyze_screenshot_with_ai(image_path, question)
    
    print("\n✅ Analysis complete!")
    print()
    print("="*70)
    print("💡 TIP: You can ask follow-up questions about the same screenshot!")
    print("="*70)


if __name__ == "__main__":
    demo_screen_understanding()
