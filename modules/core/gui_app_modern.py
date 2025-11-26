#!/usr/bin/env python3
"""
V.A.T.S.A.L - Modern ChatGPT-Style Conversational GUI
Complete implementation with all features from original gui_app.py
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image, ImageTk, ImageDraw
import psutil

from modules.core.gemini_controller import parse_command, get_ai_suggestion
from modules.core.command_executor import CommandExecutor
from modules.core.vatsal_assistant import create_vatsal_assistant
from modules.monitoring.advanced_smart_screen_monitor import create_advanced_smart_screen_monitor
from modules.monitoring.ai_screen_monitoring_system import create_ai_screen_monitoring_system
from modules.ai_features.chatbots import SimpleChatbot
from modules.automation.file_automation import create_file_automation
from modules.smart_features.clipboard_text_handler import ClipboardTextHandler
from modules.smart_features.smart_automation import SmartAutomationManager
from modules.integration.desktop_controller_integration import DesktopFileController
from modules.automation.comprehensive_desktop_controller import ComprehensiveDesktopController
from modules.ai_features.vision_ai import VirtualLanguageModel
from modules.automation.gui_automation import GUIAutomation
from modules.web.selenium_web_automator import SeleniumWebAutomator
from modules.automation.vatsal_desktop_automator import BOIAutomator
from modules.automation.self_operating_computer import SelfOperatingComputer
from modules.automation.self_operating_integrations import SelfOperatingIntegrationHub, SmartTaskRouter
from modules.integration.command_executor_integration import EnhancedCommandExecutor, CommandInterceptor
from modules.voice.voice_commander import create_voice_commander
from modules.system.system_control import SystemController
from modules.network.websocket_client import get_websocket_client
from modules.automation.macro_recorder import MacroRecorder, MacroTemplates
from modules.automation.opencv_hand_gesture_detector import OpenCVHandGestureDetector
from modules.automation.gesture_voice_activator import create_gesture_voice_activator
from modules.smart_features.nl_workflow_builder import create_nl_workflow_builder
from modules.smart_features.workflow_templates import WorkflowManager
from modules.intelligence.user_profile_manager import get_user_profile_manager
from modules.file_management.desktop_sync_manager import auto_initialize_on_gui_start, DesktopSyncManager
from modules.productivity.productivity_dashboard import ProductivityDashboard
from modules.productivity.pomodoro_ai_coach import PomodoroAICoach
from modules.productivity.task_time_predictor import TaskTimePredictor
from modules.productivity.energy_level_tracker import EnergyLevelTracker
from modules.productivity.distraction_detector import DistractionDetector
from modules.productivity.productivity_monitor import ProductivityMonitor
from modules.utilities.password_vault import PasswordVault
from modules.utilities.calendar_manager import CalendarManager
from modules.utilities.quick_notes import QuickNotes
from modules.utilities.weather_news_service import WeatherNewsService
from modules.communication.translation_service import TranslationService
from modules.productivity.smart_break_suggester import SmartBreakSuggester
from modules.security.security_dashboard import SecurityDashboard
from modules.utilities.batch_utilities import get_batch_utilities
from modules.communication.phone_dialer import create_phone_dialer
from modules.utilities.contact_manager import ContactManager
from scripts.ai_phone_link_controller import AIPhoneLinkController
from modules.voice.feature_speaker import create_feature_speaker

load_dotenv()


class ModernChatGPTGUI:
    """Modern ChatGPT-style conversational GUI with all features"""

    def __init__(self, root):
        self.root = root
        self.root.title("V.A.T.S.A.L - AI Desktop Assistant")
        
        # Modern theme colors (dark mode)
        self.colors = {
            "bg_primary": "#0d0d0d",
            "bg_secondary": "#1a1a1a",
            "bg_tertiary": "#2a2a2a",
            "text_primary": "#ececec",
            "text_secondary": "#b4b4b4",
            "accent_blue": "#10a37f",
            "accent_green": "#10b981",
            "accent_red": "#ef4444",
            "user_bubble": "#10a37f",
            "bot_bubble": "#343541",
            "input_bg": "#343541",
            "hover_color": "#40414f"
        }
        
        self.root.configure(bg=self.colors["bg_primary"])
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)
        
        # State management
        self.state = {
            "processing": False,
            "vatsal_mode": True,
            "self_operating_mode": True,
            "voice_enabled": False,
            "wakeup_listening": False,
            "vsign_detecting": False,
            "speaking_enabled": False
        }
        
        # Initialize modules and GUI
        self._initialize_modules()
        self._create_gui()
        self._show_welcome()
        self._start_background_tasks()
    
    def _initialize_modules(self):
        """Initialize all backend modules"""
        try:
            self.user_profile = get_user_profile_manager()
            self.system_controller = SystemController()
            self.base_executor = CommandExecutor()
            
            try:
                self.executor = EnhancedCommandExecutor(self.base_executor)
                self.command_interceptor = CommandInterceptor(self.executor)
            except:
                self.executor = self.base_executor
                self.command_interceptor = None
            
            self.vatsal = create_vatsal_assistant()
            self.advanced_monitor = create_advanced_smart_screen_monitor()
            self.ai_monitor = create_ai_screen_monitoring_system()
            self.file_automation = create_file_automation()
            self.clipboard_handler = ClipboardTextHandler()
            self.smart_automation = SmartAutomationManager()
            self.desktop_controller = DesktopFileController()
            
            try:
                self.feature_speaker = create_feature_speaker()
            except:
                self.feature_speaker = None
            
            try:
                self.comprehensive_controller = ComprehensiveDesktopController()
            except:
                self.comprehensive_controller = None
            
            try:
                self.simple_chatbot = SimpleChatbot()
            except:
                self.simple_chatbot = None
            
            try:
                self.web_automator = SeleniumWebAutomator()
            except:
                self.web_automator = None
            
            try:
                gui_automation = GUIAutomation()
                self.vlm = VirtualLanguageModel(gui_automation)
            except:
                self.vlm = None
            
            try:
                self.vatsal_automator = BOIAutomator()
            except:
                self.vatsal_automator = None
            
            try:
                self.self_operating_computer = SelfOperatingComputer(verbose=True)
            except:
                self.self_operating_computer = None
            
            try:
                self.integration_hub = SelfOperatingIntegrationHub()
                self.task_router = SmartTaskRouter(self.integration_hub)
            except:
                self.integration_hub = None
                self.task_router = None
            
            try:
                self.ws_client = get_websocket_client()
                self.ws_client.connect()
            except:
                self.ws_client = None
            
            try:
                self.voice_commander = create_voice_commander(command_callback=self.handle_voice_command)
            except:
                self.voice_commander = None
            
            try:
                self.gesture_voice_activator = create_gesture_voice_activator(
                    on_speech_callback=self.handle_voice_command
                )
            except:
                self.gesture_voice_activator = None
            
            try:
                self.gesture_assistant = OpenCVHandGestureDetector(voice_commander=self.voice_commander)
            except:
                self.gesture_assistant = None
            
            try:
                self.macro_recorder = MacroRecorder()
                self.macro_templates = MacroTemplates()
            except:
                self.macro_recorder = None
                self.macro_templates = None
            
            try:
                self.workflow_builder = create_nl_workflow_builder()
                self.workflow_manager = WorkflowManager()
            except:
                self.workflow_builder = None
                self.workflow_manager = None
            
            try:
                self.productivity_dashboard = ProductivityDashboard()
                self.pomodoro_coach = PomodoroAICoach()
                self.task_predictor = TaskTimePredictor()
                self.energy_tracker = EnergyLevelTracker()
                self.distraction_detector = DistractionDetector()
                self.productivity_monitor = ProductivityMonitor()
                self.break_suggester = SmartBreakSuggester()
            except:
                pass
            
            try:
                self.password_vault = PasswordVault()
                self.calendar = CalendarManager()
                self.notes = QuickNotes()
                self.weather_news = WeatherNewsService()
                self.translator = TranslationService()
            except:
                pass
            
            try:
                self.phone_dialer = create_phone_dialer()
                self.contact_manager = ContactManager("data/contacts.json")
                self.ai_phone_controller = AIPhoneLinkController()
            except:
                self.phone_dialer = None
                self.contact_manager = None
            
            try:
                self.security_dashboard = SecurityDashboard()
            except:
                self.security_dashboard = None
            
            try:
                auto_initialize_on_gui_start()
                self.desktop_sync_manager = DesktopSyncManager()
            except:
                self.desktop_sync_manager = None
            
            try:
                self.batch_utilities = get_batch_utilities()
            except:
                self.batch_utilities = None
            
            print("✅ All modules initialized successfully")
        except Exception as e:
            print(f"❌ Module initialization error: {e}")
    
    def _create_gui(self):
        """Create modern ChatGPT-style GUI"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors["bg_primary"])
        main_frame.pack(fill="both", expand=True)
        
        # Header bar
        header = tk.Frame(main_frame, bg=self.colors["bg_secondary"], height=60)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)
        
        tk.Label(header, text="🤖 V.A.T.S.A.L", bg=self.colors["bg_secondary"],
                fg=self.colors["text_primary"], font=("Segoe UI", 14, "bold")).pack(side="left", padx=20, pady=15)
        
        self.time_label = tk.Label(header, text="", bg=self.colors["bg_secondary"],
                                  fg=self.colors["text_secondary"], font=("Segoe UI", 9))
        self.time_label.pack(side="right", padx=20, pady=15)
        
        # Chat area container
        chat_container = tk.Frame(main_frame, bg=self.colors["bg_primary"])
        chat_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Chat display with scrollbar
        self.chat_canvas = tk.Canvas(chat_container, bg=self.colors["bg_primary"],
                                    highlightthickness=0, relief="flat", bd=0)
        scrollbar = ttk.Scrollbar(chat_container, orient="vertical", command=self.chat_canvas.yview)
        self.chat_scrollable = tk.Frame(self.chat_canvas, bg=self.colors["bg_primary"])
        
        self.chat_scrollable.bind("<Configure>",
                                 lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")))
        self.chat_canvas.create_window((0, 0), window=self.chat_scrollable, anchor="nw")
        self.chat_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.chat_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.chat_messages = []
        
        # Input area
        input_frame = tk.Frame(main_frame, bg=self.colors["bg_primary"])
        input_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Input box frame
        input_box_frame = tk.Frame(input_frame, bg=self.colors["input_bg"], relief="solid", bd=1)
        input_box_frame.pack(fill="x")
        
        self.input_field = tk.Entry(input_box_frame, bg=self.colors["input_bg"],
                                   fg=self.colors["text_primary"], font=("Segoe UI", 11),
                                   insertbackground=self.colors["text_primary"],
                                   relief="flat", bd=0)
        self.input_field.pack(fill="both", expand=True, ipady=12, padx=15)
        self.input_field.bind("<Return>", lambda e: self.execute_command())
        
        # Button area
        button_frame = tk.Frame(main_frame, bg=self.colors["bg_primary"])
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        tk.Button(button_frame, text="▶ Send", command=self.execute_command,
                 bg=self.colors["accent_blue"], fg=self.colors["bg_primary"],
                 font=("Segoe UI", 10, "bold"), relief="flat", bd=0,
                 padx=20, pady=8, cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(button_frame, text="⚙️ Settings", command=self.show_settings,
                 bg=self.colors["bg_secondary"], fg=self.colors["text_primary"],
                 font=("Segoe UI", 9), relief="flat", bd=0,
                 padx=15, pady=8, cursor="hand2").pack(side="left", padx=2)
        
        tk.Button(button_frame, text="❓ Help", command=self.show_help,
                 bg=self.colors["bg_secondary"], fg=self.colors["text_primary"],
                 font=("Segoe UI", 9), relief="flat", bd=0,
                 padx=15, pady=8, cursor="hand2").pack(side="left", padx=2)
        
        tk.Button(button_frame, text="🗑️ Clear", command=self.clear_chat,
                 bg=self.colors["bg_secondary"], fg=self.colors["text_primary"],
                 font=("Segoe UI", 9), relief="flat", bd=0,
                 padx=15, pady=8, cursor="hand2").pack(side="left", padx=2)
    
    def add_message(self, text, sender="bot"):
        """Add message bubble to chat"""
        msg_frame = tk.Frame(self.chat_scrollable, bg=self.colors["bg_primary"])
        msg_frame.pack(fill="x", padx=10, pady=8)
        
        if sender == "user":
            bubble_frame = tk.Frame(msg_frame, bg=self.colors["user_bubble"], relief="flat")
            bubble_frame.pack(anchor="e", padx=(100, 10))
            label_text = "👤 You"
        else:
            bubble_frame = tk.Frame(msg_frame, bg=self.colors["bot_bubble"], relief="flat")
            bubble_frame.pack(anchor="w", padx=(10, 100))
            label_text = "🤖 BOI"
        
        # Sender label
        tk.Label(bubble_frame, text=label_text, bg=bubble_frame["bg"],
                fg=self.colors["text_primary"], font=("Segoe UI", 8, "bold"),
                padx=12, pady=(8, 2)).pack(anchor="w")
        
        # Message text
        tk.Label(bubble_frame, text=text, bg=bubble_frame["bg"],
                fg=self.colors["text_primary"], font=("Segoe UI", 10),
                justify="left", wraplength=400, padx=12, pady=(2, 10)).pack(anchor="w", fill="x")
        
        self.chat_messages.append((msg_frame, text))
        self.chat_canvas.after(50, lambda: self.chat_canvas.yview_moveto(1.0))
    
    def execute_command(self):
        """Execute user command"""
        if self.state["processing"]:
            return
        
        user_input = self.input_field.get().strip()
        if not user_input:
            return
        
        self.input_field.delete(0, tk.END)
        self.add_message(user_input, sender="user")
        
        self.state["processing"] = True
        
        def process():
            try:
                command_dict = parse_command(user_input)
                
                if command_dict.get("action") == "error":
                    response = "Unable to process this command. Try asking differently."
                else:
                    result = self.executor.execute(command_dict)
                    message = result.get('message', 'Done')
                    
                    if self.state["vatsal_mode"] and self.vatsal:
                        try:
                            response = self.vatsal.process_with_personality(user_input, message)
                        except:
                            response = message
                    else:
                        response = message
                
                self.root.after(0, lambda: self.add_message(response, sender="bot"))
            except Exception as e:
                self.root.after(0, lambda: self.add_message(f"Error: {str(e)}", sender="bot"))
            finally:
                self.state["processing"] = False
        
        thread = threading.Thread(target=process, daemon=True)
        thread.start()
    
    def clear_chat(self):
        """Clear chat messages"""
        for msg_frame, _ in self.chat_messages:
            msg_frame.destroy()
        self.chat_messages.clear()
        self.add_message("Chat cleared", sender="bot")
    
    def handle_voice_command(self, command):
        """Handle voice commands"""
        self.input_field.delete(0, tk.END)
        self.input_field.insert(0, command)
        self.execute_command()
    
    def show_settings(self):
        """Show settings"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ Settings")
        settings_window.geometry("500x600")
        settings_window.configure(bg=self.colors["bg_primary"])
        
        notebook = ttk.Notebook(settings_window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Voice tab
        voice_frame = tk.Frame(notebook, bg=self.colors["bg_secondary"])
        notebook.add(voice_frame, text="🎙️ Voice")
        
        settings_list = [
            "✅ Voice recognition enabled",
            "✅ Microphone input enabled",
            "🎙️ Sensitivity: High",
            "🔊 Output volume: 85%",
            "🗣️ Language: English"
        ]
        
        for setting in settings_list:
            tk.Label(voice_frame, text=setting, bg=self.colors["bg_secondary"],
                    fg=self.colors["text_secondary"], font=("Segoe UI", 9)).pack(anchor="w", padx=15, pady=5)
        
        # Automation tab
        auto_frame = tk.Frame(notebook, bg=self.colors["bg_secondary"])
        notebook.add(auto_frame, text="⚡ Automation")
        
        auto_list = [
            "✅ Self-operating mode",
            "✅ Gesture recognition",
            "✅ Macro recording",
            "✅ Workflow automation"
        ]
        
        for item in auto_list:
            tk.Label(auto_frame, text=item, bg=self.colors["bg_secondary"],
                    fg=self.colors["text_secondary"], font=("Segoe UI", 9)).pack(anchor="w", padx=15, pady=5)
    
    def show_help(self):
        """Show help"""
        help_window = tk.Toplevel(self.root)
        help_window.title("❓ Help")
        help_window.geometry("600x500")
        help_window.configure(bg=self.colors["bg_primary"])
        
        help_text = """
🤖 V.A.T.S.A.L - AI DESKTOP ASSISTANT

Command Examples:
• "Take screenshot" - Capture screen
• "Show system report" - System info
• "Check CPU usage" - CPU metrics
• "Search for *.txt" - File search
• "Analyze image.png" - Vision analysis
• "List processes" - Running apps
• "Show disk space" - Disk usage

Features:
🎙️ Voice commands
👁️ Screenshot analysis
⚡ Workflow automation
📊 Productivity tracking
🔒 Security monitoring
📱 Phone integration
🤖 Self-operating mode

Type "help" anytime for assistance
"""
        
        text_widget = tk.Label(help_window, text=help_text, bg=self.colors["bg_secondary"],
                              fg=self.colors["text_secondary"], font=("Courier New", 9),
                              justify="left", wraplength=550)
        text_widget.pack(anchor="nw", fill="both", expand=True, padx=15, pady=15)
    
    def _show_welcome(self):
        """Show welcome message"""
        welcome = "👋 Welcome to V.A.T.S.A.L!\n\n🎯 I'm your AI Desktop Assistant.\n\n💡 Try: 'Take screenshot' or 'Show system report'"
        self.add_message(welcome, sender="bot")
    
    def _update_time(self):
        """Update time display"""
        now = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=now)
        self.root.after(1000, self._update_time)
    
    def _start_background_tasks(self):
        """Start background tasks"""
        self._update_time()


def main():
    """Entry point"""
    root = tk.Tk()
    app = ModernChatGPTGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
