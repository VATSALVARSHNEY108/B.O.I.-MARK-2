"""
AI Code Generator Module
Handles intelligent code generation for multiple programming languages
"""

import os
from google import genai
from google.genai import types
from code_templates import get_template_code, list_available_templates

client = None

def get_client():
    """Get or initialize the Gemini client"""
    global client
    if client is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        client = genai.Client(api_key=api_key)
    return client

LANGUAGE_TEMPLATES = {
    "python": {
        "extension": ".py",
        "comment_style": "#",
        "editor": "notepad" if os.name == "nt" else "gedit"
    },
    "javascript": {
        "extension": ".js",
        "comment_style": "//",
        "editor": "notepad" if os.name == "nt" else "gedit"
    },
    "java": {
        "extension": ".java",
        "comment_style": "//",
        "editor": "notepad" if os.name == "nt" else "gedit"
    },
    "c": {
        "extension": ".c",
        "comment_style": "//",
        "editor": "notepad" if os.name == "nt" else "gedit"
    },
    "cpp": {
        "extension": ".cpp",
        "comment_style": "//",
        "editor": "notepad" if os.name == "nt" else "gedit"
    },
    "csharp": {
        "extension": ".cs",
        "comment_style": "//",
        "editor": "notepad" if os.name == "nt" else "gedit"
    },
    "ruby": {
        "extension": ".rb",
        "comment_style": "#",
        "editor": "notepad" if os.name == "nt" else "gedit"
    },
    "go": {
        "extension": ".go",
        "comment_style": "//",
        "editor": "notepad" if os.name == "nt" else "gedit"
    },
    "html": {
        "extension": ".html",
        "comment_style": "<!--",
        "editor": "notepad" if os.name == "nt" else "gedit"
    },
    "css": {
        "extension": ".css",
        "comment_style": "/*",
        "editor": "notepad" if os.name == "nt" else "gedit"
    }
}

def detect_language_from_description(description: str) -> str:
    """Detect programming language from description"""
    description_lower = description.lower()
    
    language_keywords = {
        "python": ["python", "py", "django", "flask"],
        "javascript": ["javascript", "js", "node", "react", "vue"],
        "java": ["java"],
        "c": ["c programming", " c code"],
        "cpp": ["c++", "cpp"],
        "csharp": ["c#", "csharp"],
        "ruby": ["ruby", "rails"],
        "go": ["go", "golang"],
        "html": ["html", "webpage"],
        "css": ["css", "styling"]
    }
    
    for lang, keywords in language_keywords.items():
        if any(keyword in description_lower for keyword in keywords):
            return lang
    
    return "python"

def clean_code_output(code: str) -> str:
    """Remove markdown code blocks and clean up the output"""
    code = code.strip()
    
    if code.startswith("```"):
        lines = code.split("\n")
        
        if lines[0].strip().startswith("```"):
            lines = lines[1:]
        
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        
        code = "\n".join(lines)
    
    return code.strip()

def generate_code(description: str, language: str | None = None) -> dict:
    """
    Generate code using templates (fast) or Gemini AI (fallback)
    
    Args:
        description: What the code should do
        language: Programming language (auto-detected if not provided)
    
    Returns:
        dict with code, language, and metadata
    """
    if not language:
        language = detect_language_from_description(description)
    
    language = language.lower()
    
    language_info = LANGUAGE_TEMPLATES.get(language, {
        "extension": ".txt",
        "comment_style": "#",
        "editor": "notepad"
    })
    
    # Try to get template code first (instant, reliable)
    template_code = get_template_code(description, language)
    if template_code:
        return {
            "success": True,
            "code": template_code,
            "language": language,
            "extension": language_info["extension"],
            "editor": language_info["editor"],
            "description": description,
            "source": "template"
        }
    
    # Fall back to AI generation if no template available
    prompt = f"""You are an expert {language} programmer. Generate clean, well-documented code for the following task:

TASK: {description}

REQUIREMENTS:
1. Write COMPLETE, WORKING {language} code
2. Include detailed comments explaining the logic
3. Follow {language} best practices and conventions
4. Make the code beginner-friendly and educational
5. Include example usage or test cases where appropriate
6. DO NOT include any explanations before or after the code
7. DO NOT use markdown formatting (no ```)
8. ONLY return the raw code

Generate the {language} code now:"""

    try:
        api_client = get_client()
        response = api_client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
            )
        )
        
        if response.text:
            code = clean_code_output(response.text)
            
            return {
                "success": True,
                "code": code,
                "language": language,
                "extension": language_info["extension"],
                "editor": language_info["editor"],
                "description": description,
                "source": "ai"
            }
        else:
            return {
                "success": False,
                "error": "No code generated",
                "code": f"# Error: Could not generate code for: {description}"
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "code": f"# Error generating code: {str(e)}\n# Try one of these: {', '.join(list_available_templates())}"
        }

def generate_multiple_versions(description: str, language: str | None = None, count: int = 1) -> list:
    """Generate multiple versions of code for comparison"""
    versions = []
    
    for i in range(count):
        result = generate_code(description, language)
        if result["success"]:
            versions.append(result)
    
    return versions

def explain_code(code: str, language: str = "python") -> str:
    """Generate explanation for existing code"""
    prompt = f"""Explain the following {language} code in simple terms:

{code}

Provide a clear, beginner-friendly explanation of:
1. What the code does
2. How it works (step by step)
3. Key concepts used"""

    try:
        api_client = get_client()
        response = api_client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        return response.text or "Could not generate explanation"
    except Exception as e:
        return f"Error: {str(e)}"

def improve_code(code: str, language: str = "python") -> dict:
    """Suggest improvements for existing code"""
    prompt = f"""Analyze this {language} code and provide an improved version:

{code}

Improvements to make:
1. Better performance
2. More readable
3. Better error handling
4. Follow best practices
5. Add helpful comments

Return ONLY the improved code, no explanations."""

    try:
        api_client = get_client()
        response = api_client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        
        if response.text:
            improved_code = clean_code_output(response.text)
            return {
                "success": True,
                "code": improved_code,
                "language": language
            }
        else:
            return {
                "success": False,
                "error": "Could not improve code"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def debug_code(code: str, error_message: str, language: str = "python") -> dict:
    """Debug code and fix errors"""
    prompt = f"""Fix the following {language} code that has this error:

ERROR: {error_message}

CODE:
{code}

Provide the corrected code with the bug fixed. Return ONLY the fixed code."""

    try:
        api_client = get_client()
        response = api_client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        
        if response.text:
            fixed_code = clean_code_output(response.text)
            return {
                "success": True,
                "code": fixed_code,
                "language": language
            }
        else:
            return {
                "success": False,
                "error": "Could not fix code"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
