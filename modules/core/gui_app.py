import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image, ImageTk

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
from modules.automation.vatsal_desktop_automator import VATSALAutomator
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

load_dotenv()


class ModernVATSALGUI:
    """Clean, modern VATSAL GUI matching web interface design"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("V.A.T.S.A.L - AI Desktop Assistant")
        
        # Initialize theme colors (exact match to web GUI CSS)
        self.BG_PRIMARY = "#F5F1E8"      # var(--bg-primary)
        self.BG_SECONDARY = "#FAF8F3"    # var(--bg-secondary)
        self.BORDER_PRIMARY = "#D9CFC0"  # var(--border-color)
        self.TEXT_PRIMARY = "#1a1a1a"    # var(--text-primary)
        self.TEXT_SECONDARY = "#5a5a5a"  # var(--text-secondary)
        self.ACCENT_COLOR = "#3a3a3a"    # var(--accent-color)
        self.BUTTON_BG = "#F3EADA"       # var(--button-bg)
        self.BUTTON_HOVER = "#E8DCCB"    # var(--button-hover)
        self.ACTIVE_GREEN = "#007B55"    # var(--active-green)
        self.CONSOLE_BG = "#FAF6EE"      # var(--console-bg)
        self.SHADOW_COLOR = "rgba(0, 0, 0, 0.08)"  # var(--shadow)
        
        # Configure root window
        self.root.configure(bg=self.BG_PRIMARY)
        self.root.geometry("1200x900")
        
        # Set window icon
        self._set_window_icon()
        
        # State variables
        self.processing = False
        self.vatsal_mode = True
        self.self_operating_mode = True  # Default to ON to match web GUI
        self.voice_enabled = False
        self.wakeup_listening = False
        self.vsign_detecting = False
        self.speaking_enabled = False
        
        # Initialize core modules
        self._initialize_modules()
        
        # Build GUI
        self._create_gui()
        
        # Start time updates
        self._update_time()
        
        # Show welcome message
        self._show_welcome()
    
    def _set_window_icon(self):
        """Set the window icon from logo file"""
        try:
            # Get the workspace directory
            workspace_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            # Try icon version first (smaller, better for window icons)
            icon_path = os.path.join(workspace_dir, "assets", "vatsal_icon.png")
            if not os.path.exists(icon_path):
                icon_path = os.path.join(workspace_dir, "assets", "vatsal_logo.png")
            
            if os.path.exists(icon_path):
                # Load and resize for icon if needed
                icon_image = Image.open(icon_path)
                
                # Resize if too large (icons work best at 64x64 or smaller)
                if icon_image.size[0] > 256 or icon_image.size[1] > 256:
                    icon_image = icon_image.resize((64, 64), Image.Resampling.LANCZOS)
                
                # Keep as instance variable to prevent garbage collection
                self.icon_photo = ImageTk.PhotoImage(icon_image)
                self.root.iconphoto(True, self.icon_photo)
                print(f"✅ Window icon loaded from: {icon_path}")
            else:
                print(f"⚠️ Logo file not found")
        except Exception as e:
            print(f"⚠️ Could not set window icon: {e}")
            import traceback
            traceback.print_exc()
    
    def _initialize_modules(self):
        """Initialize all backend modules"""
        try:
            # User profile manager
            self.user_profile = get_user_profile_manager()
            
            # System controller
            self.system_controller = SystemController()
            
            # Base executor
            self.base_executor = CommandExecutor()
            
            # Enhanced executor with self-operating integration
            try:
                self.executor = EnhancedCommandExecutor(self.base_executor)
                self.command_interceptor = CommandInterceptor(self.executor)
                print("✅ Enhanced Command Executor initialized")
            except Exception as e:
                self.executor = self.base_executor
                self.command_interceptor = None
                print(f"⚠️ Using base executor: {e}")
            
            # Core AI modules
            self.vatsal = create_vatsal_assistant()
            self.advanced_monitor = create_advanced_smart_screen_monitor()
            self.ai_monitor = create_ai_screen_monitoring_system()
            self.file_automation = create_file_automation()
            self.clipboard_handler = ClipboardTextHandler()
            self.smart_automation = SmartAutomationManager()
            self.desktop_controller = DesktopFileController()
            
            # Comprehensive desktop controller
            try:
                self.comprehensive_controller = ComprehensiveDesktopController()
            except Exception as e:
                self.comprehensive_controller = None
                print(f"⚠️ Comprehensive controller unavailable: {e}")
            
            # Chatbot
            try:
                self.simple_chatbot = SimpleChatbot()
            except Exception as e:
                self.simple_chatbot = None
            
            # Web automator
            try:
                self.web_automator = SeleniumWebAutomator()
            except Exception as e:
                self.web_automator = None
                print(f"⚠️ Web automator unavailable: {e}")
            
            # Virtual Language Model
            try:
                gui_automation = GUIAutomation()
                self.vlm = VirtualLanguageModel(gui_automation)
                self.vlm_last_decision = None
            except Exception as e:
                self.vlm = None
                self.vlm_last_decision = None
                print(f"⚠️ VLM unavailable: {e}")
            
            # VATSAL Automator
            try:
                self.vatsal_automator = VATSALAutomator()
            except Exception as e:
                self.vatsal_automator = None
                print(f"⚠️ VATSAL Automator unavailable: {e}")
            
            # Self-Operating Computer
            try:
                self.self_operating_computer = SelfOperatingComputer(verbose=True)
                self.soc_running = False
                self.soc_thread = None
            except Exception as e:
                self.self_operating_computer = None
                self.soc_running = False
                self.soc_thread = None
                print(f"⚠️ Self-Operating Computer unavailable: {e}")
            
            # Self-Operating Integration Hub
            try:
                self.integration_hub = SelfOperatingIntegrationHub()
                self.task_router = SmartTaskRouter(self.integration_hub)
            except Exception as e:
                self.integration_hub = None
                self.task_router = None
                print(f"⚠️ Integration hub unavailable: {e}")
            
            # WebSocket client
            try:
                self.ws_client = get_websocket_client()
                self.ws_client.connect()
                print("✅ WebSocket client connected")
            except Exception as e:
                self.ws_client = None
                print(f"⚠️ WebSocket unavailable: {e}")
            
            # Voice commander
            try:
                self.voice_commander = create_voice_commander(command_callback=self.handle_voice_command)
                self.voice_listening = False
            except Exception as e:
                self.voice_commander = None
                self.voice_listening = False
                print(f"⚠️ Voice commander unavailable: {e}")
            
            # Gesture voice activator
            try:
                self.gesture_voice_activator = create_gesture_voice_activator(
                    on_speech_callback=self.handle_voice_command
                )
                self.gesture_voice_active = False
            except Exception as e:
                self.gesture_voice_activator = None
                self.gesture_voice_active = False
                print(f"⚠️ Gesture voice activator unavailable: {e}")
            
            # Hand gesture detector
            try:
                self.gesture_assistant = OpenCVHandGestureDetector(voice_commander=self.voice_commander)
                self.gesture_running = False
                self.gesture_detector_type = "OpenCV"
            except Exception as e:
                self.gesture_assistant = None
                self.gesture_running = False
                self.gesture_detector_type = None
                print(f"⚠️ Gesture detector unavailable: {e}")
            
            # Macro recorder
            try:
                self.macro_recorder = MacroRecorder()
                self.macro_templates = MacroTemplates()
            except Exception as e:
                self.macro_recorder = None
                self.macro_templates = None
                print(f"⚠️ Macro recorder unavailable: {e}")
            
            # Workflow builder
            try:
                self.workflow_builder = create_nl_workflow_builder()
                self.workflow_manager = WorkflowManager()
            except Exception as e:
                self.workflow_builder = None
                self.workflow_manager = None
                print(f"⚠️ Workflow builder unavailable: {e}")
            
            # Productivity modules
            try:
                self.productivity_dashboard = ProductivityDashboard()
                self.pomodoro_coach = PomodoroAICoach()
                self.task_predictor = TaskTimePredictor()
                self.energy_tracker = EnergyLevelTracker()
                self.distraction_detector = DistractionDetector()
                self.productivity_monitor = ProductivityMonitor()
                self.break_suggester = SmartBreakSuggester()
            except Exception as e:
                print(f"⚠️ Productivity modules unavailable: {e}")
            
            # Utility modules
            try:
                self.password_vault = PasswordVault()
                self.calendar = CalendarManager()
                self.notes = QuickNotes()
                self.weather_news = WeatherNewsService()
                self.translator = TranslationService()
            except Exception as e:
                print(f"⚠️ Utility modules unavailable: {e}")
            
            # Security dashboard
            try:
                self.security_dashboard = SecurityDashboard()
            except Exception as e:
                self.security_dashboard = None
                print(f"⚠️ Security dashboard unavailable: {e}")
            
            # Desktop sync manager
            try:
                auto_initialize_on_gui_start()
                self.desktop_sync_manager = DesktopSyncManager()
            except Exception as e:
                self.desktop_sync_manager = None
                print(f"⚠️ Desktop sync manager unavailable: {e}")
                
        except Exception as e:
            print(f"❌ Error initializing modules: {e}")
            messagebox.showerror("Initialization Error", f"Failed to initialize: {e}")
    
    def _create_gui(self):
        """Create the main GUI layout matching web design"""
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.BG_PRIMARY)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header section
        self._create_header(main_container)
        
        # Command input section
        self._create_command_section(main_container)
        
        # Output console section
        self._create_output_section(main_container)
    
    def create_rounded_button(self, parent, text, command, bg_color=None, fg_color=None, width=None, height=None):
        """Create a button with 3D effect and layered shadows"""
        if bg_color is None:
            bg_color = self.BUTTON_BG
        if fg_color is None:
            fg_color = self.TEXT_PRIMARY
        
        # Outer shadow container (multiple shadows for depth)
        outer_shadow = tk.Frame(parent, bg="#B8B8B8", bd=0)
        
        # Mid shadow layer
        mid_shadow = tk.Frame(outer_shadow, bg="#CACACA", bd=0)
        mid_shadow.pack(padx=(0, 4), pady=(0, 4))
        
        # Inner shadow layer
        inner_shadow = tk.Frame(mid_shadow, bg="#D8D8D8", bd=0)
        inner_shadow.pack(padx=(0, 2), pady=(0, 2))
        
        # Button container with highlight border for 3D effect
        btn_container = tk.Frame(
            inner_shadow, 
            bg=bg_color, 
            bd=1,
            relief="raised",
            highlightthickness=1,
            highlightbackground="#FFFFFF",
            highlightcolor="#FFFFFF"
        )
        btn_container.pack()
        
        # Actual button with gradient-like appearance
        btn = tk.Button(
            btn_container,
            text=text,
            command=command,
            bg=bg_color,
            fg=fg_color,
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            activebackground=self.BUTTON_HOVER,
            activeforeground=fg_color
        )
        
        if width:
            btn.config(width=width)
        if height:
            btn.config(height=height)
        
        btn.pack()
        
        # Enhanced hover effects with 3D lift
        def on_enter(e):
            if btn['bg'] != self.ACTIVE_GREEN:
                btn.config(bg=self.BUTTON_HOVER)
                mid_shadow.pack_configure(padx=(0, 5), pady=(0, 5))
                btn_container.config(relief="raised", bd=2)
        
        def on_leave(e):
            if btn['bg'] != self.ACTIVE_GREEN:
                btn.config(bg=bg_color)
                mid_shadow.pack_configure(padx=(0, 4), pady=(0, 4))
                btn_container.config(relief="raised", bd=1)
        
        def on_press(e):
            mid_shadow.pack_configure(padx=(0, 1), pady=(0, 1))
            btn_container.config(relief="sunken", bd=1)
        
        def on_release(e):
            mid_shadow.pack_configure(padx=(0, 4), pady=(0, 4))
            btn_container.config(relief="raised", bd=1)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<ButtonPress-1>", on_press)
        btn.bind("<ButtonRelease-1>", on_release)
        
        return outer_shadow, btn
    
    def _create_header(self, parent):
        """Create header with title and status bar"""
        header = tk.Frame(
            parent,
            bg=self.BG_SECONDARY,
            relief="solid",
            borderwidth=2,
            highlightbackground=self.BORDER_PRIMARY,
            highlightthickness=0
        )
        header.pack(fill="x", pady=(0, 20))
        
        # Title section - REDUCED PADDING
        title_section = tk.Frame(header, bg=self.BG_SECONDARY)
        title_section.pack(fill="x", padx=30, pady=(20, 10))
        
        # Main title with sparkles - SMALLER SIZE
        title_frame = tk.Frame(title_section, bg=self.BG_SECONDARY)
        title_frame.pack()
        
        # Add logo image to the left of title
        try:
            workspace_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            logo_path = os.path.join(workspace_dir, "assets", "vatsal_icon.png")
            if not os.path.exists(logo_path):
                logo_path = os.path.join(workspace_dir, "assets", "vatsal_logo.png")
            
            if os.path.exists(logo_path):
                logo_img = Image.open(logo_path)
                logo_img = logo_img.resize((50, 50), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_img)
                tk.Label(
                    title_frame,
                    image=self.logo_photo,
                    bg=self.BG_SECONDARY
                ).pack(side="left", padx=(0, 20))
        except Exception as e:
            print(f"Could not load logo in header: {e}")
        
        tk.Label(
            title_frame,
            text="✨",
            font=("Segoe UI", 22),
            bg=self.BG_SECONDARY,
            fg=self.TEXT_PRIMARY
        ).pack(side="left", padx=(0, 15))
        
        tk.Label(
            title_frame,
            text="V.A.T.S.A.L",
            font=("Georgia", 42, "bold"),
            bg=self.BG_SECONDARY,
            fg=self.TEXT_PRIMARY,
            anchor="center"
        ).pack(side="left")
        
        tk.Label(
            title_frame,
            text="✨",
            font=("Segoe UI", 22),
            bg=self.BG_SECONDARY,
            fg=self.TEXT_PRIMARY
        ).pack(side="left", padx=(15, 0))
        
        # Subtitle - SMALLER
        tk.Label(
            title_section,
            text="Vastly Advanced Technological System Above Limitations",
            font=("Georgia", 12, "italic"),
            bg=self.BG_SECONDARY,
            fg=self.TEXT_SECONDARY
        ).pack(pady=(5, 0))
        
        # Status bar - REDUCED PADDING
        status_bar = tk.Frame(
            header,
            bg=self.BG_SECONDARY,
            relief="flat",
            borderwidth=1,
            highlightbackground=self.BORDER_PRIMARY
        )
        status_bar.pack(fill="x", padx=30, pady=(15, 20))
        
        # Left side - Date and time
        left_status = tk.Frame(status_bar, bg=self.BG_SECONDARY)
        left_status.pack(side="left", pady=(20, 0))
        
        self.time_label = tk.Label(
            left_status,
            text="",
            font=("Segoe UI", 11),
            bg=self.BG_SECONDARY,
            fg=self.TEXT_SECONDARY
        )
        self.time_label.pack(side="left")
        
        tk.Label(
            left_status,
            text=" • ",
            font=("Segoe UI", 11),
            bg=self.BG_SECONDARY,
            fg=self.ACCENT_COLOR
        ).pack(side="left")
        
        tk.Label(
            left_status,
            text="100+ AI Features Available",
            font=("Segoe UI", 11),
            bg=self.BG_SECONDARY,
            fg=self.TEXT_SECONDARY
        ).pack(side="left")
        
        # Right side - Status toggles
        toggles_frame = tk.Frame(status_bar, bg=self.BG_SECONDARY)
        toggles_frame.pack(side="right", pady=(20, 0))
        
        # VATSAL toggle with 3D shadow effect
        vatsal_shadow_outer = tk.Frame(toggles_frame, bg="#B8B8B8", bd=0)
        vatsal_shadow_outer.pack(side="left", padx=(2, 12), pady=2)
        
        vatsal_shadow_mid = tk.Frame(vatsal_shadow_outer, bg="#CACACA", bd=0)
        vatsal_shadow_mid.pack(padx=(0, 3), pady=(0, 3))
        
        vatsal_container = tk.Frame(
            vatsal_shadow_mid,
            bg=self.BG_SECONDARY,
            relief="raised",
            borderwidth=2,
            highlightthickness=1,
            highlightbackground=self.BORDER_PRIMARY,
            highlightcolor=self.BORDER_PRIMARY
        )
        vatsal_container.pack()
        
        self.vatsal_toggle = tk.Button(
            vatsal_container,
            text="● VATSAL: ON",
            font=("Segoe UI", 10, "bold"),
            bg=self.BG_SECONDARY,
            fg=self.ACTIVE_GREEN,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.toggle_vatsal,
            activebackground=self.BUTTON_HOVER
        )
        self.vatsal_toggle.pack()
        
        # 3D hover effect
        def vatsal_hover_enter(e):
            vatsal_shadow_mid.pack_configure(padx=(0, 4), pady=(0, 4))
            vatsal_container.config(relief="raised", borderwidth=3)
        
        def vatsal_hover_leave(e):
            vatsal_shadow_mid.pack_configure(padx=(0, 3), pady=(0, 3))
            vatsal_container.config(relief="raised", borderwidth=2)
        
        def vatsal_press(e):
            vatsal_shadow_mid.pack_configure(padx=(0, 1), pady=(0, 1))
            vatsal_container.config(relief="sunken")
        
        def vatsal_release(e):
            vatsal_shadow_mid.pack_configure(padx=(0, 3), pady=(0, 3))
            vatsal_container.config(relief="raised")
        
        self.vatsal_toggle.bind("<Enter>", vatsal_hover_enter)
        self.vatsal_toggle.bind("<Leave>", vatsal_hover_leave)
        self.vatsal_toggle.bind("<ButtonPress-1>", vatsal_press)
        self.vatsal_toggle.bind("<ButtonRelease-1>", vatsal_release)
        
        # Self-Operating toggle with 3D shadow effect
        soc_shadow_outer = tk.Frame(toggles_frame, bg="#B8B8B8", bd=0)
        soc_shadow_outer.pack(side="left", padx=2, pady=2)
        
        soc_shadow_mid = tk.Frame(soc_shadow_outer, bg="#CACACA", bd=0)
        soc_shadow_mid.pack(padx=(0, 3), pady=(0, 3))
        
        soc_container = tk.Frame(
            soc_shadow_mid,
            bg=self.BG_SECONDARY,
            relief="raised",
            borderwidth=2,
            highlightthickness=1,
            highlightbackground=self.BORDER_PRIMARY,
            highlightcolor=self.BORDER_PRIMARY
        )
        soc_container.pack()
        
        self.soc_toggle = tk.Button(
            soc_container,
            text="🔲 Self-Operating: ON",
            font=("Segoe UI", 10, "bold"),
            bg=self.BG_SECONDARY,
            fg=self.ACTIVE_GREEN,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.toggle_self_operating,
            activebackground=self.BUTTON_HOVER
        )
        self.soc_toggle.pack()
        
        # 3D hover effect
        def soc_hover_enter(e):
            soc_shadow_mid.pack_configure(padx=(0, 4), pady=(0, 4))
            soc_container.config(relief="raised", borderwidth=3)
        
        def soc_hover_leave(e):
            soc_shadow_mid.pack_configure(padx=(0, 3), pady=(0, 3))
            soc_container.config(relief="raised", borderwidth=2)
        
        def soc_press(e):
            soc_shadow_mid.pack_configure(padx=(0, 1), pady=(0, 1))
            soc_container.config(relief="sunken")
        
        def soc_release(e):
            soc_shadow_mid.pack_configure(padx=(0, 3), pady=(0, 3))
            soc_container.config(relief="raised")
        
        self.soc_toggle.bind("<Enter>", soc_hover_enter)
        self.soc_toggle.bind("<Leave>", soc_hover_leave)
        self.soc_toggle.bind("<ButtonPress-1>", soc_press)
        self.soc_toggle.bind("<ButtonRelease-1>", soc_release)
    
    def _create_command_section(self, parent):
        """Create command input section"""
        section = tk.Frame(
            parent,
            bg=self.BG_SECONDARY,
            relief="solid",
            borderwidth=2,
            highlightbackground=self.BORDER_PRIMARY
        )
        section.pack(fill="x", pady=(0, 20))
        
        # Section header
        header = tk.Frame(section, bg=self.BG_SECONDARY)
        header.pack(fill="x", padx=25, pady=(25, 20))
        
        tk.Label(
            header,
            text="➕",
            font=("Segoe UI", 16),
            bg=self.BG_SECONDARY,
            fg=self.TEXT_PRIMARY
        ).pack(side="left", padx=(0, 10))
        
        tk.Label(
            header,
            text="Command Input",
            font=("Segoe UI", 15, "bold"),
            bg=self.BG_SECONDARY,
            fg=self.TEXT_PRIMARY
        ).pack(side="left")
        
        # Input area
        input_area = tk.Frame(section, bg=self.BG_SECONDARY)
        input_area.pack(fill="x", padx=25, pady=(0, 25))
        
        # Command input
        self.command_input = tk.Entry(
            input_area,
            bg=self.CONSOLE_BG,
            fg=self.TEXT_PRIMARY,
            font=("Segoe UI", 11),
            insertbackground=self.TEXT_PRIMARY,
            relief="flat",
            borderwidth=0,
            highlightbackground=self.BORDER_PRIMARY,
            highlightcolor=self.ACCENT_COLOR,
            highlightthickness=2
        )
        self.command_input.pack(side="left", fill="both", expand=True, ipady=14, padx=(0, 15))
        self.command_input.bind("<Return>", lambda e: self.execute_command())
        
        # Buttons container with 3D shadow
        btn_group_shadow_outer = tk.Frame(input_area, bg="#B8B8B8", bd=0)
        btn_group_shadow_outer.pack(side="left")
        
        btn_group_shadow_mid = tk.Frame(btn_group_shadow_outer, bg="#CACACA", bd=0)
        btn_group_shadow_mid.pack(padx=(0, 4), pady=(0, 4))
        
        buttons_container = tk.Frame(
            btn_group_shadow_mid,
            bg=self.BUTTON_BG,
            relief="raised",
            borderwidth=2,
            highlightbackground=self.BORDER_PRIMARY,
            highlightthickness=1,
            highlightcolor="#FFFFFF"
        )
        buttons_container.pack()
        
        # Execute button with 3D effect
        self.execute_btn = tk.Button(
            buttons_container,
            text="▶ Execute",
            font=("Segoe UI", 11, "bold"),
            bg=self.BUTTON_BG,
            fg=self.TEXT_PRIMARY,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            padx=28,
            pady=14,
            command=self.execute_command,
            highlightthickness=0,
            activebackground=self.BUTTON_HOVER
        )
        self.execute_btn.pack(side="left", padx=2, pady=2)
        
        # 3D press effect for execute button
        def exec_press(e):
            self.execute_btn.config(relief="sunken")
        
        def exec_release(e):
            self.execute_btn.config(relief="flat")
        
        self.execute_btn.bind("<ButtonPress-1>", exec_press)
        self.execute_btn.bind("<ButtonRelease-1>", exec_release)
        self._add_hover_effect(self.execute_btn, self.BUTTON_BG, self.BUTTON_HOVER)
        
        # Separator
        tk.Frame(
            buttons_container,
            bg=self.BORDER_PRIMARY,
            width=2
        ).pack(side="left", fill="y")
        
        # Icon buttons - Wakeup listener, V-sign detector, Speaking
        icon_buttons = [
            ("👂", self.toggle_wakeup_listener, "Wakeup Word Listener"),
            ("✌️", self.toggle_v_sign_detector, "V-Sign Detector"),
            ("🗣️", self.toggle_speaking, "Speaking")
        ]
        
        for icon, command, tooltip in icon_buttons:
            btn = tk.Button(
                buttons_container,
                text=icon,
                font=("Segoe UI", 16),
                bg=self.BUTTON_BG,
                fg=self.TEXT_PRIMARY,
                relief="raised",
                borderwidth=1,
                cursor="hand2",
                width=3,
                command=command,
                highlightthickness=0,
                activebackground=self.BUTTON_HOVER
            )
            btn.pack(side="left", padx=2, pady=2)
            
            # 3D press effect
            def make_press_handler(button):
                def on_press(e):
                    button.config(relief="sunken")
                return on_press
            
            def make_release_handler(button):
                def on_release(e):
                    button.config(relief="raised")
                return on_release
            
            btn.bind("<ButtonPress-1>", make_press_handler(btn))
            btn.bind("<ButtonRelease-1>", make_release_handler(btn))
            self._add_hover_effect(btn, self.BUTTON_BG, self.BUTTON_HOVER)
            
            # Store button reference for state updates
            if icon == "👂":
                self.wakeup_btn = btn
            elif icon == "✌️":
                self.vsign_btn = btn
            elif icon == "🗣️":
                self.speaking_btn = btn
            
            # Separator
            if icon != icon_buttons[-1][0]:
                tk.Frame(
                    buttons_container,
                    bg=self.BORDER_PRIMARY,
                    width=2
                ).pack(side="left", fill="y")
    
    def _create_output_section(self, parent):
        """Create output console section"""
        section = tk.Frame(
            parent,
            bg=self.BG_SECONDARY,
            relief="solid",
            borderwidth=2,
            highlightbackground=self.BORDER_PRIMARY
        )
        section.pack(fill="both", expand=True)
        
        # Section header
        header = tk.Frame(section, bg=self.BG_SECONDARY)
        header.pack(fill="x", padx=25, pady=(25, 20))
        
        # Left side
        header_left = tk.Frame(header, bg=self.BG_SECONDARY)
        header_left.pack(side="left")
        
        tk.Label(
            header_left,
            text="📋",
            font=("Segoe UI", 16),
            bg=self.BG_SECONDARY,
            fg=self.TEXT_PRIMARY
        ).pack(side="left", padx=(0, 10))
        
        tk.Label(
            header_left,
            text="Output Console",
            font=("Segoe UI", 15, "bold"),
            bg=self.BG_SECONDARY,
            fg=self.TEXT_PRIMARY
        ).pack(side="left")
        
        # Clear button (top) with 3D shadow
        clear_shadow_outer = tk.Frame(header, bg="#B8B8B8", bd=0)
        clear_shadow_outer.pack(side="right", padx=2, pady=2)
        
        clear_shadow_mid = tk.Frame(clear_shadow_outer, bg="#CACACA", bd=0)
        clear_shadow_mid.pack(padx=(0, 3), pady=(0, 3))
        
        clear_container = tk.Frame(
            clear_shadow_mid,
            bg=self.BUTTON_BG,
            relief="raised",
            borderwidth=2,
            highlightthickness=1,
            highlightbackground=self.BORDER_PRIMARY,
            highlightcolor=self.BORDER_PRIMARY
        )
        clear_container.pack()
        
        clear_btn = tk.Button(
            clear_container,
            text="■ Clear",
            font=("Segoe UI", 10, "bold"),
            bg=self.BUTTON_BG,
            fg=self.TEXT_PRIMARY,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.clear_output,
            activebackground=self.BUTTON_HOVER
        )
        clear_btn.pack()
        
        # 3D hover effect
        def clear_hover_enter(e):
            clear_shadow_mid.pack_configure(padx=(0, 4), pady=(0, 4))
            clear_container.config(relief="raised", borderwidth=3)
        
        def clear_hover_leave(e):
            clear_shadow_mid.pack_configure(padx=(0, 3), pady=(0, 3))
            clear_container.config(relief="raised", borderwidth=2)
        
        def clear_press(e):
            clear_shadow_mid.pack_configure(padx=(0, 1), pady=(0, 1))
            clear_container.config(relief="sunken")
        
        def clear_release(e):
            clear_shadow_mid.pack_configure(padx=(0, 3), pady=(0, 3))
            clear_container.config(relief="raised")
        
        clear_btn.bind("<Enter>", clear_hover_enter)
        clear_btn.bind("<Leave>", clear_hover_leave)
        clear_btn.bind("<ButtonPress-1>", clear_press)
        clear_btn.bind("<ButtonRelease-1>", clear_release)
        self._add_hover_effect(clear_btn, self.BUTTON_BG, self.BUTTON_HOVER)
        
        # Output console
        console_frame = tk.Frame(section, bg=self.BG_SECONDARY)
        console_frame.pack(fill="both", expand=True, padx=25, pady=(0, 15))
        
        self.output_area = scrolledtext.ScrolledText(
            console_frame,
            bg=self.CONSOLE_BG,
            fg=self.TEXT_PRIMARY,
            font=("Segoe UI", 10),
            relief="solid",
            borderwidth=1,
            highlightbackground=self.BORDER_PRIMARY,
            highlightthickness=1,
            padx=24,
            pady=24,
            wrap="word",
            insertbackground=self.TEXT_PRIMARY
        )
        self.output_area.pack(fill="both", expand=True)
        self.output_area.config(state="disabled")
        
        # Footer with clear button
        footer = tk.Frame(section, bg=self.BG_SECONDARY)
        footer.pack(fill="x", padx=25, pady=(0, 25))
        
        # Clear button (bottom) with 3D shadow
        clear_b_shadow_outer = tk.Frame(footer, bg="#B8B8B8", bd=0)
        clear_b_shadow_outer.pack(side="right", padx=2, pady=2)
        
        clear_b_shadow_mid = tk.Frame(clear_b_shadow_outer, bg="#CACACA", bd=0)
        clear_b_shadow_mid.pack(padx=(0, 3), pady=(0, 3))
        
        clear_b_container = tk.Frame(
            clear_b_shadow_mid,
            bg=self.BUTTON_BG,
            relief="raised",
            borderwidth=2,
            highlightthickness=1,
            highlightbackground=self.BORDER_PRIMARY,
            highlightcolor=self.BORDER_PRIMARY
        )
        clear_b_container.pack()
        
        clear_btn_bottom = tk.Button(
            clear_b_container,
            text="■ Clear",
            font=("Segoe UI", 10, "bold"),
            bg=self.BUTTON_BG,
            fg=self.TEXT_PRIMARY,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.clear_output,
            activebackground=self.BUTTON_HOVER
        )
        clear_btn_bottom.pack()
        
        # 3D hover effect
        def clear_b_hover_enter(e):
            clear_b_shadow_mid.pack_configure(padx=(0, 4), pady=(0, 4))
            clear_b_container.config(relief="raised", borderwidth=3)
        
        def clear_b_hover_leave(e):
            clear_b_shadow_mid.pack_configure(padx=(0, 3), pady=(0, 3))
            clear_b_container.config(relief="raised", borderwidth=2)
        
        def clear_b_press(e):
            clear_b_shadow_mid.pack_configure(padx=(0, 1), pady=(0, 1))
            clear_b_container.config(relief="sunken")
        
        def clear_b_release(e):
            clear_b_shadow_mid.pack_configure(padx=(0, 3), pady=(0, 3))
            clear_b_container.config(relief="raised")
        
        clear_btn_bottom.bind("<Enter>", clear_b_hover_enter)
        clear_btn_bottom.bind("<Leave>", clear_b_hover_leave)
        clear_btn_bottom.bind("<ButtonPress-1>", clear_b_press)
        clear_btn_bottom.bind("<ButtonRelease-1>", clear_b_release)
        self._add_hover_effect(clear_btn_bottom, self.BUTTON_BG, self.BUTTON_HOVER)
    
    def _add_hover_effect(self, button, normal_color, hover_color):
        """Add hover effect to button"""
        def on_enter(e):
            button['background'] = hover_color
        
        def on_leave(e):
            button['background'] = normal_color
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def _update_time(self):
        """Update time display"""
        current_time = datetime.now().strftime("%A, %B %d, %Y • %I:%M:%S %p")
        self.time_label.config(text=current_time)
        self.root.after(1000, self._update_time)
    
    def _show_welcome(self):
        """Show welcome message"""
        api_key = os.getenv("GEMINI_API_KEY")
        
        if api_key:
            self.update_output("✅ Gemini AI is ready!\n", "success")
            if self.vatsal and self.vatsal_mode:
                greeting = self.vatsal.get_greeting()
                self.update_output(f"\n🤖 VATSAL: {greeting}\n", "info")
            self.update_output("\nType a command or click a button to get started.\n", "info")
        else:
            self.update_output("⚠️ WARNING: GEMINI_API_KEY not found!\n", "warning")
            self.update_output("Please set your Gemini API key to use AI features.\n", "info")
    
    # ========== COMMAND EXECUTION ==========
    
    def execute_command(self):
        """Execute user command"""
        command = self.command_input.get().strip()
        
        if not command:
            return
        
        if self.processing:
            messagebox.showwarning("Busy", "Please wait for the current command to finish.")
            return
        
        self.processing = True
        self.execute_btn.config(state="disabled", text="⏳ Processing...")
        self.command_input.delete(0, tk.END)
        
        # Execute in thread
        thread = threading.Thread(target=self._execute_in_thread, args=(command,))
        thread.daemon = True
        thread.start()
    
    def _execute_in_thread(self, command):
        """Execute command in separate thread"""
        try:
            # Broadcast command started
            if self.ws_client and hasattr(self.ws_client, 'connected') and self.ws_client.connected:
                try:
                    self.ws_client.emit('command_started', {
                        'command': command,
                        'timestamp': datetime.now().isoformat()
                    })
                except:
                    pass
            
            self.update_output(f"\n{'=' * 60}\n", "info")
            self.update_output(f"📝 You: {command}\n", "command")
            self.update_output(f"{'=' * 60}\n\n", "info")
            
            # VATSAL acknowledgment
            if self.vatsal_mode and self.vatsal and hasattr(self.vatsal, 'acknowledge_command'):
                try:
                    ack = self.vatsal.acknowledge_command(command)
                    self.update_output(f"🤖 VATSAL: {ack}\n\n", "info")
                except Exception as e:
                    print(f"VATSAL acknowledgment error: {e}")
            
            # Parse and execute command
            command_dict = parse_command(command)
            
            if command_dict.get("action") == "error":
                error_msg = command_dict.get('description', 'Error processing command')
                
                if self.vatsal_mode and self.vatsal:
                    try:
                        vatsal_response = self.vatsal.process_with_personality(command, f"Error: {error_msg}")
                        self.update_output(f"🤖 VATSAL: {vatsal_response}\n", "error")
                    except:
                        self.update_output(f"❌ {error_msg}\n", "error")
                else:
                    self.update_output(f"❌ {error_msg}\n", "error")
                
                return
            
            # Execute command
            result = self.executor.execute(command_dict)
            
            if result["success"]:
                # Broadcast command completed
                if self.ws_client and hasattr(self.ws_client, 'connected') and self.ws_client.connected:
                    try:
                        self.ws_client.emit('command_completed', {
                            'command': command,
                            'result': str(result['message']),
                            'timestamp': datetime.now().isoformat()
                        })
                    except:
                        pass
                
                # Get VATSAL response if enabled
                if self.vatsal_mode and self.vatsal:
                    try:
                        vatsal_response = self.vatsal.process_with_personality(command, result['message'])
                        self.update_output(f"🤖 VATSAL: {vatsal_response}\n", "success")
                        
                        # Speak response if speaking enabled
                        if self.speaking_enabled and self.voice_commander:
                            try:
                                self.voice_commander.speak(vatsal_response)
                            except:
                                pass
                    except:
                        self.update_output(f"✅ {result['message']}\n", "success")
                else:
                    self.update_output(f"✅ {result['message']}\n", "success")
            else:
                # Handle error
                if self.vatsal_mode and self.vatsal:
                    try:
                        vatsal_response = self.vatsal.process_with_personality(command, result['message'])
                        self.update_output(f"🤖 VATSAL: {vatsal_response}\n", "error")
                    except:
                        self.update_output(f"❌ {result['message']}\n", "error")
                else:
                    self.update_output(f"❌ {result['message']}\n", "error")
        
        except Exception as e:
            if self.vatsal_mode and self.vatsal:
                self.update_output(f"🤖 VATSAL: Apologies, encountered an error: {str(e)}\n", "error")
            else:
                self.update_output(f"❌ Error: {str(e)}\n", "error")
        
        finally:
            self.processing = False
            self.root.after(0, lambda: self.execute_btn.config(state="normal", text="▶ Execute"))
    
    def update_output(self, message, msg_type="info"):
        """Update output console"""
        self.output_area.config(state="normal")
        
        # Add message with color coding
        if msg_type == "command":
            self.output_area.insert(tk.END, message)
        elif msg_type == "success":
            self.output_area.insert(tk.END, message)
        elif msg_type == "error":
            self.output_area.insert(tk.END, message)
        elif msg_type == "warning":
            self.output_area.insert(tk.END, message)
        else:
            self.output_area.insert(tk.END, message)
        
        self.output_area.see(tk.END)
        self.output_area.config(state="disabled")
    
    def clear_output(self):
        """Clear output console"""
        self.output_area.config(state="normal")
        self.output_area.delete(1.0, tk.END)
        self.output_area.config(state="disabled")
    
    # ========== TOGGLE FUNCTIONS ==========
    
    def toggle_vatsal(self):
        """Toggle VATSAL mode"""
        self.vatsal_mode = not self.vatsal_mode
        
        if self.vatsal_mode:
            self.vatsal_toggle.config(
                text="● VATSAL: ON",
                fg=self.ACTIVE_GREEN,
                bg=self.BG_SECONDARY
            )
            self.update_output("\n✅ VATSAL mode enabled\n", "success")
        else:
            self.vatsal_toggle.config(
                text="● VATSAL: OFF",
                fg=self.TEXT_PRIMARY,
                bg=self.BUTTON_BG
            )
            self.update_output("\n⚠️ VATSAL mode disabled\n", "warning")
    
    def toggle_self_operating(self):
        """Toggle self-operating mode"""
        self.self_operating_mode = not self.self_operating_mode
        
        if self.self_operating_mode:
            self.soc_toggle.config(
                text="🔲 Self-Operating: ON",
                fg=self.ACTIVE_GREEN,
                bg=self.BG_SECONDARY
            )
            self.update_output("\n✅ Self-Operating mode enabled\n", "success")
        else:
            self.soc_toggle.config(
                text="🔲 Self-Operating: OFF",
                fg=self.TEXT_PRIMARY,
                bg=self.BUTTON_BG
            )
            self.update_output("\n⚠️ Self-Operating mode disabled\n", "warning")
    
    def toggle_voice(self):
        """Toggle voice mode"""
        self.voice_enabled = not self.voice_enabled
        
        if self.voice_enabled:
            self.update_output("\n🔊 Voice mode enabled\n", "success")
            if self.voice_commander:
                try:
                    self.voice_commander.speak("Voice mode activated")
                except:
                    pass
        else:
            self.update_output("\n🔇 Voice mode disabled\n", "warning")
    
    # ========== MENU FUNCTIONS ==========
    
    def toggle_wakeup_listener(self):
        """Toggle wakeup word listener"""
        if not self.wakeup_listening:
            # Start listening
            self.wakeup_listening = True
            self.wakeup_btn.config(bg=self.ACTIVE_GREEN, fg="white")
            self.update_output("\n👂 Wakeup word listener activated\n", "success")
            
            # Start voice listening if available
            if self.voice_commander:
                if self.voice_listening:
                    self.update_output("⚠️ Voice listener already active\n", "warning")
                    return
                try:
                    self.voice_listening = True
                    self.voice_commander.start_continuous_listening(callback=self.handle_voice_command)
                    self.update_output("Listening for wake word...\n", "info")
                except Exception as e:
                    self.update_output(f"⚠️ Could not start listener: {e}\n", "warning")
                    self.wakeup_listening = False
                    self.voice_listening = False
                    self.wakeup_btn.config(bg=self.BUTTON_BG, fg=self.TEXT_PRIMARY)
            else:
                self.update_output("⚠️ Voice commander not available\n", "warning")
                self.wakeup_listening = False
                self.wakeup_btn.config(bg=self.BUTTON_BG, fg=self.TEXT_PRIMARY)
        else:
            # Stop listening
            self.wakeup_listening = False
            self.wakeup_btn.config(bg=self.BUTTON_BG, fg=self.TEXT_PRIMARY)
            self.update_output("\n👂 Wakeup word listener deactivated\n", "warning")
            
            # Stop voice listening
            if self.voice_commander and self.voice_listening:
                try:
                    self.voice_listening = False
                    self.voice_commander.stop_continuous_listening()
                except Exception as e:
                    print(f"Error stopping listener: {e}")
                    # Force reset on error
                    self.voice_listening = False
    
    def toggle_v_sign_detector(self):
        """Toggle V-sign gesture detector with voice activation"""
        if not self.vsign_detecting:
            # Starting detector
            self.vsign_detecting = True
            self.vsign_btn.config(bg=self.ACTIVE_GREEN, fg="white")
            self.update_output("\n✌️ V-sign detector activated\n", "success")
            self.update_output("Show ONE V-sign for 1 second to start voice listening\n", "info")
            self.update_output("Show TWO V-signs to trigger VATSAL greeting\n", "info")
            
            # Start gesture voice activator if available
            if self.gesture_voice_activator:
                if self.gesture_voice_active:
                    self.update_output("⚠️ Gesture voice already running\n", "warning")
                    return
                    
                try:
                    # Register stop callback before starting
                    self.gesture_voice_activator.set_stop_callback(self._on_gesture_voice_stopped)
                    self.gesture_voice_active = True
                    
                    # Run gesture voice activator in background thread
                    def run_gesture_voice():
                        try:
                            self.gesture_voice_activator.run()
                        except Exception as e:
                            print(f"Gesture voice error: {e}")
                        finally:
                            # Callback is called automatically in the run method
                            pass
                    
                    threading.Thread(target=run_gesture_voice, daemon=True).start()
                    self.update_output("Camera activated - show V-sign!\n", "success")
                except Exception as e:
                    self.update_output(f"⚠️ Could not start detector: {e}\n", "warning")
                    self.vsign_detecting = False
                    self.gesture_voice_active = False
                    self.vsign_btn.config(bg=self.BUTTON_BG, fg=self.TEXT_PRIMARY)
            else:
                self.update_output("⚠️ Gesture voice activator not available\n", "warning")
                self.vsign_detecting = False
                self.vsign_btn.config(bg=self.BUTTON_BG, fg=self.TEXT_PRIMARY)
        else:
            # Stopping detector
            self.vsign_detecting = False
            self.vsign_btn.config(bg=self.BUTTON_BG, fg=self.TEXT_PRIMARY)
            self.update_output("\n✌️ V-sign detector deactivated\n", "warning")
            
            # Stop gesture voice activator
            if self.gesture_voice_activator and self.gesture_voice_active:
                try:
                    self.gesture_voice_activator.stop()
                    # _on_gesture_voice_stopped will be called automatically via callback
                except Exception as e:
                    print(f"Error stopping detector: {e}")
                    # Force reset state on error
                    self.gesture_voice_active = False
    
    def _on_gesture_voice_stopped(self):
        """Callback when gesture voice activator stops"""
        self.gesture_voice_active = False
        # Only reset button if detector was still marked as active
        if self.vsign_detecting:
            self.root.after(0, lambda: self.vsign_btn.config(bg=self.BUTTON_BG, fg=self.TEXT_PRIMARY))
            self.vsign_detecting = False
    
    def toggle_speaking(self):
        """Toggle text-to-speech"""
        if not self.speaking_enabled:
            # Enable speaking
            self.speaking_enabled = True
            self.speaking_btn.config(bg=self.ACTIVE_GREEN, fg="white")
            self.update_output("\n🗣️ Speaking mode enabled\n", "success")
            
            # Test speak
            if self.voice_commander:
                try:
                    self.voice_commander.speak("Speaking mode activated")
                except Exception as e:
                    self.update_output(f"⚠️ Could not activate speaking: {e}\n", "warning")
                    self.speaking_enabled = False
                    self.speaking_btn.config(bg=self.BUTTON_BG, fg=self.TEXT_PRIMARY)
            else:
                self.update_output("⚠️ Voice system not available\n", "warning")
                self.speaking_enabled = False
                self.speaking_btn.config(bg=self.BUTTON_BG, fg=self.TEXT_PRIMARY)
        else:
            # Disable speaking
            self.speaking_enabled = False
            self.speaking_btn.config(bg=self.BUTTON_BG, fg=self.TEXT_PRIMARY)
            self.update_output("\n🗣️ Speaking mode disabled\n", "warning")
    
    def show_settings(self):
        """Show feature listing panel"""
        features_window = tk.Toplevel(self.root)
        features_window.title("VATSAL Features")
        features_window.geometry("700x600")
        features_window.configure(bg=self.BG_PRIMARY)
        
        # Header
        header_frame = tk.Frame(features_window, bg=self.BG_SECONDARY, relief="solid", borderwidth=2, highlightbackground=self.BORDER_PRIMARY)
        header_frame.pack(fill="x", padx=20, pady=20)
        
        tk.Label(
            header_frame,
            text="🔧 VATSAL Features",
            font=("Georgia", 20, "bold"),
            bg=self.BG_SECONDARY,
            fg=self.TEXT_PRIMARY
        ).pack(pady=20)
        
        tk.Label(
            header_frame,
            text="100+ AI-Powered Features Available",
            font=("Segoe UI", 11),
            bg=self.BG_SECONDARY,
            fg=self.TEXT_SECONDARY
        ).pack(pady=(0, 20))
        
        # Create scrollable frame
        canvas = tk.Canvas(features_window, bg=self.BG_PRIMARY, highlightthickness=0)
        scrollbar = tk.Scrollbar(features_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.BG_PRIMARY)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Feature categories
        features = {
            "🤖 AI & Automation": [
                "Natural language command processing",
                "VATSAL AI personality assistant",
                "Self-operating computer mode",
                "Vision AI for screen understanding",
                "Smart task routing and automation",
                "AI-powered decision making"
            ],
            "🎯 Desktop Control": [
                "File management and organization",
                "Application launching and control",
                "Window management",
                "System settings control",
                "Clipboard management",
                "Desktop file synchronization"
            ],
            "🌐 Web Automation": [
                "Browser automation with Selenium",
                "Web scraping and data extraction",
                "Form filling automation",
                "Web navigation assistance",
                "API integration support"
            ],
            "🎤 Voice & Gestures": [
                "Voice command recognition",
                "Text-to-speech responses",
                "Hand gesture detection",
                "Gesture-activated voice commands",
                "Custom voice activation"
            ],
            "📊 Productivity": [
                "Pomodoro timer with AI coaching",
                "Task time prediction",
                "Energy level tracking",
                "Distraction detection",
                "Productivity monitoring",
                "Smart break suggestions",
                "Productivity dashboard"
            ],
            "⚙️ Workflow & Macros": [
                "Macro recording and playback",
                "Natural language workflow builder",
                "Workflow templates",
                "Batch automation scripts",
                "Custom workflow creation"
            ],
            "🔒 Security & Privacy": [
                "Password vault management",
                "Encrypted storage",
                "Security dashboard",
                "2FA integration",
                "Biometric authentication"
            ],
            "📅 Utilities": [
                "Calendar management",
                "Quick notes",
                "Weather and news service",
                "Translation service",
                "QR code generation",
                "Screenshot tools"
            ],
            "🖥️ Monitoring": [
                "Smart screen monitoring",
                "AI screen analysis",
                "Activity tracking",
                "System resource monitoring",
                "Application usage tracking"
            ],
            "🔗 Integration": [
                "WebSocket communication",
                "VNC GUI integration",
                "Web GUI bridge",
                "API endpoints",
                "Third-party service integration"
            ]
        }
        
        # Add feature categories
        for category, items in features.items():
            category_frame = tk.Frame(
                scrollable_frame,
                bg=self.BG_SECONDARY,
                relief="solid",
                borderwidth=2,
                highlightbackground=self.BORDER_PRIMARY
            )
            category_frame.pack(fill="x", padx=20, pady=10)
            
            tk.Label(
                category_frame,
                text=category,
                font=("Segoe UI", 13, "bold"),
                bg=self.BG_SECONDARY,
                fg=self.TEXT_PRIMARY,
                anchor="w"
            ).pack(fill="x", padx=15, pady=(15, 10))
            
            for item in items:
                item_frame = tk.Frame(category_frame, bg=self.BG_SECONDARY)
                item_frame.pack(fill="x", padx=15, pady=2)
                
                tk.Label(
                    item_frame,
                    text="  •  ",
                    font=("Segoe UI", 10),
                    bg=self.BG_SECONDARY,
                    fg=self.ACCENT_COLOR
                ).pack(side="left")
                
                tk.Label(
                    item_frame,
                    text=item,
                    font=("Segoe UI", 10),
                    bg=self.BG_SECONDARY,
                    fg=self.TEXT_PRIMARY,
                    anchor="w"
                ).pack(side="left", fill="x", expand=True, pady=3)
            
            # Add spacing after items
            tk.Frame(category_frame, bg=self.BG_SECONDARY, height=10).pack()
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0))
        scrollbar.pack(side="right", fill="y", padx=(0, 20))
        
        # Close button with curved shadow effect
        close_btn = tk.Button(
            features_window,
            text="Close",
            font=("Segoe UI", 11, "bold"),
            bg=self.BUTTON_BG,
            fg=self.TEXT_PRIMARY,
            relief="raised",
            borderwidth=1,
            cursor="hand2",
            padx=30,
            pady=10,
            command=features_window.destroy,
            highlightthickness=0,
            overrelief="groove"
        )
        close_btn.pack(pady=20, padx=2)
        self._add_hover_effect(close_btn, self.BUTTON_BG, self.BUTTON_HOVER)
    
    def handle_voice_command(self, command):
        """Handle voice command callback"""
        self.root.after(0, lambda: self.command_input.delete(0, tk.END))
        self.root.after(0, lambda: self.command_input.insert(0, command))
        self.root.after(0, self.execute_command)
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ModernVATSALGUI(root)
    app.run()


if __name__ == "__main__":
    main()
