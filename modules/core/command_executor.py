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
from datetime import datetime
from modules.automation.gui_automation import GUIAutomation
from modules.automation.media_control_helper import MediaControlHelper
from modules.utilities.contact_manager import ContactManager
from modules.communication.messaging_service import MessagingService
from modules.communication.phone_dialer import create_phone_dialer
from modules.communication.phone_link_monitor import create_phone_link_monitor
from modules.utilities.youtube_automation import YouTubeAutomator
from modules.web.selenium_web_automator import SeleniumWebAutomator
from modules.communication.whatsapp_automation import create_whatsapp_automation
from scripts.whatsapp_contact_manager import WhatsAppContactManager
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
from modules.system.windows11_settings_controller import get_windows11_controller
from modules.smart_features.app_scheduler import AppScheduler
from modules.automation.download_organizer import DownloadOrganizer
from modules.voice.voice_assistant import VoiceAssistant
from modules.smart_features.smart_typing import SmartTyping
from modules.file_management.file_manager import FileManager
from modules.web.web_automation import WebAutomation
from modules.productivity.productivity_monitor import ProductivityMonitor
from modules.misc.fun_features import FunFeatures
from modules.utilities.spotify_desktop_automation import create_spotify_desktop_automation
from modules.utilities.spotify_local import SpotifyLocal
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
from modules.voice.feature_speaker import create_feature_speaker

# Future-Tech Core
try:
    from modules.core.future_tech_core import create_future_tech_core
    FUTURE_TECH_AVAILABLE = True
