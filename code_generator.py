"""
AI Code Generator Module
Handles intelligent code generation for multiple programming languages
"""

import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

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
    Generate code using Gemini AI
    
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
        response = client.models.generate_content(
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
                "description": description
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
            "code": f"# Error generating code: {str(e)}"
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
        response = client.models.generate_content(
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
        response = client.models.generate_content(
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
        response = client.models.generate_content(
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
