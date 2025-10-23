"""
Screenshot Analysis Module
Uses Gemini Vision API to analyze screenshots
"""

import os
from google import genai
from google.genai import types
import base64

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def analyze_screenshot(image_path: str, query: str = "Describe what you see in this image") -> str:
    """
    Analyze a screenshot using Gemini Vision
    
    Args:
        image_path: Path to the screenshot
        query: What to analyze (default: general description)
    
    Returns:
        Analysis result
    """
    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part(text=query),
                        types.Part(
                            inline_data=types.Blob(
                                mime_type="image/png",
                                data=image_data
                            )
                        )
                    ]
                )
            ]
        )
        
        return response.text or "Could not analyze image"
    
    except FileNotFoundError:
        return f"Error: Screenshot file '{image_path}' not found"
    except Exception as e:
        return f"Error analyzing screenshot: {str(e)}"

def extract_text_from_screenshot(image_path: str) -> str:
    """Extract all text from a screenshot (OCR)"""
    return analyze_screenshot(
        image_path,
        "Extract all visible text from this image. List each piece of text you can read."
    )

def find_element_in_screenshot(image_path: str, element: str) -> str:
    """Find a specific UI element in screenshot"""
    return analyze_screenshot(
        image_path,
        f"Look for '{element}' in this image. Describe where it is located and what it looks like."
    )

def get_screenshot_summary(image_path: str) -> str:
    """Get a detailed summary of a screenshot"""
    return analyze_screenshot(
        image_path,
        "Provide a detailed description of this screenshot including: 1) What application or website is shown, 2) Main elements visible, 3) Any text or important information, 4) The overall context"
    )

def compare_screenshots(image1_path: str, image2_path: str) -> str:
    """Compare two screenshots and describe differences"""
    try:
        with open(image1_path, "rb") as f1, open(image2_path, "rb") as f2:
            image1_data = f1.read()
            image2_data = f2.read()
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part(text="Compare these two screenshots and describe what changed:"),
                        types.Part(inline_data=types.Blob(mime_type="image/png", data=image1_data)),
                        types.Part(inline_data=types.Blob(mime_type="image/png", data=image2_data))
                    ]
                )
            ]
        )
        
        return response.text or "Could not compare images"
    
    except Exception as e:
        return f"Error comparing screenshots: {str(e)}"


def suggest_improvements(image_path: str) -> str:
    """
    Analyze screenshot and suggest small improvements.
    AI looks at UI/UX, design, layout, and suggests actionable changes.
    
    Args:
        image_path: Path to the screenshot
    
    Returns:
        List of improvement suggestions
    """
    prompt = """Analyze this screenshot and suggest small, actionable improvements. Focus on:

1. **UI/UX Issues**: Buttons too small, unclear labels, poor contrast, accessibility problems
2. **Design & Layout**: Spacing issues, alignment problems, color choices, font sizes
3. **User Experience**: Confusing navigation, missing feedback, unclear call-to-actions
4. **Content**: Text readability, information hierarchy, missing important details
5. **Technical Issues**: Broken layouts, overlapping elements, cut-off text

Provide 3-5 specific, actionable suggestions in this format:

**Suggestion 1: [Title]**
- **Issue**: [What's wrong]
- **Fix**: [How to improve it]
- **Impact**: [Why it matters]

Keep suggestions practical and easy to implement. Focus on quick wins that make the biggest difference."""
    
    return analyze_screenshot(image_path, prompt)


def analyze_screen_for_errors(image_path: str) -> str:
    """
    Check screenshot for visible errors, bugs, or problems.
    
    Args:
        image_path: Path to the screenshot
    
    Returns:
        List of detected issues
    """
    prompt = """Look at this screenshot carefully and identify any errors, bugs, or problems:

1. **Visible Errors**: Error messages, warnings, broken images, 404 pages
2. **Layout Problems**: Overlapping elements, cut-off text, misaligned items
3. **Broken Functionality**: Disabled buttons, missing images, broken links
4. **Console Errors**: Any visible error messages or warnings
5. **Design Bugs**: Missing styles, wrong colors, inconsistent spacing

List each issue clearly with:
- **What**: Describe the problem
- **Where**: Location on screen
- **Severity**: Critical / High / Medium / Low

If no issues found, say "No visible errors detected ✅" """
    
    return analyze_screenshot(image_path, prompt)


def get_quick_tips(image_path: str) -> str:
    """
    Get quick, actionable tips for what's on screen.
    Perfect for getting instant suggestions.
    
    Args:
        image_path: Path to the screenshot
    
    Returns:
        Quick tips and suggestions
    """
    prompt = """Give me 3 quick, actionable tips for this screen:

1. One thing that looks good ✅
2. One small thing to improve 🔧
3. One thing to watch out for ⚠️

Be specific and practical. Keep each tip to 1-2 sentences."""
    
    return analyze_screenshot(image_path, prompt)


def analyze_code_on_screen(image_path: str) -> str:
    """
    Analyze code visible in screenshot and suggest improvements.
    
    Args:
        image_path: Path to the screenshot
    
    Returns:
        Code analysis and suggestions
    """
    prompt = """Analyze the code visible in this screenshot. Look for:

1. **Code Quality**: Naming conventions, code structure, best practices
2. **Potential Bugs**: Logic errors, null checks, edge cases
3. **Performance**: Inefficient operations, unnecessary loops
4. **Readability**: Comments, formatting, variable names
5. **Security**: Potential vulnerabilities, unsafe operations

Provide specific suggestions with line references if possible.
Focus on the most important improvements."""
    
    return analyze_screenshot(image_path, prompt)


def analyze_website_design(image_path: str) -> str:
    """
    Analyze website design and provide professional suggestions.
    
    Args:
        image_path: Path to the screenshot
    
    Returns:
        Design analysis and recommendations
    """
    prompt = """Analyze this website design professionally:

**Good Points** (What works well):
- List 2-3 things done well

**Areas for Improvement**:
1. **Visual Hierarchy**: How to improve focus and flow
2. **Color & Typography**: Font, size, and color improvements  
3. **Spacing & Layout**: White space, alignment, balance
4. **Responsiveness**: Mobile-friendliness concerns
5. **Accessibility**: Color contrast, text size, readability

**Quick Wins** (Easy changes with big impact):
- 3 specific, actionable changes

Keep suggestions practical for implementation."""
    
    return analyze_screenshot(image_path, prompt)
