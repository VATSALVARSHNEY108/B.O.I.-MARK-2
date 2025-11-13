"""
⚙️ Command Executor Module
Executes commands with intelligence, personality, and humanized feedback
Integrates all automation modules with Persona services
"""

import os
import platform
import webbrowser
import time
import urllib.parse
from modules.automation.gui_automation import GUIAutomation
from modules.automation.media_control_helper import MediaControlHelper
from modules.utilities.contact_manager import ContactManager
from modules.communication.messaging_service import MessagingService
from modules.communication.phone_dialer import create_phone_dialer
from modules.utilities.youtube_automation import create_youtube_automation
from modules.communication.whatsapp_automation import create_whatsapp_automation
from modules.ai_features.code_generation import generate_code, explain_code, improve_code, debug_code
from modules.intelligence.conversation_memory import ConversationMemory
from modules.ai_features.vision_ai import analyze_screenshot, extract_text_from_screenshot, get_screenshot_summary
from modules.monitoring.screen_suggester import create_screen_suggester
from modules.communication.email_sender import create_email_sender
from modules.system.system_monitor import get_cpu_usage, get_memory_usage, get_disk_usage, get_full_system_report, get_running_processes
from modules.file_management.advanced_file_operations import search_files, find_large_files, find_duplicate_files, organize_files_by_extension, find_old_files, get_directory_size
from modules.smart_features.workflow_templates import WorkflowManager
from modules.development.code_executor import execute_python_code, execute_javascript_code, validate_code_safety
from modules.system.system_control import SystemController
from modules.smart_features.app_scheduler import AppScheduler
from modules.automation.download_organizer import DownloadOrganizer
from modules.voice.voice_assistant import VoiceAssistant
from modules.smart_features.smart_typing import SmartTyping
from modules.file_management.file_manager import FileManager
from modules.web.web_automation import WebAutomation
from modules.productivity.productivity_monitor import ProductivityMonitor
from modules.misc.fun_features import FunFeatures
from modules.utilities.spotify_desktop_automation import create_spotify_desktop_automation
from modules.utilities.weather_news_service import WeatherNewsService
from modules.communication.translation_service import TranslationService
from modules.utilities.advanced_calculator import AdvancedCalculator
from modules.utilities.quick_info import create_quick_info
from modules.utilities.password_vault import PasswordVault
from modules.utilities.quick_notes import QuickNotes
from modules.utilities.calendar_manager import CalendarManager
from modules.integration.ecosystem_manager import EcosystemManager
from modules.web.web_tools_launcher import create_web_tools_launcher
from modules.integration.tools_mapper import create_tools_mapper
from modules.ai_features.ai_features import create_ai_features
from modules.data_analysis.data_analysis import create_data_analysis_suite
from modules.intelligence.behavioral_learning import create_behavioral_learning
from modules.file_management.workspace_manager import create_workspace_manager
from modules.core.multimodal_control import create_multimodal_control
from modules.ai_features.automation_ai import create_advanced_ai_automation
from modules.intelligence.data_intelligence import create_data_intelligence
from modules.misc.collaboration_tools import create_collaboration_tools
from modules.misc.creative_utilities import create_creative_utilities
from modules.security.security_enhancements import create_security_enhancements
from modules.integration.human_interaction import create_human_interaction
from modules.integration.cloud_ecosystem import create_cloud_ecosystem
from modules.monitoring.chat_monitor import ChatMonitor
from modules.monitoring.visual_chat_monitor import create_visual_chat_monitor
from modules.monitoring.smart_screen_monitor import create_smart_screen_monitor
from modules.intelligence.desktop_rag import DesktopRAG, create_desktop_rag
from modules.communication.communication_enhancements import CommunicationEnhancements, create_communication_enhancements
from modules.batch_file_reader import batch_reader
from modules.utilities.optimistic_weather import optimistic_weather
from modules.intelligence.persona_response_service import create_persona_service


