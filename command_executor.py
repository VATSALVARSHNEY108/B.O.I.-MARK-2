import os
import platform
import webbrowser
import time
import urllib.parse
from gui_automation import GUIAutomation
from contact_manager import ContactManager
from messaging_service import MessagingService
from youtube_automation import create_youtube_automation
from whatsapp_automation import create_whatsapp_automation
from code_generator import generate_code, explain_code, improve_code, debug_code
from conversation_memory import ConversationMemory
from screenshot_analyzer import analyze_screenshot, extract_text_from_screenshot, get_screenshot_summary
from screen_suggester import create_screen_suggester
from email_sender import create_email_sender
from system_monitor import get_cpu_usage, get_memory_usage, get_disk_usage, get_full_system_report, get_running_processes
from advanced_file_operations import search_files, find_large_files, find_duplicate_files, organize_files_by_extension, find_old_files, get_directory_size
from workflow_templates import WorkflowManager
from code_executor import execute_python_code, execute_javascript_code, validate_code_safety
from system_control import SystemController
from app_scheduler import AppScheduler
from download_organizer import DownloadOrganizer
from voice_assistant import VoiceAssistant
from smart_typing import SmartTyping
from file_manager import FileManager
from web_automation import WebAutomation
from productivity_monitor import ProductivityMonitor
from fun_features import FunFeatures
from spotify_automation import create_spotify_automation

