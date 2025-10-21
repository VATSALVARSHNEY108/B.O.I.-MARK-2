import os
import json
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def validate_command_structure(data: dict) -> dict:
    """
    Validates that the parsed command has the required structure.
    Returns a validated dict with all required fields.
    """
    required_fields = ["action", "parameters", "steps", "description"]
    
    for field in required_fields:
        if field not in data:
            return {
                "action": "error",
                "parameters": {"error": f"Missing required field: {field}"},
                "steps": [],
                "description": f"Invalid response structure: missing '{field}'"
            }
    
    if not isinstance(data["parameters"], dict):
        data["parameters"] = {}
    
    if not isinstance(data["steps"], list):
        data["steps"] = []
    
    for i, step in enumerate(data["steps"]):
        if not isinstance(step, dict) or "action" not in step or "parameters" not in step:
            return {
                "action": "error",
                "parameters": {"error": f"Invalid step {i+1}"},
                "steps": [],
                "description": f"Step {i+1} has invalid structure"
            }
    
    return data

def parse_command(user_input: str) -> dict:
    """
    Uses Gemini to parse natural language commands into structured actions.
    Returns a dict with 'action', 'parameters', and 'steps' for multi-step workflows.
    """
    system_prompt = """You are a desktop automation assistant. Parse user commands into structured JSON actions.

Available actions:
- open_app: Open an application (parameters: app_name)
- type_text: Type text (parameters: text)
- click: Click at position (parameters: x, y) or click (parameters: button - left/right/middle)
- move_mouse: Move mouse (parameters: x, y)
- press_key: Press keyboard key (parameters: key)
- hotkey: Press key combination (parameters: keys - list of keys)
- screenshot: Take screenshot (parameters: filename)
- copy: Copy text to clipboard (parameters: text)
- paste: Paste from clipboard (parameters: none)
- search_web: Search the web (parameters: query)
- create_file: Create a file (parameters: filename, content)
- wait: Wait for seconds (parameters: seconds)

For multi-step tasks, return steps as a list. Each step should have action and parameters.

Respond ONLY with valid JSON in this exact format:
{
  "action": "action_name",
  "parameters": {},
  "steps": [],
  "description": "human readable description"
}

For single actions, steps will be empty.
For multi-step workflows, each step in steps array should have: {"action": "...", "parameters": {...}}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[
                types.Content(role="user", parts=[types.Part(text=f"Parse this command: {user_input}")])
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
            ),
        )

        if response.text:
            result = json.loads(response.text)
            return validate_command_structure(result)
        else:
            return {
                "action": "error",
                "parameters": {},
                "steps": [],
                "description": "Could not parse command"
            }

    except json.JSONDecodeError as e:
        return {
            "action": "error",
            "parameters": {"error": str(e)},
            "steps": [],
            "description": "Invalid JSON response from AI"
        }
    except Exception as e:
        return {
            "action": "error",
            "parameters": {"error": str(e)},
            "steps": [],
            "description": f"Error parsing command: {str(e)}"
        }

def get_ai_suggestion(context: str) -> str:
    """
    Get AI suggestions or help for automation tasks.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=f"As a desktop automation assistant, help with this: {context}"
        )
        return response.text or "No suggestion available"
    except Exception as e:
        return f"Error getting suggestion: {str(e)}"
