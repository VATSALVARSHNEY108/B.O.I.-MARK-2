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

DESKTOP AUTOMATION:
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
- open_youtube: Open a YouTube video (parameters: video_url OR video_id)
- search_youtube: Search YouTube and show results (parameters: query)
- play_youtube_video: Search YouTube and auto-play first video (parameters: query)
- play_first_result: Play the first video from current YouTube search page (parameters: none)
- search_and_play: Search YouTube and play first result (parameters: query) - Alternative to play_youtube_video
- create_file: Create a file (parameters: filename, content)
- wait: Wait for seconds (parameters: seconds)

CODE GENERATION & EXECUTION:
- generate_code: Generate code using AI and display it (parameters: description, language [optional, auto-detected])
- write_code_to_editor: Generate code and write it to text editor (parameters: description, language [optional], editor [optional, default: notepad])
- explain_code: Explain what code does (parameters: code, language [optional])
- improve_code: Improve existing code (parameters: code, language [optional])
- debug_code: Fix code errors (parameters: code, error_message, language [optional])
- execute_code: Run code and show output (parameters: code, language [default: python])

SCREENSHOT ANALYSIS (VISION AI):
- analyze_screenshot: Analyze screenshot using AI vision (parameters: image_path, query [optional])
- extract_text: Extract text from screenshot (OCR) (parameters: image_path)

SYSTEM MONITORING:
- system_report: Full system health report (CPU, RAM, disk, network)
- check_cpu: Check CPU usage
- check_memory: Check RAM usage
- check_disk: Check disk space

FILE MANAGEMENT:
- search_files: Search for files (parameters: pattern, directory [optional])
- find_large_files: Find large files (parameters: directory [optional], min_size_mb [optional])
- directory_size: Get folder size (parameters: directory)

WORKFLOW TEMPLATES:
- save_workflow: Save workflow template (parameters: name, steps, description)
- load_workflow: Run saved workflow (parameters: name)
- list_workflows: Show all saved workflows

CONVERSATION MEMORY:
- show_history: Show recent command history
- show_statistics: Show usage statistics

MESSAGING & CONTACTS:
- send_sms: Send SMS text message (parameters: contact_name OR phone, message)
- send_email: Send email (parameters: contact_name OR email, subject, body)
- send_file: Send file to contact (parameters: contact_name, file_path, message [optional])
- add_contact: Add a new contact (parameters: name, phone [optional], email [optional])
- list_contacts: List all contacts (parameters: none)
- get_contact: Get contact details (parameters: name)

IMPORTANT:
- For "send to [name]" commands, use contact_name parameter
- If user says "text John" or "message Sarah", use send_sms
- If user says "email John" or "send email to Sarah", use send_email
- If user says "send this photo/file to John", use send_file with file_path
- Extract contact names accurately (e.g., "John", "Sarah", "Mom", "Boss")
- If user says "write code for X" or "generate code for X", use write_code_to_editor action with description parameter
- Extract the programming task description accurately from the user's command
- Language is optional and will be auto-detected from the description if not specified
- For "explain this code" or "what does this code do", use explain_code
- For "improve this code" or "make this code better", use improve_code
- For "fix this code" or "debug this error", use debug_code
- For "play video X" or "play X" or "watch X video", use play_youtube_video to auto-play first result
- For "search YouTube for X", use search_youtube to just show search results
- For "open youtube video [URL]" or "play this video [URL]", use open_youtube with video_url parameter
- Extract YouTube search queries accurately (e.g., "funny cats", "music video", "tutorial")
- When user says "play", "watch", "show me", they want auto-play, so use play_youtube_video
- Default to play_youtube_video for any video-related requests unless explicitly asked to just search
- Examples that should use play_youtube_video: "play song X", "watch funny videos", "show me tutorial", "play music"

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

