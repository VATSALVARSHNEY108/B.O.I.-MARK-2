import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

# Initialize client - will be set when API key is available
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
- suggest_screen_improvements: Take screenshot and get AI improvement suggestions (parameters: none)
- check_screen_errors: Take screenshot and check for visible errors/bugs (parameters: none)
- get_screen_tips: Take screenshot and get 3 quick tips (parameters: none)
- analyze_screen_code: Take screenshot and analyze visible code (parameters: none)
- analyze_screen_design: Take screenshot and analyze website/app design (parameters: none)

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
- send_html_email: Send HTML formatted email (parameters: to, subject, html_content)
- send_email_with_attachment: Send email with file attachment (parameters: to, subject, body, attachments [list])
- send_template_email: Send email using template (parameters: to, template [welcome/notification/report/invitation], template_vars)
- send_file: Send file to contact (parameters: contact_name, file_path, message [optional])
- add_contact: Add a new contact (parameters: name, phone [optional], email [optional])
- list_contacts: List all contacts (parameters: none)
- get_contact: Get contact details (parameters: name)

WHATSAPP MESSAGING:
- send_whatsapp: Send WhatsApp message instantly (parameters: phone, message)
- send_whatsapp_scheduled: Schedule WhatsApp message (parameters: phone, message, hour, minute)
- send_whatsapp_group: Send message to WhatsApp group (parameters: group_id, message)
- send_whatsapp_image: Send image via WhatsApp (parameters: phone, image_path, caption [optional])

SYSTEM CONTROL:
- mute_mic: Mute microphone (parameters: none)
- unmute_mic: Unmute microphone (parameters: none)
- set_brightness: Set screen brightness (parameters: level [0-100])
- auto_brightness: Auto-adjust brightness based on time of day (parameters: none)
- schedule_sleep: Schedule PC sleep (parameters: time [HH:MM format])
- clear_temp_files: Clear temporary files and cache (parameters: none)
- check_disk_space: Check disk space and auto-cleanup if needed (parameters: none)

APP AUTOMATION:
- open_apps_scheduled: Open apps at scheduled time (parameters: time [HH:MM], apps [list])
- close_heavy_apps: Close heavy apps when idle (parameters: none)
- get_heavy_apps: List currently running heavy apps (parameters: none)
- close_app: Close specific application (parameters: app_name)
- organize_downloads: Organize downloads folder (parameters: none)
- enable_auto_organize: Enable automatic download organization (parameters: none)

VOICE ASSISTANT:
- listen_voice: Listen for voice command (parameters: none)

SMART TYPING:
- expand_snippet: Expand text snippet shortcut (parameters: shortcut)
- list_snippets: List all text snippets (parameters: none)
- generate_email_template: Generate email template (parameters: type [professional/casual/followup/thank_you])

FILE MANAGEMENT ADVANCED:
- auto_rename_files: Auto-rename messy files (parameters: folder, pattern [clean/timestamp/numbered])
- find_duplicates: Find duplicate files (parameters: folder)
- compress_old_files: Compress old files (parameters: folder, days_old [default: 90])
- backup_folder: Backup folder to destination (parameters: source)

WEB AUTOMATION:
- get_clipboard_history: Get clipboard history (parameters: limit [default: 10])
- search_clipboard: Search clipboard history (parameters: query)
- list_scrapers: List web scraper shortcuts (parameters: none)

PRODUCTIVITY & MONITORING:
- screen_time_dashboard: Show screen time statistics (parameters: days [default: 7])
- block_distractions: Block distraction apps (parameters: none)
- enable_focus_mode: Enable focus mode (parameters: hours [default: 2])
- productivity_score: Get productivity score for today (parameters: none)
- send_reminder: Send productivity reminder (parameters: type [water/break/posture/stretch/eyes])
- daily_summary: Generate daily activity summary (parameters: none)

FUN FEATURES:
- get_compliment: Get a random compliment (parameters: none)
- celebrate_task: Celebrate task completion (parameters: none)
- set_mood: Set mood theme (parameters: mood [happy/calm/energetic/focused/neutral])
- chatbot: Chat with mini companion (parameters: message)

SPOTIFY MUSIC CONTROL (Desktop Automation - uses keyboard shortcuts):
- spotify_open: Open Spotify desktop app (parameters: none)
- spotify_play: Toggle play/pause (parameters: none)
- spotify_pause: Toggle play/pause (parameters: none)
- spotify_next: Skip to next track (parameters: none)
- spotify_previous: Go to previous track (parameters: none)
- spotify_volume_up: Increase volume (parameters: steps [default: 1])
- spotify_volume_down: Decrease volume (parameters: steps [default: 1])
- spotify_mute: Toggle mute (parameters: none)
- spotify_play_track: Search and play a song (parameters: query [song name or "song by artist"])
- spotify_shuffle: Toggle shuffle (parameters: none)
- spotify_repeat: Toggle repeat (parameters: none)