class CommandExecutor:
    """
    Enhanced command executor with:
    - Comprehensive automation capabilities (GUI, media, system control)
    - Persona-based humanized responses
    - Desktop RAG integration for file intelligence
    - Communication enhancements for messages/emails
    - AI features (code generation, vision, NLP)
    - Data analysis and productivity monitoring
    - Multi-step workflow execution
    """
    
    def __init__(self):
        """Initialize command executor with all automation and intelligence modules"""
        # GUI and Automation
        self.gui = GUIAutomation()
        self.media_control = MediaControlHelper()
        
        # Communication
        self.contact_manager = ContactManager()
        self.messaging = MessagingService(self.contact_manager)
        self.phone_dialer = create_phone_dialer()
        self.whatsapp = create_whatsapp_automation()
        self.email_sender = create_email_sender()
        self.comm_enhancements = CommunicationEnhancements()
        
        # Media and Entertainment
        self.youtube = create_youtube_automation(self.gui)
        self.spotify = create_spotify_desktop_automation()
        
        # System Control and Monitoring
        self.system_control = SystemController()
        self.productivity_monitor = ProductivityMonitor()
        
        # File Management
        self.file_manager = FileManager()
        self.workspace_manager = create_workspace_manager()
        self.download_organizer = DownloadOrganizer()
        
        # Workflow and Productivity
        self.workflow_manager = WorkflowManager()
        self.app_scheduler = AppScheduler()
        self.smart_typing = SmartTyping()
        self.notes = QuickNotes()
        self.calendar = CalendarManager()
        
        # AI and Intelligence
        self.memory = ConversationMemory()
        self.desktop_rag = DesktopRAG()
        self.persona_service = create_persona_service()
        self.behavioral_learning = create_behavioral_learning()
        self.data_intelligence = create_data_intelligence()
        
        # Screen and Vision
        self.screen_suggester = create_screen_suggester()
        self.chat_monitor = ChatMonitor()
        self.visual_chat_monitor = create_visual_chat_monitor()
        self.smart_screen_monitor = create_smart_screen_monitor()
        
        # Utilities and Services
        self.weather_news = WeatherNewsService()
        self.translator = TranslationService()
        self.calculator = AdvancedCalculator()
        self.quick_info = create_quick_info()
        self.password_vault = PasswordVault()
        self.fun_features = FunFeatures()
        
        # Web and Integrations
        self.web_automation = WebAutomation()
        self.web_tools = create_web_tools_launcher()
        self.tools_mapper = create_tools_mapper()
        
        # Advanced AI Features
        self.ai_features = create_ai_features()
        self.data_analysis = create_data_analysis_suite()
        self.multimodal_control = create_multimodal_control()
        self.advanced_ai_automation = create_advanced_ai_automation()
        
        # Collaboration and Creative
        self.collaboration_tools = create_collaboration_tools()
        self.creative_utilities = create_creative_utilities()
        
        # Security and Cloud
        self.security_enhancements = create_security_enhancements()
        self.human_interaction = create_human_interaction()
        self.cloud_ecosystem = create_cloud_ecosystem()
        
        # Voice Assistant
        self.voice_assistant = VoiceAssistant()
        
        # Ecosystem Manager
        self.ecosystem = EcosystemManager(
            self.calendar,
            self.notes,
            self.productivity_monitor,
            self.weather_news,
            self.password_vault
        )
        
        # Tracking for persona
        self.command_count = 0
        self.error_count = 0
        
        print("⚙️ Command Executor initialized with full automation suite")
        print("   🤖 Persona Service: Active")
        print("   🧠 Desktop RAG: Active")
        print("   💬 Communication Enhancements: Active")
        print("   🎮 GUI Automation: Active")
        print("   📊 40+ Modules Loaded")
    
    def _humanize_result(self, action: str, result: dict) -> dict:
        """
        Wrap results with persona humanization
        Add milestone celebrations and helpful tips
        """
        self.command_count += 1
        
        if not result.get("success", False):
            self.error_count += 1
        
        humanized_message = self.persona_service.humanize_response(
            action=action,
            result=result,
            context={"command_count": self.command_count}
        )
        
        final_message = humanized_message
        
        return {
            "success": result.get("success", False),
            "message": final_message,
            "original_result": result
        }
    
    def execute(self, command_dict: dict) -> dict:
        """
        Execute a command dictionary returned by Gemini.
        Returns a result dict with success status and message (humanized).
        """
        # Stop any ongoing AI speech when new task is executed
        if hasattr(self, 'voice_assistant') and self.voice_assistant:
            self.voice_assistant.stop_speaking()
        
        try:
            if not isinstance(command_dict, dict):
                return {
                    "success": False,
                    "message": "Invalid command format: expected dictionary"
                }
            
            action = command_dict.get("action", "")
            parameters = command_dict.get("parameters", {})
            steps = command_dict.get("steps", [])
            description = command_dict.get("description", "")

            print(f"\n📋 Task: {description}")

            # Check for workflow first (workflows may not have action field)
            if steps and len(steps) > 0:
                return self.execute_workflow(steps)
            else:
                # Single action - validate action is present
                if not action:
                    return {
                        "success": False,
                        "message": "No action specified in command"
                    }
                
                result = self.execute_single_action(action, parameters)
                
                # Check if result is already humanized
                if isinstance(result, dict) and "original_result" in result:
                    return result
                
                # Apply humanization
                return self._humanize_result(action, result)
        
        except Exception as e:
            error_result = {
                "success": False,
                "message": f"Error executing command: {str(e)}"
            }
            return self._humanize_result("command_execution", error_result)

    def execute_workflow(self, steps: list) -> dict:
        """Execute a multi-step workflow with humanized feedback"""
        results = []
        all_success = True
        
        intro_msg = self.persona_service.handle_processing()
        print(intro_msg)
        print(f"\n🔄 Executing workflow with {len(steps)} steps...")

        for i, step in enumerate(steps, 1):
            action = step.get("action")
            parameters = step.get("parameters", {})

            print(f"\n  Step {i}/{len(steps)}: {action}")
            
            step_result = self.execute_single_action(action, parameters)
            results.append({
                "step": i,
                "action": action,
                "result": step_result
            })

            if not step_result.get("success", False):
                all_success = False
                error_msg = self.persona_service.handle_misunderstanding()
                print(f"❌ {error_msg}")
                break

        workflow_result = {
            "success": all_success,
            "message": f"Workflow completed: {len(results)}/{len(steps)} steps executed",
            "steps": results
        }
        
        return self._humanize_result("workflow", workflow_result)

    def execute_single_action(self, action: str, parameters: dict) -> dict:
        """Execute a single action - comprehensive action handler"""
        parameters = parameters or {}
        
        try:
            # ==================== GUI AUTOMATION ====================
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

            # ==================== QUICK INFORMATION ====================
            elif action == "get_time":
                result = self.quick_info.get_current_time()
                return {
                    "success": True,
                    "message": result
                }

            elif action == "get_date":
                result = self.quick_info.get_current_date(detailed=True)
                return {
                    "success": True,
                    "message": result
                }

            elif action == "get_day_info":
                result = self.quick_info.get_day_info()
                return {
                    "success": True,
                    "message": result
                }

            elif action == "get_week_info":
                result = self.quick_info.get_week_info()
                return {
                    "success": True,
                    "message": result
                }

            elif action == "get_month_info":
                result = self.quick_info.get_month_info()
                return {
                    "success": True,
                    "message": result
                }

            elif action == "get_year_info":
                result = self.quick_info.get_year_info()
                return {
                    "success": True,
                    "message": result
                }

            elif action == "get_date_time":
                result = self.quick_info.get_date_and_time()
                return {
                    "success": True,
                    "message": result
                }

            elif action == "read_desktop_time":
                result = batch_reader.read_desktop_time()
                return {
                    "success": result.get("success"),
                    "message": result.get("message")
                }

            elif action == "read_reminders":
                result = batch_reader.read_reminders()
                if result.get("success") and result.get("reminders"):
                    formatted = batch_reader.format_reminders_for_display(result["reminders"])
                    return {
                        "success": True,
                        "message": formatted
                    }
                return {
                    "success": result.get("success"),
                    "message": result.get("message")
                }

            elif action == "add_reminder":
                text = parameters.get("text", "")
                due_time = parameters.get("due_time", "")
                if not text:
                    return {
                        "success": False,
                        "message": "Please provide reminder text"
                    }
                result = batch_reader.add_reminder_via_python(text, due_time)
                return {
                    "success": result.get("success"),
                    "message": result.get("message")
                }

            # ==================== WEATHER ====================
            elif action == "get_quick_weather":
                city = parameters.get("city", "New York")
                result = self.weather_news.get_weather(city)
                return {
                    "success": True,
                    "message": result
                }

            elif action == "get_forecast":
                city = parameters.get("city", "New York")
                days = parameters.get("days", 3)
                try:
                    days = int(days)
                    days = max(1, min(days, 7))
                except (ValueError, TypeError):
                    days = 3
                result = self.weather_news.get_forecast(city, days)
                return {
                    "success": True,
                    "message": result
                }

            elif action == "get_optimistic_weather":
                city = parameters.get("city", "New York")
                result = optimistic_weather.get_optimistic_weather_from_api(city)
                return {
                    "success": True,
                    "message": result
                }

            elif action == "get_optimistic_forecast":
                city = parameters.get("city", "New York")
                days = parameters.get("days", 3)
                try:
                    days = int(days)
                    days = max(1, min(days, 7))
                except (ValueError, TypeError):
                    days = 3
                result = optimistic_weather.get_forecast_optimistic(city, days)
                return {
                    "success": True,
                    "message": result
                }

            # ==================== WEB BROWSING ====================
            elif action == "search_web":
                query = parameters.get("query", "")
                url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                webbrowser.open(url)
                return {
                    "success": True,
                    "message": f"Opened web search for: {query}"
                }

            # ==================== FOLDER OPERATIONS ====================
            elif action == "open_folder":
                folder_path = parameters.get("folder_path")
                folder_name = parameters.get("folder_name")
                success = self.gui.open_folder(folder_path=folder_path, folder_name=folder_name)
                if success:
                    target = folder_path if folder_path else folder_name
                    return {
                        "success": True,
                        "message": f"Opened folder: {target}"
                    }
                else:
                    base_msg = "Failed to open folder"
                    if folder_name:
                        base_msg = f"Failed to open folder: {folder_name}"
                    
                    suggestions = self.gui.last_folder_suggestions
                    if suggestions:
                        suggestions_text = ", ".join(f"'{s}'" for s in suggestions[:5])
                        base_msg += f". Did you mean: {suggestions_text}?"
                    
                    return {
                        "success": False,
                        "message": base_msg,
                        "suggestions": suggestions if suggestions else []
                    }

            elif action == "open_desktop_folder":
                folder_name = parameters.get("folder_name")
                success = self.gui.open_desktop_folder(folder_name=folder_name)
                if success:
                    msg = f"Opened Desktop folder: {folder_name}" if folder_name else "Opened Desktop"
                    return {
                        "success": True,
                        "message": msg
                    }
                else:
                    base_msg = f"Failed to open Desktop folder: {folder_name}" if folder_name else "Failed to open Desktop"
                    suggestions = self.gui.last_folder_suggestions
                    if suggestions:
                        suggestions_text = ", ".join(f"'{s}'" for s in suggestions[:5])
                        base_msg += f". Did you mean: {suggestions_text}?"
                    return {
                        "success": False,
                        "message": base_msg,
                        "suggestions": suggestions
                    }

            elif action == "open_desktop":
                success = self.gui.open_desktop_folder()
                return {
                    "success": success,
                    "message": "Opened Desktop" if success else "Failed to open Desktop"
                }

            # ==================== YOUTUBE ====================
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
            
            # ==================== MEDIA CONTROL ====================
            elif action == "stop_media":
                print(f"  ⏹️  Stopping media playback...")
                return self.media_control.stop()
            
            elif action == "pause_media" or action == "play_pause_media":
                print(f"  ⏸️  Toggling play/pause...")
                return self.media_control.play_pause()
            
            elif action == "next_track":
                print(f"  ⏭️  Next track...")
                return self.media_control.next_track()
            
            elif action == "previous_track":
                print(f"  ⏮️  Previous track...")
                return self.media_control.previous_track()
            
            elif action == "play_media":
                print(f"  ▶️  Playing media...")
                return self.media_control.play()
            
            # ==================== SYSTEM MONITORING ====================
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

            # ==================== FILE OPERATIONS ====================
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

            # ==================== WORKFLOWS ====================
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

            # ==================== CONVERSATION MEMORY ====================
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

            # ==================== CODE GENERATION AND ANALYSIS ====================
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

            # ==================== VISION AI ====================
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

            # ==================== SMART SCREEN ANALYSIS ====================
            elif action == "smart_analyze_screen":
                focus = parameters.get("focus", "general")
                
                print(f"\n🔍 Smart Screen Analysis (focus: {focus})...")
                result = self.smart_screen_monitor.analyze_current_screen(focus)
                
                if result.get("success"):
                    return {
                        "success": True,
                        "message": f"📸 Screen Analysis ({focus}):\n\n{result['analysis']}"
                    }
                else:
                    return result

            elif action == "detect_screen_changes":
                interval = parameters.get("interval", 5)
                duration = parameters.get("duration", 30)
                
                print(f"\n👁️ Detecting screen changes (interval: {interval}s, duration: {duration}s)...")
                result = self.smart_screen_monitor.detect_screen_changes(interval, duration)
                
                return {
                    "success": result.get("success", False),
                    "message": result.get("message", "Screen change detection complete")
                }

            elif action == "monitor_for_content":
                target = parameters.get("target", "")
                check_interval = parameters.get("check_interval", 10)
                max_checks = parameters.get("max_checks", 6)
                
                if not target:
                    return {
                        "success": False,
                        "message": "Please specify what content to monitor for"
                    }
                
                print(f"\n👀 Monitoring screen for: {target}")
                result = self.smart_screen_monitor.monitor_for_specific_content(target, check_interval, max_checks)
                
                if result.get("success"):
                    # Preserve all original data from SmartScreenMonitor
                    if result.get("found"):
                        # Build user-friendly message but keep all original fields
                        user_message = f"✅ {result.get('message', 'Content found!')}"
                        if result.get('details'):
                            user_message += f"\n\n{result['details']}"
                        # Update message but preserve all other fields
                        result["message"] = user_message
                    return result
                else:
                    return result

            elif action == "productivity_check":
                print("\n📊 Running productivity analysis...")
                result = self.smart_screen_monitor.analyze_current_screen("productivity")
                
                if result.get("success"):
                    return {
                        "success": True,
                        "message": f"📊 Productivity Analysis:\n\n{result['analysis']}"
                    }
                else:
                    return result

            elif action == "ask_about_screen":
                question = parameters.get("question", "")
                
                if not question:
                    return {
                        "success": False,
                        "message": "Please provide a question about the screen"
                    }
                
                print(f"\n❓ Analyzing screen for: {question}")
                result = self.smart_screen_monitor.smart_screenshot_with_context(question)
                
                if result.get("success"):
                    return {
                        "success": True,
                        "message": f"❓ Q: {result['question']}\n\n💡 Answer: {result['answer']}",
                        "screenshot": result.get("screenshot"),
                        "question": result.get("question"),
                        "answer": result.get("answer")
                    }
                else:
                    return result

            # ==================== SCREEN MONITORING ====================
            elif action == "monitor_screen":
                query = parameters.get("query", "What's happening on my screen?")

                if not query:
                    return {
                        "success": False,
                        "message": "No question provided"
                    }

                result = self.smart_screen_monitor.smart_screenshot_with_context(query)

                if result["success"]:
                    return {
                        "success": True,
                        "message": f"❓ Q: {result['question']}\n\n💡 A: {result['answer']}"
                    }
                return result

            # ==================== CONTACTS ====================
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

            # ==================== SYSTEM CONTROL ====================
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

            elif action == "increase_brightness":
                amount = parameters.get("amount", 10)
                result = self.system_control.increase_brightness(amount)
                return {"success": True, "message": result}

            elif action == "decrease_brightness":
                amount = parameters.get("amount", 10)
                result = self.system_control.decrease_brightness(amount)
                return {"success": True, "message": result}

            elif action == "get_brightness":
                level = self.system_control.get_brightness()
                if level is not None:
                    return {"success": True, "message": f"☀️ Current brightness: {level}%"}
                else:
                    return {"success": False, "message": "Unable to retrieve brightness level"}

            elif action == "set_volume":
                level = parameters.get("level", 50)
                result = self.system_control.set_volume(level)
                return {"success": True, "message": result}

            elif action == "increase_volume":
                amount = parameters.get("amount", 10)
                result = self.system_control.increase_volume(amount)
                return {"success": True, "message": result}

            elif action == "decrease_volume":
                amount = parameters.get("amount", 10)
                result = self.system_control.decrease_volume(amount)
                return {"success": True, "message": result}

            elif action == "volume_up":
                amount = parameters.get("amount", 10)
                result = self.system_control.increase_volume(amount)
                return {"success": True, "message": result}

            elif action == "volume_down":
                amount = parameters.get("amount", 10)
                result = self.system_control.decrease_volume(amount)
                return {"success": True, "message": result}

            elif action == "mute_volume":
                result = self.system_control.mute_volume()
                return {"success": True, "message": result}

            elif action == "unmute_volume":
                result = self.system_control.unmute_volume()
                return {"success": True, "message": result}

            elif action == "toggle_mute":
                result = self.system_control.toggle_mute()
                return {"success": True, "message": result}

            elif action == "get_volume":
                result = self.system_control.get_volume_info()
                return {"success": True, "message": result}

            # ==================== DESKTOP RAG ====================
            elif action == "index_desktop_rag":
                folder_path = parameters.get("folder_path", ".")
                result = self.desktop_rag.index_folder(folder_path)
                if result.get("success"):
                    msg = f"✅ Desktop indexed successfully!\n\n"
                    msg += f"📊 Indexed {result['files_indexed']} files\n"
                    msg += f"💾 Total size: {result['total_size_mb']} MB\n"
                    msg += f"⏱️  Time: {result['time_taken']:.2f}s\n"
                    return {"success": True, "message": msg}
                else:
                    return {"success": False, "message": f"❌ Error: {result.get('error', 'Unknown error')}"}

            elif action == "search_files_rag":
                query = parameters.get("query", "")
                if not query:
                    return {"success": False, "message": "Please provide a search query"}
                
                result = self.desktop_rag.search_files(query)
                if result.get("success"):
                    msg = f"🔍 Search Results for: '{query}'\n\n"
                    msg += f"Found {result['total_results']} relevant files\n\n"
                    if result.get('relevant_files'):
                        msg += "Top matches:\n"
                        for f in result.get('relevant_files')[:5]:
                            msg += f"  • {f}\n"
                    return {"success": True, "message": msg}
                else:
                    return {"success": False, "message": f"❌ Error: {result.get('error', 'Unknown error')}"}

            elif action == "summarize_folder_rag":
                folder_path = parameters.get("folder_path", ".")
                result = self.desktop_rag.summarize_folder(folder_path)
                if result.get("success"):
                    msg = f"📊 Folder Summary: {folder_path}\n\n"
                    msg += f"📁 Files: {result['file_count']}\n"
                    msg += f"💾 Size: {result['total_size_mb']} MB\n\n"
                    msg += f"AI Analysis:\n{result['summary']}\n"
                    return {"success": True, "message": msg}
                else:
                    return {"success": False, "message": f"❌ Error: {result.get('error', 'Unknown error')}"}

            elif action == "find_duplicates_rag":
                result = self.desktop_rag.find_duplicates_smart()
                if result.get("success"):
                    msg = f"🔍 Smart Duplicate Detection\n\n"
                    msg += f"Found {result['duplicates_found']} potential duplicates\n"
                    msg += f"💾 Potential savings: {result['potential_savings_mb']:.2f} MB\n\n"
                    if result.get('duplicates'):
                        msg += "Top duplicates:\n"
                        for dup in result['duplicates'][:10]:
                            msg += f"\n  • {dup['name']}\n"
                            msg += f"    File 1: {dup['file1']}\n"
                            msg += f"    File 2: {dup['file2']}\n"
                            msg += f"    Confidence: {dup['confidence']}\n"
                    return {"success": True, "message": msg}
                else:
                    return {"success": False, "message": "❌ Error finding duplicates"}

            elif action == "get_rag_stats":
                stats = self.desktop_rag.get_index_stats()
                msg = f"📊 Desktop RAG Index Statistics\n\n"
                msg += f"Total files indexed: {stats['total_files']}\n"
                if stats['total_files'] > 0:
                    msg += f"Files with text content: {stats['files_with_text_content']}\n"
                    msg += f"Total size: {stats['total_size_mb']} MB\n"
                    msg += f"Last updated: {stats['last_updated']}\n\n"
                    msg += "Top file types:\n"
                    for ext, count in list(stats['file_types'].items())[:10]:
                        msg += f"  {ext}: {count} files\n"
                else:
                    msg += "\nNo files indexed yet. Try 'Index my desktop files' first."
                return {"success": True, "message": msg}

            # ==================== COMMUNICATION ENHANCEMENTS ====================
            elif action == "transcribe_voice":
                audio_file = parameters.get("audio_file")
                audio_url = parameters.get("audio_url")
                result = self.comm_enhancements.transcribe_voice_message(audio_file, audio_url)
                if result.get("success"):
                    return {"success": True, "message": f"🎤 Voice Transcription:\n\n{result['transcription']}"}
                else:
                    return {"success": False, "message": result.get("message", "Transcription failed")}

            elif action == "generate_smart_replies":
                message_data = parameters.get("message_data", {})
                context = parameters.get("context", "professional")
                result = self.comm_enhancements.generate_smart_replies(message_data, context)
                if result.get("success"):
                    msg = f"💬 {result['message']}\n\n"
                    for i, reply in enumerate(result['replies'], 1):
                        msg += f"Option {i} ({reply['type']}):\n{reply['text']}\n\n"
                    return {"success": True, "message": msg}
                else:
                    return {"success": False, "message": result.get("message")}

            elif action == "rank_emails":
                emails = parameters.get("emails", [])
                result = self.comm_enhancements.rank_emails_by_priority(emails)
                if result.get("success"):
                    msg = f"📊 {result['message']}\n\n"
                    summary = result.get("summary", {})
                    msg += f"Critical: {summary.get('critical', 0)} | High: {summary.get('high', 0)} | "
                    msg += f"Medium: {summary.get('medium', 0)} | Low: {summary.get('low', 0)}\n\n"
                    msg += "Top Priority Emails:\n"
                    for i, email in enumerate(result['ranked_emails'][:5], 1):
                        msg += f"\n{i}. [{email['priority_level']}] {email.get('subject', 'No subject')}\n"
                        msg += f"   From: {email.get('from', 'Unknown')}\n"
                        msg += f"   Score: {email['priority_score']}/100\n"
                    return {"success": True, "message": msg}
                else:
                    return {"success": False, "message": result.get("message")}

            elif action == "add_followup":
                message_data = parameters.get("message_data", {})
                days = parameters.get("days", 3)
                result = self.comm_enhancements.add_follow_up_reminder(message_data, days)
                if result.get("success"):
                    return {"success": True, "message": f"⏰ {result['message']}\nRemind at: {result['remind_date']}"}
                else:
                    return {"success": False, "message": result.get("message")}

            elif action == "check_followups":
                result = self.comm_enhancements.check_follow_up_reminders()
                if result.get("success"):
                    msg = f"{result['message']}\n\n"
                    if result['due_reminders']:
                        msg += "Due Follow-ups:\n"
                        for reminder in result['due_reminders']:
                            msg += f"\n• {reminder['message'].get('subject', 'Message')}\n"
                            msg += f"  From: {reminder['message'].get('from')}\n"
                            msg += f"  Platform: {reminder['message'].get('platform')}\n"
                    return {"success": True, "message": msg}
                else:
                    return {"success": False, "message": result.get("message")}

            elif action == "send_meeting_notes":
                meeting_data = parameters.get("meeting_data", {})
                recipients = parameters.get("recipients", [])
                result = self.comm_enhancements.send_meeting_notes(meeting_data, recipients)
                return result

            elif action == "summarize_chat":
                messages = parameters.get("messages", [])
                platform = parameters.get("platform", "Slack")
                result = self.comm_enhancements.summarize_chat_thread(messages, platform)
                if result.get("success"):
                    return {"success": True, "message": f"📝 {result['message']}\n\n{result['summary']}"}
                else:
                    return {"success": False, "message": result.get("message")}

            elif action == "multilingual_reply":
                message_data = parameters.get("message_data", {})
                detect = parameters.get("detect_language", True)
                result = self.comm_enhancements.generate_multilingual_reply(message_data, detect)
                if result.get("success"):
                    msg = f"🌐 {result['message']}\n\n"
                    msg += f"Language: {result['detected_language']}\n\n"
                    msg += f"Reply:\n{result['reply']}"
                    return {"success": True, "message": msg}
                else:
                    return {"success": False, "message": result.get("message")}

            elif action == "voice_to_task":
                voice_text = parameters.get("voice_text", "")
                add_to_calendar = parameters.get("add_to_calendar", True)
                result = self.comm_enhancements.convert_voice_to_task(voice_text, add_to_calendar)
                if result.get("success"):
                    extracted = result['extracted']
                    msg = f"✅ {result['message']}\n\n"
                    msg += f"Type: {extracted.get('type', 'task').upper()}\n"
                    msg += f"Title: {extracted.get('title')}\n"
                    msg += f"Priority: {extracted.get('priority')}\n"
                    if extracted.get('datetime'):
                        msg += f"Date/Time: {extracted['datetime']}\n"
                    msg += f"Category: {extracted.get('category')}\n\n"
                    msg += f"Action Items:\n"
                    for item in extracted.get('action_items', []):
                        msg += f"  • {item}\n"
                    return {"success": True, "message": msg}
                else:
                    return {"success": False, "message": result.get("message")}

            elif action == "comm_features_summary":
                summary = self.comm_enhancements.get_feature_summary()
                return {"success": True, "message": summary}

            # ==================== CHATBOT / AI CHAT ====================
            elif action == "chatbot" or action == "chat" or action == "ask":
                from modules.core.gemini_controller import chat_response
                message = parameters.get("message", "")
                if not message:
                    return {"success": False, "message": "Please provide a message to chat"}
                
                try:
                    response = chat_response(message)
                    return {"success": True, "message": f"🤖 {response}"}
                except Exception as e:
                    return {"success": False, "message": f"Chat error: {str(e)}"}
            
            elif action == "conversational_ai":
                from modules.core.gemini_controller import chat_response
                message = parameters.get("message", "")
                context = parameters.get("context", "general")
                
                try:
                    response = chat_response(message)
                    return {"success": True, "message": response}
                except Exception as e:
                    return {"success": False, "message": f"Error: {str(e)}"}
            
            elif action == "customer_service_bot":
                from modules.core.gemini_controller import chat_response
                query = parameters.get("query", "")
                company_context = parameters.get("company_context", "")
                
                prompt = f"Customer query: {query}\nCompany context: {company_context}" if company_context else query
                try:
                    response = chat_response(prompt)
                    return {"success": True, "message": response}
                except Exception as e:
                    return {"success": False, "message": f"Error: {str(e)}"}
            
            elif action == "educational_assistant":
                from modules.core.gemini_controller import chat_response
                topic = parameters.get("topic", "")
                question = parameters.get("question", "")
                level = parameters.get("level", "intermediate")
                
                prompt = f"Topic: {topic}\nLevel: {level}\nQuestion: {question}"
                try:
                    response = chat_response(prompt)
                    return {"success": True, "message": response}
                except Exception as e:
                    return {"success": False, "message": f"Error: {str(e)}"}
            
            elif action == "domain_expert":
                from modules.core.gemini_controller import chat_response
                domain = parameters.get("domain", "")
                question = parameters.get("question", "")
                
                prompt = f"As an expert in {domain}, please answer: {question}"
                try:
                    response = chat_response(prompt)
                    return {"success": True, "message": response}
                except Exception as e:
                    return {"success": False, "message": f"Error: {str(e)}"}
            
            # ==================== TEXT GENERATION AI ====================
            elif action == "story_writer":
                from modules.core.gemini_controller import chat_response
                prompt_text = parameters.get("prompt", "")
                genre = parameters.get("genre", "general")
                length = parameters.get("length", "medium")
                
                full_prompt = f"Write a {length} {genre} story based on: {prompt_text}"
                try:
                    response = chat_response(full_prompt)
                    return {"success": True, "message": f"📖 Story:\n\n{response}"}
                except Exception as e:
                    return {"success": False, "message": f"Error: {str(e)}"}
            
            elif action == "content_creator":
                from modules.core.gemini_controller import chat_response
                topic = parameters.get("topic", "")
                content_type = parameters.get("content_type", "blog post")
                tone = parameters.get("tone", "professional")
                
                prompt = f"Create a {tone} {content_type} about: {topic}"
                try:
                    response = chat_response(prompt)
                    return {"success": True, "message": f"✍️ Content:\n\n{response}"}
                except Exception as e:
                    return {"success": False, "message": f"Error: {str(e)}"}

            # ==================== DEFAULT ====================
            else:
                return {
                    "success": False,
                    "message": f"Unknown action: {action}"
                }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error executing action '{action}': {str(e)}"
            }
