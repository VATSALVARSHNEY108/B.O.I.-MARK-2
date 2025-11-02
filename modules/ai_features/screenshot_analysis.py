"""
AI Screenshot Analysis Module
Analyze screenshots with AI vision and provide intelligent insights
"""

import os
from typing import Optional, Dict, Any
from google import genai
import base64


class ScreenshotAnalyzer:
    """AI-powered screenshot analyzer with vision capabilities"""
    
    def __init__(self):
        """Initialize screenshot analyzer"""
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.client = None
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"⚠️ Could not initialize Gemini: {e}")
        
    def analyze(self, image_path: str, prompt: str = "Describe what you see in this image") -> str:
        """
        Analyze a screenshot using AI vision
        
        Args:
            image_path: Path to the screenshot
            prompt: What to analyze
        
        Returns:
            Analysis result
        """
        if not self.client:
            return "❌ AI Vision not available - GEMINI_API_KEY not set"
        
        try:
            with open(image_path, "rb") as f:
                image_data = f.read()
            
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    {
                        "parts": [
                            {"text": prompt},
                            {"inline_data": {"mime_type": "image/png", "data": base64.b64encode(image_data).decode()}}
                        ]
                    }
                ]
            )
            
            return response.text or "Could not analyze image"
        
        except FileNotFoundError:
            return f"❌ Screenshot file not found: {image_path}"
        except Exception as e:
            return f"❌ Error analyzing screenshot: {str(e)}"
    
    def suggest_improvements(self, image_path: str) -> str:
        """Suggest UI/UX improvements for screenshot"""
        prompt = """Analyze this screenshot and suggest 3-5 actionable improvements:

1. **UI/UX Issues**: Buttons, labels, contrast, accessibility
2. **Design & Layout**: Spacing, alignment, colors, fonts
3. **User Experience**: Navigation, feedback, clarity
4. **Content**: Readability, hierarchy
5. **Technical**: Layout issues, overlaps

Format:
**Suggestion 1: [Title]**
- Issue: [What's wrong]
- Fix: [How to improve]
- Impact: [Why it matters]"""
        
        return self.analyze(image_path, prompt)
    
    def find_errors(self, image_path: str) -> str:
        """Find errors and issues in screenshot"""
        prompt = """Look for errors, bugs, or problems:

1. **Visible Errors**: Error messages, warnings, broken images
2. **Layout Problems**: Overlapping elements, cut-off text
3. **Broken Functionality**: Disabled buttons, missing images
4. **Console Errors**: Any visible error messages
5. **Design Bugs**: Missing styles, wrong colors

List each issue with:
- What: The problem
- Where: Location on screen
- Severity: Critical/High/Medium/Low

If no issues: "No visible errors detected ✅" """
        
        return self.analyze(image_path, prompt)
    
    def extract_text(self, image_path: str) -> str:
        """Extract all text from screenshot (OCR)"""
        return self.analyze(image_path, "Extract all visible text from this image. List each piece of text.")
    
    def analyze_code(self, image_path: str) -> str:
        """Analyze code visible in screenshot"""
        prompt = """Analyze the code in this screenshot:

1. Programming language
2. What the code does
3. Any bugs or issues
4. Code quality (1-10)
5. Suggestions for improvement

If no code visible: "No code detected" """
        
        return self.analyze(image_path, prompt)
    
    def analyze_design(self, image_path: str) -> str:
        """Analyze design and UI elements"""
        prompt = """Analyze the design/UI:

1. Type of design/interface
2. Color scheme and visual style
3. Layout and composition quality
4. Design suggestions

If no design work: "No design detected" """
        
        return self.analyze(image_path, prompt)
    
    def get_quick_tips(self, image_path: str) -> str:
        """Get quick tips about the screenshot"""
        prompt = "Provide 3 quick, actionable tips about what's shown in this screenshot"
        return self.analyze(image_path, prompt)


def create_screenshot_analyzer() -> ScreenshotAnalyzer:
    """Factory function to create ScreenshotAnalyzer instance"""
    return ScreenshotAnalyzer()


# Standalone functions for backward compatibility
def analyze_screenshot(image_path: str, prompt: str = "Describe what you see") -> str:
    """Analyze a screenshot"""
    analyzer = create_screenshot_analyzer()
    return analyzer.analyze(image_path, prompt)


def suggest_improvements(image_path: str) -> str:
    """Suggest improvements for screenshot"""
    analyzer = create_screenshot_analyzer()
    return analyzer.suggest_improvements(image_path)


def analyze_screen_for_errors(image_path: str) -> str:
    """Find errors in screenshot"""
    analyzer = create_screenshot_analyzer()
    return analyzer.find_errors(image_path)


def get_quick_tips(image_path: str) -> str:
    """Get quick tips"""
    analyzer = create_screenshot_analyzer()
    return analyzer.get_quick_tips(image_path)


def analyze_code_on_screen(image_path: str) -> str:
    """Analyze code in screenshot"""
    analyzer = create_screenshot_analyzer()
    return analyzer.analyze_code(image_path)


def analyze_website_design(image_path: str) -> str:
    """Analyze website design"""
    analyzer = create_screenshot_analyzer()
    return analyzer.analyze_design(image_path)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python screenshot_analysis.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    analyzer = create_screenshot_analyzer()
    result = analyzer.analyze(image_path)
    print(result)
