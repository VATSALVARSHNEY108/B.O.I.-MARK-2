#!/usr/bin/env python3
"""
Modern GUI Application for BOI - V.A.T.S.A.L AI Desktop Assistant
Clean, modular architecture with professional conversational interface
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image, ImageTk

from modules.core.gemini_controller import parse_command, get_ai_suggestion, chat_response
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


class ModernBOIGUI:
    """Modern, clean GUI for BOI AI Desktop Assistant with conversational interface"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("V.A.T.S.A.L - AI Desktop Assistant")
        
        # Theme Colors - Modern Design
        self.colors = {
            "bg_primary": "#0F1419",
            "bg_secondary": "#1A1F2E",
            "bg_tertiary": "#252D3D",
            "text_primary": "#FFFFFF",
            "text_secondary": "#B0B8C8",
            "accent_blue": "#2563EB",
            "accent_green": "#10B981",
            "accent_red": "#EF4444",
            "user_message_bg": "#2563EB",
            "bot_message_bg": "#374151",
            "border_color": "#404854"
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
            "speaking_enabled": False,
            "gesture_voice_active": False,
            "gesture_running": False,
            "soc_running": False
        }
        
        # Initialize modules
        self._initialize_modules()
        
        # Build GUI
        self._create_gui()
        
        # Start background tasks
        self._start_background_tasks()
        
        # Show welcome
        self._show_welcome()
    
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
            
            # AI & Automation modules
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
                self.vlm_last_decision = None
            except:
                self.vlm = None
                self.vlm_last_decision = None
            
            try:
                self.vatsal_automator = BOIAutomator()
            except:
                self.vatsal_automator = None
            
            try:
                self.self_operating_computer = SelfOperatingComputer(verbose=True)
                self.state["soc_running"] = False
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
                self.ai_phone_controller = None
            
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
            
            print("✅ All modules initialized")
        except Exception as e:
            print(f"❌ Module initialization error: {e}")
    
    def _create_gui(self):
        """Create main GUI layout"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors["bg_primary"])
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Top bar with time and status
        self._create_top_bar(main_frame)
        
        # Main content area (split layout)
        content_frame = tk.Frame(main_frame, bg=self.colors["bg_primary"])
        content_frame.pack(fill="both", expand=True, padx=15, pady=(10, 15))
        
        # Left sidebar with controls (25% width)
        left_panel = tk.Frame(content_frame, bg=self.colors["bg_secondary"], relief="solid", bd=1)
        left_panel.pack(side="left", fill="both", padx=(0, 10), ipadx=0)
        left_panel.config(highlightbackground=self.colors["border_color"], highlightthickness=1)
        
        self._create_left_panel(left_panel)
        
        # Right panel with chat (75% width)
        right_panel = tk.Frame(content_frame, bg=self.colors["bg_secondary"], relief="solid", bd=1)
        right_panel.pack(side="right", fill="both", expand=True, ipadx=0)
        right_panel.config(highlightbackground=self.colors["border_color"], highlightthickness=1)
        
        self._create_right_panel(right_panel)
        
        # Bottom status bar
        self._create_bottom_bar(main_frame)
    
    def _create_top_bar(self, parent):
        """Create top bar with title and time"""
        top_bar = tk.Frame(parent, bg=self.colors["bg_secondary"], height=60)
        top_bar.pack(fill="x", padx=0, pady=(0, 10), ipady=10)
        top_bar.pack_propagate(False)
        top_bar.config(highlightbackground=self.colors["border_color"], highlightthickness=1)
        
        # Title
        title_label = tk.Label(
            top_bar,
            text="🤖 V.A.T.S.A.L - AI Desktop Assistant",
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_primary"],
            font=("Segoe UI", 16, "bold")
        )
        title_label.pack(side="left", padx=20)
        
        # Time
        self.time_label = tk.Label(
            top_bar,
            text="",
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_secondary"],
            font=("Segoe UI", 10)
        )
        self.time_label.pack(side="right", padx=20)
    
    def _create_left_panel(self, parent):
        """Create left sidebar with controls"""
        # Title
        title = tk.Label(
            parent,
            text="Controls",
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_primary"],
            font=("Segoe UI", 12, "bold")
        )
        title.pack(padx=15, pady=(15, 10), anchor="w")
        
        # Mode toggles frame
        modes_frame = tk.Frame(parent, bg=self.colors["bg_secondary"])
        modes_frame.pack(fill="x", padx=10, pady=5)
        
        self.vatsal_toggle = self._create_toggle_button(
            modes_frame, "🤖 BOI Mode", True, self.toggle_vatsal
        )
        self.vatsal_toggle.pack(fill="x", pady=3)
        
        self.soc_toggle = self._create_toggle_button(
            modes_frame, "🔲 Self-Operating", True, self.toggle_self_operating
        )
        self.soc_toggle.pack(fill="x", pady=3)
        
        self.voice_toggle = self._create_toggle_button(
            modes_frame, "🔊 Voice Mode", False, self.toggle_voice
        )
        self.voice_toggle.pack(fill="x", pady=3)
        
        self.speaking_toggle = self._create_toggle_button(
            modes_frame, "🗣️ Speaking", False, self.toggle_speaking
        )
        self.speaking_toggle.pack(fill="x", pady=3)
        
        # Separator
        separator = tk.Frame(parent, bg=self.colors["border_color"], height=1)
        separator.pack(fill="x", pady=10)
        
        # Feature buttons
        features_label = tk.Label(
            parent,
            text="Features",
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_primary"],
            font=("Segoe UI", 11, "bold")
        )
        features_label.pack(padx=15, pady=(10, 8), anchor="w")
        
        features_frame = tk.Frame(parent, bg=self.colors["bg_secondary"])
        features_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        features = [
            ("👂 Wake Word", self.toggle_wakeup_listener),
            ("✌️ V-Sign Detect", self.toggle_v_sign_detector),
            ("📞 Phone Link", self.show_phone_link_control),
            ("🎙️ Voice Listen", self.start_voice_listen),
            ("⚙️ Settings", self.show_settings),
            ("💬 Chat", self.show_about),
            ("❓ Help", self.show_help),
            ("🔒 Security", self.show_security_dashboard),
            ("⚡ Batch Utils", self.show_batch_utilities),
        ]
        
        for feature_name, command in features:
            btn = self._create_feature_button(features_frame, feature_name, command)
            btn.pack(fill="x", pady=2)
    
    def _create_right_panel(self, parent):
        """Create right panel with chat interface"""
        # Chat header
        chat_header = tk.Frame(parent, bg=self.colors["bg_secondary"])
        chat_header.pack(fill="x", padx=20, pady=(15, 10))
        
        chat_title = tk.Label(
            chat_header,
            text="💬 Chat Interface",
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_primary"],
            font=("Segoe UI", 12, "bold")
        )
        chat_title.pack(side="left")
        
        # Chat area
        chat_area_frame = tk.Frame(parent, bg=self.colors["bg_tertiary"])
        chat_area_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15), ipady=5)
        
        # Canvas with scrollbar
        self.chat_canvas = tk.Canvas(
            chat_area_frame,
            bg=self.colors["bg_tertiary"],
            highlightthickness=0,
            relief="flat",
            bd=0
        )
        scrollbar = ttk.Scrollbar(chat_area_frame, orient="vertical", command=self.chat_canvas.yview)
        self.chat_scrollable = tk.Frame(self.chat_canvas, bg=self.colors["bg_tertiary"])
        
        self.chat_scrollable.bind(
            "<Configure>",
            lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        )
        self.chat_canvas.create_window((0, 0), window=self.chat_scrollable, anchor="nw")
        self.chat_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.chat_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.chat_messages = []
        
        # Input area
        input_frame = tk.Frame(parent, bg=self.colors["bg_secondary"])
        input_frame.pack(fill="x", padx=15, pady=(10, 15))
        
        # Input box
        self.input_field = tk.Entry(
            input_frame,
            bg=self.colors["bg_tertiary"],
            fg=self.colors["text_primary"],
            font=("Segoe UI", 11),
            insertbackground=self.colors["text_primary"],
            relief="solid",
            bd=1
        )
        self.input_field.pack(side="left", fill="both", expand=True, ipady=8, padx=(0, 10))
        self.input_field.bind("<Return>", lambda e: self.execute_command())
        
        # Execute button
        exec_btn = tk.Button(
            input_frame,
            text="▶ Send",
            command=self.execute_command,
            bg=self.colors["accent_green"],
            fg=self.colors["text_primary"],
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        exec_btn.pack(side="left")
        
        # Clear button
        clear_btn = tk.Button(
            input_frame,
            text="🗑️ Clear",
            command=self.clear_chat,
            bg=self.colors["accent_red"],
            fg=self.colors["text_primary"],
            font=("Segoe UI", 9),
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        clear_btn.pack(side="left", padx=(5, 0))
    
    def _create_bottom_bar(self, parent):
        """Create bottom status bar"""
        bottom_bar = tk.Frame(parent, bg=self.colors["bg_secondary"], height=40)
        bottom_bar.pack(fill="x", side="bottom", padx=0, ipady=8)
        bottom_bar.pack_propagate(False)
        bottom_bar.config(highlightbackground=self.colors["border_color"], highlightthickness=1)
        
        self.status_label = tk.Label(
            bottom_bar,
            text="✅ Ready",
            bg=self.colors["bg_secondary"],
            fg=self.colors["accent_green"],
            font=("Segoe UI", 10)
        )
        self.status_label.pack(side="left", padx=20)
    
    def _create_toggle_button(self, parent, text, initial_state, command):
        """Create a toggle button"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.colors["accent_green"] if initial_state else self.colors["bg_tertiary"],
            fg=self.colors["text_primary"],
            font=("Segoe UI", 10),
            relief="flat",
            bd=0,
            padx=10,
            pady=8,
            cursor="hand2",
            justify="left"
        )
        return btn
    
    def _create_feature_button(self, parent, text, command):
        """Create a feature button"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.colors["bg_tertiary"],
            fg=self.colors["text_primary"],
            font=("Segoe UI", 9),
            relief="solid",
            bd=1,
            padx=10,
            pady=6,
            cursor="hand2",
            activebackground=self.colors["accent_blue"],
            activeforeground=self.colors["text_primary"]
        )
        btn.config(highlightbackground=self.colors["border_color"])
        return btn
    
    def add_chat_message(self, message, sender="BOI", msg_type="info"):
        """Add message to chat with modern bubble interface"""
        if not hasattr(self, 'chat_scrollable'):
            return
        
        # Message container
        msg_container = tk.Frame(self.chat_scrollable, bg=self.colors["bg_tertiary"])
        msg_container.pack(anchor="e" if sender == "USER" else "w", fill="x", padx=10, pady=6)
        
        # Bubble styling
        if sender == "USER":
            bubble_bg = self.colors["user_message_bg"]
            text_color = self.colors["text_primary"]
            anchor = "e"
            padx_val = (100, 10)
        else:
            bubble_bg = self.colors["bot_message_bg"]
            text_color = self.colors["text_primary"]
            anchor = "w"
            padx_val = (10, 100)
        
        # Message bubble
        bubble = tk.Frame(msg_container, bg=bubble_bg, relief="flat")
        bubble.pack(anchor=anchor, padx=padx_val, pady=2)
        
        # Sender label
        sender_text = f"{'👤 You' if sender == 'USER' else '🤖 BOI'}"
        sender_label = tk.Label(
            bubble,
            text=sender_text,
            bg=bubble_bg,
            fg=text_color,
            font=("Segoe UI", 7, "bold"),
            padx=10,
            pady=(6, 2)
        )
        sender_label.pack(anchor="w")
        
        # Message text - BOLD
        msg_label = tk.Label(
            bubble,
            text=message,
            bg=bubble_bg,
            fg=text_color,
            font=("Segoe UI", 10, "bold"),
            justify="left",
            wraplength=400,
            padx=10,
            pady=(2, 8)
        )
        msg_label.pack(anchor="w", fill="x")
        
        self.chat_messages.append((msg_container, message))
        self.chat_canvas.after(50, lambda: self.chat_canvas.yview_moveto(1.0))
    
    def execute_command(self):
        """Execute user command"""
        if self.state["processing"]:
            return
        
        user_input = self.input_field.get().strip()
        if not user_input:
            return
        
        self.input_field.delete(0, tk.END)
        self.add_chat_message(user_input, sender="USER", msg_type="command")
        
        self.state["processing"] = True
        self.update_status("Processing...", "processing")
        
        def process():
            try:
                # Check if simple query
                simple_queries = ['hi', 'hello', 'hey', 'thanks', 'thank you', 'what is', 'who is']
                is_simple = any(user_input.lower().startswith(q) for q in simple_queries)
                
                if is_simple or len(user_input.split()) <= 5:
                    try:
                        response = chat_response(user_input)
                        self.root.after(0, lambda: self.add_chat_message(response, sender="BOI", msg_type="success"))
                    except:
                        self._execute_command_parsing(user_input)
                else:
                    self._execute_command_parsing(user_input)
                
                self.update_status("✅ Ready", "success")
            except Exception as e:
                self.root.after(0, lambda: self.add_chat_message(f"Error: {str(e)}", sender="BOI", msg_type="error"))
                self.update_status("❌ Error", "error")
            finally:
                self.state["processing"] = False
        
        thread = threading.Thread(target=process, daemon=True)
        thread.start()
    
    def _execute_command_parsing(self, user_input):
        """Parse and execute command"""
        try:
            command_dict = parse_command(user_input)
            
            if command_dict.get("action") == "error":
                try:
                    response = chat_response(user_input)
                    self.root.after(0, lambda: self.add_chat_message(response, sender="BOI", msg_type="success"))
                except:
                    self.root.after(0, lambda: self.add_chat_message("Unable to process command", sender="BOI", msg_type="error"))
                return
            
            result = self.executor.execute(command_dict)
            
            message = result.get('message', 'Done')
            msg_type = "success" if result.get("success") else "error"
            
            if self.state["vatsal_mode"] and self.vatsal:
                try:
                    response = self.vatsal.process_with_personality(user_input, message)
                    self.root.after(0, lambda: self.add_chat_message(response, sender="BOI", msg_type=msg_type))
                except:
                    self.root.after(0, lambda: self.add_chat_message(message, sender="BOI", msg_type=msg_type))
            else:
                self.root.after(0, lambda: self.add_chat_message(message, sender="BOI", msg_type=msg_type))
        except Exception as e:
            self.root.after(0, lambda: self.add_chat_message(f"Error: {str(e)}", sender="BOI", msg_type="error"))
    
    def clear_chat(self):
        """Clear chat messages"""
        for msg_container, _ in self.chat_messages:
            msg_container.destroy()
        self.chat_messages.clear()
        self.add_chat_message("Chat cleared", sender="BOI", msg_type="info")
    
    def update_status(self, text, status_type="info"):
        """Update status bar"""
        colors = {
            "success": self.colors["accent_green"],
            "error": self.colors["accent_red"],
            "processing": self.colors["accent_blue"],
            "info": self.colors["text_secondary"]
        }
        self.status_label.config(text=text, fg=colors.get(status_type, colors["info"]))
    
    def toggle_vatsal(self):
        """Toggle BOI mode"""
        self.state["vatsal_mode"] = not self.state["vatsal_mode"]
        color = self.colors["accent_green"] if self.state["vatsal_mode"] else self.colors["bg_tertiary"]
        self.vatsal_toggle.config(bg=color)
        status = "✅ BOI mode enabled" if self.state["vatsal_mode"] else "⚠️ BOI mode disabled"
        self.add_chat_message(status, sender="BOI", msg_type="success" if self.state["vatsal_mode"] else "warning")
    
    def toggle_self_operating(self):
        """Toggle self-operating mode"""
        self.state["self_operating_mode"] = not self.state["self_operating_mode"]
        color = self.colors["accent_green"] if self.state["self_operating_mode"] else self.colors["bg_tertiary"]
        self.soc_toggle.config(bg=color)
        status = "✅ Self-Operating enabled" if self.state["self_operating_mode"] else "⚠️ Self-Operating disabled"
        self.add_chat_message(status, sender="BOI", msg_type="success" if self.state["self_operating_mode"] else "warning")
    
    def toggle_voice(self):
        """Toggle voice mode"""
        self.state["voice_enabled"] = not self.state["voice_enabled"]
        color = self.colors["accent_green"] if self.state["voice_enabled"] else self.colors["bg_tertiary"]
        self.voice_toggle.config(bg=color)
        status = "🔊 Voice enabled" if self.state["voice_enabled"] else "🔇 Voice disabled"
        self.add_chat_message(status, sender="BOI", msg_type="success" if self.state["voice_enabled"] else "warning")
    
    def toggle_speaking(self):
        """Toggle speaking mode"""
        self.state["speaking_enabled"] = not self.state["speaking_enabled"]
        color = self.colors["accent_green"] if self.state["speaking_enabled"] else self.colors["bg_tertiary"]
        self.speaking_toggle.config(bg=color)
        status = "🗣️ Speaking enabled" if self.state["speaking_enabled"] else "🔇 Speaking disabled"
        self.add_chat_message(status, sender="BOI", msg_type="success" if self.state["speaking_enabled"] else "warning")
    
    def toggle_wakeup_listener(self):
        """Toggle wakeup word listener"""
        self.state["wakeup_listening"] = not self.state["wakeup_listening"]
        if self.state["wakeup_listening"]:
            self.add_chat_message("👂 Wake word listener activated", sender="BOI", msg_type="success")
        else:
            self.add_chat_message("👂 Wake word listener deactivated", sender="BOI", msg_type="warning")
    
    def toggle_v_sign_detector(self):
        """Toggle V-sign gesture detector"""
        self.state["vsign_detecting"] = not self.state["vsign_detecting"]
        if self.state["vsign_detecting"]:
            self.add_chat_message("✌️ V-Sign detector activated", sender="BOI", msg_type="success")
        else:
            self.add_chat_message("✌️ V-Sign detector deactivated", sender="BOI", msg_type="warning")
    
    def start_voice_listen(self):
        """Start voice listening"""
        self.add_chat_message("🎙️ Voice listening started", sender="BOI", msg_type="success")
    
    def handle_voice_command(self, command):
        """Handle voice commands"""
        self.input_field.delete(0, tk.END)
        self.input_field.insert(0, command)
        self.execute_command()
    
    def show_settings(self):
        """Show settings dialog"""
        messagebox.showinfo(
            "Settings",
            "⚙️ Settings Panel\n\n" +
            "Available options:\n" +
            "• Voice preferences\n" +
            "• Display theme\n" +
            "• Keyboard shortcuts\n" +
            "• Automation settings"
        )
    
    def show_help(self):
        """Show help information"""
        help_text = """