except ImportError:
    FUTURE_TECH_AVAILABLE = False
    print("⚠️ Future-Tech Core not available")


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
        self.contact_manager = ContactManager("data/contacts.json")
        self.messaging = MessagingService(self.contact_manager)
        self.phone_dialer = create_phone_dialer()
        self.phone_link_monitor = create_phone_link_monitor()
        self.whatsapp = create_whatsapp_automation()
        self.whatsapp_contacts = WhatsAppContactManager()
        self.email_sender = create_email_sender()
        self.comm_enhancements = CommunicationEnhancements()
        
        # Media and Entertainment
        self.youtube = YouTubeAutomator()
        self.selenium_youtube = None
        
        # Spotify - Try API mode first, fallback to desktop mode
        self.spotify_mode = "desktop"
        try:
            if os.getenv('SPOTIFY_CLIENT_ID') and os.getenv('SPOTIFY_CLIENT_SECRET'):
                self.spotify = SpotifyLocal()
                self.spotify_mode = "api"
                print("🎵 Spotify API mode enabled")
            else:
                self.spotify = create_spotify_desktop_automation()
                print("🎵 Spotify Desktop mode (limited features)")
        except Exception as e:
            self.spotify = create_spotify_desktop_automation()
            print(f"🎵 Spotify Desktop mode (API failed: {e})")
        
        # System Control and Monitoring
        self.system_control = SystemController()
        self.productivity_monitor = ProductivityMonitor()
        
        # Windows 11 Settings Controller (only on Windows)
        if platform.system() == "Windows":
            try:
                self.win11_settings = get_windows11_controller()
                print("⚙️ Windows 11 Settings Controller: Active")
            except Exception as e:
                self.win11_settings = None
                print(f"⚠️ Windows 11 Settings Controller unavailable: {e}")
        else:
            self.win11_settings = None
        
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
        
        # Voice Assistant & Feature Speaker
        self.voice_assistant = VoiceAssistant()
        try:
            self.feature_speaker = create_feature_speaker()
            print("🔊 Feature Speaker: ACTIVE")
        except Exception as e:
            self.feature_speaker = None
            print(f"⚠️ Feature Speaker unavailable: {e}")
        
        # Ecosystem Manager
        self.ecosystem = EcosystemManager(
            self.calendar,
            self.notes,
            self.productivity_monitor,
            self.weather_news,
            self.password_vault
        )
        
        # Future-Tech Core (Ultra-Advanced AI System)
        if FUTURE_TECH_AVAILABLE:
            try:
                self.future_tech = create_future_tech_core()
                print("🌟 Future-Tech Core: ACTIVE")
            except Exception as e:
                self.future_tech = None
                print(f"⚠️ Future-Tech Core initialization failed: {e}")
        else:
            self.future_tech = None
        
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
    
    def _expand_path_shortcuts(self, file_path: str) -> str:
        """
        Expand common path shortcuts to full paths
        Supports: Desktop, Downloads, Documents, Home, etc.
        Handles OneDrive synced folders
        IMPORTANT: Always returns paths with forward slashes to avoid escape character issues
        """
        from pathlib import Path
        import re
        
        # Remove any quotes
        file_path = file_path.strip('"').strip("'")
        
        # Get common user directories
        home = Path.home()
        
        # Check for OneDrive Desktop first (common on Windows)
        onedrive_desktop = home / "OneDrive" / "Desktop"
        if onedrive_desktop.exists():
            desktop = onedrive_desktop
        else:
            desktop = home / "Desktop"
        
        # Check for OneDrive Documents
        onedrive_documents = home / "OneDrive" / "Documents"
        if onedrive_documents.exists():
            documents = onedrive_documents
        else:
            documents = home / "Documents"
        
        # Downloads is typically not synced by OneDrive
        downloads = home / "Downloads"
        
        # Pictures might be in OneDrive
        onedrive_pictures = home / "OneDrive" / "Pictures"
        if onedrive_pictures.exists():
            pictures = onedrive_pictures
        else:
            pictures = home / "Pictures"
        
        # Convert paths to strings with forward slashes (avoid escape character issues)
        desktop_str = str(desktop).replace('\\', '/')
        documents_str = str(documents).replace('\\', '/')
        downloads_str = str(downloads).replace('\\', '/')
        pictures_str = str(pictures).replace('\\', '/')
        home_str = str(home).replace('\\', '/')
        
        # Case-insensitive replacement patterns (use forward slashes)
        replacements = {
            r'^desktop[/\\]': desktop_str + '/',
            r'^downloads[/\\]': downloads_str + '/',
            r'^documents[/\\]': documents_str + '/',
            r'^pictures[/\\]': pictures_str + '/',
            r'^home[/\\]': home_str + '/',
            r'^~[/\\]': home_str + '/',
        }
        
        # Check each pattern
        file_path_lower = file_path.lower()
        for pattern, replacement in replacements.items():
            if re.match(pattern, file_path_lower):
                # Preserve the original case of the filename
                file_path = re.sub(pattern, replacement, file_path, flags=re.IGNORECASE)
                break
        
        # Handle special case: just "desktop" or "Desktop" -> Desktop path
        if file_path_lower == "desktop":
            file_path = desktop_str
        elif file_path_lower == "downloads":
            file_path = downloads_str
        elif file_path_lower == "documents":
            file_path = documents_str
        
        # Ensure all backslashes are converted to forward slashes
        file_path = file_path.replace('\\', '/')
        
        return file_path
    
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

                if not query:
                    return {
                        "success": False,
                        "message": "No search query provided"
                    }

                # Search YouTube and play first video in Brave
                result = self.youtube.search_and_play(query)
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
            
            # ==================== SPOTIFY CONTROL ====================
            elif action == "spotify_play":
                print(f"  ▶️  Playing Spotify...")
                result = self.spotify.play()
                return {"success": True, "message": result if isinstance(result, str) else result.get("message", "Playing")}
            
            elif action == "spotify_pause":
                print(f"  ⏸️  Pausing Spotify...")
                result = self.spotify.pause()
                return {"success": True, "message": result if isinstance(result, str) else result.get("message", "Paused")}
            
            elif action == "spotify_next":
                print(f"  ⏭️  Next track on Spotify...")
                result = self.spotify.next_track()
                return {"success": True, "message": result if isinstance(result, str) else result.get("message", "Next track")}
            
            elif action == "spotify_previous":
                print(f"  ⏮️  Previous track on Spotify...")
                result = self.spotify.previous_track()
                return {"success": True, "message": result if isinstance(result, str) else result.get("message", "Previous track")}
            
            elif action == "spotify_play_track" or action == "play_song" or action == "play_spotify_song":
                query = parameters.get("query", "") or parameters.get("song", "") or parameters.get("song_name", "") or parameters.get("track", "")
                if not query:
                    return {"success": False, "message": "No song name provided. Please specify what song to play."}
                
                print(f"  🎵 Searching and playing '{query}' on Spotify...")
                
                if self.spotify_mode == "api":
                    result = self.spotify.play_track(query)
                    if isinstance(result, dict):
                        return result
                    return {"success": True, "message": result}
                else:
                    # Desktop mode doesn't support search, suggest opening Spotify
                    return {
                        "success": False, 
                        "message": f"Desktop mode can't search for songs. Please open Spotify and search for '{query}' manually, or connect Spotify API for full control."
                    }
            
            elif action == "spotify_volume":
                volume = parameters.get("volume", 50)
                print(f"  🔊 Setting Spotify volume to {volume}%...")
                
                if self.spotify_mode == "api":
                    result = self.spotify.set_volume(volume)
                    if isinstance(result, dict):
                        return result
                    return {"success": True, "message": result}
                else:
                    return {"success": False, "message": "Volume control requires API mode. Desktop mode can only use volume up/down."}
            
            elif action == "spotify_current_track":
                print(f"  🎵 Getting current track...")
                result = self.spotify.get_current_track()
                if isinstance(result, dict):
                    return result
                return {"success": True, "message": result}
            
            elif action == "spotify_search":
                query = parameters.get("query", "")
                search_type = parameters.get("type", "track")
                
                if not query:
                    return {"success": False, "message": "No search query provided"}
                
                print(f"  🔍 Searching Spotify for '{query}'...")
                
                if self.spotify_mode == "api":
                    result = self.spotify.search(query, search_type)
                    if isinstance(result, dict):
                        return result
                    return {"success": True, "message": result}
                else:
                    return {"success": False, "message": "Search requires API mode. Upgrade to use this feature."}
            
            elif action == "spotify_playlists":
                print(f"  📚 Getting your Spotify playlists...")
                
                if self.spotify_mode == "api":
                    result = self.spotify.get_playlists()
                    if isinstance(result, dict):
                        return result
                    return {"success": True, "message": result}
                else:
                    return {"success": False, "message": "Playlists require API mode. Upgrade to use this feature."}
            
            elif action == "spotify_shuffle":
                state = parameters.get("state", True)
                print(f"  🔀 Setting Spotify shuffle to {state}...")
                
                if self.spotify_mode == "api":
                    result = self.spotify.shuffle(state)
                    if isinstance(result, dict):
                        return result
                    return {"success": True, "message": result}
                else:
                    result = self.spotify.shuffle()
                    if isinstance(result, dict):
                        return result
                    return {"success": True, "message": result}
            
            elif action == "spotify_repeat":
                state = parameters.get("state", "context")
                print(f"  🔁 Setting Spotify repeat to {state}...")
                
                if self.spotify_mode == "api":
                    result = self.spotify.repeat(state)
                    if isinstance(result, dict):
                        return result
                    return {"success": True, "message": result}
                else:
                    result = self.spotify.repeat()
                    if isinstance(result, dict):
                        return result
                    return {"success": True, "message": result}
            
            elif action == "spotify_open" or action == "open_spotify":
                print(f"  🎵 Opening Spotify web player...")
                result = self.spotify.open_spotify()
                return {"success": True, "message": result}
            
            # ==================== PHONE CALLS ====================
            elif action == "dial_call" or action == "make_call" or action == "call_contact":
                name_or_number = (parameters.get("contact", "") or 
                                 parameters.get("contact_name", "") or 
                                 parameters.get("name", "") or 
                                 parameters.get("phone", "") or 
                                 parameters.get("phone_number", "") or 
                                 parameters.get("number", ""))
                message = parameters.get("message", None)
                
                if not name_or_number:
                    return {
                        "success": False,
                        "message": "No contact name or phone number provided. Please specify who to call."
                    }
                
                print(f"  📞 Calling {name_or_number}...")
                result = self.phone_dialer.quick_dial(name_or_number, message)
                return result
            
            elif action == "dial_phone_link" or action == "phone_link_dial":
                phone_number = parameters.get("phone", "") or parameters.get("number", "")
                if not phone_number:
                    return {
                        "success": False,
                        "message": "No phone number provided. Please specify a phone number to dial."
                    }
                
                print(f"  📱 Dialing {phone_number} with Phone Link...")
                result = self.phone_dialer.dial_with_phone_link(phone_number)
                return result
            
            elif action == "open_phone_link":
                print(f"  📱 Opening Phone Link app...")
                result = self.phone_dialer.open_phone_link()
                return result
            
            # ==================== PHONE LINK NOTIFICATIONS ====================
            elif action == "check_phone_notifications" or action == "read_phone_notifications":
                print(f"  📱 Checking Phone Link notifications...")
                new_notifs = self.phone_link_monitor.check_new_notifications()
                
                if new_notifs:
                    messages = [f"📱 {len(new_notifs)} new notification(s):\n"]
                    for i, notif in enumerate(new_notifs, 1):
                        messages.append(f"\n{i}. {notif['type'].upper()}")
                        if notif.get('sender'):
                            messages.append(f"   From: {notif['sender']}")
                        if notif.get('title'):
                            messages.append(f"   {notif['title']}")
                        if notif.get('message'):
                            messages.append(f"   {notif['message']}")
                    
                    return {
                        "success": True,
                        "message": "\n".join(messages),
                        "notifications": new_notifs
                    }
                else:
                    return {
                        "success": True,
                        "message": "ℹ️ No new Phone Link notifications"
                    }
            
            elif action == "recent_phone_notifications":
                limit = parameters.get("limit", 5)
                notif_type = parameters.get("type", None)
                
                print(f"  📋 Getting recent notifications...")
                recent = self.phone_link_monitor.get_recent_notifications(limit, notif_type)
                
                if recent:
                    messages = [f"📋 Recent notifications ({len(recent)}):\n"]
                    for i, notif in enumerate(recent, 1):
                        messages.append(f"\n{i}. {notif['type'].upper()}")
                        if notif.get('title'):
                            messages.append(f"   {notif['title']}")
                        if notif.get('message'):
                            messages.append(f"   {notif['message'][:100]}")
                    
                    return {
                        "success": True,
                        "message": "\n".join(messages),
                        "notifications": recent
                    }
                else:
                    return {
                        "success": True,
                        "message": "ℹ️ No stored notifications"
                    }
            
            elif action == "start_notification_monitoring":
                interval = parameters.get("interval", 5)
                print(f"  📱 Starting notification monitoring...")
                result = self.phone_link_monitor.start_monitoring(interval)
                return result
            
            elif action == "stop_notification_monitoring":
                print(f"  ⏹️ Stopping notification monitoring...")
                result = self.phone_link_monitor.stop_monitoring()
                return result
            
            elif action == "notification_count":
                print(f"  📊 Getting notification counts...")
                counts = self.phone_link_monitor.get_unread_count()
                
                messages = [f"📊 Total notifications: {counts['total']}\n"]
                if counts.get('by_type'):
                    messages.append("By type:")
                    for notif_type, count in counts['by_type'].items():
                        messages.append(f"  • {notif_type}: {count}")
                
                return {
                    "success": True,
                    "message": "\n".join(messages),
                    "data": counts
                }
            
            # ==================== WHATSAPP MESSAGING ====================
            elif action == "send_whatsapp":
                phone = parameters.get("phone", "") or parameters.get("phone_number", "") or parameters.get("number", "")
                contact_name = parameters.get("contact", "") or parameters.get("contact_name", "") or parameters.get("name", "")
                message = parameters.get("message", "")
                
                # If no phone provided, try to look up by contact name
                if not phone and contact_name:
                    print(f"  🔍 Looking up contact '{contact_name}'...")
                    contact = self.whatsapp_contacts.find_contact(contact_name)
                    if contact:
                        phone = contact.get('phone', '')
                        print(f"  ✅ Found contact: {contact['name']} ({phone})")
                    else:
                        return {
                            "success": False,
                            "message": f"❌ Contact '{contact_name}' not found. Please add them first or use a phone number with country code (e.g., +1234567890)"
                        }
                
                if not phone:
                    return {
                        "success": False,
                        "message": "❌ No phone number or contact name provided. Please specify who to message"
                    }
                
                if not message:
                    return {
                        "success": False,
                        "message": "❌ No message provided. Please specify what message to send"
                    }
                
                print(f"  📱 Sending WhatsApp message to {phone}...")
                result = self.whatsapp.send_message_instantly(phone, message)
                return result
            
            elif action == "send_whatsapp_scheduled":
                phone = parameters.get("phone", "") or parameters.get("phone_number", "") or parameters.get("number", "")
                message = parameters.get("message", "")
                hour = parameters.get("hour", 12)
                minute = parameters.get("minute", 0)
                
                if not phone or not message:
                    return {
                        "success": False,
                        "message": "❌ Phone number and message are required"
                    }
                
                print(f"  📱 Scheduling WhatsApp message to {phone} for {hour}:{minute:02d}...")
                result = self.whatsapp.send_message_scheduled(phone, message, hour, minute)
                return result
            
            elif action == "send_whatsapp_group":
                group_id = parameters.get("group_id", "") or parameters.get("group", "")
                message = parameters.get("message", "")
                
                if not group_id or not message:
                    return {
                        "success": False,
                        "message": "❌ Group ID and message are required"
                    }
                
                print(f"  📱 Sending WhatsApp message to group...")
                result = self.whatsapp.send_to_group_instantly(group_id, message)
                return result
            
            elif action == "send_whatsapp_image":
                phone = parameters.get("phone", "") or parameters.get("phone_number", "") or parameters.get("number", "")
                image_path = parameters.get("image_path", "") or parameters.get("image", "") or parameters.get("path", "")
                caption = parameters.get("caption", "")
                
                if not phone or not image_path:
                    return {
                        "success": False,
                        "message": "❌ Phone number and image path are required"
                    }
                
                print(f"  📱 Sending WhatsApp image to {phone}...")
                result = self.whatsapp.send_image(phone, image_path, caption)
                return result
            
            elif action == "open_whatsapp":
                print(f"  📱 Opening WhatsApp Desktop...")
                result = self.whatsapp.open_whatsapp_desktop()
                return result
            
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
            
            elif action == "create_file":
                file_path = parameters.get("file_path", "")
                content = parameters.get("content", "")
                
                if not file_path:
                    return {
                        "success": False,
                        "message": "File path is required"
                    }
                
                # Expand common path shortcuts
                file_path = self._expand_path_shortcuts(file_path)
                
                print(f"  📝 Creating file: {file_path}")
                result = self.file_manager.create_file(file_path, content)
                
                print(f"  {result}")
                
                return {
                    "success": "✅" in result,
                    "message": result
                }
            
            elif action == "write_file":
                file_path = parameters.get("file_path", "")
                content = parameters.get("content", "")
                mode = parameters.get("mode", "w")
                
                if not file_path or not content:
                    return {
                        "success": False,
                        "message": "File path and content are required"
                    }
                
                # Expand common path shortcuts
                file_path = self._expand_path_shortcuts(file_path)
                
                print(f"  📝 Writing to file: {file_path}")
                result = self.file_manager.write_to_file(file_path, content, mode)
                
                print(f"  {result}")
                
                return {
                    "success": "✅" in result,
                    "message": result
                }
            
            elif action == "read_file":
                file_path = parameters.get("file_path", "")
                
                if not file_path:
                    return {
                        "success": False,
                        "message": "File path is required"
                    }
                
                # Expand common path shortcuts
                file_path = self._expand_path_shortcuts(file_path)
                
                print(f"  📖 Reading file: {file_path}")
                content = self.file_manager.read_file(file_path)
                
                if "❌" in content:
                    return {
                        "success": False,
                        "message": content
                    }
                else:
                    print(f"  ✅ File read successfully ({len(content)} characters)")
                    return {
                        "success": True,
                        "message": f"File read: {len(content)} characters",
                        "content": content
                    }
            
            elif action == "delete_file":
                file_path = parameters.get("file_path", "")
                
                if not file_path:
                    return {
                        "success": False,
                        "message": "File path is required"
                    }
                
                # Expand common path shortcuts
                file_path = self._expand_path_shortcuts(file_path)
                
                print(f"  🗑️ Deleting file: {file_path}")
                result = self.file_manager.delete_file(file_path)
                
                print(f"  {result}")
                
                return {
                    "success": "✅" in result,
                    "message": result
                }
            
            # ==================== QUICK NOTES ====================
            elif action == "quick_note":
                content = parameters.get("content", "")
                category = parameters.get("category", "general")
                tags = parameters.get("tags", [])
                
                if not content:
                    return {
                        "success": False,
                        "message": "Note content is required"
                    }
                
                print(f"  📝 Creating quick note...")
                result = self.notes.add_note(content, category, tags)
                print(result)
                
                return {
                    "success": True,
                    "message": "Quick note created successfully",
                    "details": result
                }
            
            elif action == "list_notes":
                category = parameters.get("category", None)
                limit = parameters.get("limit", 20)
                
                print(f"  📋 Listing notes...")
                result = self.notes.list_notes(category, limit)
                print(result)
                
                return {
                    "success": True,
                    "message": "Notes listed",
                    "details": result
                }
            
            elif action == "search_notes":
                query = parameters.get("query", "")
                
                if not query:
                    return {
                        "success": False,
                        "message": "Search query is required"
                    }
                
                print(f"  🔍 Searching notes for: {query}")
                result = self.notes.search_notes(query)
                print(result)
                
                return {
                    "success": True,
                    "message": f"Search results for '{query}'",
                    "details": result
                }
            
            elif action == "get_note":
                note_id = parameters.get("note_id", 0)
                
                if not note_id:
                    return {
                        "success": False,
                        "message": "Note ID is required"
                    }
                
                print(f"  📄 Getting note #{note_id}...")
                result = self.notes.get_note(note_id)
                print(result)
                
                return {
                    "success": "⚠️" not in result,
                    "message": result
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
                editor = parameters.get("editor", "notepad").lower()
                fullscreen = parameters.get("fullscreen", True)

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
                
                # Use specialized notepad_writer for notepad, otherwise generic method
                if "notepad" in editor or "text" in editor:
                    print(f"  📝 Opening Notepad in fullscreen and writing code...")
                    
                    # Import notepad_writer
                    from modules.utilities.notepad_writer import write_code_to_notepad
                    
                    notepad_result = write_code_to_notepad(
                        code=code,
                        language=detected_lang,
                        fullscreen=fullscreen
                    )
                    
                    if notepad_result.get("success"):
                        return {
                            "success": True,
                            "message": f"✅ Generated and wrote {detected_lang} code to Notepad in fullscreen!",
                            "generated_code": code,
                            "language": detected_lang,
                            "chars_written": notepad_result.get("chars_written", len(code))
                        }
                    else:
                        # Fallback to generic method if notepad_writer fails
                        print(f"  ⚠️  Notepad writer failed: {notepad_result.get('message')}")
                        print(f"  🔄 Falling back to generic method...")
                
                # Generic method for other editors or if notepad_writer failed
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

            elif action == "lock_screen":
                result = self.system_control.lock_screen()
                return {"success": True, "message": result}

            elif action == "shutdown":
                delay = parameters.get("delay", 10)
                result = self.system_control.shutdown_system(delay)
                return {"success": True, "message": result}

            elif action == "restart":
                delay = parameters.get("delay", 10)
                result = self.system_control.restart_system(delay)
                return {"success": True, "message": result}

            elif action == "sleep":
                result = self.system_control.sleep_mode()
                return {"success": True, "message": result}

            elif action == "hibernate":
                result = self.system_control.hibernate()
                return {"success": True, "message": result}

            elif action == "cancel_shutdown":
                result = self.system_control.cancel_shutdown_restart()
                return {"success": True, "message": result}

            elif action == "schedule_sleep":
                time_str = parameters.get("time", "23:00")
                result = self.system_control.schedule_sleep(time_str)
                return {"success": True, "message": result}

            elif action == "cancel_sleep":
                result = self.system_control.cancel_sleep()
                return {"success": True, "message": result}

            elif action == "schedule_wake":
                time_str = parameters.get("time", "07:00")
                result = self.system_control.schedule_wake(time_str)
                return {"success": True, "message": result}

            elif action == "clear_temp":
                result = self.system_control.clear_temp_files()
                return {"success": True, "message": result}

            elif action == "empty_recycle_bin":
                result = self.system_control.empty_recycle_bin()
                return {"success": True, "message": result}

            elif action == "check_disk_space":
                result = self.system_control.check_disk_space()
                return {"success": True, "message": result}

            elif action == "get_cpu_usage":
                result = self.system_control.get_cpu_usage()
                return {"success": True, "message": result}

            elif action == "get_ram_usage":
                result = self.system_control.get_ram_usage()
                return {"success": True, "message": result}

            elif action == "get_battery":
                result = self.system_control.get_battery_status()
                return {"success": True, "message": result}

            elif action == "get_uptime":
                result = self.system_control.get_system_uptime()
                return {"success": True, "message": result}

            elif action == "get_network_status":
                result = self.system_control.get_network_status()
                return {"success": True, "message": result}

            elif action == "get_disk_usage":
                result = self.system_control.get_disk_usage()
                return {"success": True, "message": result}

            elif action == "get_full_system_info":
                result = self.system_control.get_system_info()
                return {"success": True, "message": result}

            elif action == "minimize_all":
                result = self.system_control.minimize_all_windows()
                return {"success": True, "message": result}

            elif action == "show_desktop":
                result = self.system_control.show_desktop()
                return {"success": True, "message": result}

            elif action == "close_all_windows":
                result = self.system_control.close_all_windows()
                return {"success": True, "message": result}

            elif action == "close_all_tabs":
                result = self.system_control.close_all_tabs()
                return {"success": True, "message": result}

            elif action == "list_windows":
                result = self.system_control.list_open_windows()
                return {"success": True, "message": result}

            elif action == "list_processes":
                limit = parameters.get("limit", 10)
                result = self.system_control.list_running_processes(limit)
                return {"success": True, "message": result}

            elif action == "kill_process":
                process_name = parameters.get("process_name", "")
                result = self.system_control.kill_process(process_name)
                return {"success": True, "message": result}

            elif action == "open_calculator":
                result = self.system_control.open_calculator()
                return {"success": True, "message": result}

            elif action == "open_notepad":
                result = self.system_control.open_notepad()
                return {"success": True, "message": result}

            elif action == "open_task_manager":
                result = self.system_control.open_task_manager()
                return {"success": True, "message": result}

            elif action == "open_file_explorer":
                path = parameters.get("path", None)
                result = self.system_control.open_file_explorer(path)
                return {"success": True, "message": result}

            elif action == "open_cmd":
                result = self.system_control.open_command_prompt()
                return {"success": True, "message": result}

            elif action == "set_timer":
                seconds = parameters.get("seconds", 60)
                message = parameters.get("message", "Timer finished!")
                result = self.system_control.set_timer(seconds, message)
                return {"success": True, "message": result}

            elif action == "set_alarm":
                time_str = parameters.get("time", "")
                message = parameters.get("message", "Alarm!")
                result = self.system_control.set_alarm(time_str, message)
                return {"success": True, "message": result}

            elif action == "clipboard_copy":
                text = parameters.get("text", "")
                result = self.system_control.copy_to_clipboard(text)
                return {"success": True, "message": result}

            elif action == "clipboard_get":
                result = self.system_control.get_clipboard()
                return {"success": True, "message": result}

            elif action == "clipboard_clear":
                result = self.system_control.clear_clipboard()
                return {"success": True, "message": result}

            elif action == "open_volume_menu":
                result = self.system_control.open_volume_brightness_menu()
                return {"success": True, "message": result}

            # ==================== WINDOWS 11 SETTINGS ====================
            # Display Settings
            elif action == "get_display_info":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                result = self.win11_settings.get_display_info()
                return result
            
            elif action == "set_display_resolution":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                width = parameters.get("width", 1920)
                height = parameters.get("height", 1080)
                result = self.win11_settings.set_display_resolution(width, height)
                return result
            
            elif action == "set_display_scaling":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                scale = parameters.get("scale", 100)
                result = self.win11_settings.set_display_scaling(scale)
                return result
            
            elif action == "set_night_light":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                temperature = parameters.get("temperature", 4800)
                result = self.win11_settings.set_night_light(enabled, temperature)
                return result
            
            elif action == "set_refresh_rate":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                rate = parameters.get("rate", 60)
                result = self.win11_settings.set_refresh_rate(rate)
                return result
            
            # Sound Settings
            elif action == "list_audio_devices":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                device_type = parameters.get("type", "playback")
                result = self.win11_settings.list_audio_devices(device_type)
                return result
            
            elif action == "set_default_audio_device":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                device_name = parameters.get("device_name", "")
                device_type = parameters.get("type", "playback")
                result = self.win11_settings.set_default_audio_device(device_name, device_type)
                return result
            
            elif action == "set_spatial_sound":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                format_type = parameters.get("format", "WindowsSonic")
                result = self.win11_settings.set_spatial_sound(enabled, format_type)
                return result
            
            # Network Settings
            elif action == "get_network_adapters":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                result = self.win11_settings.get_network_adapters()
                return result
            
            elif action == "set_wifi":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                result = self.win11_settings.set_wifi_state(enabled)
                return result
            
            elif action == "set_airplane_mode":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                result = self.win11_settings.set_airplane_mode(enabled)
                return result
            
            elif action == "set_mobile_hotspot":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                ssid = parameters.get("ssid", None)
                password = parameters.get("password", None)
                result = self.win11_settings.set_mobile_hotspot(enabled, ssid, password)
                return result
            
            elif action == "set_proxy":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                server = parameters.get("server", None)
                port = parameters.get("port", None)
                result = self.win11_settings.set_proxy(enabled, server, port)
                return result
            
            elif action == "flush_dns":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                result = self.win11_settings.flush_dns_cache()
                return result
            
            elif action == "reset_network":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                adapter = parameters.get("adapter", None)
                result = self.win11_settings.reset_network_adapter(adapter)
                return result
            
            # Bluetooth Settings
            elif action == "set_bluetooth":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                result = self.win11_settings.set_bluetooth_state(enabled)
                return result
            
            elif action == "list_bluetooth_devices":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                result = self.win11_settings.list_bluetooth_devices()
                return result
            
            elif action == "set_bluetooth_discoverable":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                result = self.win11_settings.set_bluetooth_discoverable(enabled)
                return result
            
            # Privacy & Security
            elif action == "set_camera_access":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                app = parameters.get("app", None)
                result = self.win11_settings.set_camera_access(enabled, app)
                return result
            
            elif action == "set_microphone_access":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                app = parameters.get("app", None)
                result = self.win11_settings.set_microphone_access(enabled, app)
                return result
            
            elif action == "set_location_access":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                result = self.win11_settings.set_location_access(enabled)
                return result
            
            elif action == "set_telemetry":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                level = parameters.get("level", "basic")
                result = self.win11_settings.set_telemetry_level(level)
                return result
            
            elif action == "set_windows_defender":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                result = self.win11_settings.set_windows_defender(enabled)
                return result
            
            elif action == "set_firewall":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                profile = parameters.get("profile", "all")
                result = self.win11_settings.set_firewall_state(enabled, profile)
                return result
            
            # Personalization
            elif action == "set_dark_mode":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                result = self.win11_settings.set_dark_mode(enabled)
                return result
            
            elif action == "set_wallpaper":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                image_path = parameters.get("image_path", "")
                result = self.win11_settings.set_wallpaper(image_path)
                return result
            
            elif action == "set_accent_color":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                color = parameters.get("color", "#0078D4")
                result = self.win11_settings.set_accent_color(color)
                return result
            
            elif action == "set_transparency":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                result = self.win11_settings.set_transparency_effects(enabled)
                return result
            
            elif action == "set_taskbar_position":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                position = parameters.get("position", "bottom")
                result = self.win11_settings.set_taskbar_position(position)
                return result
            
            elif action == "set_taskbar_autohide":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                result = self.win11_settings.set_taskbar_auto_hide(enabled)
                return result
            
            elif action == "set_start_layout":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                layout = parameters.get("layout", "default")
                result = self.win11_settings.set_start_menu_layout(layout)
                return result
            
            # System Settings
            elif action == "set_notifications":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                app = parameters.get("app", None)
                result = self.win11_settings.set_notifications(enabled, app)
                return result
            
            elif action == "set_focus_assist":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                mode = parameters.get("mode", "off")
                result = self.win11_settings.set_focus_assist(mode)
                return result
            
            elif action == "set_clipboard_history":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                result = self.win11_settings.set_clipboard_history(enabled)
                return result
            
            elif action == "set_storage_sense":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                result = self.win11_settings.set_storage_sense(enabled)
                return result
            
            elif action == "set_remote_desktop":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                result = self.win11_settings.set_remote_desktop(enabled)
                return result
            
            elif action == "get_storage_usage":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                result = self.win11_settings.get_storage_usage()
                return result
            
            # Accessibility
            elif action == "set_narrator":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                result = self.win11_settings.set_narrator(enabled)
                return result
            
            elif action == "set_magnifier":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                zoom = parameters.get("zoom", 200)
                result = self.win11_settings.set_magnifier(enabled, zoom)
                return result
            
            elif action == "set_high_contrast":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                result = self.win11_settings.set_high_contrast(enabled)
                return result
            
            elif action == "set_sticky_keys":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                result = self.win11_settings.set_sticky_keys(enabled)
                return result
            
            elif action == "set_filter_keys":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                result = self.win11_settings.set_filter_keys(enabled)
                return result
            
            elif action == "set_mouse_pointer_size":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                size = parameters.get("size", 1)
                result = self.win11_settings.set_mouse_pointer_size(size)
                return result
            
            # Windows Update
            elif action == "check_updates":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                result = self.win11_settings.check_windows_updates()
                return result
            
            elif action == "install_updates":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                result = self.win11_settings.install_windows_updates()
                return result
            
            elif action == "pause_updates":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                days = parameters.get("days", 7)
                result = self.win11_settings.pause_windows_updates(days)
                return result
            
            elif action == "resume_updates":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                result = self.win11_settings.resume_windows_updates()
                return result
            
            # App & Startup
            elif action == "list_startup_apps":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                result = self.win11_settings.list_startup_apps()
                return result
            
            elif action == "disable_startup_app":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                app_name = parameters.get("app_name", "")
                result = self.win11_settings.disable_startup_app(app_name)
                return result
            
            elif action == "set_default_browser":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                browser = parameters.get("browser", "edge")
                result = self.win11_settings.set_default_browser(browser)
                return result
            
            # Time & Language
            elif action == "set_timezone":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                timezone = parameters.get("timezone", "")
                result = self.win11_settings.set_time_zone(timezone)
                return result
            
            elif action == "list_timezones":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                result = self.win11_settings.list_timezones()
                return result
            
            # Gaming
            elif action == "set_game_mode":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                result = self.win11_settings.set_game_mode(enabled)
                return result
            
            elif action == "set_game_bar":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                enabled = parameters.get("enabled", True)
                result = self.win11_settings.set_game_bar(enabled)
                return result
            
            # Power Settings
            elif action == "set_power_plan":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                plan = parameters.get("plan", "balanced")
                result = self.win11_settings.set_power_plan(plan)
                return result
            
            elif action == "set_sleep_timeout":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                minutes = parameters.get("minutes", 30)
                on_battery = parameters.get("on_battery", False)
                result = self.win11_settings.set_sleep_timeout(minutes, on_battery)
                return result
            
            elif action == "set_screen_timeout":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                minutes = parameters.get("minutes", 10)
                on_battery = parameters.get("on_battery", False)
                result = self.win11_settings.set_screen_timeout(minutes, on_battery)
                return result
            
            # Advanced System
            elif action == "set_virtual_memory":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                drive = parameters.get("drive", "C")
                initial_mb = parameters.get("initial_mb", 1024)
                maximum_mb = parameters.get("maximum_mb", 4096)
                result = self.win11_settings.set_virtual_memory(drive, initial_mb, maximum_mb)
                return result
            
            elif action == "set_performance_options":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                option = parameters.get("option", "best_performance")
                result = self.win11_settings.set_performance_options(option)
                return result
            
            elif action == "optimize_system":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                result = self.win11_settings.optimize_system_performance()
                return result
            
            elif action == "get_all_settings":
                if not self.win11_settings:
                    return {"success": False, "message": "Windows 11 Settings Controller not available"}
                result = self.win11_settings.get_all_settings_summary()
                return result

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
            
            # ==================== ACCESS CONTROL & SECURITY ====================
            elif action == "enable_smart_access":
                method = parameters.get("method", "facial_recognition")
                return self.security_enhancements.enable_smart_access_control(method)
            
            elif action == "get_access_control_status":
                status = self.security_enhancements.get_access_control_status()
                return {"success": True, "message": status}
            
            elif action == "add_trusted_device":
                device_name = parameters.get("device_name", "Unknown Device")
                device_id = parameters.get("device_id", f"device_{datetime.now().strftime('%Y%m%d%H%M%S')}")
                return self.security_enhancements.add_trusted_device(device_name, device_id)
            
            elif action == "list_trusted_devices":
                devices = self.security_enhancements.list_trusted_devices()
                return {"success": True, "message": devices}
            
            elif action == "detect_security_threats":
                return self.security_enhancements.detect_threats()
            
            elif action == "enable_auto_vpn":
                network_name = parameters.get("network_name", None)
                return self.security_enhancements.enable_auto_vpn(network_name)
            
            elif action == "schedule_data_wipe":
                interval = parameters.get("interval", "weekly")
                target = parameters.get("target", "temp_files")
                return self.security_enhancements.schedule_data_wipe(interval, target)
            
            elif action == "get_threat_log":
                log = self.security_enhancements.get_threat_log()
                return {"success": True, "message": log}
            
            # ==================== FEATURE SPEAKER ====================
            elif action == "speak_main_features":
                if not self.feature_speaker:
                    return {"success": False, "message": "Feature Speaker not available"}
                return self.feature_speaker.speak_main_features()
            
            elif action == "speak_brief_features":
                if not self.feature_speaker:
                    return {"success": False, "message": "Feature Speaker not available"}
                return self.feature_speaker.speak_brief_features()
            
            elif action == "speak_quick_start":
                if not self.feature_speaker:
                    return {"success": False, "message": "Feature Speaker not available"}
                return self.feature_speaker.speak_quick_start()
            
            elif action == "speak_text":
                if not self.feature_speaker:
                    return {"success": False, "message": "Feature Speaker not available"}
                text = parameters.get("text", "")
                if not text:
                    return {"success": False, "message": "No text provided to speak"}
                return self.feature_speaker.speak_custom(text)
            
            # ==================== FUTURE-TECH CORE ====================
            elif action == "future_tech_process" or action == "ultra_intelligent_command":
                if not self.future_tech:
                    return {"success": False, "message": "Future-Tech Core not available. Install required modules."}
                
                command = parameters.get("command", "")
                screenshot = parameters.get("screenshot_path")
                
                result = self.future_tech.process_ultra_intelligent_command(command, screenshot)
                
                msg = f"🌟 FUTURE-TECH PROCESSING\n\n✅ Command: {command}\n\n"
                
                if result.get("emotion_state"):
                    state = result["emotion_state"]
                    msg += f"🎭 State: {state.get('emotion')} (Stress: {state.get('stress_level', 0):.0%})\n\n"
                
                if result.get("predictions"):
                    msg += "🔮 Predictions:\n" + "\n".join([f"  • {p.get('action', p)}" for p in result["predictions"][:3]]) + "\n\n"
                
                if result.get("suggestions"):
                    msg += "💡 Suggestions:\n" + "\n".join([f"  • {s}" for s in result["suggestions"][:3]])
                
                return {"success": True, "message": msg, "full_result": result}
            
            elif action == "future_tech_status":
                if not self.future_tech:
                    return {"success": False, "message": "Future-Tech Core not available"}
                
                status = self.future_tech.get_status_report()
                msg = f"🌟 FUTURE-TECH STATUS\n\nMemory: {status['memory_size']:,} | Productivity: {status['productivity_score']:.1%}\n"
                msg += f"State: {status['emotion_state'].get('emotion')} | Monitoring: {'✅' if status['monitoring'] else '⏸️'}"
                
                return {"success": True, "message": msg}

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


# ============================================================
# FACTORY FUNCTION - Creates properly initialized CommandExecutor
# ============================================================

def create_command_executor(enable_future_tech=True, auto_start_monitoring=False):
    """
    Factory function to create a fully initialized CommandExecutor instance
    
    Args:
        enable_future_tech (bool): Enable Future-Tech Core if available
        auto_start_monitoring (bool): Start background monitoring automatically
    
    Returns:
        CommandExecutor: Fully initialized and ready-to-use executor
    
    Example:
        executor = create_command_executor()
        result = executor.execute_single_action("send_email", {
            "to": "user@example.com",
            "subject": "Hello",
            "body": "Test message"
        })
    """
    print("\n" + "="*70)
    print("🤖 INITIALIZING COMMAND EXECUTOR")
    print("="*70)
    
    try:
        # Create executor instance
        executor = CommandExecutor()
        print("✅ CommandExecutor initialized")
        
        # Initialize Future-Tech Core if available and enabled
        if enable_future_tech and FUTURE_TECH_AVAILABLE:
            print("🌟 Initializing Future-Tech Core...")
            try:
                executor.future_tech = create_future_tech_core()
                print("✅ Future-Tech Core ready")
                
                # Start monitoring if requested
                if auto_start_monitoring:
                    executor.future_tech.start_continuous_monitoring()
                    print("✅ Background monitoring started")
            except Exception as e:
                print(f"⚠️ Future-Tech Core initialization failed: {e}")
                executor.future_tech = None
        else:
            executor.future_tech = None
        
        # Verify all core systems
        systems_status = {
            "GUI Automation": "✅" if executor.gui else "❌",
            "Email": "✅" if executor.email_sender else "❌",
            "Phone Dialer": "✅" if executor.phone_dialer else "❌",
            "WhatsApp": "✅" if executor.whatsapp else "❌",
            "System Control": "✅" if executor.system_controller else "❌",
            "Persona Service": "✅" if executor.persona_service else "❌",
            "Desktop RAG": "✅" if executor.desktop_rag else "❌",
            "Future-Tech": "✅" if executor.future_tech else "⏸️",
        }
        
        print("\n📊 SYSTEM STATUS:")
        for system, status in systems_status.items():
            print(f"  {status} {system}")
        
        print("\n" + "="*70)
        print("🚀 CommandExecutor Ready!")
        print("="*70 + "\n")
        
        return executor
        
    except Exception as e:
        print(f"\n❌ FATAL ERROR initializing CommandExecutor: {e}")
        print("="*70 + "\n")
        import traceback
        traceback.print_exc()
        raise


def create_command_executor_minimal():
    """
    Create a minimal CommandExecutor with only core features
    Useful for testing or low-resource environments
    
    Returns:
        CommandExecutor: Basic executor without heavy features
    """
    print("Creating minimal CommandExecutor...")
    executor = CommandExecutor()
    executor.future_tech = None  # Don't load Future-Tech
    print("✅ Minimal CommandExecutor created")
    return executor


def get_command_executor():
    """
    Get or create the global CommandExecutor instance
    Uses lazy loading for performance
    
    Returns:
        CommandExecutor: Global executor instance
    """
    global _GLOBAL_EXECUTOR
    if '_GLOBAL_EXECUTOR' not in globals() or _GLOBAL_EXECUTOR is None:
        _GLOBAL_EXECUTOR = create_command_executor()
    return _GLOBAL_EXECUTOR


# Module-level executor instance (lazy loaded)
_GLOBAL_EXECUTOR = None


if __name__ == "__main__":
    # Example usage when running directly
    executor = create_command_executor()
    
    # Test a simple action
    print("\n📝 Testing basic action...")
    result = executor.execute_single_action("get_quick_weather", {})
    print(f"Weather: {result.get('message')}")
    
    print("\n✅ CommandExecutor working correctly!")