WEB TOOLS (500+ TOOLS - IN-ONE-BOX WEB APP):
- launch_web_tools: Launch the comprehensive web tools application (parameters: none)
- open_web_tool: Open a specific web tool category (parameters: category, tool [optional])
- list_web_tools: Show all available web tool categories (parameters: none)
- web_tools_status: Check if web tools app is running (parameters: none)
- stop_web_tools: Stop the web tools application (parameters: none)
- parse_web_tool_command: Parse natural language to find and open web tool (parameters: query)

Available Web Tool Categories:
- Text Tools (50+ tools): QR codes, Base64, hashes, word counter, case converter, etc.
- Image Tools (40+ tools): Format conversion, resizing, compression, filters, etc.
- File Tools (45+ tools): Compression, encryption, conversion, duplicate finder, etc.
- Coding Tools (35+ tools): Code formatter, minifier, JSON validator, regex tester, etc.
- Color Tools (20+ tools): Color picker, palette generator, gradient maker, etc.
- CSS Tools (25+ tools): CSS generator, box shadow, flexbox generator, etc.
- Data Tools (30+ tools): CSV/JSON converter, data validator, SQL formatter, etc.
- Security Tools (25+ tools): Password generator, encryption, hash generator, etc.
- Math/Science Tools (30+ tools): Calculator, unit converter, equation solver, etc.
- SEO/Marketing Tools (35+ tools): Keyword research, meta tags, sitemap creator, etc.
- Social Media Tools (30+ tools): Post scheduler, hashtag generator, analytics, etc.
- Audio/Video Tools (35+ tools): Format conversion, trimming, compression, etc.
- Web Developer Tools (40+ tools): HTML/CSS/JS formatters, performance tester, etc.
- AI Tools (30+ tools): Text generation, image analysis, language translation, etc.
- News & Events Tools (20+ tools): News aggregator, RSS reader, weather forecast, etc.

IMPORTANT:
- For "send to [name]" commands, use contact_name parameter
- If user says "text John" or "message Sarah", use send_sms
- If user says "email John" or "send email to Sarah", use send_email
- If user says "send this photo/file to John", use send_file with file_path
- If user says "whatsapp [name/number]" or "send whatsapp to [name/number]", use send_whatsapp
- For WhatsApp, phone must include country code (e.g., "+1234567890")
- If user says "suggest improvements", "analyze my screen", "what can I improve", use suggest_screen_improvements
- If user says "check for errors", "find bugs on screen", use check_screen_errors
- If user says "give me tips", "quick suggestions", use get_screen_tips
- If user says "analyze this code", "review code on screen", use analyze_screen_code
- If user says "analyze this design", "review this website", use analyze_screen_design
- If user says "schedule whatsapp at 3pm", use send_whatsapp_scheduled with hour=15
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
- For Spotify commands like "play song X on Spotify", "pause Spotify", "next song", "previous track", use spotify_ actions
- If user says "open Spotify" or "launch Spotify", use spotify_open
- If user says "play [song name] on Spotify" or "play Spotify song [name]", use spotify_play_track
- If user says "pause music" or "pause Spotify" or "stop music", use spotify_pause
- If user says "resume", "play Spotify", "continue playing", use spotify_play
- If user says "next" or "skip" or "next song", use spotify_next
- If user says "previous" or "back" or "previous song", use spotify_previous
- If user says "volume up" or "louder" or "increase volume", use spotify_volume_up
- If user says "volume down" or "quieter" or "decrease volume", use spotify_volume_down
- If user says "mute Spotify" or "mute music", use spotify_mute
- If user says "shuffle" or "shuffle on/off", use spotify_shuffle
- If user says "repeat" or "loop", use spotify_repeat
- For web tools, if user says "generate QR code", "convert image", "create hash", etc., use parse_web_tool_command with query parameter
- If user says "open text tools", "launch image converter", "show color picker", use open_web_tool with appropriate category
- If user says "list web tools", "what web tools available", "show all tools", use list_web_tools
- If user says "launch web app", "open web tools", "start toolkit", use launch_web_tools
- Examples for web tools: "generate QR code" → parse_web_tool_command with query="generate QR code"
- Examples for web tools: "convert image to PNG" → parse_web_tool_command with query="convert image to PNG"
- Examples for web tools: "open text tools" → open_web_tool with category="Text Tools"

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
        api_client = get_client()
        response = api_client.models.generate_content(
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
        api_client = get_client()
        response = api_client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=f"As a desktop automation assistant, help with this: {context}"
        )
        return response.text or "No suggestion available"
    except Exception as e:
        return f"Error getting suggestion: {str(e)}"

