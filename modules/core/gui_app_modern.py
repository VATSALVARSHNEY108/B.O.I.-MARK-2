#!/usr/bin/env python3
"""
V.A.T.S.A.L - Enhanced Modern ChatGPT-Style Conversational GUI
Premium dark theme with advanced UI/UX features
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
import time

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


class EnhancedChatGPTGUI:
    """Premium Enhanced ChatGPT-style GUI with advanced UI/UX"""

    def __init__(self, root):
        self.root = root
        self.root.title("V.A.T.S.A.L - AI Desktop Assistant")
        
        # Premium theme colors
        self.colors = {
            "bg_primary": "#0a0e27",
            "bg_secondary": "#10141e",
            "bg_tertiary": "#16213e",
            "text_primary": "#f0f0f0",
            "text_secondary": "#a0a0a0",
            "text_muted": "#707070",
            "accent_primary": "#10a37f",
            "accent_secondary": "#1f7e6f",
            "accent_red": "#ef4444",
            "accent_blue": "#3b82f6",
            "user_bubble": "#10a37f",
            "bot_bubble": "#1a202c",
            "input_bg": "#16213e",
            "hover_color": "#2d3748",
            "border_color": "#2d3748",
            "success_green": "#10b981",
            "warning_yellow": "#f59e0b",
        }
        
        self.root.configure(bg=self.colors["bg_primary"])
        self.root.geometry("1500x950")
        self.root.minsize(1100, 750)
        
        # Configure ttk style
        self._setup_ttk_style()
        
        # State management
        self.state = {
            "processing": False,
            "vatsal_mode": True,
            "self_operating_mode": True,
            "voice_enabled": False,
            "connected": True,
            "typing": False
        }
        
        # Initialize modules and GUI
        self._initialize_modules()
        self._create_gui()
        self._show_welcome()
        self._start_background_tasks()
    
    def _setup_ttk_style(self):
        """Configure ttk widget styling"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TScrollbar', background=self.colors["bg_tertiary"], 
                       troughcolor=self.colors["bg_secondary"])
        style.configure('TNotebook', background=self.colors["bg_primary"],
                       foreground=self.colors["text_primary"])
        style.configure('TNotebook.Tab', padding=[10, 8])
        style.map('TNotebook.Tab', background=[('selected', self.colors["bg_tertiary"])])
    
    def _initialize_modules(self):
        """Initialize all backend modules with error handling"""
        try:
            self.user_profile = get_user_profile_manager()
            self.system_controller = SystemController()
            self.base_executor = CommandExecutor()
            
            try:
                self.executor = EnhancedCommandExecutor(self.base_executor)
                self.command_interceptor = CommandInterceptor(self.executor)
            except:
                self.executor = self.base_executor
            
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
            
            try:
                self.workflow_builder = create_nl_workflow_builder()
                self.workflow_manager = WorkflowManager()
            except:
                self.workflow_builder = None
            
            try:
                self.productivity_dashboard = ProductivityDashboard()
                self.pomodoro_coach = PomodoroAICoach()
            except:
                pass
            
            try:
                self.password_vault = PasswordVault()
                self.calendar = CalendarManager()
                self.notes = QuickNotes()
            except:
                pass
            
            print("✅ Modules initialized successfully")
        except Exception as e:
            print(f"❌ Module initialization error: {e}")
    
    def _create_gui(self):
        """Create enhanced modern GUI"""
        main_frame = tk.Frame(self.root, bg=self.colors["bg_primary"])
        main_frame.pack(fill="both", expand=True)
        
        # Header with enhanced styling
        self._create_header(main_frame)
        
        # Divider line
        divider1 = tk.Frame(main_frame, bg=self.colors["border_color"], height=1)
        divider1.pack(fill="x")
        
        # Main content area with two sections
        content_frame = tk.Frame(main_frame, bg=self.colors["bg_primary"])
        content_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Chat area
        chat_frame = tk.Frame(content_frame, bg=self.colors["bg_primary"])
        chat_frame.pack(fill="both", expand=True, padx=16, pady=16)
        
        self._create_chat_area(chat_frame)
        
        # Input section with divider
        divider2 = tk.Frame(main_frame, bg=self.colors["border_color"], height=1)
        divider2.pack(fill="x")
        
        self._create_input_section(main_frame)
        
        # Status bar
        self._create_status_bar(main_frame)
    
    def _create_header(self, parent):
        """Create premium header with branding and controls"""
        header = tk.Frame(parent, bg=self.colors["bg_secondary"], height=70)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)
        
        # Left side - Logo and title
        left_frame = tk.Frame(header, bg=self.colors["bg_secondary"])
        left_frame.pack(side="left", padx=20, pady=15)
        
        tk.Label(left_frame, text="🤖", bg=self.colors["bg_secondary"],
                fg=self.colors["accent_primary"], font=("Segoe UI", 20)).pack(side="left", padx=(0, 10))
        
        title_frame = tk.Frame(left_frame, bg=self.colors["bg_secondary"])
        title_frame.pack(side="left", fill="both")
        
        tk.Label(title_frame, text="V.A.T.S.A.L", bg=self.colors["bg_secondary"],
                fg=self.colors["text_primary"], font=("Segoe UI", 16, "bold")).pack(anchor="w")
        
        tk.Label(title_frame, text="AI Desktop Assistant", bg=self.colors["bg_secondary"],
                fg=self.colors["text_secondary"], font=("Segoe UI", 8)).pack(anchor="w")
        
        # Center - Status info
        center_frame = tk.Frame(header, bg=self.colors["bg_secondary"])
        center_frame.pack(side="left", expand=True, fill="x", padx=20)
        
        self.status_indicator = tk.Label(center_frame, text="● Online", bg=self.colors["bg_secondary"],
                                         fg=self.colors["success_green"], font=("Segoe UI", 9, "bold"))
        self.status_indicator.pack(anchor="w")
        
        # Right side - Time and controls
        right_frame = tk.Frame(header, bg=self.colors["bg_secondary"])
        right_frame.pack(side="right", padx=20, pady=15)
        
        self.time_label = tk.Label(right_frame, text="", bg=self.colors["bg_secondary"],
                                  fg=self.colors["text_secondary"], font=("Segoe UI", 9))
        self.time_label.pack(side="left", padx=(0, 15))
        
        # Control buttons
        btn_frame = tk.Frame(right_frame, bg=self.colors["bg_secondary"])
        btn_frame.pack(side="left")
        
        self._create_header_button(btn_frame, "⚙️", self.show_settings)
        self._create_header_button(btn_frame, "❓", self.show_help)
        self._create_header_button(btn_frame, "☰", self.show_menu)
    
    def _create_header_button(self, parent, text, command):
        """Create styled header button"""
        btn = tk.Button(parent, text=text, command=command,
                       bg=self.colors["bg_secondary"], fg=self.colors["text_primary"],
                       font=("Segoe UI", 11), relief="flat", bd=0,
                       padx=8, pady=2, cursor="hand2",
                       activebackground=self.colors["hover_color"],
                       activeforeground=self.colors["accent_primary"])
        btn.pack(side="left", padx=4)
        
        # Hover effect
        btn.bind("<Enter>", lambda e: btn.config(bg=self.colors["hover_color"]))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.colors["bg_secondary"]))
    
    def _create_chat_area(self, parent):
        """Create beautiful chat area with rounded corners effect"""
        # Chat container with border
        chat_container = tk.Frame(parent, bg=self.colors["bg_secondary"], relief="flat", bd=0)
        chat_container.pack(fill="both", expand=True)
        
        # Canvas with scrollbar
        self.chat_canvas = tk.Canvas(chat_container, bg=self.colors["bg_secondary"],
                                    highlightthickness=0, relief="flat", bd=0)
        scrollbar = ttk.Scrollbar(chat_container, orient="vertical", command=self.chat_canvas.yview)
        self.chat_scrollable = tk.Frame(self.chat_canvas, bg=self.colors["bg_secondary"])
        
        self.chat_scrollable.bind("<Configure>",
                                 lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")))
        self.chat_canvas.create_window((0, 0), window=self.chat_scrollable, anchor="nw", width=self.chat_canvas.winfo_width())
        self.chat_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.chat_canvas.pack(side="left", fill="both", expand=True, padx=0, pady=0)
        scrollbar.pack(side="right", fill="y", padx=0)
        
        self.chat_messages = []
        self.message_count = 0
    
    def _create_input_section(self, parent):
        """Create enhanced input section"""
        input_frame = tk.Frame(parent, bg=self.colors["bg_primary"])
        input_frame.pack(fill="x", padx=16, pady=16)
        
        # Input box with enhanced styling
        input_container = tk.Frame(input_frame, bg=self.colors["input_bg"], relief="flat", bd=1)
        input_container.pack(fill="x", pady=(0, 12))
        
        # Padding frame
        pad_frame = tk.Frame(input_container, bg=self.colors["input_bg"])
        pad_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Input field with icon
        input_inner = tk.Frame(pad_frame, bg=self.colors["input_bg"])
        input_inner.pack(fill="x")
        
        tk.Label(input_inner, text="✎", bg=self.colors["input_bg"],
                fg=self.colors["accent_primary"], font=("Segoe UI", 12)).pack(side="left", padx=10)
        
        self.input_field = tk.Entry(input_inner, bg=self.colors["input_bg"],
                                   fg=self.colors["text_primary"], font=("Segoe UI", 11),
                                   insertbackground=self.colors["accent_primary"],
                                   relief="flat", bd=0)
        self.input_field.pack(fill="both", expand=True, ipady=12, padx=5)
        self.input_field.bind("<Return>", lambda e: self.execute_command())
        self.input_field.bind("<Control-a>", lambda e: self.input_field.select_range(0, tk.END))
        
        # Clear button
        clear_btn = tk.Button(input_inner, text="✕", command=self.clear_input,
                             bg=self.colors["input_bg"], fg=self.colors["text_muted"],
                             font=("Segoe UI", 10), relief="flat", bd=0, padx=8,
                             cursor="hand2", activebackground=self.colors["hover_color"],
                             activeforeground=self.colors["accent_red"])
        clear_btn.pack(side="right", padx=5)
        
        # Control buttons row
        button_frame = tk.Frame(input_frame, bg=self.colors["bg_primary"])
        button_frame.pack(fill="x")
        
        # Send button
        send_btn = tk.Button(button_frame, text="▶ Send", command=self.execute_command,
                            bg=self.colors["accent_primary"], fg=self.colors["bg_primary"],
                            font=("Segoe UI", 10, "bold"), relief="flat", bd=0,
                            padx=24, pady=10, cursor="hand2",
                            activebackground=self.colors["accent_secondary"],
                            activeforeground=self.colors["bg_primary"])
        send_btn.pack(side="left", padx=4)
        send_btn.bind("<Enter>", lambda e: send_btn.config(bg=self.colors["accent_secondary"]))
        send_btn.bind("<Leave>", lambda e: send_btn.config(bg=self.colors["accent_primary"]))
        
        # Secondary buttons
        for icon, label, cmd in [("🎙️", "Voice", self.toggle_voice),
                                 ("⚡", "Auto", self.toggle_automation),
                                 ("🗑️", "Clear", self.clear_chat)]:
            btn = tk.Button(button_frame, text=f"{icon} {label}", command=cmd,
                           bg=self.colors["bg_secondary"], fg=self.colors["text_primary"],
                           font=("Segoe UI", 9), relief="flat", bd=0,
                           padx=12, pady=8, cursor="hand2",
                           activebackground=self.colors["hover_color"])
            btn.pack(side="left", padx=2)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.colors["hover_color"]))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.colors["bg_secondary"]))
    
    def _create_status_bar(self, parent):
        """Create status bar at bottom"""
        status_bar = tk.Frame(parent, bg=self.colors["bg_secondary"], height=40)
        status_bar.pack(fill="x", padx=0, pady=0)
        status_bar.pack_propagate(False)
        
        # Left status
        left_status = tk.Frame(status_bar, bg=self.colors["bg_secondary"])
        left_status.pack(side="left", padx=16, pady=8)
        
        tk.Label(left_status, text="Ready", bg=self.colors["bg_secondary"],
                fg=self.colors["text_secondary"], font=("Segoe UI", 8)).pack()
        
        # Right status
        right_status = tk.Frame(status_bar, bg=self.colors["bg_secondary"])
        right_status.pack(side="right", padx=16, pady=8)
        
        self.msg_count_label = tk.Label(right_status, text=f"Messages: 0", bg=self.colors["bg_secondary"],
                                        fg=self.colors["text_secondary"], font=("Segoe UI", 8))
        self.msg_count_label.pack()
    
    def add_message(self, text, sender="bot", timestamp=True):
        """Add message with enhanced styling"""
        self.message_count += 1
        self.msg_count_label.config(text=f"Messages: {self.message_count}")
        
        msg_container = tk.Frame(self.chat_scrollable, bg=self.colors["bg_secondary"])
        msg_container.pack(fill="x", padx=8, pady=10)
        
        # Create bubble
        if sender == "user":
            bubble_frame = tk.Frame(msg_container, bg=self.colors["user_bubble"], relief="flat")
            bubble_frame.pack(anchor="e", padx=40)
            icon = "👤"
        else:
            bubble_frame = tk.Frame(msg_container, bg=self.colors["bot_bubble"], relief="flat")
            bubble_frame.pack(anchor="w", padx=40)
            icon = "🤖"
        
        # Inner padding
        inner_frame = tk.Frame(bubble_frame, bg=bubble_frame["bg"])
        inner_frame.pack(fill="both", padx=14, pady=10)
        
        # Header with sender and time
        header_frame = tk.Frame(inner_frame, bg=bubble_frame["bg"])
        header_frame.pack(anchor="w", fill="x", pady=(0, 6))
        
        header_text = f"{icon} {'You' if sender == 'user' else 'BOI'}"
        if timestamp:
            header_text += f" · {datetime.now().strftime('%H:%M')}"
        
        tk.Label(header_frame, text=header_text, bg=bubble_frame["bg"],
                fg=self.colors["text_primary"], font=("Segoe UI", 8, "bold")).pack(anchor="w")
        
        # Message text
        tk.Label(inner_frame, text=text, bg=bubble_frame["bg"],
                fg=self.colors["text_primary"], font=("Segoe UI", 10),
                justify="left", wraplength=450).pack(anchor="w", fill="x")
        
        self.chat_messages.append((msg_container, text))
        self.chat_canvas.after(50, lambda: self.chat_canvas.yview_moveto(1.0))
    
    def add_typing_indicator(self):
        """Show typing indicator"""
        self.state["typing"] = True
        typing_container = tk.Frame(self.chat_scrollable, bg=self.colors["bg_secondary"])
        typing_container.pack(fill="x", padx=8, pady=10)
        
        bubble_frame = tk.Frame(typing_container, bg=self.colors["bot_bubble"], relief="flat")
        bubble_frame.pack(anchor="w", padx=40)
        
        inner_frame = tk.Frame(bubble_frame, bg=bubble_frame["bg"])
        inner_frame.pack(fill="both", padx=14, pady=10)
        
        tk.Label(inner_frame, text="🤖 BOI", bg=bubble_frame["bg"],
                fg=self.colors["text_primary"], font=("Segoe UI", 8, "bold")).pack(anchor="w")
        
        tk.Label(inner_frame, text="Thinking... ◐", bg=bubble_frame["bg"],
                fg=self.colors["text_secondary"], font=("Segoe UI", 9)).pack(anchor="w")
        
        self.typing_container = typing_container
        self.chat_canvas.yview_moveto(1.0)
    
    def remove_typing_indicator(self):
        """Remove typing indicator"""
        if hasattr(self, 'typing_container'):
            self.typing_container.destroy()
            self.state["typing"] = False
    
    def execute_command(self):
        """Execute command with async processing"""
        if self.state["processing"]:
            return
        
        user_input = self.input_field.get().strip()
        if not user_input:
            return
        
        self.input_field.delete(0, tk.END)
        self.add_message(user_input, sender="user")
        self.add_typing_indicator()
        
        self.state["processing"] = True
        
        def process():
            try:
                command_dict = parse_command(user_input)
                
                if command_dict.get("action") == "error":
                    response = "Unable to process command. Please try differently."
                else:
                    result = self.executor.execute(command_dict)
                    message = result.get('message', 'Command executed')
                    response = message
                
                self.root.after(0, lambda: self._add_bot_response(response))
            except Exception as e:
                self.root.after(0, lambda: self._add_bot_response(f"Error: {str(e)}"))
            finally:
                self.state["processing"] = False
        
        thread = threading.Thread(target=process, daemon=True)
        thread.start()
    
    def _add_bot_response(self, response):
        """Add bot response and remove typing indicator"""
        self.remove_typing_indicator()
        self.add_message(response, sender="bot")
    
    def toggle_voice(self):
        """Toggle voice input"""
        self.state["voice_enabled"] = not self.state["voice_enabled"]
        messagebox.showinfo("Voice", f"Voice: {'Enabled' if self.state['voice_enabled'] else 'Disabled'}")
    
    def toggle_automation(self):
        """Toggle automation"""
        self.state["self_operating_mode"] = not self.state["self_operating_mode"]
        messagebox.showinfo("Automation", f"Auto Mode: {'Enabled' if self.state['self_operating_mode'] else 'Disabled'}")
    
    def clear_input(self):
        """Clear input field"""
        self.input_field.delete(0, tk.END)
    
    def clear_chat(self):
        """Clear chat history"""
        for msg_frame, _ in self.chat_messages:
            msg_frame.destroy()
        self.chat_messages.clear()
        self.message_count = 0
        self.msg_count_label.config(text="Messages: 0")
    
    def handle_voice_command(self, command):
        """Handle voice input"""
        self.input_field.delete(0, tk.END)
        self.input_field.insert(0, command)
        self.execute_command()
    
    def show_settings(self):
        """Show settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ Settings")
        settings_window.geometry("550x650")
        settings_window.configure(bg=self.colors["bg_primary"])
        settings_window.resizable(False, False)
        
        notebook = ttk.Notebook(settings_window)
        notebook.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Voice tab
        voice_frame = tk.Frame(notebook, bg=self.colors["bg_secondary"])
        notebook.add(voice_frame, text="🎙️ Voice")
        self._populate_settings_tab(voice_frame, [
            ("Voice Recognition", "✅ Enabled"),
            ("Microphone Input", "✅ Active"),
            ("Sensitivity", "High"),
            ("Output Volume", "85%"),
            ("Language", "English"),
        ])
        
        # Automation tab
        auto_frame = tk.Frame(notebook, bg=self.colors["bg_secondary"])
        notebook.add(auto_frame, text="⚡ Automation")
        self._populate_settings_tab(auto_frame, [
            ("Self-Operating Mode", "✅ Enabled"),
            ("Gesture Recognition", "✅ Ready"),
            ("Macro Recording", "✅ Available"),
            ("Workflow Automation", "✅ Active"),
        ])
        
        # Display tab
        display_frame = tk.Frame(notebook, bg=self.colors["bg_secondary"])
        notebook.add(display_frame, text="🎨 Display")
        self._populate_settings_tab(display_frame, [
            ("Theme", "Dark Premium"),
            ("Font Size", "Normal"),
            ("Notifications", "✅ On"),
            ("Auto-scroll", "✅ On"),
        ])
    
    def _populate_settings_tab(self, parent, items):
        """Populate settings tab"""
        for label, value in items:
            item_frame = tk.Frame(parent, bg=self.colors["bg_secondary"])
            item_frame.pack(fill="x", padx=16, pady=12, border=1)
            
            tk.Label(item_frame, text=label, bg=self.colors["bg_secondary"],
                    fg=self.colors["text_primary"], font=("Segoe UI", 10, "bold")).pack(anchor="w")
            
            tk.Label(item_frame, text=value, bg=self.colors["bg_secondary"],
                    fg=self.colors["text_secondary"], font=("Segoe UI", 9)).pack(anchor="w", pady=(4, 0))
    
    def show_help(self):
        """Show help dialog"""
        help_window = tk.Toplevel(self.root)
        help_window.title("❓ Help & Commands")
        help_window.geometry("600x700")
        help_window.configure(bg=self.colors["bg_primary"])
        
        # Close button
        close_btn = tk.Button(help_window, text="Close", command=help_window.destroy,
                             bg=self.colors["accent_primary"], fg=self.colors["bg_primary"],
                             font=("Segoe UI", 9, "bold"), relief="flat", bd=0, pady=8)
        close_btn.pack(side="bottom", fill="x", padx=16, pady=16)
        
        help_text = """
        🤖 V.A.T.S.A.L - AI DESKTOP ASSISTANT

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        📝 BASIC COMMANDS:
        
        • "Take screenshot" - Capture screen
        • "Show system report" - System info
        • "Check CPU usage" - CPU metrics
        • "List files" - Directory listing
        • "Analyze image.png" - Vision analysis
        
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        🎤 VOICE COMMANDS:
        
        Use microphone to give commands
        Say "Wake up" to activate
        
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        ⚡ FEATURES:
        
        🎙️ Voice Control & Recognition
        👁️ Screenshot Analysis
        ⚡ Automation & Workflows
        📊 Productivity Tracking
        🔒 Security Monitoring
        📱 Phone Integration
        🤖 Self-Operating Mode
        
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        💡 Type "help" for more options
        """
        
        text_label = tk.Label(help_window, text=help_text, bg=self.colors["bg_secondary"],
                             fg=self.colors["text_secondary"], font=("Courier New", 9),
                             justify="left", wraplength=560)
        text_label.pack(anchor="nw", fill="both", expand=True, padx=16, pady=16)
    
    def show_menu(self):
        """Show menu dialog"""
        menu_window = tk.Toplevel(self.root)
        menu_window.title("Menu")
        menu_window.geometry("400x350")
        menu_window.configure(bg=self.colors["bg_primary"])
        menu_window.resizable(False, False)
        
        menu_items = [
            ("📊 Productivity Dashboard", None),
            ("🔒 Security Monitor", None),
            ("📁 File Manager", None),
            ("⌨️ Keyboard Controls", None),
            ("🌐 Network Tools", None),
            ("📞 Phone Link", None),
            ("🔧 System Utilities", None),
            ("❌ Exit", menu_window.destroy)
        ]
        
        for label, cmd in menu_items:
            btn = tk.Button(menu_window, text=label, command=cmd or (lambda: None),
                           bg=self.colors["bg_secondary"], fg=self.colors["text_primary"],
                           font=("Segoe UI", 10), relief="flat", bd=0,
                           padx=16, pady=12, cursor="hand2",
                           activebackground=self.colors["hover_color"])
            btn.pack(fill="x", padx=16, pady=6)
    
    def _show_welcome(self):
        """Show welcome message"""
        welcome = "👋 Welcome to V.A.T.S.A.L!\n\n🎯 I'm your AI Desktop Assistant.\n\n💡 Try: 'Take screenshot' or 'Show system report'"
        self.add_message(welcome, sender="bot", timestamp=False)
    
    def _update_time(self):
        """Update time and status"""
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%a, %b %d")
        self.time_label.config(text=f"{date_str} • {time_str}")
        self.root.after(1000, self._update_time)
    
    def _start_background_tasks(self):
        """Start background tasks"""
        self._update_time()


def main():
    """Entry point"""
    root = tk.Tk()
    app = EnhancedChatGPTGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
