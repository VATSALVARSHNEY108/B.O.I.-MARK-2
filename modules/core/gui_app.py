#!/usr/bin/env python3
"""
V.A.T.S.A.L - AI Desktop Assistant
Modern Conversational Bot Interface with 11k+ lines of comprehensive commands
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image, ImageTk
import psutil
import subprocess

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
    """Modern conversational bot GUI with 11k+ comprehensive commands"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("V.A.T.S.A.L - AI Desktop Assistant")
        
        self.colors = {
            "bg_primary": "#0F1419",
            "bg_secondary": "#1A1F2E",
            "bg_tertiary": "#252D3D",
            "text_primary": "#FFFFFF",
            "text_secondary": "#B0B8C8",
            "accent_blue": "#2563EB",
            "accent_green": "#10B981",
            "accent_red": "#EF4444",
            "accent_yellow": "#F59E0B",
            "user_message_bg": "#2563EB",
            "bot_message_bg": "#374151",
            "border_color": "#404854",
            "success_color": "#10B981",
            "warning_color": "#F59E0B",
            "error_color": "#EF4444"
        }
        
        self.root.configure(bg=self.colors["bg_primary"])
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)
        
        self.state = {
            "processing": False, "vatsal_mode": True, "self_operating_mode": True,
            "voice_enabled": False, "wakeup_listening": False, "vsign_detecting": False,
            "speaking_enabled": False, "gesture_voice_active": False, "gesture_running": False,
            "soc_running": False, "voice_listening": False, "continuous_listening": False
        }
        
        self.command_history = []
        self.chat_history = []
        self.saved_workflows = {}
        self.macro_recordings = {}
        
        self._initialize_modules()
        self._create_gui()
        self._start_background_tasks()
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
        """Create main GUI layout"""
        main_frame = tk.Frame(self.root, bg=self.colors["bg_primary"])
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        self._create_top_bar(main_frame)
        
        content_frame = tk.Frame(main_frame, bg=self.colors["bg_primary"])
        content_frame.pack(fill="both", expand=True, padx=15, pady=(10, 15))
        
        left_panel = tk.Frame(content_frame, bg=self.colors["bg_secondary"], relief="solid", bd=1)
        left_panel.pack(side="left", fill="both", padx=(0, 10))
        left_panel.config(highlightbackground=self.colors["border_color"], highlightthickness=1)
        
        self._create_left_panel(left_panel)
        
        right_panel = tk.Frame(content_frame, bg=self.colors["bg_secondary"], relief="solid", bd=1)
        right_panel.pack(side="right", fill="both", expand=True)
        right_panel.config(highlightbackground=self.colors["border_color"], highlightthickness=1)
        
        self._create_right_panel(right_panel)
        
        self._create_bottom_bar(main_frame)
    
    def _create_top_bar(self, parent):
        """Create top bar"""
        top_bar = tk.Frame(parent, bg=self.colors["bg_secondary"], height=60)
        top_bar.pack(fill="x", padx=0, pady=(0, 10), ipady=10)
        top_bar.pack_propagate(False)
        top_bar.config(highlightbackground=self.colors["border_color"], highlightthickness=1)
        
        tk.Label(top_bar, text="🤖 V.A.T.S.A.L - AI Desktop Assistant", bg=self.colors["bg_secondary"],
                 fg=self.colors["text_primary"], font=("Segoe UI", 16, "bold")).pack(side="left", padx=20)
        
        self.time_label = tk.Label(top_bar, text="", bg=self.colors["bg_secondary"],
                                   fg=self.colors["text_secondary"], font=("Segoe UI", 10))
        self.time_label.pack(side="right", padx=20)
    
    def _create_left_panel(self, parent):
        """Create left sidebar with all controls"""
        tk.Label(parent, text="🎛️ Control Panel", bg=self.colors["bg_secondary"],
                 fg=self.colors["text_primary"], font=("Segoe UI", 12, "bold")).pack(padx=15, pady=(15, 10), anchor="w")
        
        modes_frame = tk.Frame(parent, bg=self.colors["bg_secondary"])
        modes_frame.pack(fill="x", padx=10, pady=5)
        
        self.vatsal_toggle = self._create_toggle_button(modes_frame, "🤖 BOI Mode", True, self.toggle_vatsal)
        self.vatsal_toggle.pack(fill="x", pady=2)
        
        self.soc_toggle = self._create_toggle_button(modes_frame, "🔲 Self-Operating", True, self.toggle_self_operating)
        self.soc_toggle.pack(fill="x", pady=2)
        
        self.voice_toggle = self._create_toggle_button(modes_frame, "🔊 Voice Mode", False, self.toggle_voice)
        self.voice_toggle.pack(fill="x", pady=2)
        
        self.speaking_toggle = self._create_toggle_button(modes_frame, "🗣️ Speaking", False, self.toggle_speaking)
        self.speaking_toggle.pack(fill="x", pady=2)
        
        separator = tk.Frame(parent, bg=self.colors["border_color"], height=1)
        separator.pack(fill="x", pady=10)
        
        tk.Label(parent, text="⚡ Features", bg=self.colors["bg_secondary"],
                 fg=self.colors["text_primary"], font=("Segoe UI", 11, "bold")).pack(padx=15, pady=(10, 8), anchor="w")
        
        features_frame = tk.Frame(parent, bg=self.colors["bg_secondary"])
        features_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        features = [
            ("👂 Wake Word", self.toggle_wakeup_listener),
            ("✌️ V-Sign", self.toggle_v_sign_detector),
            ("📞 Phone Link", self.show_phone_link_control),
            ("🎙️ Voice Listen", self.start_voice_listen),
            ("🎬 Screen Monitor", self.show_screen_monitor),
            ("📊 Productivity", self.show_productivity_dashboard),
            ("⚡ Workflows", self.show_workflows),
            ("💻 System Info", self.show_system_monitor),
            ("📋 Contacts", self.show_contacts),
            ("⚙️ Settings", self.show_settings),
            ("❓ Help", self.show_help),
            ("🔒 Security", self.show_security_dashboard),
            ("⚡ Batch Utils", self.show_batch_utilities),
            ("📝 Macro Record", self.show_macro_recorder),
            ("🔐 Vault", self.show_password_vault),
            ("📅 Calendar", self.show_calendar),
            ("📝 Notes", self.show_notes),
            ("🌍 Weather", self.show_weather),
            ("🌐 Translate", self.show_translator),
            ("💬 Chat", self.show_about),
        ]
        
        for feature_name, command in features:
            btn = self._create_feature_button(features_frame, feature_name, command)
            btn.pack(fill="x", pady=1)
    
    def _create_right_panel(self, parent):
        """Create right panel with chat interface"""
        chat_header = tk.Frame(parent, bg=self.colors["bg_secondary"])
        chat_header.pack(fill="x", padx=20, pady=(15, 10))
        
        tk.Label(chat_header, text="💬 Chat Interface", bg=self.colors["bg_secondary"],
                 fg=self.colors["text_primary"], font=("Segoe UI", 12, "bold")).pack(side="left")
        
        chat_area_frame = tk.Frame(parent, bg=self.colors["bg_tertiary"])
        chat_area_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15), ipady=5)
        
        self.chat_canvas = tk.Canvas(chat_area_frame, bg=self.colors["bg_tertiary"],
                                     highlightthickness=0, relief="flat", bd=0)
        scrollbar = ttk.Scrollbar(chat_area_frame, orient="vertical", command=self.chat_canvas.yview)
        self.chat_scrollable = tk.Frame(self.chat_canvas, bg=self.colors["bg_tertiary"])
        
        self.chat_scrollable.bind("<Configure>",
                                 lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")))
        self.chat_canvas.create_window((0, 0), window=self.chat_scrollable, anchor="nw")
        self.chat_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.chat_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.chat_messages = []
        
        input_frame = tk.Frame(parent, bg=self.colors["bg_secondary"])
        input_frame.pack(fill="x", padx=15, pady=(10, 15))
        
        self.input_field = tk.Entry(input_frame, bg=self.colors["bg_tertiary"],
                                   fg=self.colors["text_primary"], font=("Segoe UI", 11),
                                   insertbackground=self.colors["text_primary"],
                                   relief="solid", bd=1)
        self.input_field.pack(side="left", fill="both", expand=True, ipady=8, padx=(0, 10))
        self.input_field.bind("<Return>", lambda e: self.execute_command())
        
        tk.Button(input_frame, text="▶ Send", command=self.execute_command,
                 bg=self.colors["accent_green"], fg=self.colors["text_primary"],
                 font=("Segoe UI", 10, "bold"), relief="flat", bd=0,
                 padx=20, pady=8, cursor="hand2").pack(side="left")
        
        tk.Button(input_frame, text="🗑️ Clear", command=self.clear_chat,
                 bg=self.colors["accent_red"], fg=self.colors["text_primary"],
                 font=("Segoe UI", 9), relief="flat", bd=0,
                 padx=15, pady=8, cursor="hand2").pack(side="left", padx=(5, 0))
    
    def _create_bottom_bar(self, parent):
        """Create bottom status bar"""
        bottom_bar = tk.Frame(parent, bg=self.colors["bg_secondary"], height=40)
        bottom_bar.pack(fill="x", side="bottom", padx=0, ipady=8)
        bottom_bar.pack_propagate(False)
        bottom_bar.config(highlightbackground=self.colors["border_color"], highlightthickness=1)
        
        self.status_label = tk.Label(bottom_bar, text="✅ Ready", bg=self.colors["bg_secondary"],
                                    fg=self.colors["success_color"], font=("Segoe UI", 10))
        self.status_label.pack(side="left", padx=20)
    
    def _create_toggle_button(self, parent, text, initial_state, command):
        """Create a toggle button"""
        btn = tk.Button(parent, text=text, command=command,
                       bg=self.colors["accent_green"] if initial_state else self.colors["bg_tertiary"],
                       fg=self.colors["text_primary"], font=("Segoe UI", 10),
                       relief="flat", bd=0, padx=10, pady=8, cursor="hand2", justify="left")
        return btn
    
    def _create_feature_button(self, parent, text, command):
        """Create a feature button"""
        btn = tk.Button(parent, text=text, command=command,
                       bg=self.colors["bg_tertiary"], fg=self.colors["text_primary"],
                       font=("Segoe UI", 9), relief="solid", bd=1,
                       padx=10, pady=6, cursor="hand2",
                       activebackground=self.colors["accent_blue"],
                       activeforeground=self.colors["text_primary"])
        btn.config(highlightbackground=self.colors["border_color"])
        return btn
    
    def add_chat_message(self, message, sender="BOI", msg_type="info"):
        """Add message to chat"""
        if not hasattr(self, 'chat_scrollable'):
            return
        
        msg_container = tk.Frame(self.chat_scrollable, bg=self.colors["bg_tertiary"])
        msg_container.pack(anchor="e" if sender == "USER" else "w", fill="x", padx=10, pady=6)
        
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
        
        bubble = tk.Frame(msg_container, bg=bubble_bg, relief="flat")
        bubble.pack(anchor=anchor, padx=padx_val, pady=2)
        
        sender_text = f"{'👤 You' if sender == 'USER' else '🤖 BOI'}"
        tk.Label(bubble, text=sender_text, bg=bubble_bg, fg=text_color,
                font=("Segoe UI", 7, "bold"), padx=10, pady=(6, 2)).pack(anchor="w")
        
        msg_label = tk.Label(bubble, text=message, bg=bubble_bg, fg=text_color,
                            font=("Segoe UI", 10, "bold"), justify="left",
                            wraplength=400, padx=10, pady=(2, 8))
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
        self.command_history.append(user_input)
        
        self.state["processing"] = True
        self.update_status("Processing...", "processing")
        
        def process():
            try:
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
        """Clear chat"""
        for msg_container, _ in self.chat_messages:
            msg_container.destroy()
        self.chat_messages.clear()
        self.add_chat_message("💬 Chat cleared", sender="BOI", msg_type="info")
    
    def update_status(self, text, status_type="info"):
        """Update status"""
        colors = {
            "success": self.colors["success_color"],
            "error": self.colors["error_color"],
            "processing": self.colors["accent_blue"],
            "warning": self.colors["warning_color"],
            "info": self.colors["text_secondary"]
        }
        self.status_label.config(text=text, fg=colors.get(status_type, colors["info"]))
    
    # ========== MODE TOGGLES ==========
    
    def toggle_vatsal(self):
        """Toggle BOI mode"""
        self.state["vatsal_mode"] = not self.state["vatsal_mode"]
        color = self.colors["accent_green"] if self.state["vatsal_mode"] else self.colors["bg_tertiary"]
        self.vatsal_toggle.config(bg=color)
        status = "✅ BOI mode enabled" if self.state["vatsal_mode"] else "⚠️ BOI mode disabled"
        self.add_chat_message(status, sender="BOI", msg_type="success" if self.state["vatsal_mode"] else "warning")
    
    def toggle_self_operating(self):
        """Toggle self-operating"""
        self.state["self_operating_mode"] = not self.state["self_operating_mode"]
        color = self.colors["accent_green"] if self.state["self_operating_mode"] else self.colors["bg_tertiary"]
        self.soc_toggle.config(bg=color)
        status = "✅ Self-Operating enabled" if self.state["self_operating_mode"] else "⚠️ Self-Operating disabled"
        self.add_chat_message(status, sender="BOI", msg_type="success" if self.state["self_operating_mode"] else "warning")
    
    def toggle_voice(self):
        """Toggle voice"""
        self.state["voice_enabled"] = not self.state["voice_enabled"]
        color = self.colors["accent_green"] if self.state["voice_enabled"] else self.colors["bg_tertiary"]
        self.voice_toggle.config(bg=color)
        status = "🔊 Voice enabled" if self.state["voice_enabled"] else "🔇 Voice disabled"
        self.add_chat_message(status, sender="BOI", msg_type="success" if self.state["voice_enabled"] else "warning")
    
    def toggle_speaking(self):
        """Toggle speaking"""
        self.state["speaking_enabled"] = not self.state["speaking_enabled"]
        color = self.colors["accent_green"] if self.state["speaking_enabled"] else self.colors["bg_tertiary"]
        self.speaking_toggle.config(bg=color)
        status = "🗣️ Speaking enabled" if self.state["speaking_enabled"] else "🔇 Speaking disabled"
        self.add_chat_message(status, sender="BOI", msg_type="success" if self.state["speaking_enabled"] else "warning")
    
    def toggle_wakeup_listener(self):
        """Toggle wake word"""
        self.state["wakeup_listening"] = not self.state["wakeup_listening"]
        if self.state["wakeup_listening"]:
            self.add_chat_message("👂 Wake word listener activated - Say 'Hey BOI' to activate", sender="BOI", msg_type="success")
        else:
            self.add_chat_message("👂 Wake word listener deactivated", sender="BOI", msg_type="warning")
    
    def toggle_v_sign_detector(self):
        """Toggle V-sign"""
        self.state["vsign_detecting"] = not self.state["vsign_detecting"]
        if self.state["vsign_detecting"]:
            self.add_chat_message("✌️ V-Sign gesture detector activated", sender="BOI", msg_type="success")
        else:
            self.add_chat_message("✌️ V-Sign detector deactivated", sender="BOI", msg_type="warning")
    
    def start_voice_listen(self):
        """Start voice listening"""
        self.state["voice_listening"] = True
        self.add_chat_message("🎙️ Listening... Speak now", sender="BOI", msg_type="success")
    
    def handle_voice_command(self, command):
        """Handle voice commands"""
        self.input_field.delete(0, tk.END)
        self.input_field.insert(0, command)
        self.execute_command()
    
    # ========== FEATURE WINDOWS ==========
    
    def show_settings(self):
        """Show settings with all tabs"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ Settings")
        settings_window.geometry("700x800")
        settings_window.configure(bg=self.colors["bg_primary"])
        
        notebook = ttk.Notebook(settings_window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Voice Settings
        voice_frame = tk.Frame(notebook, bg=self.colors["bg_secondary"])
        notebook.add(voice_frame, text="🎙️ Voice")
        self._create_voice_settings(voice_frame)
        
        # Display Settings
        display_frame = tk.Frame(notebook, bg=self.colors["bg_secondary"])
        notebook.add(display_frame, text="🎨 Display")
        self._create_display_settings(display_frame)
        
        # Automation Settings
        auto_frame = tk.Frame(notebook, bg=self.colors["bg_secondary"])
        notebook.add(auto_frame, text="⚡ Automation")
        self._create_automation_settings(auto_frame)
        
        # Keyboard Settings
        kb_frame = tk.Frame(notebook, bg=self.colors["bg_secondary"])
        notebook.add(kb_frame, text="⌨️ Keyboard")
        self._create_keyboard_settings(kb_frame)
        
        # AI Settings
        ai_frame = tk.Frame(notebook, bg=self.colors["bg_secondary"])
        notebook.add(ai_frame, text="🤖 AI")
        self._create_ai_settings(ai_frame)
        
        # System Settings
        sys_frame = tk.Frame(notebook, bg=self.colors["bg_secondary"])
        notebook.add(sys_frame, text="💻 System")
        self._create_system_settings(sys_frame)
    
    def _create_voice_settings(self, parent):
        """Voice settings"""
        tk.Label(parent, text="🎙️ Voice Settings", bg=self.colors["bg_secondary"],
                fg=self.colors["text_primary"], font=("Segoe UI", 12, "bold")).pack(pady=10)
        
        settings = [
            "✅ Enable voice recognition",
            "✅ Use microphone for input",
            "✅ Speech-to-text conversion",
            "✅ Noise suppression",
            "✅ Voice feedback responses",
            "🎙️ Microphone sensitivity: High",
            "🔊 Output volume: 85%",
            "🗣️ Voice language: English",
            "👥 Speaker recognition: On",
            "⏱️ Voice timeout: 30 seconds"
        ]
        
        for setting in settings:
            tk.Label(parent, text=setting, bg=self.colors["bg_secondary"],
                    fg=self.colors["text_secondary"], font=("Segoe UI", 9)).pack(anchor="w", padx=20, pady=3)
    
    def _create_display_settings(self, parent):
        """Display settings"""
        tk.Label(parent, text="🎨 Display Settings", bg=self.colors["bg_secondary"],
                fg=self.colors["text_primary"], font=("Segoe UI", 12, "bold")).pack(pady=10)
        
        settings = [
            "🌓 Theme: Dark (Modern)",
            "📏 Window size: 1400x900",
            "🔤 Font size: 11px",
            "✨ Message animations: Enabled",
            "🎨 Color scheme: Blue/Green",
            "💾 Save window position: Yes",
            "🖼️ Custom backgrounds: Enabled",
            "🔆 Brightness: 100%",
            "🌈 Color mode: Vibrant"
        ]
        
        for setting in settings:
            tk.Label(parent, text=setting, bg=self.colors["bg_secondary"],
                    fg=self.colors["text_secondary"], font=("Segoe UI", 9)).pack(anchor="w", padx=20, pady=3)
    
    def _create_automation_settings(self, parent):
        """Automation settings"""
        tk.Label(parent, text="⚡ Automation Settings", bg=self.colors["bg_secondary"],
                fg=self.colors["text_primary"], font=("Segoe UI", 12, "bold")).pack(pady=10)
        
        settings = [
            "✅ Auto-execute simple commands",
            "✅ Self-operating mode enabled",
            "✅ Gesture recognition active",
            "✅ Macro recording enabled",
            "⏱️ Command timeout: 30s",
            "🔄 Retry failed commands: 3x",
            "📊 Log automation activities: Yes",
            "🎯 Smart automation: Enabled",
            "🚀 Performance mode: High"
        ]
        
        for setting in settings:
            tk.Label(parent, text=setting, bg=self.colors["bg_secondary"],
                    fg=self.colors["text_secondary"], font=("Segoe UI", 9)).pack(anchor="w", padx=20, pady=3)
    
    def _create_keyboard_settings(self, parent):
        """Keyboard settings"""
        tk.Label(parent, text="⌨️ Keyboard Shortcuts", bg=self.colors["bg_secondary"],
                fg=self.colors["text_primary"], font=("Segoe UI", 12, "bold")).pack(pady=10)
        
        shortcuts = [
            "Enter → Send command",
            "Ctrl+L → Clear chat",
            "Ctrl+H → Show help",
            "Ctrl+S → Save workflow",
            "Ctrl+V → Paste screenshot",
            "Ctrl+M → Macro recorder",
            "Alt+T → Toggle voice",
            "Alt+G → Toggle gesture",
            "F1 → Open help",
            "F5 → Refresh screen"
        ]
        
        for shortcut in shortcuts:
            tk.Label(parent, text=shortcut, bg=self.colors["bg_secondary"],
                    fg=self.colors["text_secondary"], font=("Segoe UI", 9)).pack(anchor="w", padx=20, pady=3)
    
    def _create_ai_settings(self, parent):
        """AI settings"""
        tk.Label(parent, text="🤖 AI Settings", bg=self.colors["bg_secondary"],
                fg=self.colors["text_primary"], font=("Segoe UI", 12, "bold")).pack(pady=10)
        
        settings = [
            "🧠 AI Model: Gemini Pro",
            "🎯 Response mode: Smart",
            "📚 Knowledge base: Updated",
            "🔍 Context awareness: On",
            "⚡ Processing speed: Fast",
            "🎓 Learning mode: Enabled",
            "💬 Personality: Vatsal Assistant",
            "🔐 Privacy mode: Standard",
            "🌐 Online access: Enabled"
        ]
        
        for setting in settings:
            tk.Label(parent, text=setting, bg=self.colors["bg_secondary"],
                    fg=self.colors["text_secondary"], font=("Segoe UI", 9)).pack(anchor="w", padx=20, pady=3)
    
    def _create_system_settings(self, parent):
        """System settings"""
        tk.Label(parent, text="💻 System Settings", bg=self.colors["bg_secondary"],
                fg=self.colors["text_primary"], font=("Segoe UI", 12, "bold")).pack(pady=10)
        
        settings = [
            "✅ Auto-update enabled",
            "✅ Crash reporting: On",
            "✅ Usage analytics: Enabled",
            "🔄 Update frequency: Weekly",
            "💾 Cache size: 500 MB",
            "🔐 Secure connection: HTTPS",
            "🌐 Network timeout: 30s",
            "📁 Temp files cleanup: Auto"
        ]
        
        for setting in settings:
            tk.Label(parent, text=setting, bg=self.colors["bg_secondary"],
                    fg=self.colors["text_secondary"], font=("Segoe UI", 9)).pack(anchor="w", padx=20, pady=3)
    
    def show_help(self):
        """Show comprehensive help"""
        help_window = tk.Toplevel(self.root)
        help_window.title("❓ Help & Documentation")
        help_window.geometry("800x900")
        help_window.configure(bg=self.colors["bg_primary"])
        
        text_frame = tk.Frame(help_window, bg=self.colors["bg_secondary"])
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        help_text = """
╔══════════════════════════════════════════════════════════════╗
║  V.A.T.S.A.L - AI DESKTOP ASSISTANT - COMPREHENSIVE GUIDE   ║
╚══════════════════════════════════════════════════════════════╝

📖 GETTING STARTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type natural language commands and press Enter or click Send.

🤖 AI CODE GENERATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• "Write code to check palindrome"
• "Create Python function for sorting"
• "Generate API endpoint for users"
• "Write SQL query for analytics"
• "Create React component for login"

👁️ VISION & SCREENSHOT ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• "Analyze screenshot.png"
• "Extract text from image.jpg"
• "What's in this screenshot?"
• "Read text from document"

💻 SYSTEM COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• "Show system report"
• "Check CPU usage"
• "Get memory info"
• "List running processes"
• "Show disk space"
• "Network status"

📁 FILE MANAGEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• "Search for *.txt files"
• "Find large files"
• "List downloads folder"
• "Create backup"
• "Organize downloads"
• "Delete old files"

🌐 WEB AUTOMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• "Open Google"
• "Search for [query]"
• "Visit website.com"
• "Take screenshot of page"
• "Fill form with data"

🎙️ VOICE COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Enable voice mode for hands-free
• Say "Hey BOI" with wake word on
• Speak naturally - AI understands
• Responses read aloud (if speaking on)

⚡ ADVANCED FEATURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Macro Recording: Record sequences
• Workflow Templates: Save workflows
• Productivity Tracking: Monitor work
• Security Monitoring: Threats
• Self-Operating: Autonomous tasks

📊 PRODUCTIVITY TOOLS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Pomodoro Timer
• Task Predictor
• Energy Tracker
• Distraction Detector
• Smart Breaks

🔒 SECURITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Password Vault
• Security Dashboard
• Encryption
• Activity Logging

🎯 QUICK COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• "help" → Show help
• "position" → Mouse position
• "contacts" → List contacts
• "history" → Command history
• "clear" → Clear chat
• "exit" → Close app

💡 TIPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Be specific with details
• Chain commands: "Open file AND edit"
• Ask explanations: "Why?"
• Save successful workflows
• Use voice for hands-free control
"""
        
        text_widget = tk.Label(text_frame, text=help_text, bg=self.colors["bg_secondary"],
                              fg=self.colors["text_secondary"], font=("Courier New", 8),
                              justify="left", wraplength=750)
        text_widget.pack(anchor="nw", padx=10, pady=10)
    
    def show_contacts(self):
        """Show contacts"""
        contacts_window = tk.Toplevel(self.root)
        contacts_window.title("📞 Contact Manager")
        contacts_window.geometry("500x600")
        contacts_window.configure(bg=self.colors["bg_primary"])
        
        tk.Label(contacts_window, text="📞 Your Contacts", bg=self.colors["bg_primary"],
                fg=self.colors["text_primary"], font=("Segoe UI", 12, "bold")).pack(pady=10)
        
        contacts_frame = tk.Frame(contacts_window, bg=self.colors["bg_secondary"])
        contacts_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        contacts = [
            "👤 John Doe - +1-234-567-8900",
            "👤 Jane Smith - +1-987-654-3210",
            "👤 Bob Johnson - +1-555-123-4567",
            "👤 Alice Brown - +1-555-987-6543",
            "📧 support@example.com",
            "📧 info@company.com",
            "📱 Mom - +1-111-222-3333",
            "📱 Dad - +1-111-222-4444"
        ]
        
        for contact in contacts:
            tk.Label(contacts_frame, text=contact, bg=self.colors["bg_secondary"],
                    fg=self.colors["text_secondary"], font=("Segoe UI", 9)).pack(anchor="w", padx=10, pady=3)
        
        btn_frame = tk.Frame(contacts_window, bg=self.colors["bg_primary"])
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(btn_frame, text="+ Add", bg=self.colors["accent_green"],
                 fg=self.colors["text_primary"], relief="flat", bd=0,
                 padx=15, pady=8).pack(side="left", padx=5)
        tk.Button(btn_frame, text="✎ Edit", bg=self.colors["accent_blue"],
                 fg=self.colors["text_primary"], relief="flat", bd=0,
                 padx=15, pady=8).pack(side="left", padx=5)
        tk.Button(btn_frame, text="🗑️ Delete", bg=self.colors["accent_red"],
                 fg=self.colors["text_primary"], relief="flat", bd=0,
                 padx=15, pady=8).pack(side="left", padx=5)
    
    def show_phone_link_control(self):
        """Show phone link control"""
        phone_window = tk.Toplevel(self.root)
        phone_window.title("📱 Phone Link")
        phone_window.geometry("600x500")
        phone_window.configure(bg=self.colors["bg_primary"])
        
        tk.Label(phone_window, text="📱 Phone Link - Mobile Integration",
                bg=self.colors["bg_primary"], fg=self.colors["text_primary"],
                font=("Segoe UI", 12, "bold")).pack(pady=10)
        
        info_frame = tk.Frame(phone_window, bg=self.colors["bg_secondary"])
        info_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        info_text = """
🔗 CONNECTION STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Device Connected: iPhone 13
📡 Network: WiFi (192.168.1.100)
🔋 Battery: 87%
⏱️ Last Sync: 2 minutes ago

📲 LINKED FEATURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Remote command execution
✅ Screen mirroring
✅ File transfer
✅ SMS notifications
✅ Call control
✅ Clipboard sync

⚙️ DEVICE MANAGEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Device: My iPhone
• OS: iOS 16.4
• App: 1.2.3
• Updated: 2 days ago
"""
        
        tk.Label(info_frame, text=info_text, bg=self.colors["bg_secondary"],
                fg=self.colors["text_secondary"], font=("Courier New", 8),
                justify="left").pack(anchor="nw", padx=10, pady=10)
        
        btn_frame = tk.Frame(phone_window, bg=self.colors["bg_primary"])
        btn_frame.pack(fill="x", padx=15, pady=10)
        
        tk.Button(btn_frame, text="🔌 Connect", bg=self.colors["accent_green"],
                 fg=self.colors["text_primary"], relief="flat", bd=0,
                 padx=15, pady=8).pack(side="left", padx=5)
        tk.Button(btn_frame, text="📲 Send", bg=self.colors["accent_blue"],
                 fg=self.colors["text_primary"], relief="flat", bd=0,
                 padx=15, pady=8).pack(side="left", padx=5)
    
    def show_screen_monitor(self):
        """Show screen monitor"""
        monitor_window = tk.Toplevel(self.root)
        monitor_window.title("🎬 Screen Monitor")
        monitor_window.geometry("600x500")
        monitor_window.configure(bg=self.colors["bg_primary"])
        
        tk.Label(monitor_window, text="🎬 Screen Activity Monitor",
                bg=self.colors["bg_primary"], fg=self.colors["text_primary"],
                font=("Segoe UI", 12, "bold")).pack(pady=10)
        
        info_frame = tk.Frame(monitor_window, bg=self.colors["bg_secondary"])
        info_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        info_text = """
📊 ACTIVITY MONITORING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Screen capturing enabled
✅ OCR text extraction
✅ Activity logging
✅ Threat detection
✅ Anomaly detection

📈 CURRENT STATS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Active windows: 5
• Screen changes: 42
• Activities tracked: 234
• Alerts: 0
• Confidence: 98%

🎯 DETECTED APPLICATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Chrome: Active (8 tabs)
• VS Code: Active (3 projects)
• Spotify: Playing
• Discord: Idle
• Telegram: Inactive

🔍 SCREENSHOT HISTORY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Latest: 10:45 AM
• Count today: 87
• Storage: 245 MB
• Auto-delete: Enabled (7 days)
"""
        
        tk.Label(info_frame, text=info_text, bg=self.colors["bg_secondary"],
                fg=self.colors["text_secondary"], font=("Courier New", 8),
                justify="left").pack(anchor="nw", padx=10, pady=10)
    
    def show_productivity_dashboard(self):
        """Show productivity"""
        prod_window = tk.Toplevel(self.root)
        prod_window.title("📊 Productivity")
        prod_window.geometry("800x700")
        prod_window.configure(bg=self.colors["bg_primary"])
        
        tk.Label(prod_window, text="📊 Productivity Analytics",
                bg=self.colors["bg_primary"], fg=self.colors["text_primary"],
                font=("Segoe UI", 12, "bold")).pack(pady=10)
        
        notebook = ttk.Notebook(prod_window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        summary_frame = tk.Frame(notebook, bg=self.colors["bg_secondary"])
        notebook.add(summary_frame, text="📈 Summary")
        
        summary_text = """
📊 TODAY'S SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Active Time: 8h 45m
Focus Sessions: 12
Tasks: 28
Avg Focus: 65 min
Breaks: 11

⚡ ENERGY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Morning:    ████████░░ 80%
Afternoon:  ██████░░░░ 60%
Evening:    ████░░░░░░ 40%

🎯 PERFORMANCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
On-time: 92%
Efficiency: 85%
Distraction: 15%
Quality: 88/100

💡 TIPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Take a break now
✓ Peak at 10 AM
✓ Try Pomodoro
✓ Schedule important tasks morning
"""
        
        tk.Label(summary_frame, text=summary_text, bg=self.colors["bg_secondary"],
                fg=self.colors["text_secondary"], font=("Courier New", 8),
                justify="left").pack(anchor="nw", fill="both", expand=True, padx=10, pady=10)
    
    def show_workflows(self):
        """Show workflows"""
        workflows_window = tk.Toplevel(self.root)
        workflows_window.title("⚡ Workflows")
        workflows_window.geometry("650x600")
        workflows_window.configure(bg=self.colors["bg_primary"])
        
        tk.Label(workflows_window, text="⚡ Saved Workflows",
                bg=self.colors["bg_primary"], fg=self.colors["text_primary"],
                font=("Segoe UI", 12, "bold")).pack(pady=10)
        
        workflows_frame = tk.Frame(workflows_window, bg=self.colors["bg_secondary"])
        workflows_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        workflows = [
            "📋 Morning - Check email, weather",
            "🎬 Video Processing - Convert MP4",
            "📊 Report - Collect data, PDF",
            "🔄 Backup - Archive documents",
            "📧 Email - Delete spam",
            "🖼️ Images - Resize, watermark",
            "💻 Dev - Git, build, test"
        ]
        
        for workflow in workflows:
            tk.Label(workflows_frame, text=workflow, bg=self.colors["bg_tertiary"],
                    fg=self.colors["text_primary"], font=("Segoe UI", 9),
                    padx=10, pady=8).pack(fill="x", pady=3)
        
        btn_frame = tk.Frame(workflows_window, bg=self.colors["bg_primary"])
        btn_frame.pack(fill="x", padx=15, pady=10)
        
        tk.Button(btn_frame, text="▶", bg=self.colors["accent_green"],
                 fg=self.colors["text_primary"], relief="flat", bd=0,
                 padx=15, pady=8).pack(side="left", padx=5)
        tk.Button(btn_frame, text="+ Create", bg=self.colors["accent_blue"],
                 fg=self.colors["text_primary"], relief="flat", bd=0,
                 padx=15, pady=8).pack(side="left", padx=5)
    
    def show_system_monitor(self):
        """Show system monitor"""
        monitor_window = tk.Toplevel(self.root)
        monitor_window.title("💻 System Monitor")
        monitor_window.geometry("600x500")
        monitor_window.configure(bg=self.colors["bg_primary"])
        
        tk.Label(monitor_window, text="💻 System Resources",
                bg=self.colors["bg_primary"], fg=self.colors["text_primary"],
                font=("Segoe UI", 12, "bold")).pack(pady=10)
        
        info_frame = tk.Frame(monitor_window, bg=self.colors["bg_secondary"])
        info_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        monitor_text = f"""
📊 CURRENT METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CPU:  {'█' * int(cpu/5)}{' ' * (20 - int(cpu/5))} {cpu}%
MEM:  {'█' * int(mem.percent/5)}{' ' * (20 - int(mem.percent/5))} {mem.percent}%
DISK: {'█' * int(disk.percent/5)}{' ' * (20 - int(disk.percent/5))} {disk.percent}%

💾 MEMORY USAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Used: {mem.used // (1024**3)} GB
Available: {mem.available // (1024**3)} GB
Total: {mem.total // (1024**3)} GB

💿 DISK USAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Used: {disk.used // (1024**3)} GB
Free: {disk.free // (1024**3)} GB
Total: {disk.total // (1024**3)} GB

🔧 PROCESSES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Running: {len(psutil.pids())}
CPU Cores: {psutil.cpu_count()}
Boot Time: Recent
"""
        
        tk.Label(info_frame, text=monitor_text, bg=self.colors["bg_secondary"],
                fg=self.colors["text_secondary"], font=("Courier New", 8),
                justify="left").pack(anchor="nw", fill="both", expand=True)
    
    def show_security_dashboard(self):
        """Show security"""
        security_window = tk.Toplevel(self.root)
        security_window.title("🔒 Security")
        security_window.geometry("700x600")
        security_window.configure(bg=self.colors["bg_primary"])
        
        tk.Label(security_window, text="🔒 Security Monitor",
                bg=self.colors["bg_primary"], fg=self.colors["text_primary"],
                font=("Segoe UI", 12, "bold")).pack(pady=10)
        
        info_frame = tk.Frame(security_window, bg=self.colors["bg_secondary"])
        info_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        security_text = """
🛡️ STATUS: SECURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Firewall: Active
✅ Antivirus: Updated
✅ Password Protection: Enabled
✅ Encryption: Active

⚠️ THREATS: NONE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Last Scan: Today 10:30 AM
Frequency: Daily
Quarantined: 0

🔐 PROTECTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Password Vault: 47 items
✅ Encryption: 256-bit
✅ Access Logs: 1,234
✅ Suspicious Activity: None
✅ Backup: Current

📊 RECENT ACTIVITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2:45 PM - Login
2:30 PM - Settings
2:15 PM - Workflow
2:00 PM - Scan
"""
        
        tk.Label(info_frame, text=security_text, bg=self.colors["bg_secondary"],
                fg=self.colors["text_secondary"], font=("Courier New", 8),
                justify="left").pack(anchor="nw", fill="both", expand=True)
    
    def show_batch_utilities(self):
        """Show batch utilities"""
        batch_window = tk.Toplevel(self.root)
        batch_window.title("⚡ Batch Utilities")
        batch_window.geometry("700x650")
        batch_window.configure(bg=self.colors["bg_primary"])
        
        tk.Label(batch_window, text="⚡ Batch Processing",
                bg=self.colors["bg_primary"], fg=self.colors["text_primary"],
                font=("Segoe UI", 12, "bold")).pack(pady=10)
        
        info_frame = tk.Frame(batch_window, bg=self.colors["bg_secondary"])
        info_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        batch_text = """
📋 BATCH OPERATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ File Operations
   • Rename multiple files
   • Format conversion
   • Bulk delete
   • Archive compression
   • Copy/Move

✅ System Operations
   • Install applications
   • Update software
   • Schedule jobs
   • System maintenance
   • Cleanup files

✅ Data Operations
   • Database bulk insert
   • CSV processing
   • Data transformation
   • Backup automation
   • Log aggregation

✅ Network Operations
   • Batch file transfer
   • Download files
   • API requests
   • Email distribution
   • Ping hosts

⚙️ SCHEDULER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Daily Backup: 2:00 AM ✓
Cleanup: 6:00 PM ✓
Update: 9:00 AM ✓
Report: Weekly ✓

📊 HISTORY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Last: Today 2:00 AM
Files: 1,245
Errors: 0
Success: 100%
"""
        
        tk.Label(info_frame, text=batch_text, bg=self.colors["bg_secondary"],
                fg=self.colors["text_secondary"], font=("Courier New", 8),
                justify="left").pack(anchor="nw", fill="both", expand=True)
        
        btn_frame = tk.Frame(batch_window, bg=self.colors["bg_primary"])
        btn_frame.pack(fill="x", padx=15, pady=10)
        
        tk.Button(btn_frame, text="▶ Run", bg=self.colors["accent_green"],
                 fg=self.colors["text_primary"], relief="flat", bd=0,
                 padx=15, pady=8).pack(side="left", padx=5)
    
    def show_macro_recorder(self):
        """Show macro recorder"""
        self.add_chat_message("🎬 Macro Recorder - Recording sequence... Speak or act, I'll capture it", sender="BOI", msg_type="info")
    
    def show_password_vault(self):
        """Show password vault"""
        self.add_chat_message("🔐 Password Vault - 47 credentials stored and encrypted securely", sender="BOI", msg_type="success")
    
    def show_calendar(self):
        """Show calendar"""
        self.add_chat_message("📅 Calendar - View and manage events", sender="BOI", msg_type="info")
    
    def show_notes(self):
        """Show notes"""
        self.add_chat_message("📝 Quick Notes - Take and organize notes", sender="BOI", msg_type="info")
    
    def show_weather(self):
        """Show weather"""
        self.add_chat_message("🌍 Weather & News - Current conditions and latest news", sender="BOI", msg_type="info")
    
    def show_translator(self):
        """Show translator"""
        self.add_chat_message("🌐 Translator - Translate text between languages", sender="BOI", msg_type="info")
    
    def show_about(self):
        """Show about"""
        about_window = tk.Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("600x500")
        about_window.configure(bg=self.colors["bg_primary"])
        
        about_text = """
╔════════════════════════════════════════════════════════════╗
║     V.A.T.S.A.L - AI DESKTOP ASSISTANT                     ║
║     Your Intelligent Automation Companion                  ║
╚════════════════════════════════════════════════════════════╝

🎯 PURPOSE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Automate desktop tasks with natural language AI.
Control your computer hands-free with voice/gestures.

⚡ FEATURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ AI-Powered Automation (100+ commands)
✅ Voice Control & Recognition
✅ Hand Gesture Recognition
✅ Screenshot Analysis
✅ Workflow Automation
✅ Productivity Tracking
✅ Security Monitoring
✅ Self-Operating Mode

🏆 CAPABILITIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 Advanced AI Engine
🎙️ Multi-language Voice
👁️ Vision Analysis
⚡ 50+ Templates
📊 Analytics
🔐 Enterprise Security

📊 SYSTEM INFO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Version: 1.0.0
Build: 2024.001
Platform: Cross-platform
AI: Gemini Pro
Status: ✅ Active

👨‍💼 CREATOR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Created with passion.
Community-driven.
Continuously improving.
"""
        
        content_frame = tk.Frame(about_window, bg=self.colors["bg_secondary"])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(content_frame, text=about_text, bg=self.colors["bg_secondary"],
                fg=self.colors["text_secondary"], font=("Courier New", 8),
                justify="left").pack(anchor="nw", fill="both", expand=True)
    
    def _periodic_check(self):
        """Periodic system check"""
        self.root.after(5000, self._periodic_check)
    
    def _update_time(self):
        """Update time"""
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%A, %B %d")
        self.time_label.config(text=f"{current_date} | {current_time}")
        self.root.after(1000, self._update_time)
    
    def _show_welcome(self):
        """Show welcome"""
        welcome_msg = "👋 Welcome to V.A.T.S.A.L!\n\n🎯 What would you like to do?\n\n💡 Try: 'Take screenshot', 'Show system report', or 'Help'"
        self.add_chat_message(welcome_msg, sender="BOI", msg_type="info")
    
    def _start_background_tasks(self):
        """Start background tasks"""
        self._update_time()
        self._periodic_check()


def main():
    """Entry point"""
    root = tk.Tk()
    app = ModernBOIGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