class CommandExecutor:
    """Executes parsed commands using the GUI automation module"""
    
    def __init__(self):
        self.gui = GUIAutomation()
        self.contact_manager = ContactManager()
        self.messaging = MessagingService(self.contact_manager)
        self.memory = ConversationMemory()
        self.workflow_manager = WorkflowManager()
        self.youtube = create_youtube_automation(self.gui)
        self.whatsapp = create_whatsapp_automation()
        self.screen_suggester = create_screen_suggester()
        self.email_sender = create_email_sender()
        self.system_control = SystemController()
        self.app_scheduler = AppScheduler()
        self.download_organizer = DownloadOrganizer()
        self.voice_assistant = VoiceAssistant()
        self.smart_typing = SmartTyping()
        self.file_manager = FileManager()
        self.web_automation = WebAutomation()
        self.productivity_monitor = ProductivityMonitor()
        self.fun_features = FunFeatures()
        self.spotify = create_spotify_automation()
    
    def execute(self, command_dict: dict) -> dict:
        """
        Execute a command dictionary returned by Gemini.
        Returns a result dict with success status and message.
        """
        if not command_dict:
            return {"success": False, "message": "No command provided"}
        
        action = command_dict.get("action", "")
        parameters = command_dict.get("parameters", {})
        steps = command_dict.get("steps", [])
        description = command_dict.get("description", "")
        
        print(f"\n📋 Task: {description}")
        
        if steps:
            return self.execute_workflow(steps)
        else:
            return self.execute_single_action(action, parameters)
    
    def execute_workflow(self, steps: list) -> dict:
        """Execute a multi-step workflow"""
        print(f"\n🔄 Executing workflow with {len(steps)} steps...")
        
        results = []
        for i, step in enumerate(steps, 1):
            action = step.get("action", "")
            parameters = step.get("parameters", {})
            
            print(f"\n  Step {i}/{len(steps)}: {action}")
            result = self.execute_single_action(action, parameters)
            results.append(result)
            
            if not result["success"]:
                return {
                    "success": False,
                    "message": f"Workflow failed at step {i}: {result['message']}"
                }
        
        return {
            "success": True,
            "message": f"Workflow completed successfully ({len(steps)} steps)"
        }
    
    def execute_single_action(self, action: str, parameters: dict) -> dict:
        """Execute a single action"""
        try:
            if action == "open_app":
                app_name = parameters.get("app_name", "")
                success = self.gui.open_application(app_name)
                return {
                    "success": success,
                    "message": f"Opened {app_name}" if success else f"Failed to open {app_name}"
                }
            
            elif action == "type_text":
                text = parameters.get("text", "")
                interval = parameters.get("interval", 0.05)
                success = self.gui.type_text(text, interval)
                return {
                    "success": success,
                    "message": f"Typed text" if success else "Failed to type text"
                }
            
            elif action == "click":
                x = parameters.get("x")
                y = parameters.get("y")
                button = parameters.get("button", "left")
                success = self.gui.click(x, y, button)
                return {
                    "success": success,
                    "message": "Clicked" if success else "Failed to click"
                }
            
            elif action == "move_mouse":
                x = parameters.get("x", 0)
                y = parameters.get("y", 0)
                success = self.gui.move_mouse(x, y)
                return {
                    "success": success,
                    "message": f"Moved mouse to ({x}, {y})" if success else "Failed to move mouse"
                }
            
            elif action == "press_key":
                key = parameters.get("key", "")
                success = self.gui.press_key(key)
                return {
                    "success": success,
                    "message": f"Pressed {key}" if success else f"Failed to press {key}"
                }
            
            elif action == "hotkey":
                keys = parameters.get("keys", [])
                if isinstance(keys, list):
                    success = self.gui.hotkey(*keys)
                    return {
                        "success": success,
                        "message": f"Pressed {'+'.join(keys)}" if success else "Failed to press hotkey"
                    }
                else:
                    return {"success": False, "message": "Keys must be a list"}
            
            elif action == "screenshot":
                filename = parameters.get("filename", "screenshot.png")
                success = self.gui.screenshot(filename)
                return {
                    "success": success,
                    "message": f"Screenshot saved as {filename}" if success else "Failed to take screenshot"
                }
            
            elif action == "copy":
                text = parameters.get("text", "")
                success = self.gui.copy_to_clipboard(text)
                return {
                    "success": success,
                    "message": "Copied to clipboard" if success else "Failed to copy"
                }
            
            elif action == "paste":
                success = self.gui.paste_from_clipboard()
                return {
                    "success": success,
                    "message": "Pasted from clipboard" if success else "Failed to paste"
                }
            
            elif action == "wait":
                seconds = parameters.get("seconds", 1)
                success = self.gui.wait(seconds)
                return {
                    "success": success,
                    "message": f"Waited {seconds} seconds" if success else "Failed to wait"
                }
            
            elif action == "search_web":
                query = parameters.get("query", "")
                url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                webbrowser.open(url)
                return {
                    "success": True,
                    "message": f"Opened web search for: {query}"
                }
            
            elif action == "open_youtube":
                video_url = parameters.get("video_url", "")
                video_id = parameters.get("video_id", "")
                
                if video_url:
                    result = self.youtube.open_video_url(video_url)
                    return result
                elif video_id:
                    url = f"https://www.youtube.com/watch?v={video_id}"
                    result = self.youtube.open_video_url(url)
                    return result
                else:
                    return {
                        "success": False,
                        "message": "No video URL or ID provided"
                    }
            
            elif action == "search_youtube":
                query = parameters.get("query", "")
                
                if not query:
                    return {
                        "success": False,
                        "message": "No search query provided"
                    }
                
                # Use smart YouTube automation for search
                result = self.youtube.search_only(query)
                return result
            
            elif action == "play_youtube_video":
                query = parameters.get("query", "")
                method = parameters.get("method", "auto")
                
                if not query:
                    return {
                        "success": False,
                        "message": "No search query provided"
                    }
                
                print(f"  🎬 Smart YouTube Player Activated")
                print(f"  🔍 Query: {query}")
                
                # Use the smart YouTube automation module
                result = self.youtube.smart_play_video(query, method)
                
                return result
            
            elif action == "play_first_result":
                wait_time = parameters.get("wait_time", 3)
                use_mouse = parameters.get("use_mouse", True)
                
                print(f"  ▶️  Playing first video from current search results...")
                result = self.youtube.play_first_result(wait_time, use_mouse)
                
                return result
            
            elif action == "search_and_play":
                query = parameters.get("query", "")
                wait_time = parameters.get("wait_time", 3)
                use_mouse = parameters.get("use_mouse", True)
                
                if not query:
                    return {
                        "success": False,
                        "message": "No search query provided"
                    }
                
                print(f"  🎬 Searching and playing: {query}")
                result = self.youtube.search_and_play(query, wait_time, use_mouse)
                
                return result
            
            elif action == "create_file":
                filename = parameters.get("filename", "")
                content = parameters.get("content", "")
                try:
                    with open(filename, 'w') as f:
                        f.write(content)
                    return {
                        "success": True,
                        "message": f"Created file: {filename}"
                    }
                except Exception as e:
                    return {
                        "success": False,
                        "message": f"Failed to create file: {str(e)}"
                    }
            
            elif action == "send_sms":
                contact_name = parameters.get("contact_name")
                phone = parameters.get("phone")
                message = parameters.get("message", "")
                result = self.messaging.send_sms(contact_name=contact_name, phone=phone, message=message)
                return result
            
            elif action == "send_email":
                contact_name = parameters.get("contact_name")
                email = parameters.get("email")
                subject = parameters.get("subject", "")
                body = parameters.get("body", "")
                result = self.messaging.send_email(contact_name=contact_name, email=email, subject=subject, body=body)
                return result
            
            elif action == "send_html_email":
                to = parameters.get("to", "")
                subject = parameters.get("subject", "")
                html_content = parameters.get("html_content", "")
                
                if not to or not subject:
                    return {
                        "success": False,
                        "message": "Email address and subject are required"
                    }
                
                result = self.email_sender.send_html_email(to, subject, html_content)
                return result
            
            elif action == "send_email_with_attachment":
                to = parameters.get("to", "")
                subject = parameters.get("subject", "")
                body = parameters.get("body", "")
                attachments = parameters.get("attachments", [])
                
                if not to or not subject:
                    return {
                        "success": False,
                        "message": "Email address and subject are required"
                    }
                
                result = self.email_sender.send_email(
                    to=[to],
                    subject=subject,
                    body=body,
                    attachments=attachments
                )
                return result
            
            elif action == "send_template_email":
                to = parameters.get("to", "")
                template = parameters.get("template", "")
                template_vars = parameters.get("template_vars", {})
                
                if not to or not template:
                    return {
                        "success": False,
                        "message": "Email address and template name are required"
                    }
                
                result = self.email_sender.send_template_email(to, template, **template_vars)
                return result
            
            elif action == "send_file":
                contact_name = parameters.get("contact_name", "")
                file_path = parameters.get("file_path", "")
                message = parameters.get("message", "")
                method = parameters.get("method", "auto")
                result = self.messaging.send_file(contact_name, file_path, message, method)
                return result
            
            elif action == "send_whatsapp":
                phone = parameters.get("phone", "")
                message = parameters.get("message", "")
                
                if not phone:
                    return {
                        "success": False,
                        "message": "No phone number provided"
                    }
                
                if not message:
                    return {
                        "success": False,
                        "message": "No message provided"
                    }
                
                result = self.whatsapp.send_message_instantly(phone, message)
                return result
            
            elif action == "send_whatsapp_scheduled":
                phone = parameters.get("phone", "")
                message = parameters.get("message", "")
                hour = parameters.get("hour", 0)
                minute = parameters.get("minute", 0)
                
                if not phone or not message:
                    return {
                        "success": False,
                        "message": "Phone number and message are required"
                    }
                
                result = self.whatsapp.send_message_scheduled(phone, message, hour, minute)
                return result
            
            elif action == "send_whatsapp_group":
                group_id = parameters.get("group_id", "")
                message = parameters.get("message", "")
                
                if not group_id or not message:
                    return {
                        "success": False,
                        "message": "Group ID and message are required"
                    }
                
                result = self.whatsapp.send_to_group_instantly(group_id, message)
                return result
            
            elif action == "send_whatsapp_image":
                phone = parameters.get("phone", "")
                image_path = parameters.get("image_path", "")
                caption = parameters.get("caption", "")
                
                if not phone or not image_path:
                    return {
                        "success": False,
                        "message": "Phone number and image path are required"
                    }
                
                result = self.whatsapp.send_image(phone, image_path, caption)
                return result
            
            elif action == "add_contact":
                name = parameters.get("name", "")
                phone = parameters.get("phone")
                email = parameters.get("email")
                success = self.contact_manager.add_contact(name, phone, email)
                return {
                    "success": success,
                    "message": f"Added contact: {name}" if success else f"Failed to add contact: {name}"
                }
            
            elif action == "list_contacts":
                contacts = self.contact_manager.list_contacts()
                if contacts:
                    contact_list = "\n".join([
                        f"  • {c['name']} - Phone: {c['phone'] or 'N/A'}, Email: {c['email'] or 'N/A'}"
                        for c in contacts
                    ])
                    return {
                        "success": True,
                        "message": f"Contacts:\n{contact_list}"
                    }
                else:
                    return {
                        "success": True,
                        "message": "No contacts found. Use 'add contact' to create one."
                    }
            
            elif action == "get_contact":
                name = parameters.get("name", "")
                contact = self.contact_manager.get_contact(name)
                if contact:
                    return {
                        "success": True,
                        "message": f"Contact: {contact['name']}\n  Phone: {contact['phone'] or 'N/A'}\n  Email: {contact['email'] or 'N/A'}"
                    }
                else:
                    return {
                        "success": False,
                        "message": f"Contact not found: {name}"
                    }
            
            elif action == "generate_code":
                description = parameters.get("description", "")
                language = parameters.get("language", None)
                
                if not description:
                    return {
                        "success": False,
                        "message": "No code description provided"
                    }
                
                print(f"  🤖 Generating code for: {description}...")
                result = generate_code(description, language)
                
                if result.get("success"):
                    code = result["code"]
                    detected_lang = result["language"]
                    source = result.get("source", "ai")
                    
                    if source == "template":
                        print(f"  ⚡ Using built-in template (instant!)")
                    
                    print(f"\n{'='*60}")
                    print(f"  Generated {detected_lang.upper()} Code:")
                    print(f"{'='*60}")
                    print(code)
                    print(f"{'='*60}\n")
                    
                    return {
                        "success": True,
                        "message": f"✅ Generated {detected_lang} code successfully!",
                        "generated_code": code,
                        "language": detected_lang
                    }
                else:
                    return {
                        "success": False,
                        "message": f"❌ Error: {result.get('error', 'Code generation failed')}"
                    }
            
            elif action == "write_code_to_editor":
                description = parameters.get("description", "")
                language = parameters.get("language", None)
                editor = parameters.get("editor", "notepad")
                
                if not description:
                    return {
                        "success": False,
                        "message": "No code description provided"
                    }
                
                print(f"  🤖 Generating code for: {description}...")
                result = generate_code(description, language)
                
                if not result.get("success"):
                    return {
                        "success": False,
                        "message": f"❌ Code generation failed: {result.get('error', 'Unknown error')}"
                    }
                
                code = result["code"]
                detected_lang = result["language"]
                source = result.get("source", "ai")
                
                if source == "template":
                    print(f"  ⚡ Using built-in template (instant!)")
                
                print(f"\n  ✅ Generated {detected_lang} code ({len(code)} characters)")
                print(f"  📝 Opening {editor}...")
                
                self.gui.open_application(editor)
                time.sleep(2)
                
                print(f"  📋 Copying code to clipboard...")
                self.gui.copy_to_clipboard(code)
                time.sleep(0.5)
                
                print(f"  📝 Pasting code into editor...")
                self.gui.paste_from_clipboard()
                
                print(f"  ✅ Done! Code written to {editor}")
                
                return {
                    "success": True,
                    "message": f"✅ Generated and wrote {detected_lang} code to {editor}!",
                    "generated_code": code,
                    "language": detected_lang
                }
            
            elif action == "explain_code":
                code = parameters.get("code", "")
                language = parameters.get("language", "python")
                
                if not code:
                    return {
                        "success": False,
                        "message": "No code provided to explain"
                    }
                
                print(f"  🤔 Analyzing {language} code...")
                explanation = explain_code(code, language)
                
                print(f"\n{'='*60}")
                print(f"  Code Explanation:")
                print(f"{'='*60}")
                print(explanation)
                print(f"{'='*60}\n")
                
                return {
                    "success": True,
                    "message": "Code explained successfully",
                    "explanation": explanation
                }
            
            elif action == "improve_code":
                code = parameters.get("code", "")
                language = parameters.get("language", "python")
                
                if not code:
                    return {
                        "success": False,
                        "message": "No code provided to improve"
                    }
                
                print(f"  🔧 Improving {language} code...")
                result = improve_code(code, language)
                
                if result.get("success"):
                    improved = result["code"]
                    
                    print(f"\n{'='*60}")
                    print(f"  Improved Code:")
                    print(f"{'='*60}")
                    print(improved)
                    print(f"{'='*60}\n")
                    
                    return {
                        "success": True,
                        "message": "Code improved successfully",
                        "improved_code": improved
                    }
                else:
                    return {
                        "success": False,
                        "message": f"Error: {result.get('error')}"
                    }
            
            elif action == "debug_code":
                code = parameters.get("code", "")
                error_message = parameters.get("error_message", "")
                language = parameters.get("language", "python")
                
                if not code:
                    return {
                        "success": False,
                        "message": "No code provided to debug"
                    }
                
                print(f"  🐛 Debugging {language} code...")
                result = debug_code(code, error_message, language)
                
                if result.get("success"):
                    fixed = result["code"]
                    
                    print(f"\n{'='*60}")
                    print(f"  Fixed Code:")
                    print(f"{'='*60}")
                    print(fixed)
                    print(f"{'='*60}\n")
                    
                    return {
                        "success": True,
                        "message": "Code debugged and fixed",
                        "fixed_code": fixed
                    }
                else:
                    return {
                        "success": False,
                        "message": f"Error: {result.get('error')}"
                    }
            
            elif action == "analyze_screenshot":
                image_path = parameters.get("image_path", "screenshot.png")
                query = parameters.get("query", "Describe what you see")
                
                print(f"  🔍 Analyzing screenshot: {image_path}...")
                analysis = analyze_screenshot(image_path, query)
                
                print(f"\n{'='*60}")
                print(f"  Screenshot Analysis:")
                print(f"{'='*60}")
                print(analysis)
                print(f"{'='*60}\n")
                
                return {
                    "success": True,
                    "message": "Screenshot analyzed",
                    "analysis": analysis
                }
            
            elif action == "extract_text":
                image_path = parameters.get("image_path", "screenshot.png")
                
                print(f"  📝 Extracting text from: {image_path}...")
                text = extract_text_from_screenshot(image_path)
                
                print(f"\n  Extracted Text:\n{text}\n")
                
                return {
                    "success": True,
                    "message": "Text extracted from screenshot",
                    "text": text
                }
            
            elif action == "suggest_screen_improvements":
                result = self.screen_suggester.analyze_and_suggest()
                return {
                    "success": True,
                    "message": "AI suggestions generated",
                    "suggestions": result
                }
            
            elif action == "check_screen_errors":
                result = self.screen_suggester.check_for_errors()
                return {
                    "success": True,
                    "message": "Screen checked for errors",
                    "errors": result
                }
            
            elif action == "get_screen_tips":
                result = self.screen_suggester.get_quick_tips()
                return {
                    "success": True,
                    "message": "Quick tips generated",
                    "tips": result
                }
            
            elif action == "analyze_screen_code":
                result = self.screen_suggester.analyze_code()
                return {
                    "success": True,
                    "message": "Code analyzed",
                    "analysis": result
                }
            
            elif action == "analyze_screen_design":
                result = self.screen_suggester.analyze_website()
                return {
                    "success": True,
                    "message": "Design analyzed",
                    "analysis": result
                }
            
            elif action == "system_report":
                print(f"  📊 Generating system report...")
                report = get_full_system_report()
                
                print(report)
                
                return {
                    "success": True,
                    "message": "System report generated",
                    "report": report
                }
            
            elif action == "check_cpu":
                cpu = get_cpu_usage()
                msg = f"CPU Usage: {cpu['usage_percent']}% ({cpu['status']})"
                print(f"  {msg}")
                return {"success": True, "message": msg, "data": cpu}
            
            elif action == "check_memory":
                mem = get_memory_usage()
                msg = f"Memory: {mem['used_gb']}/{mem['total_gb']} ({mem['usage_percent']}% - {mem['status']})"
                print(f"  {msg}")
                return {"success": True, "message": msg, "data": mem}
            
            elif action == "check_disk":
                disk = get_disk_usage()
                msg = f"Disk: {disk['used_gb']}/{disk['total_gb']} ({disk['usage_percent']}% - {disk['status']})"
                print(f"  {msg}")
                return {"success": True, "message": msg, "data": disk}
            
            elif action == "search_files":
                pattern = parameters.get("pattern", "*")
                directory = parameters.get("directory", ".")
                
                print(f"  🔍 Searching for files: {pattern}")
                files = search_files(pattern, directory)
                
                msg = f"Found {len(files)} files matching '{pattern}'"
                print(f"\n  {msg}")
                for f in files[:20]:
                    print(f"    • {f}")
                if len(files) > 20:
                    print(f"    ... and {len(files)-20} more")
                
                return {
                    "success": True,
                    "message": msg,
                    "files": files
                }
            
            elif action == "find_large_files":
                directory = parameters.get("directory", ".")
                min_size = parameters.get("min_size_mb", 10)
                
                print(f"  🔍 Finding large files (>{min_size}MB)...")
                large_files = find_large_files(directory, min_size)
                
                print(f"\n  Found {len(large_files)} large files:")
                for f in large_files[:10]:
                    print(f"    • {f['size_mb']} - {f['path']}")
                
                return {
                    "success": True,
                    "message": f"Found {len(large_files)} large files",
                    "files": large_files
                }
            
            elif action == "directory_size":
                directory = parameters.get("directory", ".")
                
                print(f"  📊 Calculating directory size...")
                size_info = get_directory_size(directory)
                
                msg = f"{directory}: {size_info['total_size_gb']} ({size_info['file_count']} files)"
                print(f"  {msg}")
                
                return {
                    "success": True,
                    "message": msg,
                    "data": size_info
                }
            
            elif action == "save_workflow":
                name = parameters.get("name", "")
                steps = parameters.get("steps", [])
                description = parameters.get("description", "")
                
                if not name or not steps:
                    return {
                        "success": False,
                        "message": "Workflow name and steps required"
                    }
                
                success = self.workflow_manager.save_workflow(name, steps, description)
                return {
                    "success": success,
                    "message": f"Workflow '{name}' saved" if success else "Failed to save workflow"
                }
            
            elif action == "load_workflow":
                name = parameters.get("name", "")
                
                workflow = self.workflow_manager.load_workflow(name)
                if workflow:
                    return self.execute_workflow(workflow["steps"])
                else:
                    return {
                        "success": False,
                        "message": f"Workflow '{name}' not found"
                    }
            
            elif action == "list_workflows":
                workflows = self.workflow_manager.list_workflows()
                
                print(f"\n  📋 Saved Workflows ({len(workflows)}):")
                for w in workflows:
                    print(f"    • {w['name']}: {w['description']} ({w['steps_count']} steps, used {w['usage_count']} times)")
                
                return {
                    "success": True,
                    "message": f"Found {len(workflows)} workflows",
                    "workflows": workflows
                }
            
            elif action == "show_history":
                history = self.memory.get_recent_history(10)
                
                print(f"\n  📜 Recent Command History:")
                for entry in history:
                    status = "✅" if entry["result"]["success"] else "❌"
                    print(f"    {status} {entry['user_input']}")
                
                return {
                    "success": True,
                    "message": f"Showing {len(history)} recent commands",
                    "history": history
                }
            
            elif action == "show_statistics":
                stats = self.memory.get_statistics()
                
                msg = f"Total: {stats['total_commands']}, Success: {stats['successful']}, Failed: {stats['failed']}, Success Rate: {stats['success_rate']}"
                print(f"\n  📊 Statistics: {msg}")
                
                return {
                    "success": True,
                    "message": msg,
                    "statistics": stats
                }
            
            elif action == "execute_code":
                code = parameters.get("code", "")
                language = parameters.get("language", "python").lower()
                
                if not code:
                    return {
                        "success": False,
                        "message": "No code provided to execute"
                    }
                
                safety_check = validate_code_safety(code, language)
                if not safety_check["is_safe"]:
                    return {
                        "success": False,
                        "message": f"Code safety check failed: {', '.join(safety_check['warnings'])}"
                    }
                
                print(f"  ▶️  Executing {language} code...")
                
                if language == "python":
                    result = execute_python_code(code)
                elif language == "javascript":
                    result = execute_javascript_code(code)
                else:
                    return {
                        "success": False,
                        "message": f"Execution not supported for {language}"
                    }
                
                if result["success"]:
                    print(f"\n  ✅ Output:\n{result['output']}")
                    return {
                        "success": True,
                        "message": "Code executed successfully",
                        "output": result["output"]
                    }
                else:
                    print(f"\n  ❌ Error:\n{result['error']}")
                    return {
                        "success": False,
                        "message": f"Execution failed: {result['error']}"
                    }
            
            elif action == "mute_mic":
                result = self.system_control.mute_microphone()
                return {"success": True, "message": result}
            
            elif action == "unmute_mic":
                result = self.system_control.unmute_microphone()
                return {"success": True, "message": result}
            
            elif action == "set_brightness":
                level = parameters.get("level", 50)
                result = self.system_control.set_brightness(level)
                return {"success": True, "message": result}
            
            elif action == "auto_brightness":
                result = self.system_control.auto_brightness()
                return {"success": True, "message": result}
            
            elif action == "schedule_sleep":
                time_str = parameters.get("time", "23:00")
                result = self.system_control.schedule_sleep(time_str)
                return {"success": True, "message": result}
            
            elif action == "clear_temp_files":
                result = self.system_control.clear_temp_files()
                return {"success": True, "message": result}
            
            elif action == "check_disk_space":
                result = self.system_control.check_disk_space()
                return {"success": True, "message": result}
            
            elif action == "open_apps_scheduled":
                time_str = parameters.get("time", "09:00")
                apps = parameters.get("apps", [])
                result = self.app_scheduler.open_apps_at_time(time_str, apps)
                return {"success": True, "message": result}
            
            elif action == "close_heavy_apps":
                result = self.app_scheduler.detect_idle_and_close_heavy_apps()
                return {"success": True, "message": result}
            
            elif action == "get_heavy_apps":
                result = self.app_scheduler.get_heavy_apps()
                return {"success": True, "message": result}
            
            elif action == "close_app":
                app_name = parameters.get("app_name", "")
                result = self.app_scheduler.close_app(app_name)
                return {"success": True, "message": result}
            
            elif action == "organize_downloads":
                result = self.download_organizer.organize_downloads()
                return {"success": True, "message": result}
            
            elif action == "enable_auto_organize":
                result = self.download_organizer.enable_auto_organize()
                return {"success": True, "message": result}
            
            elif action == "listen_voice":
                command = self.voice_assistant.listen_once()
                return {"success": True, "message": f"Heard: {command}"}
            
            elif action == "expand_snippet":
                shortcut = parameters.get("shortcut", "")
                text = self.smart_typing.get_snippet(shortcut)
                if text:
                    import pyperclip
                    pyperclip.copy(text)
                    return {"success": True, "message": f"Snippet copied: {text[:50]}..."}
                return {"success": False, "message": f"Snippet not found: {shortcut}"}
            
            elif action == "list_snippets":
                result = self.smart_typing.list_snippets()
                return {"success": True, "message": result}
            
            elif action == "generate_email_template":
                email_type = parameters.get("type", "professional")
                result = self.smart_typing.generate_email_template(email_type)
                return {"success": True, "message": result}
            
            elif action == "auto_rename_files":
                folder = parameters.get("folder", ".")
                pattern = parameters.get("pattern", "clean")
                result = self.file_manager.auto_rename_files(folder, pattern)
                return {"success": True, "message": result}
            
            elif action == "find_duplicates":
                folder = parameters.get("folder", ".")
                result = self.file_manager.find_duplicates(folder)
                return {"success": True, "message": result}
            
            elif action == "compress_old_files":
                folder = parameters.get("folder", ".")
                days = parameters.get("days_old", 90)
                result = self.file_manager.compress_old_files(folder, days)
                return {"success": True, "message": result}
            
            elif action == "backup_folder":
                source = parameters.get("source", ".")
                result = self.file_manager.backup_folder(source)
                return {"success": True, "message": result}
            
            elif action == "get_clipboard_history":
                limit = parameters.get("limit", 10)
                result = self.web_automation.get_clipboard_history(limit)
                return {"success": True, "message": result}
            
            elif action == "search_clipboard":
                query = parameters.get("query", "")
                result = self.web_automation.search_clipboard_history(query)
                return {"success": True, "message": result}
            
            elif action == "list_scrapers":
                result = self.web_automation.list_scrapers()
                return {"success": True, "message": result}
            
            elif action == "screen_time_dashboard":
                days = parameters.get("days", 7)
                result = self.productivity_monitor.get_screen_time_dashboard(days)
                return {"success": True, "message": result}
            
            elif action == "block_distractions":
                result = self.productivity_monitor.block_distractions()
                return {"success": True, "message": result}
            
            elif action == "enable_focus_mode":
                hours = parameters.get("hours", 2)
                result = self.productivity_monitor.enable_focus_mode(hours)
                return {"success": True, "message": result}
            
            elif action == "productivity_score":
                result = self.productivity_monitor.get_productivity_score()
                return {"success": True, "message": result}
            
            elif action == "send_reminder":
                reminder_type = parameters.get("type", "water")
                result = self.productivity_monitor.send_reminder(reminder_type)
                return {"success": True, "message": result}
            
            elif action == "daily_summary":
                result = self.productivity_monitor.generate_daily_summary()
                return {"success": True, "message": result}
            
            elif action == "get_compliment":
                result = self.fun_features.get_random_compliment()
                return {"success": True, "message": result}
            
            elif action == "celebrate_task":
                result = self.fun_features.celebrate_task_completion()
                return {"success": True, "message": result}
            
            elif action == "set_mood":
                mood = parameters.get("mood", "neutral")
                result = self.fun_features.set_mood_theme(mood)
                return {"success": True, "message": result}
            
            elif action == "chatbot":
                user_input = parameters.get("message", "")
                result = self.fun_features.chatbot_respond(user_input)
                return {"success": True, "message": result}
            
            elif action == "spotify_play":
                uri = parameters.get("uri")
                result = self.spotify.play(uri)
                return result
            
            elif action == "spotify_pause":
                result = self.spotify.pause()
                return result
            
            elif action == "spotify_next":
                result = self.spotify.next_track()
                return result
            
            elif action == "spotify_previous":
                result = self.spotify.previous_track()
                return result
            
            elif action == "spotify_volume":
                volume = parameters.get("volume", 50)
                result = self.spotify.set_volume(volume)
                return result
            
            elif action == "spotify_current":
                result = self.spotify.get_current_track()
                return result
            
            elif action == "spotify_search":
                query = parameters.get("query", "")
                search_type = parameters.get("type", "track")
                limit = parameters.get("limit", 5)
                if not query:
                    return {"success": False, "message": "No search query provided"}
                result = self.spotify.search(query, search_type, limit)
                return result
            
            elif action == "spotify_play_track":
                query = parameters.get("query", "")
                if not query:
                    return {"success": False, "message": "No song/artist specified"}
                result = self.spotify.play_track(query)
                return result
            
            elif action == "spotify_playlists":
                limit = parameters.get("limit", 20)
                result = self.spotify.get_playlists(limit)
                return result
            
            elif action == "spotify_shuffle":
                state = parameters.get("state", True)
                result = self.spotify.shuffle(state)
                return result
            
            elif action == "spotify_repeat":
                state = parameters.get("state", "context")
                result = self.spotify.repeat(state)
                return result
            
            elif action == "error":
                error_msg = parameters.get("error", "Unknown error")
                return {
                    "success": False,
                    "message": f"Command parsing error: {error_msg}"
                }
            
            else:
                return {
                    "success": False,
                    "message": f"Unknown action: {action}"
                }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error executing {action}: {str(e)}"
            }