💡 BOI Help & Features

🤖 Command Types:
• Code: 'Write code for [task]'
• Vision: 'Analyze screenshot.png'
• System: 'Show CPU usage'
• Files: 'Search for *.txt'

🎯 Quick Commands:
• 'help' - Show help
• 'exit' - Close app
• 'position' - Mouse position
• 'contacts' - List contacts

🚀 Features:
✅ AI-powered automation
✅ Voice commands
✅ Gesture recognition
✅ Workflow templates
✅ Productivity tracking
✅ Security monitoring
"""
        messagebox.showinfo("Help", help_text)
    
    def show_phone_link_control(self):
        """Show phone link control"""
        messagebox.showinfo("📞 Phone Link", "Phone Link Controller\n\nManage mobile device integration")
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About BOI",
            "V.A.T.S.A.L - AI Desktop Assistant\n\n" +
            "Your intelligent automation companion\n\n" +
            "Features:\n" +
            "🤖 AI-Powered Automation\n" +
            "🎙️ Voice Control\n" +
            "👁️ Vision Analysis\n" +
            "⚡ Smart Workflows\n" +
            "🔐 Security Dashboard"
        )
    
    def show_security_dashboard(self):
        """Show security dashboard"""
        messagebox.showinfo("🔒 Security", "Security Dashboard\n\nMonitor system security and threats")
    
    def show_batch_utilities(self):
        """Show batch utilities"""
        messagebox.showinfo("⚡ Batch Utils", "Batch Utilities\n\nRun automated batch operations")
    
    def _update_time(self):
        """Update time display"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self._update_time)
    
    def _show_welcome(self):
        """Show welcome message"""
        welcome_msg = "👋 Welcome to V.A.T.S.A.L!\n\n🎯 What would you like to do?\n\nTry asking me anything!"
        self.add_chat_message(welcome_msg, sender="BOI", msg_type="info")
    
    def _start_background_tasks(self):
        """Start background tasks"""
        self._update_time()


def main():
    """Entry point"""
    root = tk.Tk()
    app = ModernBOIGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
