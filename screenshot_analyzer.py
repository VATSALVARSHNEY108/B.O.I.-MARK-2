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
