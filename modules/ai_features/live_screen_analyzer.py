#!/usr/bin/env python3
"""
Live Screen Analyzer
AI continuously understands what's on your screen
"""

import os
import time
from datetime import datetime
from google import genai
from google.genai import types


class LiveScreenAnalyzer:
    """
    AI that continuously monitors and understands your screen
    
    Features:
    - Real-time screen analysis
    - Context awareness
    - Error detection
    - Productivity monitoring
    - Activity tracking
    """
    
    def __init__(self):
        """Initialize the live screen analyzer"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.client = None
        self.is_analyzing = False
        self.analysis_history = []
        
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
                print("✅ Live Screen Analyzer initialized")
            except Exception as e:
                print(f"⚠️  Error initializing Gemini: {e}")
        else:
            print("⚠️  GEMINI_API_KEY not set")
    
    def analyze_screenshot(self, image_path: str, focus: str = "general") -> dict:
        """
        Analyze a screenshot with AI vision
        
        Args:
            image_path: Path to screenshot
            focus: What to focus on - 'general', 'errors', 'code', 'productivity', 'text'
        
        Returns:
            Dict with analysis results
        """
        
        if not self.client:
            return {
                "success": False,
                "message": "Gemini AI not configured"
            }
        
        if not os.path.exists(image_path):
            return {
                "success": False,
                "message": f"Image not found: {image_path}"
            }
        
        # Create focused prompts
        prompts = {
            "general": """Analyze this screenshot and tell me:
1. What application/program is visible?
2. What is the user currently doing?
3. What content is displayed?
4. Overall context and purpose

Be clear and concise.""",
            
            "errors": """Look for errors or issues on this screen:
1. Any error messages or warnings?
2. Red text or error indicators?
3. Dialog boxes with problems?
4. Issues that need attention?

If no errors, say "No errors detected".""",
            
            "code": """Analyze the code visible on screen:
1. What programming language?
2. What does this code do?
3. Any bugs or issues visible?
4. Code quality (1-10)

If no code visible, say "No code detected".""",
            
            "productivity": """Analyze productivity on this screen:
1. What task is being done?
2. Work-related or distraction?
3. Focus level (1-10)
4. Any distractions visible?

Provide insights.""",
            
            "text": """Extract and summarize all visible text:
1. Main text content
2. Important information
3. Key points
4. Summary

Be thorough."""
        }
        
        prompt = prompts.get(focus, prompts["general"])
        
        try:
            # Read image
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            print(f"\n🔍 Analyzing screen (focus: {focus})...")
            
            # Generate analysis
            response = self.client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=[
                    types.Part.from_bytes(
                        data=image_data,
                        mime_type='image/png'
                    ),
                    prompt
                ]
            )
            
            analysis = response.text
            
            # Save to history
            result = {
                "success": True,
                "analysis": analysis,
                "focus": focus,
                "timestamp": datetime.now().isoformat(),
                "image_path": image_path
            }
            
            self.analysis_history.append(result)
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error analyzing screenshot: {str(e)}"
            }
    
    def understand_what_im_doing(self, image_path: str) -> str:
        """
        Simple method: Tell me what I'm doing right now
        
        Args:
            image_path: Path to screenshot
        
        Returns:
            Human-readable description
        """
        result = self.analyze_screenshot(image_path, "general")
        
        if result["success"]:
            return f"🧠 {result['analysis']}"
        else:
            return f"❌ {result['message']}"
    
    def check_for_errors(self, image_path: str) -> str:
        """
        Check if there are any errors on screen
        
        Args:
            image_path: Path to screenshot
        
        Returns:
            Error detection results
        """
        result = self.analyze_screenshot(image_path, "errors")
        
        if result["success"]:
            return f"🔍 {result['analysis']}"
        else:
            return f"❌ {result['message']}"
    
    def analyze_my_code(self, image_path: str) -> str:
        """
        Analyze code visible on screen
        
        Args:
            image_path: Path to screenshot
        
        Returns:
            Code analysis
        """
        result = self.analyze_screenshot(image_path, "code")
        
        if result["success"]:
            return f"💻 {result['analysis']}"
        else:
            return f"❌ {result['message']}"
    
    def read_screen_text(self, image_path: str) -> str:
        """
        Extract all text from screen
        
        Args:
            image_path: Path to screenshot
        
        Returns:
            Extracted text
        """
        result = self.analyze_screenshot(image_path, "text")
        
        if result["success"]:
            return f"📝 {result['analysis']}"
        else:
            return f"❌ {result['message']}"
    
    def get_analysis_summary(self) -> str:
        """Get summary of recent analyses"""
        if not self.analysis_history:
            return "No analyses yet"
        
        summary = f"\n📊 Analysis History ({len(self.analysis_history)} total)\n"
        summary += "="*60 + "\n"
        
        for i, analysis in enumerate(self.analysis_history[-5:], 1):
            summary += f"\n{i}. [{analysis['focus']}] - {analysis['timestamp']}\n"
            summary += f"   {analysis['analysis'][:100]}...\n"
        
        return summary


# Easy-to-use function
def understand_screen(image_path: str, question: str = "What do you see?") -> str:
    """
    Simple function to understand what's on a screenshot
    
    Args:
        image_path: Path to screenshot
        question: What to ask about it
    
    Returns:
        AI's understanding of the screen
    """
    analyzer = LiveScreenAnalyzer()
    
    if not analyzer.client:
        return "❌ Gemini AI not configured. Set GEMINI_API_KEY."
    
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        response = analyzer.client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=[
                types.Part.from_bytes(
                    data=image_data,
                    mime_type='image/png'
                ),
                question
            ]
        )
        
        return response.text
        
    except Exception as e:
        return f"❌ Error: {str(e)}"


# Create global instance
screen_analyzer = LiveScreenAnalyzer()
