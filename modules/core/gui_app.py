import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image, ImageTk, ImageDraw

from modules.core.gemini_controller import parse_command, get_ai_suggestion
from modules.core.command_executor import CommandExecutor
from modules.core.vatsal_assistant import create_boi_assistant
from modules.monitoring.advanced_smart_screen_monitor import AIScreenMonitoringSystem, create_advanced_smart_screen_monitor
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
    """Clean, modern BOI GUI matching web interface design"""

    def __init__(self, root):
        self.root = root
        self.root.title("B.O.I. - not your friend")

        # Initialize theme colors (exact match to web GUI CSS)
        self.BG_PRIMARY = "#F5F1E8"  # var(--bg-primary)
        self.BG_SECONDARY = "#FAF8F3"  # var(--bg-secondary)
        self.BORDER_PRIMARY = "#D9CFC0"  # var(--border-color)
        self.TEXT_PRIMARY = "#1a1a1a"  # var(--text-primary)
        self.TEXT_SECONDARY = "#5a5a5a"  # var(--text-secondary)
        self.ACCENT_COLOR = "#3a3a3a"  # var(--accent-color)
        self.BUTTON_BG = "#F3EADA"  # var(--button-bg)
        self.BUTTON_HOVER = "#E8DCCB"  # var(--button-hover)
        self.ACTIVE_GREEN = "#007B55"  # var(--active-green)
        self.CONSOLE_BG = "#FAF6EE"  # var(--console-bg)
        self.SHADOW_COLOR = "rgba(0, 0, 0, 0.08)"  # var(--shadow)

        # Configure root window
        self.root.configure(bg=self.BG_PRIMARY)
        self.root.geometry("700x900")

        # Set window icon
        self._set_window_icon()

        # State variables
        self.processing = False
        self.boi_mode = True
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
            icon_path = os.path.join(workspace_dir, "assets", "boi_icon.png")
            if not os.path.exists(icon_path):
                icon_path = os.path.join(workspace_dir, "assets", "boi_logo.png")

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
            self.boi = create_boi_assistant()
            self.advanced_monitor = create_advanced_smart_screen_monitor()
            self.ai_monitor = self.advanced_monitor  # Use single monitoring system
            self.file_automation = create_file_automation()
            self.clipboard_handler = ClipboardTextHandler()
            self.smart_automation = SmartAutomationManager()
            self.desktop_controller = DesktopFileController()

            # Feature Speaker (for speaking output)
            try:
                self.feature_speaker = create_feature_speaker()
                print("🔊 Feature Speaker initialized")
            except Exception as e:
                self.feature_speaker = None
                print(f"⚠️ Feature Speaker unavailable: {e}")

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

            # BOI Automator
            try:
                self.boi_automator = BOIAutomator()
            except Exception as e:
                self.boi_automator = None
                print(f"⚠️ BOI Automator unavailable: {e}")

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

            # Phone Link & Contact Management
            try:
                self.phone_dialer = create_phone_dialer()
                self.contact_manager = ContactManager("data/contacts.json")
                self.ai_phone_controller = AIPhoneLinkController()
                print("✅ Phone Link Controller initialized")
            except Exception as e:
                self.phone_dialer = None
                self.contact_manager = None
                self.ai_phone_controller = None
                print(f"⚠️ Phone Link unavailable: {e}")

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

            # Automation Orchestrator - Real autonomous task execution
            try:
                # AutomationOrchestrator not yet available, use executor for task handling
                self.automation_orchestrator = None
                print("⚠️ Automation Orchestrator pending implementation")
            except Exception as e:
                self.automation_orchestrator = None
                print(f"⚠️ Automation Orchestrator unavailable: {e}")

            # Batch Utilities - Python implementations of batch file functionalities
            try:
                self.batch_utilities = get_batch_utilities()
                print("✅ Batch Utilities initialized")
            except Exception as e:
                self.batch_utilities = None
                print(f"⚠️ Batch Utilities unavailable: {e}")

        except Exception as e:
            print(f"❌ Error initializing modules: {e}")
            messagebox.showerror("Initialization Error", f"Failed to initialize: {e}")

    def _create_gui(self):
        """Create the main GUI layout"""
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.BG_PRIMARY)
        main_container.pack(fill="both", expand=True, padx=8, pady=8)

        # Header section
        self._create_header(main_container)

        # Create main interface directly (no tabs)
        self._create_main_interface(main_container)

        # Footer with buttons and status
        self._create_footer()

    def _create_main_interface(self, parent):
        """Create the main command interface (no tabs)"""
        # Content container
        content_frame = tk.Frame(parent, bg=self.BG_PRIMARY)
        content_frame.pack(fill="both", expand=True, pady=(0, 20))

        # Command input section
        self._create_command_section_for_tab(content_frame)

        # Output console section
        self._create_output_section_for_tab(content_frame)

    def _create_command_section_for_tab(self, parent):
        """Create command input section for tab"""
        # Modern clean section with beautiful shadow
        section_shadow, section = self.create_shadowed_frame(parent)
        section_shadow.pack(fill="x", pady=(8, 10), padx=8)

        # Section header
        header = tk.Frame(section, bg=self.BG_SECONDARY)
        header.pack(fill="x", padx=15, pady=(10, 8))

        tk.Label(
            header,
            text="💬",
            font=("Segoe UI", 12),
            bg=self.BG_SECONDARY,
            fg=self.TEXT_PRIMARY
        ).pack(side="left", padx=(0, 8))

        tk.Label(
            header,
            text="Command Input",
            font=("Segoe UI", 11, "bold"),
            bg=self.BG_SECONDARY,
            fg=self.TEXT_PRIMARY
        ).pack(side="left")

        # Input area with better layout
        input_area = tk.Frame(section, bg=self.BG_SECONDARY)
        input_area.pack(fill="x", padx=15, pady=(0, 12))

        # Input row
        input_row = tk.Frame(input_area, bg=self.BG_SECONDARY)
        input_row.pack(fill="x", pady=(0, 8))

        # Command input with better styling
        self.command_input = tk.Entry(
            input_row,
            bg="white",
            fg=self.TEXT_PRIMARY,
            font=("Segoe UI", 10, "bold"),
            insertbackground=self.TEXT_PRIMARY,
            relief="solid",
            borderwidth=1,
            highlightbackground=self.BORDER_PRIMARY,
            highlightcolor=self.ACTIVE_GREEN,
            highlightthickness=1
        )
        self.command_input.pack(side="left", fill="both", expand=True, ipady=8)
        self.command_input.bind("<Return>", lambda e: self.execute_command())

        # Buttons row - separated for better organization
        buttons_row = tk.Frame(input_area, bg=self.BG_SECONDARY)
        buttons_row.pack(fill="x")

        # Execute button - larger and more prominent with shadow
        execute_shadow, self.execute_btn = self.create_shadowed_button(
            buttons_row,
            text="▶ Exec",
            command=self.execute_command,
            bg_color=self.ACTIVE_GREEN,
            fg_color="white",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8
        )
        execute_shadow.pack(side="left", padx=(0, 8))

        # Icon buttons with labels - more intuitive with shadows
        icon_buttons = [
            ("👂", "Wake", self.toggle_wakeup_listener),
            ("✌️", "Sign", self.toggle_v_sign_detector),
            ("🗣️", "Speak", self.toggle_speaking)
        ]

        for icon, label, command in icon_buttons:
            # Create shadowed button
            btn_shadow, btn = self.create_shadowed_button(
                buttons_row,
                text=f"{icon}\n{label}",
                command=command,
                font=("Segoe UI", 8, "bold"),
                padx=10,
                pady=5
            )
            btn_shadow.pack(side="left", padx=2)

            # Store button references
            if icon == "👂":
                self.wakeup_btn = btn
            elif icon == "✌️":
                self.vsign_btn = btn
            elif icon == "🗣️":
                self.speaking_btn = btn

    def _create_output_section_for_tab(self, parent):
        """Create ChatGPT-like chat interface"""
        # Main container
        section_shadow, section = self.create_shadowed_frame(parent)
        section_shadow.pack(fill="both", expand=True, padx=5, pady=(0, 5))

        # Header with title
        header = tk.Frame(section, bg=self.BG_SECONDARY)
        header.pack(fill="x", padx=12, pady=(8, 6))

        tk.Label(
            header,
            text="💬",
            font=("Segoe UI", 12),
            bg=self.BG_SECONDARY,
            fg=self.TEXT_PRIMARY
        ).pack(side="left", padx=(0, 8))

        tk.Label(
            header,
            text="BOI Chat",
            font=("Segoe UI", 11, "bold"),
            bg=self.BG_SECONDARY,
            fg=self.TEXT_PRIMARY
        ).pack(side="left")

        # Chat area frame
        chat_frame = tk.Frame(section, bg="#f7f7f7", relief="solid", borderwidth=1)
        chat_frame.pack(fill="both", expand=True, padx=12, pady=(8, 10))

        # Canvas with scrollbar for chat messages (ChatGPT-style)
        self.chat_canvas = tk.Canvas(chat_frame, bg="#f7f7f7", highlightthickness=0, relief="flat", borderwidth=0)
        scrollbar = ttk.Scrollbar(chat_frame, orient="vertical", command=self.chat_canvas.yview)
        self.chat_scrollable = tk.Frame(self.chat_canvas, bg="#f7f7f7")

        self.chat_scrollable.bind("<Configure>",
                                  lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")))
        self.chat_canvas.create_window((0, 0), window=self.chat_scrollable, anchor="nw")
        self.chat_canvas.configure(yscrollcommand=scrollbar.set)

        self.chat_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mousewheel scrolling
        def _on_mousewheel(event):
            self.chat_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.chat_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        self.chat_messages = []

    def create_rounded_rectangle(self, width, height, radius, color):
        """Create a rounded rectangle image using PIL"""
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Draw rounded rectangle
        draw.rounded_rectangle(
            [(0, 0), (width - 1, height - 1)],
            radius=radius,
            fill=color
        )

        return ImageTk.PhotoImage(image)

    def round_corners_canvas(self, canvas, width, height, radius, fill_color, outline_color=None, outline_width=0):
        """Draw a rounded rectangle on a canvas"""
        points = [
            radius, 0,
            width - radius, 0,
            width, 0,
            width, radius,
            width, height - radius,
            width, height,
            width - radius, height,
            radius, height,
            0, height,
            0, height - radius,
            0, radius,
            0, 0
        ]

        return canvas.create_polygon(
            points,
            smooth=True,
            fill=fill_color,
            outline=outline_color or fill_color,
            width=outline_width
        )

    def create_rounded_button(self, parent, text, command, bg_color=None, fg_color=None, width=None, height=None):
        """Create a button with enhanced 3D effect, dramatic shadows, and rounded corners"""
        if bg_color is None:
            bg_color = self.BUTTON_BG
        if fg_color is None:
            fg_color = self.TEXT_PRIMARY

        # Outer shadow container (darker, more pronounced - ENHANCED!)
        outer_shadow = tk.Frame(parent, bg="#707070", bd=0)

        # Mid shadow layer (stronger gradient - ENHANCED!)
        mid_shadow = tk.Frame(outer_shadow, bg="#959595", bd=0)
        mid_shadow.pack(padx=(0, 8), pady=(0, 8))

        # Inner shadow layer (ENHANCED!)
        inner_shadow = tk.Frame(mid_shadow, bg="#B8B8B8", bd=0)
        inner_shadow.pack(padx=(0, 4), pady=(0, 4))

        # Canvas for rounded corners
        canvas = tk.Canvas(
            inner_shadow,
            bg=self.BG_PRIMARY,
            highlightthickness=0,
            bd=0
        )
        canvas.pack()

        # Actual button with enhanced appearance and rounded style
        btn = tk.Button(
            canvas,
            text=text,
            command=command,
            bg=bg_color,
            fg=fg_color,
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            bd=0,
            padx=18,
            pady=10,
            cursor="hand2",
            activebackground=self.BUTTON_HOVER,
            activeforeground=fg_color,
            borderwidth=0
        )

        if width:
            btn.config(width=width)
        if height:
            btn.config(height=height)

        # Create window in canvas for rounded effect
        btn_window = canvas.create_window(0, 0, anchor='nw', window=btn)

        # Update canvas size to match button
        btn.update_idletasks()
        btn_width = btn.winfo_reqwidth()
        btn_height = btn.winfo_reqheight()

        # Draw rounded rectangle background
        radius = 15
        canvas.config(width=btn_width, height=btn_height)

        # Draw rounded background
        canvas_bg = canvas.create_rounded_rectangle = lambda x1, y1, x2, y2, r, **kwargs: canvas.create_polygon(
            x1 + r, y1,
            x1 + r, y1,
            x2 - r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1 + r,
            x1, y1,
            smooth=True,
            **kwargs
        )

        # Enhanced hover effects with dramatic 3D lift
        def on_enter(e):
            if btn['bg'] != self.ACTIVE_GREEN:
                btn.config(bg=self.BUTTON_HOVER)
                mid_shadow.pack_configure(padx=(0, 8), pady=(0, 8))

        def on_leave(e):
            if btn['bg'] != self.ACTIVE_GREEN:
                btn.config(bg=bg_color)
                mid_shadow.pack_configure(padx=(0, 6), pady=(0, 6))

        def on_press(e):
            mid_shadow.pack_configure(padx=(0, 2), pady=(0, 2))

        def on_release(e):
            mid_shadow.pack_configure(padx=(0, 6), pady=(0, 6))

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<ButtonPress-1>", on_press)
        btn.bind("<ButtonRelease-1>", on_release)

        return outer_shadow, btn

    def create_shadowed_frame(self, parent, bg_color=None, **kwargs):
        """Create a frame with beautiful multi-layer shadow for aesthetic depth"""
        if bg_color is None:
            bg_color = self.BG_SECONDARY

        # Outer shadow layer (darkest)
        outer_shadow = tk.Frame(parent, bg="#707070", bd=0)

        # Mid shadow layer (gradient)
        mid_shadow = tk.Frame(outer_shadow, bg="#959595", bd=0)
        mid_shadow.pack(padx=(0, 8), pady=(0, 8), fill="both", expand=True)

        # Inner shadow layer (lightest shadow)
        inner_shadow = tk.Frame(mid_shadow, bg="#B8B8B8", bd=0)
        inner_shadow.pack(padx=(0, 4), pady=(0, 4), fill="both", expand=True)

        # Actual content frame
        content_frame = tk.Frame(
            inner_shadow,
            bg=bg_color,
            relief="flat",
            borderwidth=1,
            highlightbackground=self.BORDER_PRIMARY,
            highlightthickness=1,
            **kwargs
        )
        content_frame.pack(fill="both", expand=True)

        return outer_shadow, content_frame

    def create_shadowed_button(self, parent, text, command, bg_color=None, fg_color=None, **kwargs):
        """Create a regular button with beautiful shadow"""
        if bg_color is None:
            bg_color = self.BUTTON_BG
        if fg_color is None:
            fg_color = self.TEXT_PRIMARY

        # Outer shadow layer
        outer_shadow = tk.Frame(parent, bg="#707070", bd=0)

        # Mid shadow layer
        mid_shadow = tk.Frame(outer_shadow, bg="#959595", bd=0)
        mid_shadow.pack(padx=(0, 6), pady=(0, 6))

        # Inner shadow layer
        inner_shadow = tk.Frame(mid_shadow, bg="#B8B8B8", bd=0)
        inner_shadow.pack(padx=(0, 3), pady=(0, 3))

        # Actual button
        btn = tk.Button(
            inner_shadow,
            text=text,
            command=command,
            bg=bg_color,
            fg=fg_color,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            activebackground=self.BUTTON_HOVER,
            activeforeground=fg_color,
            **kwargs
        )
        btn.pack()

        # Enhanced hover effects
        def on_enter(e):
            btn.config(bg=self.BUTTON_HOVER)
            mid_shadow.pack_configure(padx=(0, 8), pady=(0, 8))

        def on_leave(e):
            btn.config(bg=bg_color)
            mid_shadow.pack_configure(padx=(0, 6), pady=(0, 6))

        def on_press(e):
            mid_shadow.pack_configure(padx=(0, 2), pady=(0, 2))

        def on_release(e):
            mid_shadow.pack_configure(padx=(0, 6), pady=(0, 6))

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<ButtonPress-1>", on_press)
        btn.bind("<ButtonRelease-1>", on_release)

        return outer_shadow, btn

    def _create_header(self, parent):
        """Create modern clean header"""
        # Create header with beautiful shadow
        header_shadow, header = self.create_shadowed_frame(parent)
        header_shadow.pack(fill="x", pady=(0, 15))

        # Title section with compact layout
        title_section = tk.Frame(header, bg=self.BG_SECONDARY)
        title_section.pack(fill="x", padx=25, pady=(15, 12))

        # Compact title with logo
        title_frame = tk.Frame(title_section, bg=self.BG_SECONDARY)
        title_frame.pack(side="left")

        # Add logo
        try:
            workspace_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            logo_path = os.path.join(workspace_dir, "assets", "boi_icon.png")
            if not os.path.exists(logo_path):
                logo_path = os.path.join(workspace_dir, "assets", "boi_logo.png")

            if os.path.exists(logo_path):
                logo_img = Image.open(logo_path)
                logo_img = logo_img.resize((40, 40), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_img)
                tk.Label(
                    title_frame,
                    image=self.logo_photo,
                    bg=self.BG_SECONDARY
                ).pack(side="left", padx=(0, 12))
        except Exception as e:
            print(f"Could not load logo: {e}")

        # Title and subtitle in vertical layout
        title_text = tk.Frame(title_frame, bg=self.BG_SECONDARY)
        title_text.pack(side="left")

        tk.Label(
            title_text,
            text="B.O.I.",
            font=("Segoe UI", 18, "bold"),
            bg=self.BG_SECONDARY,
            fg=self.TEXT_PRIMARY
        ).pack(anchor="w")

        tk.Label(
            title_text,
            text="Barely Obey Instructions",
            font=("Segoe UI", 9, "bold"),
            bg=self.BG_SECONDARY,
            fg=self.TEXT_SECONDARY
        ).pack(anchor="w")

        # Compact status bar on right side
        status_bar = tk.Frame(title_section, bg=self.BG_SECONDARY)
        status_bar.pack(side="right")

        # Time display
        self.time_label = tk.Label(
            status_bar,
            text="",
            font=("Segoe UI", 10, "bold"),
            bg=self.BG_SECONDARY,
            fg=self.TEXT_SECONDARY
        )
        self.time_label.pack(side="top", anchor="e", pady=(0, 5))

        # Toggles in horizontal layout
        toggles_frame = tk.Frame(status_bar, bg=self.BG_SECONDARY)
        toggles_frame.pack(side="top")

        # Simple modern toggle buttons with shadows
        boi_shadow, self.boi_toggle = self.create_shadowed_button(
            toggles_frame,
            text="● BOI: ON",
            command=self.toggle_boi,
            fg_color=self.ACTIVE_GREEN,
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=6
        )
        boi_shadow.pack(side="left", padx=(0, 8))

        soc_shadow, self.soc_toggle = self.create_shadowed_button(
            toggles_frame,
            text="🤖 Self-Operating: ON",
            command=self.toggle_self_operating,
            fg_color=self.ACTIVE_GREEN,
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=6
        )
        soc_shadow.pack(side="left")

    def _create_command_section(self, parent):
        """Create command input section"""
        # Enhanced outer shadow for dramatic 3D effect
        section_shadow_outer = tk.Frame(parent, bg="#808080", bd=0)
        section_shadow_outer.pack(fill="x", pady=(0, 20))

        section_shadow_mid = tk.Frame(section_shadow_outer, bg="#A0A0A0", bd=0)
        section_shadow_mid.pack(fill="x", padx=(0, 8), pady=(0, 8))

        section_shadow_inner = tk.Frame(section_shadow_mid, bg="#C0C0C0", bd=0)
        section_shadow_inner.pack(fill="x", padx=(0, 4), pady=(0, 4))

        section = tk.Frame(
            section_shadow_inner,
            bg=self.BG_SECONDARY,
            relief="raised",
            borderwidth=4,
            highlightbackground="#FFFFFF",
            highlightthickness=2
        )
        section.pack(fill="x")

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
            font=("Segoe UI", 11, "bold"),
            insertbackground=self.TEXT_PRIMARY,
            relief="flat",
            borderwidth=0,
            highlightbackground=self.BORDER_PRIMARY,
            highlightcolor=self.ACCENT_COLOR,
            highlightthickness=2
        )
        self.command_input.pack(side="left", fill="both", expand=True, ipady=14, padx=(0, 15))
        self.command_input.bind("<Return>", lambda e: self.execute_command())

        # Buttons container with enhanced 3D shadow
        btn_group_shadow_outer = tk.Frame(input_area, bg="#909090", bd=0)
        btn_group_shadow_outer.pack(side="left")

        btn_group_shadow_mid = tk.Frame(btn_group_shadow_outer, bg="#B0B0B0", bd=0)
        btn_group_shadow_mid.pack(padx=(0, 6), pady=(0, 6))

        # Canvas for rounded button container (wider for more buttons)
        buttons_canvas = tk.Canvas(
            btn_group_shadow_mid,
            bg=self.BG_PRIMARY,
            highlightthickness=0,
            bd=0,
            width=550,
            height=65
        )
        buttons_canvas.pack()

        # Draw rounded background for button group
        self.round_corners_canvas(buttons_canvas, 550, 65, 20, self.BUTTON_BG, "#FFFFFF", 3)

        # Frame inside canvas for buttons
        buttons_container = tk.Frame(
            buttons_canvas,
            bg=self.BUTTON_BG
        )
        buttons_canvas.create_window(275, 32, window=buttons_container)

        # Execute button with enhanced 3D effect
        self.execute_btn = tk.Button(
            buttons_container,
            text="▶ Execute",
            font=("Segoe UI", 12, "bold"),
            bg=self.BUTTON_BG,
            fg=self.TEXT_PRIMARY,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            padx=32,
            pady=14,
            command=self.execute_command,
            highlightthickness=0,
            activebackground=self.BUTTON_HOVER
        )
        self.execute_btn.pack(side="left", padx=3, pady=3)

        # Enhanced 3D press effect for execute button
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

        # Icon buttons - Wakeup, V-sign, Speaking
        icon_buttons = [
            ("👂", self.toggle_wakeup_listener, "Wakeup Word Listener"),
            ("✌️", self.toggle_v_sign_detector, "V-Sign Detector"),
            ("🗣️", self.toggle_speaking, "Speaking")
        ]

        for icon, command, tooltip in icon_buttons:
            btn = tk.Button(
                buttons_container,
                text=icon,
                font=("Segoe UI", 18),
                bg=self.BUTTON_BG,
                fg=self.TEXT_PRIMARY,
                relief="raised",
                borderwidth=2,
                cursor="hand2",
                width=3,
                command=command,
                highlightthickness=1,
                highlightbackground="#FFFFFF",
                activebackground=self.BUTTON_HOVER
            )
            btn.pack(side="left", padx=3, pady=3)

            # Enhanced 3D press effect
            def make_press_handler(button):
                def on_press(e):
                    button.config(relief="sunken", borderwidth=1)

                return on_press

            def make_release_handler(button):
                def on_release(e):
                    button.config(relief="raised", borderwidth=2)

                return on_release

            def make_hover_enter(button):
                def on_enter(e):
                    button.config(borderwidth=3, bg=self.BUTTON_HOVER)

                return on_enter

            def make_hover_leave(button):
                def on_leave(e):
                    button.config(borderwidth=2, bg=self.BUTTON_BG)

                return on_leave

            btn.bind("<Enter>", make_hover_enter(btn))
            btn.bind("<Leave>", make_hover_leave(btn))
            btn.bind("<ButtonPress-1>", make_press_handler(btn))
            btn.bind("<ButtonRelease-1>", make_release_handler(btn))

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
        # Enhanced outer shadow for dramatic 3D effect
        output_shadow_outer = tk.Frame(parent, bg="#808080", bd=0)
        output_shadow_outer.pack(fill="both", expand=True)

        output_shadow_mid = tk.Frame(output_shadow_outer, bg="#A0A0A0", bd=0)
        output_shadow_mid.pack(fill="both", expand=True, padx=(0, 8), pady=(0, 8))

        output_shadow_inner = tk.Frame(output_shadow_mid, bg="#C0C0C0", bd=0)
        output_shadow_inner.pack(fill="both", expand=True, padx=(0, 4), pady=(0, 4))

        section = tk.Frame(
            output_shadow_inner,
            bg=self.BG_SECONDARY,
            relief="raised",
            borderwidth=4,
            highlightbackground="#FFFFFF",
            highlightthickness=2
        )
        section.pack(fill="both", expand=True)

        # Section header
        header = tk.Frame(section, bg=self.BG_SECONDARY)
        header.pack(fill="x", padx=20, pady=(20, 15))

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

        # Clear button (top) with enhanced 3D shadow
        clear_shadow_outer = tk.Frame(header, bg="#909090", bd=0)
        clear_shadow_outer.pack(side="right", padx=2, pady=2)

        clear_shadow_mid = tk.Frame(clear_shadow_outer, bg="#B0B0B0", bd=0)
        clear_shadow_mid.pack(padx=(0, 5), pady=(0, 5))

        # Canvas for rounded Clear button (top)
        clear_canvas = tk.Canvas(
            clear_shadow_mid,
            bg=self.BG_PRIMARY,
            highlightthickness=0,
            bd=0,
            width=120,
            height=48
        )
        clear_canvas.pack()

        # Draw rounded background
        self.round_corners_canvas(clear_canvas, 120, 48, 18, self.BUTTON_BG, self.BORDER_PRIMARY, 3)

        clear_btn = tk.Button(
            clear_canvas,
            text="■ Clear",
            font=("Segoe UI", 11, "bold"),
            bg=self.BUTTON_BG,
            fg=self.TEXT_PRIMARY,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            padx=24,
            pady=8,
            command=self.clear_output,
            activebackground=self.BUTTON_HOVER
        )
        clear_canvas.create_window(60, 24, window=clear_btn)

        # Enhanced 3D hover effect
        def clear_hover_enter(e):
            clear_shadow_mid.pack_configure(padx=(0, 7), pady=(0, 7))

        def clear_hover_leave(e):
            clear_shadow_mid.pack_configure(padx=(0, 5), pady=(0, 5))

        def clear_press(e):
            clear_shadow_mid.pack_configure(padx=(0, 2), pady=(0, 2))

        def clear_release(e):
            clear_shadow_mid.pack_configure(padx=(0, 5), pady=(0, 5))

        clear_btn.bind("<Enter>", clear_hover_enter)
        clear_btn.bind("<Leave>", clear_hover_leave)
        clear_btn.bind("<ButtonPress-1>", clear_press)
        clear_btn.bind("<ButtonRelease-1>", clear_release)
        self._add_hover_effect(clear_btn, self.BUTTON_BG, self.BUTTON_HOVER)

        # Output console
        console_frame = tk.Frame(section, bg=self.BG_SECONDARY)
        console_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.output_area = scrolledtext.ScrolledText(
            console_frame,
            bg=self.CONSOLE_BG,
            fg=self.TEXT_PRIMARY,
            font=("Segoe UI", 10, "bold"),
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
        footer.pack(fill="x", padx=20, pady=(0, 30))

        # Clear button (bottom) with enhanced 3D shadow
        clear_b_shadow_outer = tk.Frame(footer, bg="#909090", bd=0)
        clear_b_shadow_outer.pack(side="right", padx=2, pady=2)

        clear_b_shadow_mid = tk.Frame(clear_b_shadow_outer, bg="#B0B0B0", bd=0)
        clear_b_shadow_mid.pack(padx=(0, 5), pady=(0, 5))

        # Canvas for rounded Clear button (bottom)
        clear_b_canvas = tk.Canvas(
            clear_b_shadow_mid,
            bg=self.BG_PRIMARY,
            highlightthickness=0,
            bd=0,
            width=120,
            height=48
        )
        clear_b_canvas.pack()

        # Draw rounded background
        self.round_corners_canvas(clear_b_canvas, 120, 48, 18, self.BUTTON_BG, self.BORDER_PRIMARY, 3)

        clear_btn_bottom = tk.Button(
            clear_b_canvas,
            text="■ Clear",
            font=("Segoe UI", 11, "bold"),
            bg=self.BUTTON_BG,
            fg=self.TEXT_PRIMARY,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            padx=24,
            pady=8,
            command=self.clear_output,
            activebackground=self.BUTTON_HOVER
        )
        clear_b_canvas.create_window(60, 24, window=clear_btn_bottom)

        # Enhanced 3D hover effect
        def clear_b_hover_enter(e):
            clear_b_shadow_mid.pack_configure(padx=(0, 7), pady=(0, 7))

        def clear_b_hover_leave(e):
            clear_b_shadow_mid.pack_configure(padx=(0, 5), pady=(0, 5))

        def clear_b_press(e):
            clear_b_shadow_mid.pack_configure(padx=(0, 2), pady=(0, 2))

        def clear_b_release(e):
            clear_b_shadow_mid.pack_configure(padx=(0, 5), pady=(0, 5))

        clear_btn_bottom.bind("<Enter>", clear_b_hover_enter)
        clear_btn_bottom.bind("<Leave>", clear_b_hover_leave)
        clear_btn_bottom.bind("<ButtonPress-1>", clear_b_press)
        clear_btn_bottom.bind("<ButtonRelease-1>", clear_b_release)
        self._add_hover_effect(clear_btn_bottom, self.BUTTON_BG, self.BUTTON_HOVER)

    def _create_footer(self):
        """Create footer with buttons and status"""
        footer = tk.Frame(
            self.root,
            bg=self.BG_SECONDARY,
            relief="raised",
            borderwidth=4,
            highlightbackground=self.BORDER_PRIMARY,
            highlightthickness=2
        )
        footer.pack(fill="x", side="bottom", padx=20, pady=(0, 20))

        # Inner container
        footer_content = tk.Frame(footer, bg=self.BG_SECONDARY)
        footer_content.pack(fill="x", padx=20, pady=15)

        # Left side - Action buttons
        button_container = tk.Frame(footer_content, bg=self.BG_SECONDARY)
        button_container.pack(side="left")

        # Define bottom buttons with beautiful shadows
        bottom_buttons = [
            ("❓ Help", self.show_help),
            ("👥 Contacts", self.show_contacts),
            ("📞 Phone Link", self.show_phone_link_control),
            ("ℹ️ About", self.show_about),
            ("💡 Suggestion", self.show_suggestion),
            ("🛡️ Security", self.show_security_dashboard),
            ("🔧 Batch Tools", self.show_batch_utilities)
        ]

        for text, command in bottom_buttons:
            btn_shadow, btn = self.create_shadowed_button(
                button_container,
                text=text,
                command=command,
                font=("Segoe UI", 10, "bold"),
                padx=15,
                pady=8
            )
            btn_shadow.pack(side="left", padx=5)

        # Right side - Status label
        status_container = tk.Frame(
            footer_content,
            bg=self.CONSOLE_BG,
            relief="solid",
            borderwidth=2,
            highlightbackground=self.BORDER_PRIMARY,
            highlightthickness=1
        )
        status_container.pack(side="right", padx=10)

        self.status_label = tk.Label(
            status_container,
            text="✅ Ready",
            bg=self.CONSOLE_BG,
            fg=self.ACTIVE_GREEN,
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=10
        )
        self.status_label.pack()

    def _add_hover_effect(self, button, normal_color, hover_color):
        """Add hover effect to button"""

        def on_enter(e):
            button['background'] = hover_color

        def on_leave(e):
            button['background'] = normal_color

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def add_hover_effect(self, button, normal_color, hover_color):
        """Add hover effect to button (legacy method for tab compatibility)"""

        def on_enter(e):
            button['background'] = hover_color

        def on_leave(e):
            button['background'] = normal_color

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def add_gradient_effect(self, widget):
        """Add gradient border effect to widget"""
        widget.configure(highlightbackground=self.BORDER_PRIMARY, highlightthickness=1)

    def _update_time(self):
        """Update time display"""
        current_time = datetime.now().strftime("%A, %B %d, %Y • %I:%M:%S %p")
        self.time_label.config(text=current_time)
        self.root.after(1000, self._update_time)

    def _show_welcome(self):
        """Show welcome message"""
        api_key = os.getenv("GEMINI_API_KEY")

        if api_key:
            self.update_output("✅ Gemini AI is ready!", "success")
            if self.boi and self.boi_mode:
                greeting = self.boi.get_greeting()
                self.update_output(f"🤖 BOI: {greeting}", "info")
            self.update_output("Type a command or click a button to get started.", "info")
        else:
            self.update_output("⚠️ WARNING: GEMINI_API_KEY not found!", "warning")
            self.update_output("Please set your Gemini API key to use AI features.", "info")

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

            # Display user command in chat (BLUE - USER category)
            self.add_chat_message(command, sender="USER", msg_type="command")

            # BOI acknowledgment
            if self.boi_mode and self.boi and hasattr(self.boi, 'acknowledge_command'):
                try:
                    ack = self.boi.acknowledge_command(command)
                    self.update_output(f"{ack}", "info")
                except Exception as e:
                    print(f"BOI acknowledgment error: {e}")

            # Parse and execute command
            command_dict = parse_command(command)

            if command_dict.get("action") == "error":
                error_msg = command_dict.get('description', 'Error processing command')

                if self.boi_mode and self.boi:
                    try:
                        boi_response = self.boi.process_with_personality(command, f"Error: {error_msg}")
                        self.update_output(boi_response, "error")
                    except:
                        self.update_output(error_msg, "error")
                else:
                    self.update_output(error_msg, "error")

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

                # Get BOI response if enabled
                if self.boi_mode and self.boi:
                    try:
                        boi_response = self.boi.process_with_personality(command, result['message'])
                        self.update_output(boi_response, "success")

                        # Speak response if speaking enabled
                        if self.speaking_enabled and self.voice_commander:
                            try:
                                self.voice_commander.speak(boi_response)
                            except:
                                pass
                    except:
                        self.update_output(result['message'], "success")
                else:
                    self.update_output(result['message'], "success")
            else:
                # Handle error
                if self.boi_mode and self.boi:
                    try:
                        boi_response = self.boi.process_with_personality(command, result['message'])
                        self.update_output(boi_response, "error")
                    except:
                        self.update_output(result['message'], "error")
                else:
                    self.update_output(result['message'], "error")

        except Exception as e:
            if self.boi_mode and self.boi:
                self.update_output(f"Apologies, encountered an error: {str(e)}", "error")
            else:
                self.update_output(f"Error: {str(e)}", "error")

        finally:
            self.processing = False
            self.root.after(0, lambda: self.execute_btn.config(state="normal", text="▶ Execute"))

    def add_chat_message(self, message, sender="BOI", msg_type="info"):
        """Add a chat message with DISTINCT COLORS - USER=BLUE, BOI=GREEN"""
        if not hasattr(self, 'chat_scrollable') or self.chat_scrollable is None:
            return

        # Create row for this message
        row = tk.Frame(self.chat_scrollable, bg="#ffffff")
        row.pack(fill="x", padx=5, pady=6)

        is_user = (sender.strip().upper() == "USER")

        if is_user:
            # USER PROMPT - BRIGHT BLUE (#2196F3) with WHITE text
            bubble = tk.Frame(row, bg="#2196F3", relief="solid", bd=3)
            bubble.pack(fill="x", padx=2, pady=2)

            header_text = tk.Label(bubble, text="👤 YOU", bg="#2196F3", fg="#FFFFFF", font=("Segoe UI", 11, "bold"), padx=12, pady=6)
            header_text.pack(anchor="w")

            msg_text = tk.Label(bubble, text=message, bg="#2196F3", fg="#FFFFFF", font=("Segoe UI", 11, "italic"), justify="left", wraplength=280, padx=12, pady=8)
            msg_text.pack(anchor="w", fill="x")
        else:
            # BOI REPLY - BRIGHT GREEN (#4CAF50) with WHITE text
            bubble = tk.Frame(row, bg="#4CAF50", relief="solid", bd=3)
            bubble.pack(fill="x", padx=2, pady=2)

            header_text = tk.Label(bubble, text="🤖 BOI", bg="#4CAF50", fg="#FFFFFF", font=("Segoe UI", 11, "bold"), padx=12, pady=6)
            header_text.pack(anchor="w")

            msg_text = tk.Label(bubble, text=message, bg="#4CAF50", fg="#FFFFFF", font=("Segoe UI", 11), justify="left", wraplength=280, padx=12, pady=8)
            msg_text.pack(anchor="w", fill="x")

        self.chat_messages.append((row, message))
        self.chat_canvas.after(50, lambda: self.chat_canvas.yview_moveto(1.0))

    def update_output(self, message, msg_type="info"):
        """Add message to chat interface"""
        # Clean up newlines from old format
        message = message.strip().replace("\n", " ").replace("📝 You: ", "👤 ")
        if message:
            self.add_chat_message(message, sender="BOI", msg_type=msg_type)

    def clear_output(self):
        """Clear chat messages"""
        if hasattr(self, 'chat_messages') and self.chat_messages:
            for msg_box, _ in self.chat_messages:
                msg_box.destroy()
            self.chat_messages.clear()
        self.add_chat_message("✨ Chat cleared", sender="BOI", msg_type="info")

    # ========== TOGGLE FUNCTIONS ==========

    def toggle_boi(self):
        """Toggle BOI mode"""
        self.boi_mode = not self.boi_mode

        if self.boi_mode:
            self.boi_toggle.config(
                text="● BOI: ON",
                fg=self.ACTIVE_GREEN,
                bg=self.BG_SECONDARY
            )
            self.update_output("✅ BOI mode enabled", "success")
        else:
            self.boi_toggle.config(
                text="● BOI: OFF",
                fg=self.TEXT_PRIMARY,
                bg=self.BUTTON_BG
            )
            self.update_output("⚠️ BOI mode disabled", "warning")

    def toggle_self_operating(self):
        """Toggle self-operating mode"""
        self.self_operating_mode = not self.self_operating_mode

        if self.self_operating_mode:
            self.soc_toggle.config(
                text="🔲 Self-Operating: ON",
                fg=self.ACTIVE_GREEN,
                bg=self.BG_SECONDARY
            )
            self.update_output("✅ Self-Operating mode enabled", "success")
        else:
            self.soc_toggle.config(
                text="🔲 Self-Operating: OFF",
                fg=self.TEXT_PRIMARY,
                bg=self.BUTTON_BG
            )
            self.update_output("⚠️ Self-Operating mode disabled", "warning")

    def toggle_voice(self):
        """Toggle voice mode"""
        self.voice_enabled = not self.voice_enabled

        if self.voice_enabled:
            self.update_output("🔊 Voice mode enabled", "success")
            if self.voice_commander:
                try:
                    self.voice_commander.speak("Voice mode activated")
                except:
                    pass
        else:
            self.update_output("🔇 Voice mode disabled", "warning")

    # ========== MENU FUNCTIONS ==========

    def toggle_wakeup_listener(self):
        """Toggle wakeup word listener"""
        if not self.wakeup_listening:
            # Start listening
            self.wakeup_listening = True
            self.wakeup_btn.config(bg=self.ACTIVE_GREEN, fg="white")
            self.update_output("👂 Wakeup word listener activated", "success")

            # Start voice listening if available
            if self.voice_commander:
                if self.voice_listening:
                    self.update_output("⚠️ Voice listener already active", "warning")
                    return
                try:
                    self.voice_listening = True
                    self.voice_commander.start_continuous_listening(callback=self.handle_voice_command)
                    self.update_output("Listening for wake word...", "info")
                except Exception as e:
                    self.update_output(f"⚠️ Could not start listener: {e}", "warning")
                    self.wakeup_listening = False
                    self.voice_listening = False
                    self.wakeup_btn.config(bg=self.BUTTON_BG, fg=self.TEXT_PRIMARY)
            else:
                self.update_output("⚠️ Voice commander not available", "warning")
                self.wakeup_listening = False
                self.wakeup_btn.config(bg=self.BUTTON_BG, fg=self.TEXT_PRIMARY)
        else:
            # Stop listening
            self.wakeup_listening = False
            self.wakeup_btn.config(bg=self.BUTTON_BG, fg=self.TEXT_PRIMARY)
            self.update_output("👂 Wakeup word listener deactivated", "warning")

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
            self.update_output("✌️ V-sign detector activated", "success")
            self.update_output("Show ONE V-sign for 1 second to start voice listening", "info")
            self.update_output("Show TWO V-signs to trigger BOI greeting", "info")

            # Start gesture voice activator if available
            if self.gesture_voice_activator:
                if self.gesture_voice_active:
                    self.update_output("⚠️ Gesture voice already running", "warning")
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
                    self.update_output("Camera activated - show V-sign!", "success")
                except Exception as e:
                    self.update_output(f"⚠️ Could not start detector: {e}", "warning")
                    self.vsign_detecting = False
                    self.gesture_voice_active = False
                    self.vsign_btn.config(bg=self.BUTTON_BG, fg=self.TEXT_PRIMARY)
            else:
                self.update_output("⚠️ Gesture voice activator not available", "warning")
                self.vsign_detecting = False
                self.vsign_btn.config(bg=self.BUTTON_BG, fg=self.TEXT_PRIMARY)
        else:
            # Stopping detector
            self.vsign_detecting = False
            self.vsign_btn.config(bg=self.BUTTON_BG, fg=self.TEXT_PRIMARY)
            self.update_output("✌️ V-sign detector deactivated", "warning")

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
            self.update_output("🗣️ Speaking mode enabled", "success")

            # Test speak
            if self.voice_commander:
                try:
                    self.voice_commander.speak("Speaking mode activated")
                except Exception as e:
                    self.update_output(f"⚠️ Could not activate speaking: {e}", "warning")
                    self.speaking_enabled = False
                    self.speaking_btn.config(bg=self.BUTTON_BG, fg=self.TEXT_PRIMARY)
            else:
                self.update_output("⚠️ Voice system not available", "warning")
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
        features_window.title("BOI Features")
        features_window.geometry("700x600")
        features_window.configure(bg=self.BG_PRIMARY)

        # Header
        header_frame = tk.Frame(features_window, bg=self.BG_SECONDARY, relief="solid", borderwidth=2,
                                highlightbackground=self.BORDER_PRIMARY)
        header_frame.pack(fill="x", padx=20, pady=20)

        tk.Label(
            header_frame,
            text="🔧 BOI Features",
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
                "BOI (Barely Obeys Instructions) personality assistant",
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

    # ========== VOICE AND SOUND METHODS ==========

    def start_voice_listen(self):
        """Start push-to-talk voice command"""
        if not self.voice_commander:
            messagebox.showerror("Voice Error", "Voice commander not available")
            return

        if self.processing:
            messagebox.showwarning("Busy", "Please wait for the current command to finish.")
            return

        def voice_thread():
            self.update_output("\n🎤 Listening for voice command...\n", "info")
            self.update_status("🎤 Listening...", self.ACCENT_COLOR)
            # self.root.after(0, lambda: self.voice_listen_btn.config(bg=self.ACTIVE_GREEN))

            result = self.voice_commander.listen_once(timeout=10)

            # self.root.after(0, lambda: self.voice_listen_btn.config(bg=self.BUTTON_BG))

            if result['success'] and result['text']:
                self.root.after(0, lambda: self.command_input.delete(0, tk.END))
                self.root.after(0, lambda: self.command_input.insert(0, result['text']))
                self.update_output(f"📝 Voice command received: {result['text']}\n\n", "success")
                self.update_status("✅ Ready", self.ACTIVE_GREEN)
                self.root.after(100, self.execute_command)
            else:
                error_msg = result.get('message', 'No command received')
                self.update_output(f"❌ Voice error: {error_msg}\n", "error")
                self.update_status("⚠️ Voice Error", "#f38ba8")

        threading.Thread(target=voice_thread, daemon=True).start()

    def toggle_continuous_listening(self):
        """Toggle continuous voice listening mode"""
        if not self.voice_commander:
            messagebox.showerror("Voice Error", "Voice commander not available")
            return

        if not self.voice_listening:
            result = self.voice_commander.start_continuous_listening()

            if result['success']:
                self.voice_listening = True
                # self.voice_continuous_btn.config(bg=self.ACTIVE_GREEN)

                wake_words = ", ".join(self.voice_commander.get_wake_words()[:3])
                wake_status = ""
                if self.voice_commander.wake_word_enabled:
                    wake_status = f"\n💬 Wake words: {wake_words}\n"

                self.update_output("\n🔊 Continuous voice listening ENABLED\n", "success")
                self.update_output(wake_status, "info")
                self.update_output("Say 'stop listening' to disable\n\n", "info")
                self.update_status("🎤 Voice Active", self.ACTIVE_GREEN)
            else:
                messagebox.showerror("Voice Error", result['message'])
        else:
            result = self.voice_commander.stop_continuous_listening()

            if result['success']:
                self.voice_listening = False
                # self.voice_continuous_btn.config(bg=self.BUTTON_BG)
                self.update_output("\n🔇 Continuous voice listening DISABLED\n", "warning")
                self.update_status("✅ Ready", self.ACTIVE_GREEN)
            else:
                messagebox.showerror("Voice Error", result['message'])

    def toggle_sound_effects(self):
        """Toggle voice sound effects on/off"""
        if not self.voice_commander:
            messagebox.showerror("Voice Error", "Voice commander not available")
            return

        result = self.voice_commander.toggle_sound_effects()

        if result['success']:
            if result['enabled']:
                # self.sound_fx_btn.config(bg=self.ACTIVE_GREEN)
                self.update_output(f"\n🔊 Voice sound effects ENABLED\n", "success")
                self.update_output(f"You'll hear beeps during voice interactions\n", "info")

                if self.voice_commander.sound_effects:
                    self.voice_commander.sound_effects.play_sound('success', async_play=True)
            else:
                # self.sound_fx_btn.config(bg=self.BUTTON_BG)
                self.update_output(f"\n🔇 Voice sound effects DISABLED\n", "warning")
        else:
            messagebox.showerror("Sound Error", result.get('message', 'Error toggling sound effects'))

    def show_sound_settings(self):
        """Show sound effects settings dialog"""
        if not self.voice_commander or not self.voice_commander.sound_effects:
            messagebox.showerror("Sound Error", "Sound effects not available")
            return

        settings_window = tk.Toplevel(self.root)
        settings_window.title("🔊 Sound Effects Settings")
        settings_window.geometry("500x450")
        settings_window.configure(bg=self.BG_PRIMARY)

        header = tk.Label(settings_window,
                          text="🔊 Voice Sound Effects Settings",
                          bg=self.BG_PRIMARY,
                          fg=self.TEXT_PRIMARY,
                          font=("Segoe UI", 16, "bold"),
                          pady=20)
        header.pack()

        status_frame = tk.Frame(settings_window, bg=self.BG_SECONDARY, relief="flat")
        status_frame.pack(fill="x", padx=20, pady=10)

        sounds_list = self.voice_commander.list_sound_effects()
        status_text = "🎵 Available Sound Effects:\n\n"

        if sounds_list['success']:
            for name, info in sounds_list['sounds'].items():
                status = "✅" if info['exists'] else "❌"
                status_text += f"{status} {name.replace('_', ' ').title()}\n"

        status_label = tk.Label(status_frame,
                                text=status_text,
                                bg=self.BG_SECONDARY,
                                fg=self.TEXT_PRIMARY,
                                font=("Segoe UI", 11),
                                justify="left",
                                pady=15,
                                padx=15)
        status_label.pack()

        close_btn = tk.Button(settings_window,
                              text="Close",
                              bg=self.BUTTON_BG,
                              fg=self.TEXT_PRIMARY,
                              font=("Segoe UI", 11, "bold"),
                              relief="raised",
                              cursor="hand2",
                              command=settings_window.destroy,
                              padx=30,
                              pady=10)
        close_btn.pack(pady=20)
        self._add_hover_effect(close_btn, self.BUTTON_BG, self.BUTTON_HOVER)

    def update_status(self, text, color):
        """Update status label"""

        def _update():
            self.status_label.config(text=text, fg=color)

        self.root.after(0, _update)

    # ========== DIALOG METHODS ==========

    def show_help(self):
        """Show help dialog"""
        help_window = tk.Toplevel(self.root)
        help_window.title("❓ Help Guide")
        help_window.geometry("900x700")
        help_window.configure(bg=self.BG_PRIMARY)

        header = tk.Label(help_window,
                          text="🤖 BOI (Barely Obeys Instructions) Desktop Assistant - Help Guide",
                          bg=self.BG_PRIMARY,
                          fg=self.TEXT_PRIMARY,
                          font=("Segoe UI", 16, "bold"),
                          pady=20)
        header.pack()

        text_area = scrolledtext.ScrolledText(help_window,
                                              bg=self.CONSOLE_BG,
                                              fg=self.TEXT_PRIMARY,
                                              font=("Segoe UI", 11),
                                              wrap="word",
                                              padx=20,
                                              pady=20)
        text_area.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        help_text = """
🎯 QUICK START GUIDE

The BOI (Barely Obeys Instructions) Desktop Assistant is your personal AI-powered assistant for automating tasks on your computer.

📋 HOW TO USE:

1. Type a natural language command in the input field
2. Press Enter or click the Execute button
3. View the results in the Output Console

💡 EXAMPLE COMMANDS:

Desktop Control:
• "Take a screenshot"
• "Open notepad"
• "Search Google for Python tutorials"
• "Lock the computer"
• "Open Task Manager"

File Management:
• "Create a folder named Projects"
• "Search for PDF files"
• "Organize desktop files"
• "Move file to Documents"

Voice & Automation:
• Click the 🎤 button to use push-to-talk voice
• Click the 🔊 button for continuous voice listening
• Use V-sign detector for hands-free voice activation

🎯 FEATURES:

✅ Natural Language Processing
✅ Voice Commands
✅ Self-Operating Computer Mode
✅ Desktop Automation
✅ Web Automation with Selenium
✅ File Management
✅ Productivity Tools
✅ Security Dashboard
✅ And 100+ more features!

⌨️ KEYBOARD SHORTCUTS:

• Enter - Execute command
• Ctrl+Return - Quick execute (when enabled)

🛡️ SECURITY:

• All commands are processed securely
• Sensitive data is encrypted
• User confirmation for destructive actions

💬 SUPPORT:

For more information or support, check the About section.
        """

        text_area.insert(1.0, help_text)
        text_area.config(state='disabled')

        close_btn = tk.Button(help_window,
                              text="Close",
                              bg=self.BUTTON_BG,
                              fg=self.TEXT_PRIMARY,
                              font=("Segoe UI", 11, "bold"),
                              relief="raised",
                              cursor="hand2",
                              command=help_window.destroy,
                              padx=30,
                              pady=10)
        close_btn.pack(pady=20)
        self._add_hover_effect(close_btn, self.BUTTON_BG, self.BUTTON_HOVER)

    def show_contacts(self):
        """Show contacts manager"""
        contacts_window = tk.Toplevel(self.root)
        contacts_window.title("👥 Contacts Manager")
        contacts_window.geometry("700x600")
        contacts_window.configure(bg=self.BG_PRIMARY)

        header = tk.Label(contacts_window,
                          text="👥 Contact Manager",
                          bg=self.BG_PRIMARY,
                          fg=self.TEXT_PRIMARY,
                          font=("Segoe UI", 16, "bold"),
                          pady=20)
        header.pack()

        info = tk.Label(contacts_window,
                        text="Manage your contacts for email and messaging automation",
                        bg=self.BG_PRIMARY,
                        fg=self.TEXT_SECONDARY,
                        font=("Segoe UI", 10))
        info.pack()

        text_area = scrolledtext.ScrolledText(contacts_window,
                                              bg=self.CONSOLE_BG,
                                              fg=self.TEXT_PRIMARY,
                                              font=("Segoe UI", 11),
                                              wrap="word",
                                              padx=20,
                                              pady=20)
        text_area.pack(fill="both", expand=True, padx=20, pady=20)

        try:
            command_dict = parse_command("List all contacts")
            result = self.executor.execute(command_dict)
            if result["success"]:
                text_area.insert(1.0, result["message"])
            else:
                text_area.insert(1.0, f"Error: {result['message']}")
        except Exception as e:
            text_area.insert(1.0,
                             f"No contacts found or error loading contacts.\n\nUse the command:\n'Add contact NAME with phone NUMBER and email EMAIL'\n\nError details: {str(e)}")

        close_btn = tk.Button(contacts_window,
                              text="Close",
                              bg=self.BUTTON_BG,
                              fg=self.TEXT_PRIMARY,
                              font=("Segoe UI", 11, "bold"),
                              relief="raised",
                              cursor="hand2",
                              command=contacts_window.destroy,
                              padx=30,
                              pady=10)
        close_btn.pack(pady=20)
        self._add_hover_effect(close_btn, self.BUTTON_BG, self.BUTTON_HOVER)

    def show_about(self):
        """Show about dialog"""
        about_window = tk.Toplevel(self.root)
        about_window.title("ℹ️ About BOI")
        about_window.geometry("700x600")
        about_window.configure(bg=self.BG_PRIMARY)

        header = tk.Label(about_window,
                          text="🤖 BOI - AI Desktop Assistant",
                          bg=self.BG_PRIMARY,
                          fg=self.TEXT_PRIMARY,
                          font=("Segoe UI", 18, "bold"),
                          pady=20)
        header.pack()

        version = tk.Label(about_window,
                           text="Version 2.1.0 - BOI Edition (Powered by BOI)",
                           bg=self.BG_PRIMARY,
                           fg=self.ACCENT_COLOR,
                           font=("Segoe UI", 11))
        version.pack()

        description_frame = tk.Frame(about_window, bg=self.BG_SECONDARY)
        description_frame.pack(fill="both", expand=True, padx=30, pady=30)

        description = tk.Label(description_frame,
                               text="""
⚡ BOI - Your Intelligent Desktop AI Assistant

Powered by Google Gemini AI & BOI Framework

BOI is your intelligent AI assistant with sophisticated 
personality and advanced automation capabilities.

🤖 Features:
• Natural Language Understanding
• Voice Command Support
• Self-Operating Computer Mode
• Desktop & Web Automation
• Productivity Tools & Dashboards
• Security & Privacy Features

💡 Technology Stack:
• Google Gemini AI
• Python 3.11
• Tkinter GUI
• OpenCV
• Selenium WebDriver
• And many more...

🌟 Created by the BOI Team

© 2024 BOI. All rights reserved.
                               """,
                               bg=self.BG_SECONDARY,
                               fg=self.TEXT_PRIMARY,
                               font=("Segoe UI", 11),
                               justify="left")
        description.pack(padx=20, pady=20)

        close_btn = tk.Button(about_window,
                              text="Close",
                              bg=self.BUTTON_BG,
                              fg=self.TEXT_PRIMARY,
                              font=("Segoe UI", 11, "bold"),
                              relief="raised",
                              cursor="hand2",
                              command=about_window.destroy,
                              padx=30,
                              pady=10)
        close_btn.pack(pady=20)
        self._add_hover_effect(close_btn, self.BUTTON_BG, self.BUTTON_HOVER)

    def show_suggestion(self):
        """Show BOI proactive suggestion"""
        if self.boi:
            suggestion = self.boi.get_proactive_suggestion()
            self.update_output(f"\n{suggestion}\n\n", "info")
        else:
            self.update_output("\n💡 BOI (Barely Obeys Instructions) is not available for suggestions\n\n", "warning")

    def show_security_dashboard(self):
        """Display AI-Powered Security Dashboard"""
        if not self.security_dashboard:
            messagebox.showerror("Error", "Security Dashboard not initialized")
            return

        sec_window = tk.Toplevel(self.root)
        sec_window.title("🛡️ AI-Powered Security Dashboard")
        sec_window.geometry("1000x700")
        sec_window.configure(bg=self.BG_PRIMARY)

        header_frame = tk.Frame(sec_window, bg=self.BG_SECONDARY)
        header_frame.pack(fill="x", pady=(0, 10))

        header = tk.Label(header_frame,
                          text="🛡️ Security Dashboard with Gemini AI",
                          bg=self.BG_SECONDARY,
                          fg="#f38ba8",
                          font=("Segoe UI", 18, "bold"),
                          pady=15)
        header.pack()

        subtitle = tk.Label(header_frame,
                            text="🤖 AI-Powered Threat Analysis • 🔐 Enhanced Security Features",
                            bg=self.BG_SECONDARY,
                            fg=self.TEXT_SECONDARY,
                            font=("Segoe UI", 10, "italic"))
        subtitle.pack()

        main_frame = tk.Frame(sec_window, bg=self.BG_PRIMARY)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        text_area = scrolledtext.ScrolledText(main_frame,
                                              bg=self.CONSOLE_BG,
                                              fg=self.TEXT_PRIMARY,
                                              font=("Segoe UI", 11),
                                              wrap="word",
                                              padx=20,
                                              pady=20)
        text_area.pack(fill="both", expand=True)

        try:
            if hasattr(self.security_dashboard, 'get_security_status'):
                status = self.security_dashboard.get_security_status()
                text_area.insert(1.0, f"Security Status: {status}\n\n")
            else:
                text_area.insert(1.0, "🛡️ Security Dashboard\n\n")
                text_area.insert(tk.END, "Security features are available.\n\n")
            text_area.insert(tk.END, "For full security features, please use the command:\n")
            text_area.insert(tk.END, "'Show security dashboard' or 'Run security scan'\n")
        except Exception as e:
            text_area.insert(1.0, f"Security Dashboard:\n\nError loading: {str(e)}\n")

        close_btn = tk.Button(sec_window,
                              text="Close",
                              bg=self.BUTTON_BG,
                              fg=self.TEXT_PRIMARY,
                              font=("Segoe UI", 11, "bold"),
                              relief="raised",
                              cursor="hand2",
                              command=sec_window.destroy,
                              padx=30,
                              pady=10)
        close_btn.pack(pady=20)
        self._add_hover_effect(close_btn, self.BUTTON_BG, self.BUTTON_HOVER)

    def show_batch_utilities(self):
        """Show comprehensive batch utilities menu"""
        if not self.batch_utilities:
            messagebox.showerror("Error", "Batch Utilities not initialized")
            return

        batch_window = tk.Toplevel(self.root)
        batch_window.title("🔧 Batch Utilities")
        batch_window.geometry("1000x700")
        batch_window.configure(bg=self.BG_PRIMARY)

        header_frame = tk.Frame(batch_window, bg=self.BG_SECONDARY)
        header_frame.pack(fill="x", pady=(0, 10))

        header = tk.Label(header_frame,
                          text="🔧 Batch Utilities - System Control & Automation",
                          bg=self.BG_SECONDARY,
                          fg=self.TEXT_PRIMARY,
                          font=("Segoe UI", 18, "bold"),
                          pady=15)
        header.pack()

        subtitle = tk.Label(header_frame,
                            text="Python implementations of all batch file functionalities",
                            bg=self.BG_SECONDARY,
                            fg=self.TEXT_SECONDARY,
                            font=("Segoe UI", 10, "italic"))
        subtitle.pack()

        # Create notebook for categorized utilities
        notebook = ttk.Notebook(batch_window)
        notebook.pack(fill="both", expand=True, padx=20, pady=10)

        # System Control Tab
        sys_frame = tk.Frame(notebook, bg=self.BG_PRIMARY)
        notebook.add(sys_frame, text="⚙️ System Control")
        self._create_system_control_tab(sys_frame)

        # File Management Tab
        file_frame = tk.Frame(notebook, bg=self.BG_PRIMARY)
        notebook.add(file_frame, text="📁 File Management")
        self._create_file_management_tab(file_frame)

        # Network Tab
        net_frame = tk.Frame(notebook, bg=self.BG_PRIMARY)
        notebook.add(net_frame, text="🌐 Network")
        self._create_network_tab(net_frame)

        # Maintenance Tab
        maint_frame = tk.Frame(notebook, bg=self.BG_PRIMARY)
        notebook.add(maint_frame, text="🔧 Maintenance")
        self._create_maintenance_tab(maint_frame)

        close_btn = tk.Button(batch_window,
                              text="Close",
                              bg=self.BUTTON_BG,
                              fg=self.TEXT_PRIMARY,
                              font=("Segoe UI", 11, "bold"),
                              relief="raised",
                              cursor="hand2",
                              command=batch_window.destroy,
                              padx=30,
                              pady=10)
        close_btn.pack(pady=20)
        self._add_hover_effect(close_btn, self.BUTTON_BG, self.BUTTON_HOVER)

    def show_phone_link_control(self):
        """Show Phone Link Control & Contact Management"""
        if not self.phone_dialer:
            messagebox.showerror("Error", "Phone Link not initialized")
            return

        phone_window = tk.Toplevel(self.root)
        phone_window.title("📞 Phone Link Control")
        phone_window.geometry("1000x700")
        phone_window.configure(bg=self.BG_PRIMARY)

        header_frame = tk.Frame(phone_window, bg=self.BG_SECONDARY)
        header_frame.pack(fill="x", pady=(0, 10))

        header = tk.Label(header_frame,
                          text="📞 Phone Link Control - Windows Phone Integration",
                          bg=self.BG_SECONDARY,
                          fg=self.TEXT_PRIMARY,
                          font=("Segoe UI", 18, "bold"),
                          pady=15)
        header.pack()

        subtitle = tk.Label(header_frame,
                            text="Call contacts by name • Automatic dialing • Contact management",
                            bg=self.BG_SECONDARY,
                            fg=self.TEXT_SECONDARY,
                            font=("Segoe UI", 10, "italic"))
        subtitle.pack()

        # Main container
        main_frame = tk.Frame(phone_window, bg=self.BG_PRIMARY)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Left panel - Quick Call
        left_panel = tk.Frame(main_frame, bg=self.BG_SECONDARY, relief="raised", bd=2)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Quick Call Section
        call_header = tk.Label(left_panel,
                               text="📱 Quick Call",
                               bg=self.BG_SECONDARY,
                               fg=self.TEXT_PRIMARY,
                               font=("Segoe UI", 14, "bold"),
                               pady=10)
        call_header.pack()

        # Call by name input
        name_frame = tk.Frame(left_panel, bg=self.BG_SECONDARY)
        name_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(name_frame,
                 text="Contact Name:",
                 bg=self.BG_SECONDARY,
                 fg=self.TEXT_PRIMARY,
                 font=("Segoe UI", 11)).pack(anchor="w", pady=(0, 5))

        self.phone_name_input = tk.Entry(name_frame,
                                         bg="white",
                                         fg=self.TEXT_PRIMARY,
                                         font=("Segoe UI", 12),
                                         relief="solid",
                                         bd=1)
        self.phone_name_input.pack(fill="x", ipady=8)

        # Or separator
        tk.Label(left_panel,
                 text="— OR —",
                 bg=self.BG_SECONDARY,
                 fg=self.TEXT_SECONDARY,
                 font=("Segoe UI", 9)).pack(pady=5)

        # Call by number input
        number_frame = tk.Frame(left_panel, bg=self.BG_SECONDARY)
        number_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(number_frame,
                 text="Phone Number:",
                 bg=self.BG_SECONDARY,
                 fg=self.TEXT_PRIMARY,
                 font=("Segoe UI", 11)).pack(anchor="w", pady=(0, 5))

        self.phone_number_input = tk.Entry(number_frame,
                                           bg="white",
                                           fg=self.TEXT_PRIMARY,
                                           font=("Segoe UI", 12),
                                           relief="solid",
                                           bd=1)
        self.phone_number_input.pack(fill="x", ipady=8)

        # Call button
        call_btn = tk.Button(left_panel,
                             text="📞 Call Now (Auto-Dial)",
                             bg=self.ACTIVE_GREEN,
                             fg="white",
                             font=("Segoe UI", 13, "bold"),
                             relief="raised",
                             cursor="hand2",
                             command=self.make_phone_call,
                             padx=30,
                             pady=15)
        call_btn.pack(pady=20)
        self._add_hover_effect(call_btn, self.ACTIVE_GREEN, "#006644")

        # Call history
        history_label = tk.Label(left_panel,
                                 text="📜 Recent Calls",
                                 bg=self.BG_SECONDARY,
                                 fg=self.TEXT_PRIMARY,
                                 font=("Segoe UI", 12, "bold"))
        history_label.pack(pady=(10, 5))

        self.phone_history_text = scrolledtext.ScrolledText(left_panel,
                                                            bg=self.CONSOLE_BG,
                                                            fg=self.TEXT_PRIMARY,
                                                            font=("Segoe UI", 9),
                                                            wrap="word",
                                                            height=8,
                                                            relief="solid",
                                                            bd=1)
        self.phone_history_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Right panel - Contact Manager
        right_panel = tk.Frame(main_frame, bg=self.BG_SECONDARY, relief="raised", bd=2)
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))

        contact_header = tk.Label(right_panel,
                                  text="📇 Contacts",
                                  bg=self.BG_SECONDARY,
                                  fg=self.TEXT_PRIMARY,
                                  font=("Segoe UI", 14, "bold"),
                                  pady=10)
        contact_header.pack()

        # Search contacts
        search_frame = tk.Frame(right_panel, bg=self.BG_SECONDARY)
        search_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(search_frame,
                 text="Search:",
                 bg=self.BG_SECONDARY,
                 fg=self.TEXT_PRIMARY,
                 font=("Segoe UI", 10)).pack(side="left", padx=(0, 10))

        self.contact_search_input = tk.Entry(search_frame,
                                             bg="white",
                                             fg=self.TEXT_PRIMARY,
                                             font=("Segoe UI", 10),
                                             relief="solid",
                                             bd=1)
        self.contact_search_input.pack(side="left", fill="x", expand=True, ipady=5)
        self.contact_search_input.bind("<KeyRelease>", lambda e: self.search_contacts())

        # Contact list
        contacts_frame = tk.Frame(right_panel, bg=self.BG_SECONDARY)
        contacts_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.contacts_listbox = tk.Listbox(contacts_frame,
                                           bg="white",
                                           fg=self.TEXT_PRIMARY,
                                           font=("Segoe UI", 10),
                                           relief="solid",
                                           bd=1,
                                           selectmode=tk.SINGLE)
        self.contacts_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(contacts_frame, command=self.contacts_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.contacts_listbox.config(yscrollcommand=scrollbar.set)

        # Double-click to call
        self.contacts_listbox.bind("<Double-Button-1>", self.call_selected_contact)

        # Contact management buttons
        btn_frame = tk.Frame(right_panel, bg=self.BG_SECONDARY)
        btn_frame.pack(fill="x", padx=20, pady=(10, 20))

        buttons = [
            ("➕ Add", self.add_contact),
            ("✏️ Edit", self.edit_contact),
            ("🗑️ Delete", self.delete_contact),
            ("🔄 Refresh", self.refresh_contacts),
        ]

        for text, command in buttons:
            btn = tk.Button(btn_frame,
                            text=text,
                            bg=self.BUTTON_BG,
                            fg=self.TEXT_PRIMARY,
                            font=("Segoe UI", 9, "bold"),
                            relief="raised",
                            cursor="hand2",
                            command=command,
                            padx=10,
                            pady=5)
            btn.pack(side="left", padx=5, expand=True, fill="x")
            self._add_hover_effect(btn, self.BUTTON_BG, self.BUTTON_HOVER)

        # Load initial contacts
        self.refresh_contacts()

        # Close button
        close_btn = tk.Button(phone_window,
                              text="Close",
                              bg=self.BUTTON_BG,
                              fg=self.TEXT_PRIMARY,
                              font=("Segoe UI", 11, "bold"),
                              relief="raised",
                              cursor="hand2",
                              command=phone_window.destroy,
                              padx=30,
                              pady=10)
        close_btn.pack(pady=10)
        self._add_hover_effect(close_btn, self.BUTTON_BG, self.BUTTON_HOVER)

    def _create_system_control_tab(self, parent):
        """Create system control utilities tab"""
        scroll = scrolledtext.ScrolledText(parent, bg=self.CONSOLE_BG, fg=self.TEXT_PRIMARY,
                                           font=("Segoe UI", 10), wrap="word", padx=20, pady=20)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        buttons_frame = tk.Frame(parent, bg=self.BG_PRIMARY)
        buttons_frame.pack(fill="x", padx=10, pady=10)

        system_tools = [
            ("💻 System Info", lambda: self._batch_action(scroll, self.batch_utilities.get_system_info)),
            ("🔋 Battery Info", lambda: self._batch_action(scroll, self.batch_utilities.get_battery_info)),
            ("📸 Screenshot", lambda: self._batch_screenshot(scroll)),
            ("📋 Processes", lambda: self._batch_action(scroll, self.batch_utilities.get_process_list)),
            ("⚡ Power Options", lambda: self._batch_power_menu(scroll)),
            ("🔊 Volume Control", lambda: self._batch_volume_menu(scroll))
        ]

        for i, (text, command) in enumerate(system_tools):
            btn = tk.Button(buttons_frame, text=text, command=command, bg=self.BUTTON_BG,
                            fg=self.TEXT_PRIMARY, font=("Segoe UI", 10, "bold"),
                            relief="raised", cursor="hand2", padx=15, pady=8)
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky="ew")
            self._add_hover_effect(btn, self.BUTTON_BG, self.BUTTON_HOVER)

        for i in range(3):
            buttons_frame.columnconfigure(i, weight=1)

    def _create_file_management_tab(self, parent):
        """Create file management utilities tab"""
        scroll = scrolledtext.ScrolledText(parent, bg=self.CONSOLE_BG, fg=self.TEXT_PRIMARY,
                                           font=("Segoe UI", 10), wrap="word", padx=20, pady=20)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        buttons_frame = tk.Frame(parent, bg=self.BG_PRIMARY)
        buttons_frame.pack(fill="x", padx=10, pady=10)

        file_tools = [
            ("📂 Organize Downloads", lambda: self._batch_action(scroll, self.batch_utilities.organize_downloads)),
            ("🔍 Search Files", lambda: self._batch_search_files(scroll)),
            ("🔄 Find Duplicates", lambda: self._batch_find_duplicates(scroll)),
            ("💾 Create Backup", lambda: self._batch_create_backup(scroll))
        ]

        for i, (text, command) in enumerate(file_tools):
            btn = tk.Button(buttons_frame, text=text, command=command, bg=self.BUTTON_BG,
                            fg=self.TEXT_PRIMARY, font=("Segoe UI", 10, "bold"),
                            relief="raised", cursor="hand2", padx=15, pady=8)
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky="ew")
            self._add_hover_effect(btn, self.BUTTON_BG, self.BUTTON_HOVER)

        for i in range(3):
            buttons_frame.columnconfigure(i, weight=1)

    def _create_network_tab(self, parent):
        """Create network utilities tab"""
        scroll = scrolledtext.ScrolledText(parent, bg=self.CONSOLE_BG, fg=self.TEXT_PRIMARY,
                                           font=("Segoe UI", 10), wrap="word", padx=20, pady=20)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        buttons_frame = tk.Frame(parent, bg=self.BG_PRIMARY)
        buttons_frame.pack(fill="x", padx=10, pady=10)

        net_tools = [
            ("🌐 Network Info", lambda: self._batch_action(scroll, self.batch_utilities.get_network_info)),
            ("🔗 Active Connections", lambda: self._batch_action(scroll, self.batch_utilities.get_active_connections)),
            ("⚡ Speed Test", lambda: self._batch_action(scroll, self.batch_utilities.test_network_speed))
        ]

        for i, (text, command) in enumerate(net_tools):
            btn = tk.Button(buttons_frame, text=text, command=command, bg=self.BUTTON_BG,
                            fg=self.TEXT_PRIMARY, font=("Segoe UI", 10, "bold"),
                            relief="raised", cursor="hand2", padx=15, pady=8)
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky="ew")
            self._add_hover_effect(btn, self.BUTTON_BG, self.BUTTON_HOVER)

        for i in range(3):
            buttons_frame.columnconfigure(i, weight=1)

    def _create_maintenance_tab(self, parent):
        """Create maintenance utilities tab"""
        scroll = scrolledtext.ScrolledText(parent, bg=self.CONSOLE_BG, fg=self.TEXT_PRIMARY,
                                           font=("Segoe UI", 10), wrap="word", padx=20, pady=20)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        buttons_frame = tk.Frame(parent, bg=self.BG_PRIMARY)
        buttons_frame.pack(fill="x", padx=10, pady=10)

        maint_tools = [
            ("🗑️ Disk Cleanup", lambda: self._batch_disk_cleanup(scroll)),
            ("🚀 Startup Programs", lambda: self._batch_action(scroll, self.batch_utilities.get_startup_programs)),
            ("🌐 Browser Cleanup", lambda: self._batch_browser_cleanup(scroll)),
            ("❌ Kill Process", lambda: self._batch_kill_process(scroll))
        ]

        for i, (text, command) in enumerate(maint_tools):
            btn = tk.Button(buttons_frame, text=text, command=command, bg=self.BUTTON_BG,
                            fg=self.TEXT_PRIMARY, font=("Segoe UI", 10, "bold"),
                            relief="raised", cursor="hand2", padx=15, pady=8)
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky="ew")
            self._add_hover_effect(btn, self.BUTTON_BG, self.BUTTON_HOVER)

        for i in range(3):
            buttons_frame.columnconfigure(i, weight=1)

    def _batch_action(self, output_widget, action_func):
        """Execute a batch action and display results (with threading for long operations)"""

        def update_processing():
            output_widget.config(state="normal")
            output_widget.delete(1.0, tk.END)
            output_widget.insert(1.0, "⏳ Processing...\n\n")
            output_widget.config(state="disabled")

        def execute_and_display():
            try:
                result = action_func()

                # Update UI from main thread
                self.root.after(0, lambda: self._display_batch_result(output_widget, result))
            except Exception as e:
                error_result = {"success": False, "error": str(e)}
                self.root.after(0, lambda: self._display_batch_result(output_widget, error_result))

        # Update processing message
        update_processing()

        # Execute in background thread to prevent UI freezing
        thread = threading.Thread(target=execute_and_display, daemon=True)
        thread.start()

    def _display_batch_result(self, output_widget, result):
        """Display batch action result in output widget (call from main thread)"""
        try:
            output_widget.config(state="normal")
            output_widget.delete(1.0, tk.END)

            if result.get("success"):
                output_widget.insert(1.0, "✅ SUCCESS\n\n", "success")
                if "info" in result:
                    for key, value in result["info"].items():
                        output_widget.insert(tk.END, f"{key}: {value}\n")
                elif "processes" in result:
                    output_widget.insert(tk.END, f"Top {len(result['processes'])} Processes:\n\n")
                    for proc in result["processes"]:
                        output_widget.insert(tk.END,
                                             f"PID: {proc['PID']} | {proc['Name']} | CPU: {proc['CPU']} | Mem: {proc['Memory']}\n")
                elif "connections" in result:
                    output_widget.insert(tk.END, f"Active Connections ({len(result['connections'])}):\n\n")
                    for conn in result["connections"]:
                        output_widget.insert(tk.END, f"{conn['Local']} → {conn['Remote']} | Status: {conn['Status']}\n")
                elif "result" in result:
                    output_widget.insert(tk.END, result["result"])
                elif "message" in result:
                    output_widget.insert(tk.END, result["message"] + "\n")
                    if "files" in result:
                        output_widget.insert(tk.END, "\nFiles processed:\n")
                        for file in result["files"][:20]:
                            output_widget.insert(tk.END, f"  • {file}\n")
                    if "duplicates" in result:
                        output_widget.insert(tk.END, f"\nDuplicates found: {len(result['duplicates'])}\n")
                        for dup in result["duplicates"][:10]:
                            output_widget.insert(tk.END, f"  • {dup['duplicate']}\n    (original: {dup['original']})\n")
                    if "results" in result and "count" in result:
                        output_widget.insert(tk.END, f"\nSearch Results ({result['count']}):\n")
                        for item in result["results"][:20]:
                            output_widget.insert(tk.END,
                                                 f"  • {item['name']} ({item['type']})\n    Path: {item['path']}\n")
            else:
                output_widget.insert(1.0, f"❌ ERROR: {result.get('error', 'Unknown error')}\n")

            output_widget.config(state="disabled")
        except Exception as e:
            output_widget.config(state="normal")
            output_widget.delete(1.0, tk.END)
            output_widget.insert(1.0, f"❌ ERROR: {str(e)}\n")
            output_widget.config(state="disabled")

    def _batch_screenshot(self, output_widget):
        """Take a screenshot with optional delay"""
        delay = messagebox.askquestion("Screenshot", "Add 5 second delay?")
        delay_time = 5 if delay == "yes" else 0

        # Update UI from main thread
        output_widget.config(state="normal")
        output_widget.delete(1.0, tk.END)
        if delay_time > 0:
            output_widget.insert(1.0, f"⏳ Taking screenshot in {delay_time} seconds...\n")
        else:
            output_widget.insert(1.0, "⏳ Taking screenshot...\n")
        output_widget.config(state="disabled")

        # Use threading to avoid blocking UI during delay
        def take_screenshot_threaded():
            result = self.batch_utilities.take_screenshot(delay=delay_time)
            # Update UI from main thread via after()
            self.root.after(0, lambda: self._display_batch_result(output_widget, result))

        thread = threading.Thread(target=take_screenshot_threaded, daemon=True)
        thread.start()

    def _batch_power_menu(self, output_widget):
        """Show power options menu"""
        power_window = tk.Toplevel(self.root)
        power_window.title("⚡ Power Options")
        power_window.geometry("400x400")
        power_window.configure(bg=self.BG_PRIMARY)

        tk.Label(power_window, text="⚡ Power Options", bg=self.BG_PRIMARY,
                 fg=self.TEXT_PRIMARY, font=("Segoe UI", 14, "bold"), pady=20).pack()

        options = [
            ("🔌 Shutdown", "shutdown"),
            ("🔄 Restart", "restart"),
            ("💤 Sleep", "sleep"),
            ("🔒 Lock", "lock"),
            ("📴 Hibernate", "hibernate"),
            ("🚪 Logoff", "logoff")
        ]

        for text, option in options:
            btn = tk.Button(power_window, text=text,
                            command=lambda o=option: self._execute_power_option(o, output_widget, power_window),
                            bg=self.BUTTON_BG, fg=self.TEXT_PRIMARY,
                            font=("Segoe UI", 11, "bold"), relief="raised",
                            cursor="hand2", padx=20, pady=10, width=20)
            btn.pack(pady=5)
            self._add_hover_effect(btn, self.BUTTON_BG, self.BUTTON_HOVER)

    def _execute_power_option(self, option, output_widget, window):
        """Execute power option with confirmation"""
        if messagebox.askyesno("Confirm", f"Are you sure you want to {option}?"):
            window.destroy()
            result = self.batch_utilities.power_options(option)
            self._batch_action(output_widget, lambda: result)

    def _batch_volume_menu(self, output_widget):
        """Show volume control menu"""
        vol_window = tk.Toplevel(self.root)
        vol_window.title("🔊 Volume Control")
        vol_window.geometry("400x300")
        vol_window.configure(bg=self.BG_PRIMARY)

        tk.Label(vol_window, text="🔊 Volume Control", bg=self.BG_PRIMARY,
                 fg=self.TEXT_PRIMARY, font=("Segoe UI", 14, "bold"), pady=20).pack()

        options = [
            ("🔊 Volume Up", "up"),
            ("🔉 Volume Down", "down"),
            ("🔇 Mute/Unmute", "mute"),
            ("📊 Set to 50%", "set_50")
        ]

        for text, action in options:
            if action == "set_50":
                btn = tk.Button(vol_window, text=text,
                                command=lambda: self._execute_volume(output_widget, "set", 50, vol_window),
                                bg=self.BUTTON_BG, fg=self.TEXT_PRIMARY,
                                font=("Segoe UI", 11, "bold"), relief="raised",
                                cursor="hand2", padx=20, pady=10, width=20)
            else:
                btn = tk.Button(vol_window, text=text,
                                command=lambda a=action: self._execute_volume(output_widget, a, None, vol_window),
                                bg=self.BUTTON_BG, fg=self.TEXT_PRIMARY,
                                font=("Segoe UI", 11, "bold"), relief="raised",
                                cursor="hand2", padx=20, pady=10, width=20)
            btn.pack(pady=5)
            self._add_hover_effect(btn, self.BUTTON_BG, self.BUTTON_HOVER)

    def _execute_volume(self, output_widget, action, value, window):
        """Execute volume control"""
        window.destroy()
        result = self.batch_utilities.volume_control(action, value)
        self._batch_action(output_widget, lambda: result)

    def _batch_search_files(self, output_widget):
        """Search for files"""
        pattern = tk.simpledialog.askstring("Search Files", "Enter search pattern:")
        if pattern:
            result = self.batch_utilities.search_files(pattern)
            self._batch_action(output_widget, lambda: result)

    def _batch_find_duplicates(self, output_widget):
        """Find duplicate files"""
        if messagebox.askyesno("Find Duplicates", "Search in Downloads folder?"):
            result = self.batch_utilities.find_duplicates()
        else:
            directory = filedialog.askdirectory(title="Select Directory")
            if directory:
                result = self.batch_utilities.find_duplicates(directory)
            else:
                return
        self._batch_action(output_widget, lambda: result)

    def _batch_create_backup(self, output_widget):
        """Create a backup"""
        source = filedialog.askdirectory(title="Select Source Directory")
        if source:
            result = self.batch_utilities.create_backup(source)
            self._batch_action(output_widget, lambda: result)

    def _batch_disk_cleanup(self, output_widget):
        """Perform disk cleanup with confirmation"""
        if messagebox.askyesno("Disk Cleanup", "This will clean temporary files. Continue?"):
            result = self.batch_utilities.disk_cleanup()
            self._batch_action(output_widget, lambda: result)

    def _batch_browser_cleanup(self, output_widget):
        """Perform browser cleanup with confirmation"""
        if messagebox.askyesno("Browser Cleanup", "This will clean browser cache. Continue?"):
            result = self.batch_utilities.browser_cleanup()
            self._batch_action(output_widget, lambda: result)

    def _batch_kill_process(self, output_widget):
        """Kill a process"""
        pid_or_name = tk.simpledialog.askstring("Kill Process", "Enter PID or process name:")
        if pid_or_name:
            if messagebox.askyesno("Confirm", f"Kill process '{pid_or_name}'?"):
                result = self.batch_utilities.kill_process(pid_or_name)
                self._batch_action(output_widget, lambda: result)

    def handle_voice_command(self, command):
        """Handle voice command callback"""
        self.root.after(0, lambda: self.command_input.delete(0, tk.END))
        self.root.after(0, lambda: self.command_input.insert(0, command))
        self.root.after(0, self.execute_command)

    def _orchestrator_status_update(self, message):
        """Callback for orchestrator status updates (thread-safe)"""

        def update_ui():
            # Update chat display if it exists
            if hasattr(self, 'boi_conversation_display'):
                self.boi_conversation_display.config(state='normal')
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.boi_conversation_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
                self.boi_conversation_display.insert(tk.END, "🤖 Auto: ", "boi")
                self.boi_conversation_display.insert(tk.END, f"{message}\n")
                self.boi_conversation_display.see(tk.END)
                self.boi_conversation_display.config(state='disabled')

        self.root.after(0, update_ui)

    def _orchestrator_task_complete(self, task):
        """Callback when orchestrator completes a task (thread-safe)"""

        def update_ui():
            if hasattr(self, 'boi_conversation_display'):
                self.boi_conversation_display.config(state='normal')
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.boi_conversation_display.insert(tk.END, f"[{timestamp}] ", "timestamp")

                if task.state.value == "completed":
                    self.boi_conversation_display.insert(tk.END, "✅ Task Complete: ", "boi")
                    self.boi_conversation_display.insert(tk.END, f"{task.intent}\n")
                    if task.result:
                        self.boi_conversation_display.insert(tk.END, f"Result: {task.result}\n")
                else:
                    self.boi_conversation_display.insert(tk.END, "❌ Task Failed: ", "boi")
                    self.boi_conversation_display.insert(tk.END, f"{task.intent}\n")
                    if task.error:
                        self.boi_conversation_display.insert(tk.END, f"Error: {task.error}\n")

                self.boi_conversation_display.see(tk.END)
                self.boi_conversation_display.config(state='disabled')

        self.root.after(0, update_ui)

    def _orchestrator_confirm_task(self, intent, command):
        """Callback to confirm potentially destructive tasks (thread-safe)"""
        result = messagebox.askyesno(
            "Autonomous Task Confirmation",
            f"The autonomous system wants to execute:\n\n"
            f"Task: {intent}\n"
            f"Command: {command}\n\n"
            f"This action may make changes to your system.\n"
            f"Do you want to proceed?"
        )
        return result

    def create_boi_ai_tab(self, notebook):
        """Simple BOI Chatbot"""
        tab = tk.Frame(notebook, bg="#1a1d2e")
        notebook.add(tab, text="💬 BOI Chat")

        header_frame = tk.Frame(tab, bg="#252941")
        header_frame.pack(fill="x", pady=(10, 0), padx=10)

        header = tk.Label(header_frame,
                          text="💬 BOI - Simple AI Chatbot",
                          bg="#252941",
                          fg="#00d4aa",
                          font=("Segoe UI", 14, "bold"))
        header.pack(pady=12)

        info = tk.Label(header_frame,
                        text="For direct and Quick Questions and Answers , giveing bot",
                        bg="#252941",
                        fg="#b0b0b0",
                        font=("Segoe UI", 9, "italic"))
        info.pack(pady=(0, 12))

        self.boi_conversation_display = scrolledtext.ScrolledText(
            tab,
            bg="#16182a",
            fg="#e0e0e0",
            font=("Consolas", 10),
            wrap=tk.WORD,
            state='disabled',
            relief="flat",
            padx=10,
            pady=10
        )
        self.boi_conversation_display.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        self.boi_conversation_display.tag_config("boi", foreground="#89b4fa", font=("Consolas", 10, "bold"))
        self.boi_conversation_display.tag_config("user", foreground="#a6e3a1", font=("Consolas", 10, "bold"))
        self.boi_conversation_display.tag_config("timestamp", foreground="#6c7086", font=("Consolas", 8))

        input_frame = tk.Frame(tab, bg="#1a1d2e")
        input_frame.pack(fill="x", padx=10, pady=5)

        input_label = tk.Label(input_frame,
                               text="💬 Type your message:",
                               bg="#1a1d2e",
                               fg="#b0b0b0",
                               font=("Segoe UI", 9, "bold"))
        input_label.pack(anchor="w", padx=5, pady=(5, 2))

        input_box_frame = tk.Frame(input_frame, bg="#1a1d2e")
        input_box_frame.pack(fill="x", padx=5, pady=(0, 5))

        self.boi_input = tk.Entry(input_box_frame,
                                     bg="#2e3350",
                                     fg="#e0e0e0",
                                     font=("Segoe UI", 12),
                                     relief="solid",
                                     bd=2,
                                     insertbackground="#00d4aa")
        self.boi_input.pack(side="left", fill="x", expand=True, ipady=10)
        self.boi_input.bind("<Return>", lambda e: self.send_to_boi_ai())

        send_btn = tk.Button(input_box_frame,
                             text="➤ Send",
                             bg="#00d4aa",
                             fg="#0f0f1e",
                             font=("Segoe UI", 11, "bold"),
                             relief="flat",
                             cursor="hand2",
                             command=self.send_to_boi_ai,
                             padx=25,
                             pady=10)
        send_btn.pack(side="right", padx=(5, 0))
        self.add_hover_effect(send_btn, "#89b4fa", "#74c7ec")

        button_frame = tk.Frame(tab, bg="#1a1d2e")
        button_frame.pack(fill="x", padx=10, pady=(0, 10))

        start_btn = tk.Button(button_frame,
                              text="▶️ Start Conversation",
                              bg="#2e3350",
                              fg="#e0e0e0",
                              font=("Segoe UI", 9, "bold"),
                              relief="flat",
                              cursor="hand2",
                              command=self.start_boi_ai_conversation,
                              padx=15,
                              pady=8)
        start_btn.pack(side="left", padx=5)
        self.add_hover_effect(start_btn, "#313244", "#45475a")

        suggest_btn = tk.Button(button_frame,
                                text="💡 Help Me Start",
                                bg="#2e3350",
                                fg="#e0e0e0",
                                font=("Segoe UI", 9, "bold"),
                                relief="flat",
                                cursor="hand2",
                                command=self.boi_ai_get_suggestion,
                                padx=15,
                                pady=8)
        suggest_btn.pack(side="left", padx=5)
        self.add_hover_effect(suggest_btn, "#313244", "#45475a")

        clear_btn = tk.Button(button_frame,
                              text="🗑️ Clear Chat",
                              bg="#2e3350",
                              fg="#e0e0e0",
                              font=("Segoe UI", 9, "bold"),
                              relief="flat",
                              cursor="hand2",
                              command=self.clear_boi_ai_conversation,
                              padx=15,
                              pady=8)
        clear_btn.pack(side="left", padx=5)
        self.add_hover_effect(clear_btn, "#313244", "#45475a")

        stats_btn = tk.Button(button_frame,
                              text="📊 View Stats",
                              bg="#2e3350",
                              fg="#e0e0e0",
                              font=("Segoe UI", 9, "bold"),
                              relief="flat",
                              cursor="hand2",
                              command=self.show_boi_ai_stats,
                              padx=15,
                              pady=8)
        stats_btn.pack(side="left", padx=5)
        self.add_hover_effect(stats_btn, "#313244", "#45475a")

    def create_boi_automator_tab(self, notebook):
        """BOI Intelligent Desktop Automator - Local execution with AI understanding"""
        tab = tk.Frame(notebook, bg="#1a1d2e")
        notebook.add(tab, text="⚡ BOI Auto")

        header_frame = tk.Frame(tab, bg="#252941")
        header_frame.pack(fill="x", pady=(10, 0), padx=10)

        header = tk.Label(header_frame,
                          text="⚡ BOI Desktop Automator",
                          bg="#252941",
                          fg="#f9e2af",
                          font=("Segoe UI", 14, "bold"))
        header.pack(pady=12)

        info = tk.Label(header_frame,
                        text="🤖 AI Understanding • 💻 Local Execution • ⚠️ Safe Confirmations",
                        bg="#252941",
                        fg="#b0b0b0",
                        font=("Segoe UI", 9, "italic"))
        info.pack(pady=(0, 12))

        description_frame = tk.Frame(tab, bg="#1a1d2e")
        description_frame.pack(fill="x", padx=10, pady=5)

        desc_text = tk.Label(description_frame,
                             text="Intelligent desktop automation that uses Gemini only for understanding commands.\nAll actions execute locally via Python modules. Destructive actions require confirmation.",
                             bg="#1a1d2e",
                             fg="#b0b0b0",
                             font=("Segoe UI", 9),
                             justify="left")
        desc_text.pack(anchor="w", padx=10, pady=5)

        self.boi_automator_output = scrolledtext.ScrolledText(
            tab,
            bg="#16182a",
            fg="#e0e0e0",
            font=("Consolas", 10),
            wrap=tk.WORD,
            height=10,
            state='disabled',
            relief="flat",
            padx=10,
            pady=10
        )
        self.boi_automator_output.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        self.boi_automator_output.tag_config("success", foreground="#a6e3a1")
        self.boi_automator_output.tag_config("error", foreground="#f38ba8")
        self.boi_automator_output.tag_config("warning", foreground="#f9e2af")
        self.boi_automator_output.tag_config("info", foreground="#89b4fa")

        input_frame = tk.Frame(tab, bg="#1a1d2e")
        input_frame.pack(fill="x", padx=10, pady=5)

        input_label = tk.Label(input_frame,
                               text="💬 Command (e.g., 'Open notepad and type Hello', 'Show system info'):",
                               bg="#1a1d2e",
                               fg="#b0b0b0",
                               font=("Segoe UI", 9, "bold"))
        input_label.pack(anchor="w", padx=5, pady=(5, 2))

        input_box_frame = tk.Frame(input_frame, bg="#1a1d2e")
        input_box_frame.pack(fill="x", padx=5, pady=(0, 5))

        self.boi_automator_input = tk.Entry(input_box_frame,
                                               bg="#2e3350",
                                               fg="#e0e0e0",
                                               font=("Segoe UI", 12),
                                               relief="solid",
                                               bd=2,
                                               insertbackground="#00d4aa")
        self.boi_automator_input.pack(side="left", fill="x", expand=True, ipady=10)
        self.boi_automator_input.bind("<Return>", lambda e: self.execute_boi_automator_command())

        execute_btn = tk.Button(input_box_frame,
                                text="▶️ Execute",
                                bg="#00ff88",
                                fg="#0f0f1e",
                                font=("Segoe UI", 11, "bold"),
                                relief="flat",
                                cursor="hand2",
                                command=self.execute_boi_automator_command,
                                padx=25,
                                pady=10)
        execute_btn.pack(side="right", padx=(5, 0))
        self.add_hover_effect(execute_btn, "#a6e3a1", "#94e2d5")

        quick_actions_frame = tk.Frame(tab, bg="#1a1d2e")
        quick_actions_frame.pack(fill="x", padx=10, pady=(0, 10))

        actions_label = tk.Label(quick_actions_frame,
                                 text="⚡ Quick Actions:",
                                 bg="#1a1d2e",
                                 fg="#b0b0b0",
                                 font=("Segoe UI", 9, "bold"))
        actions_label.pack(anchor="w", padx=5, pady=(5, 2))

        button_container = tk.Frame(quick_actions_frame, bg="#1a1d2e")
        button_container.pack(fill="x", padx=5)

        quick_actions = [
            ("💻 System Info", "Show system info"),
            ("📸 Screenshot", "Take a screenshot"),
            ("📂 Open Desktop", "Open Desktop folder"),
            ("📝 Notepad", "Open notepad"),
            ("🧹 Clear Output", None)
        ]

        for text, command in quick_actions:
            btn = tk.Button(button_container,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 9, "bold"),
                            relief="flat",
                            cursor="hand2",
                            command=lambda cmd=command: self.boi_quick_action(cmd),
                            padx=12,
                            pady=8)
            btn.pack(side="left", padx=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def create_self_operating_tab(self, notebook):
        """Self-Operating Computer - Autonomous AI Control with Vision"""
        tab = tk.Frame(notebook, bg=self.BG_PRIMARY)
        notebook.add(tab, text="🎮 Self-Operating")

        header_frame = tk.Frame(tab, bg=self.BG_SECONDARY, relief="flat", bd=1, highlightbackground=self.BORDER_PRIMARY,
                                highlightthickness=1)
        header_frame.pack(fill="x", pady=(10, 0), padx=10)

        header = tk.Label(header_frame,
                          text="🎮 Self-Operating Computer",
                          bg=self.BG_SECONDARY,
                          fg=self.TEXT_PRIMARY,
                          font=("Segoe UI", 14, "bold"))
        header.pack(pady=12)

        info = tk.Label(header_frame,
                        text="👁️ AI Vision • 🖱️ Autonomous Control • 🎯 Goal-Driven Operation",
                        bg=self.BG_SECONDARY,
                        fg=self.TEXT_SECONDARY,
                        font=("Segoe UI", 9, "italic"))
        info.pack(pady=(0, 12))

        desc_frame = tk.Frame(tab, bg=self.BG_PRIMARY)
        desc_frame.pack(fill="x", padx=10, pady=5)

        desc_text = tk.Label(desc_frame,
                             text="AI views your screen like a human and autonomously performs mouse/keyboard actions to accomplish objectives.\nInspired by OthersideAI's self-operating-computer, powered by Gemini Vision.",
                             bg=self.BG_PRIMARY,
                             fg=self.TEXT_SECONDARY,
                             font=("Segoe UI", 9),
                             justify="left")
        desc_text.pack(anchor="w", padx=10, pady=5)

        main_container = tk.Frame(tab, bg="#1a1d2e")
        main_container.pack(fill="both", expand=True, padx=10, pady=5)

        left_column = tk.Frame(main_container, bg="#1a1d2e")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 5))

        status_frame = tk.Frame(left_column, bg="#2e3350", relief="flat")
        status_frame.pack(fill="x", pady=(0, 10))

        status_label = tk.Label(status_frame,
                                text="Status: Ready",
                                bg="#2e3350",
                                fg="#00ff88",
                                font=("Segoe UI", 10, "bold"),
                                anchor="w",
                                padx=10,
                                pady=8)
        status_label.pack(fill="x")
        self.soc_status_label = status_label

        input_section = tk.Frame(left_column, bg="#1a1d2e")
        input_section.pack(fill="x", pady=(5, 10))

        input_label = tk.Label(input_section,
                               text="🎯 Enter your objective:",
                               bg="#1a1d2e",
                               fg="#b0b0b0",
                               font=("Segoe UI", 9, "bold"))
        input_label.pack(anchor="w", padx=5, pady=(0, 5))

        self.soc_objective = tk.Text(input_section,
                                     bg="#2e3350",
                                     fg="#e0e0e0",
                                     font=("Segoe UI", 11),
                                     height=3,
                                     relief="solid",
                                     bd=2,
                                     insertbackground="#cba6f7",
                                     padx=8,
                                     pady=8,
                                     wrap=tk.WORD)
        self.soc_objective.pack(fill="x", padx=5)
        self.soc_objective.bind('<Control-Return>', lambda e: self.auto_start_if_enabled())

        hint_label = tk.Label(input_section,
                              text="💡 Tip: Press Ctrl+Enter to quick-start when Auto Mode is enabled",
                              bg="#1a1d2e",
                              fg="#b0b0b0",
                              font=("Segoe UI", 8, "italic"))
        hint_label.pack(anchor="w", padx=5, pady=(2, 0))

        controls_frame = tk.Frame(left_column, bg="#1a1d2e")
        controls_frame.pack(fill="x", pady=5)

        start_text_btn = tk.Button(controls_frame,
                                   text="▶️ Start (Text)",
                                   bg="#cba6f7",
                                   fg="#0f0f1e",
                                   font=("Segoe UI", 10, "bold"),
                                   relief="flat",
                                   cursor="hand2",
                                   command=self.start_self_operating_text,
                                   padx=20,
                                   pady=10)
        start_text_btn.pack(side="left", expand=True, fill="x", padx=(5, 2))
        self.add_hover_effect(start_text_btn, "#cba6f7", "#b4befe")

        start_voice_btn = tk.Button(controls_frame,
                                    text="🎤 Start (Voice)",
                                    bg="#00d4aa",
                                    fg="#0f0f1e",
                                    font=("Segoe UI", 10, "bold"),
                                    relief="flat",
                                    cursor="hand2",
                                    command=self.start_self_operating_voice,
                                    padx=20,
                                    pady=10)
        start_voice_btn.pack(side="left", expand=True, fill="x", padx=2)
        self.add_hover_effect(start_voice_btn, "#89b4fa", "#74c7ec")

        stop_btn = tk.Button(controls_frame,
                             text="⏹️ Stop",
                             bg="#00d4aa",
                             fg="#0f0f1e",
                             font=("Segoe UI", 10, "bold"),
                             relief="flat",
                             cursor="hand2",
                             command=self.stop_self_operating,
                             padx=20,
                             pady=10)
        stop_btn.pack(side="left", expand=True, fill="x", padx=(2, 5))
        self.add_hover_effect(stop_btn, "#f38ba8", "#eba0ac")

        gesture_controls_frame = tk.Frame(left_column, bg="#1a1d2e")
        gesture_controls_frame.pack(fill="x", pady=5)

        self.gesture_voice_btn = tk.Button(gesture_controls_frame,
                                           text="✌️ Gesture Voice",
                                           bg="#ffd700",
                                           fg="#0f0f1e",
                                           font=("Segoe UI", 10, "bold"),
                                           relief="flat",
                                           cursor="hand2",
                                           command=self.toggle_gesture_voice,
                                           padx=20,
                                           pady=10)
        self.gesture_voice_btn.pack(side="left", expand=True, fill="x", padx=5)
        self.add_hover_effect(self.gesture_voice_btn, "#ffd700", "#ffed4e")

        toggle_frame = tk.Frame(left_column, bg="#1a1d2e")
        toggle_frame.pack(fill="x", pady=10)

        toggle_label_text = tk.Label(toggle_frame,
                                     text="🔄 Auto Self-Control Mode:",
                                     bg="#1a1d2e",
                                     fg="#b0b0b0",
                                     font=("Segoe UI", 9, "bold"))
        toggle_label_text.pack(side="left", padx=5)

        self.auto_control_enabled = False
        self.auto_control_btn = tk.Button(toggle_frame,
                                          text="❌ Disabled",
                                          bg="#2e3350",
                                          fg="#00d4aa",
                                          font=("Segoe UI", 9, "bold"),
                                          relief="flat",
                                          cursor="hand2",
                                          command=self.toggle_auto_control,
                                          padx=20,
                                          pady=8)
        self.auto_control_btn.pack(side="left", padx=5)
        self.add_hover_effect(self.auto_control_btn, "#313244", "#45475a")

        toggle_info = tk.Label(toggle_frame,
                               text="When enabled, AI will automatically start self-operating mode after commands",
                               bg="#1a1d2e",
                               fg="#b0b0b0",
                               font=("Segoe UI", 8, "italic"))
        toggle_info.pack(side="left", padx=10)

        examples_frame = tk.Frame(left_column, bg="#1a1d2e")
        examples_frame.pack(fill="x", pady=(10, 5))

        examples_label = tk.Label(examples_frame,
                                  text="💡 Example Objectives:",
                                  bg="#1a1d2e",
                                  fg="#b0b0b0",
                                  font=("Segoe UI", 9, "bold"))
        examples_label.pack(anchor="w", padx=5)

        examples_text = tk.Text(examples_frame,
                                bg="#16182a",
                                fg="#89dceb",
                                font=("Consolas", 8),
                                height=5,
                                relief="flat",
                                padx=8,
                                pady=8,
                                wrap=tk.WORD)
        examples_text.pack(fill="x", padx=5, pady=5)
        examples_text.insert("1.0",
                             "• Open Google Chrome and search for Python tutorials\n"
                             "• Open a new file in Notepad and write 'Hello World'\n"
                             "• Go to YouTube and play a video about AI\n"
                             "• Open Calculator and calculate 25 * 47\n"
                             "• Create a new folder on Desktop named 'AI Projects'")
        examples_text.config(state='disabled')

        right_column = tk.Frame(main_container, bg="#1a1d2e")
        right_column.pack(side="right", fill="both", expand=True, padx=(5, 0))

        output_label = tk.Label(right_column,
                                text="📊 Real-Time Output:",
                                bg="#1a1d2e",
                                fg="#b0b0b0",
                                font=("Segoe UI", 9, "bold"))
        output_label.pack(anchor="w", padx=5, pady=(0, 5))

        self.soc_output = scrolledtext.ScrolledText(
            right_column,
            bg="#16182a",
            fg="#e0e0e0",
            font=("Consolas", 9),
            wrap=tk.WORD,
            state='disabled',
            relief="flat",
            padx=10,
            pady=10
        )
        self.soc_output.pack(fill="both", expand=True, padx=5, pady=5)

        self.soc_output.tag_config("iteration", foreground="#cba6f7", font=("Consolas", 9, "bold"))
        self.soc_output.tag_config("thought", foreground="#89dceb")
        self.soc_output.tag_config("action", foreground="#a6e3a1", font=("Consolas", 9, "bold"))
        self.soc_output.tag_config("progress", foreground="#f9e2af")
        self.soc_output.tag_config("success", foreground="#a6e3a1", font=("Consolas", 9, "bold"))
        self.soc_output.tag_config("error", foreground="#f38ba8", font=("Consolas", 9, "bold"))
        self.soc_output.tag_config("warning", foreground="#f9e2af")

        bottom_frame = tk.Frame(tab, bg="#1a1d2e")
        bottom_frame.pack(fill="x", padx=10, pady=(5, 10))

        buttons = [
            ("📖 View Guide", self.show_soc_guide, "#89b4fa"),
            ("🔄 Clear Output", self.clear_soc_output, "#313244"),
            ("📸 View Screenshots", self.view_soc_screenshots, "#89dceb")
        ]

        for text, command, color in buttons:
            btn = tk.Button(bottom_frame,
                            text=text,
                            bg=color,
                            fg="#0f0f1e" if color != "#313244" else "#ffffff",
                            font=("Segoe UI", 9, "bold"),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            padx=15,
                            pady=8)
            btn.pack(side="left", expand=True, fill="x", padx=3)
            hover_color = "#b4befe" if color == "#89b4fa" else "#74c7ec" if color == "#89dceb" else "#45475a"
            self.add_hover_effect(btn, color, hover_color)

    def create_comprehensive_controller_tab(self, notebook):
        """
        Comprehensive Desktop Controller Tab for GUI
        This creates the UI tab for the 3-phase automation system
        3-Phase Desktop Automation Controller Tab
        - Phase 1: Understand the Prompt
        - Phase 2: Break into Steps
        - Phase 3: Monitor & Execute
        """
        tab = tk.Frame(notebook, bg="#1a1d2e")
        notebook.add(tab, text="🎯 Smart Control")

        # Header
        header_frame = tk.Frame(tab, bg="#252941")
        header_frame.pack(fill="x", pady=(10, 0), padx=10)

        header = tk.Label(header_frame,
                          text="🎯 Comprehensive Desktop Controller",
                          bg="#252941",
                          fg="#f9e2af",
                          font=("Segoe UI", 14, "bold"))
        header.pack(pady=12)

        info = tk.Label(header_frame,
                        text="🧠 Understands → 📋 Plans → 👁️ Monitors • AI-Powered 3-Phase Automation",
                        bg="#252941",
                        fg="#b0b0b0",
                        font=("Segoe UI", 9, "italic"))
        info.pack(pady=(0, 12))

        # Phase indicator
        phase_frame = tk.Frame(tab, bg="#1a1d2e")
        phase_frame.pack(fill="x", padx=10, pady=5)

        self.phase_labels = {}
        phases = [
            ("🧠", "UNDERSTAND", "#89b4fa"),
            ("📋", "PLAN", "#f9e2af"),
            ("👁️", "MONITOR", "#a6e3a1")
        ]

        for icon, name, color in phases:
            phase_container = tk.Frame(phase_frame, bg="#2e3350", relief="flat")
            phase_container.pack(side="left", expand=True, fill="x", padx=5, pady=5)

            label = tk.Label(phase_container,
                             text=f"{icon} {name}",
                             bg="#2e3350",
                             fg=color,
                             font=("Segoe UI", 9, "bold"),
                             pady=8)
            label.pack()
            self.phase_labels[name] = label

        # Main container with two columns
        main_container = tk.Frame(tab, bg="#1a1d2e")
        main_container.pack(fill="both", expand=True, padx=10, pady=5)

        # Left column - Input and controls
        left_column = tk.Frame(main_container, bg="#1a1d2e")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Input section
        input_section = tk.Frame(left_column, bg="#1a1d2e")
        input_section.pack(fill="x", pady=(5, 10))

        input_label = tk.Label(input_section,
                               text="🎯 Enter your automation command:",
                               bg="#1a1d2e",
                               fg="#b0b0b0",
                               font=("Segoe UI", 9, "bold"))
        input_label.pack(anchor="w", padx=5, pady=(0, 5))

        # Input box with send button
        input_box_frame = tk.Frame(input_section, bg="#1a1d2e")
        input_box_frame.pack(fill="x", padx=5)

        self.comprehensive_input = tk.Entry(input_box_frame,
                                            bg="#2e3350",
                                            fg="#e0e0e0",
                                            font=("Segoe UI", 11),
                                            relief="solid",
                                            bd=2,
                                            insertbackground="#f9e2af")
        self.comprehensive_input.pack(side="left", fill="x", expand=True, ipady=8)
        self.comprehensive_input.bind("<Return>", lambda e: self.execute_comprehensive_command())

        execute_btn = tk.Button(input_box_frame,
                                text="▶️ Execute",
                                bg="#f9e2af",
                                fg="#0f0f1e",
                                font=("Segoe UI", 10, "bold"),
                                relief="flat",
                                cursor="hand2",
                                command=self.execute_comprehensive_command,
                                padx=20,
                                pady=8)
        execute_btn.pack(side="right", padx=(5, 0))
        self.add_hover_effect(execute_btn, "#f9e2af", "#f5c2e7")

        # Quick actions section with navigation - REMOVED
        # self.quick_actions_container = tk.Frame(left_column, bg="#1a1d2e")
        # self.quick_actions_container.pack(fill="both", expand=True, pady=(5, 10))

        # # Create main menu view
        # self.quick_menu_view = tk.Frame(self.quick_actions_container, bg="#1a1d2e")

        # # Header
        # menu_header = tk.Label(self.quick_menu_view,
        #                       text="⚡ Quick Actions Centre",
        #                       bg="#1a1d2e",
        #                       fg="#f9e2af",
        #                       font=("Segoe UI", 11, "bold"))
        # menu_header.pack(anchor="w", padx=8, pady=(5, 2))

        # # Subtitle
        # menu_subtitle = tk.Label(self.quick_menu_view,
        #                         text="Choose an action below",
        #                         bg="#1a1d2e",
        #                         fg="#b0b0b0",
        #                         font=("Segoe UI", 8))
        # menu_subtitle.pack(anchor="w", padx=8, pady=(0, 8))

        # # Scrollable menu - REMOVED
        # menu_canvas = tk.Canvas(self.quick_menu_view, bg="#1a1d2e", highlightthickness=0, height=400)
        # menu_scrollbar = ttk.Scrollbar(self.quick_menu_view, orient="vertical", command=menu_canvas.yview)
        # menu_scrollable = tk.Frame(menu_canvas, bg="#1a1d2e")

        # menu_scrollable.bind(
        #     "<Configure>",
        #     lambda e: menu_canvas.configure(scrollregion=menu_canvas.bbox("all"))
        # )

        # menu_canvas.create_window((0, 0), window=menu_scrollable, anchor="nw", width=400)
        # menu_canvas.configure(yscrollcommand=menu_scrollbar.set)

        # # Define quick actions with features - REMOVED
        # self.quick_actions_data = [
        #     ("🖥️ SYSTEM", None, "#89b4fa", True, None),
        #     ("💻 Screenshot", "Take a screenshot", "#89b4fa", False, "screenshot"),
        #     ("🔒 Lock PC", "Lock the computer", "#f38ba8", False, "lock"),
        #     ("📊 Task Manager", "Open Task Manager", "#cba6f7", False, "taskmanager"),

        #     ("🌐 WEB & APPS", None, "#89dceb", True, None),
        #     ("🌍 Chrome", "Open Chrome and go to Google", "#89dceb", False, "chrome"),
        #     ("🔍 Google Search", "Search Google for Python tutorials", "#a6e3a1", False, "google"),
        #     ("📧 Gmail", "Open Gmail in browser", "#f38ba8", False, "gmail"),
        #     ("💬 WhatsApp", "Open WhatsApp Web", "#a6e3a1", False, "whatsapp"),

        #     ("📁 PRODUCTIVITY", None, "#a6e3a1", True, None),
        #     ("📝 VS Code", "Launch VS Code", "#89b4fa", False, "vscode"),
        #     ("📂 File Explorer", "Open File Explorer", "#f9e2af", False, "explorer"),
        #     ("🗒️ Notepad", "Open Notepad", "#cba6f7", False, "notepad"),

        #     ("🎵 MEDIA", None, "#f5c2e7", True, None),
        #     ("🎵 Spotify", "Launch Spotify", "#a6e3a1", False, "spotify"),
        #     ("🎬 YouTube", "Open YouTube", "#f38ba8", False, "youtube"),
        #     ("🔊 Volume", "Control system volume", "#89dceb", False, "volume"),
        # ]

        # # Create menu buttons - REMOVED
        # for item in self.quick_actions_data:
        #     text, description, color, is_header, feature_id = item

        #     if is_header:
        #         header_container = tk.Frame(menu_scrollable, bg="#1a1d2e", height=35)
        #         header_container.pack(fill="x", padx=5, pady=(8, 3))
        #         header_container.pack_propagate(False)

        #         accent = tk.Frame(header_container, bg=color, width=3)
        #         accent.pack(side="left", fill="y", padx=(0, 8))

        #         header_label = tk.Label(header_container,
        #                                text=text,
        #                                bg="#1a1d2e",
        #                                fg=color,
        #                                font=("Segoe UI", 9, "bold"))
        #         header_label.pack(side="left", pady=8)
        #     else:
        #         btn = tk.Button(menu_scrollable,
        #                        text=text,
        #                        bg="#2e3350",
        #                        fg="#e0e0e0",
        #                        font=("Segoe UI", 9, "bold"),
        #                        relief="flat",
        #                        cursor="hand2",
        #                        command=lambda t=text, d=description, c=color, f=feature_id: self.show_quick_action_feature(t, d, c, f),
        #                        padx=15,
        #                        pady=10,
        #                        anchor="w",
        #                        bd=0)
        #         btn.pack(fill="x", padx=8, pady=2)

        #         def make_hover(button, accent_color):
        #             def on_enter(e):
        #                 button.config(bg="#3d4466", fg=accent_color)
        #             def on_leave(e):
        #                 button.config(bg="#2e3350", fg="#e0e0e0")
        #             button.bind("<Enter>", on_enter)
        #             button.bind("<Leave>", on_leave)

        #         make_hover(btn, color)

        # self.menu_canvas.pack(side="left", fill="both", expand=True)
        # menu_scrollbar.pack(side="right", fill="y")

        # # Create feature view (initially hidden) - REMOVED
        # self.quick_feature_view = tk.Frame(self.quick_actions_container, bg="#1a1d2e")

        # # Feature view header
        # feature_header_frame = tk.Frame(self.quick_feature_view, bg="#1a1d2e", height=50)
        # feature_header_frame.pack(fill="x", pady=(0, 10))
        # feature_header_frame.pack_propagate(False)

        # # Back button
        # self.back_button = tk.Button(feature_header_frame,
        #                              text="← Back",
        #                              bg="#2e3350",
        #                              fg="#00d4aa",
        #                              font=("Segoe UI", 10, "bold"),
        #                              relief="flat",
        #                              cursor="hand2",
        #                              command=self.show_quick_actions_menu,
        #                              padx=15,
        #                              pady=8)
        # self.back_button.pack(side="left", padx=8, pady=8)
        # self.add_hover_effect(self.back_button, "#313244", "#45475a")

        # # Feature title
        # self.feature_title = tk.Label(feature_header_frame,
        #                              text="",
        #                              bg="#1a1d2e",
        #                              fg="#f9e2af",
        #                              font=("Segoe UI", 12, "bold"))
        # self.feature_title.pack(side="left", padx=10, pady=8)

        # # Feature content area
        # self.feature_content = tk.Frame(self.quick_feature_view, bg="#181825", relief="flat")
        # self.feature_content.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        # # Show menu view by default
        # self.quick_menu_view.pack(fill="both", expand=True)

        # Example prompts
        examples_frame = tk.Frame(left_column, bg="#1a1d2e")
        examples_frame.pack(fill="x", pady=(10, 5))

        examples_label = tk.Label(examples_frame,
                                  text="💡 Example Prompts:",
                                  bg="#1a1d2e",
                                  fg="#b0b0b0",
                                  font=("Segoe UI", 9, "bold"))
        examples_label.pack(anchor="w", padx=5)

        examples_text = tk.Text(examples_frame,
                                bg="#16182a",
                                fg="#89dceb",
                                font=("Consolas", 8),
                                height=4,
                                relief="flat",
                                padx=8,
                                pady=8,
                                wrap=tk.WORD)
        examples_text.pack(fill="x", padx=5, pady=5)
        examples_text.insert("1.0",
                             "• Open Chrome, navigate to GitHub, and screenshot\n"
                             "• Launch Spotify and play jazz music\n"
                             "• Search Google for Python tutorials, open first 3 results\n"
                             "• Create a new folder on Desktop named 'Projects'")
        examples_text.config(state='disabled')

        # Right column - Output
        right_column = tk.Frame(main_container, bg="#1a1d2e")
        right_column.pack(side="right", fill="both", expand=True, padx=(5, 0))

        output_label = tk.Label(right_column,
                                text="📊 Execution Output:",
                                bg="#1a1d2e",
                                fg="#b0b0b0",
                                font=("Segoe UI", 9, "bold"))
        output_label.pack(anchor="w", padx=5, pady=(0, 5))

        # Output display with scrollbar
        self.comprehensive_output = scrolledtext.ScrolledText(
            right_column,
            bg="#16182a",
            fg="#e0e0e0",
            font=("Consolas", 9),
            wrap=tk.WORD,
            state='disabled',
            relief="flat",
            padx=10,
            pady=10
        )
        self.comprehensive_output.pack(fill="both", expand=True, padx=5, pady=5)

        # Configure text tags for colored output
        self.comprehensive_output.tag_config("phase1", foreground="#89b4fa", font=("Consolas", 9, "bold"))
        self.comprehensive_output.tag_config("phase2", foreground="#f9e2af", font=("Consolas", 9, "bold"))
        self.comprehensive_output.tag_config("phase3", foreground="#a6e3a1", font=("Consolas", 9, "bold"))
        self.comprehensive_output.tag_config("success", foreground="#a6e3a1", font=("Consolas", 9, "bold"))
        self.comprehensive_output.tag_config("error", foreground="#f38ba8", font=("Consolas", 9, "bold"))
        self.comprehensive_output.tag_config("info", foreground="#89dceb")
        self.comprehensive_output.tag_config("highlight", foreground="#f9e2af", font=("Consolas", 9, "bold"))

        # Bottom buttons
        bottom_frame = tk.Frame(tab, bg="#1a1d2e")
        bottom_frame.pack(fill="x", padx=10, pady=(5, 10))

        buttons = [
            ("📖 View Guide", self.show_comprehensive_guide, "#89b4fa"),
            ("🔄 Clear Output", self.clear_comprehensive_output, "#313244"),
            ("📸 View Screenshots", self.view_comprehensive_screenshots, "#89dceb"),
            ("📊 View Stats", self.show_comprehensive_stats, "#a6e3a1")
        ]

        for btn_text, command, color in buttons:
            btn = tk.Button(bottom_frame,
                            text=btn_text,
                            bg=color,
                            fg="#0f0f1e" if color != "#313244" else "#ffffff",
                            font=("Segoe UI", 9, "bold"),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            padx=15,
                            pady=8)
            btn.pack(side="left", padx=5)
            hover_color = "#74c7ec" if color == "#89b4fa" else "#45475a" if color == "#313244" else color
            self.add_hover_effect(btn, color, hover_color)

        # Status indicator
        status_container = tk.Frame(bottom_frame, bg="#2e3350", relief="flat")
        status_container.pack(side="right", padx=5)

        self.comprehensive_status = tk.Label(status_container,
                                             text="✅ Ready",
                                             bg="#2e3350",
                                             fg="#00ff88",
                                             font=("Segoe UI", 9, "bold"),
                                             padx=15,
                                             pady=8)
        self.comprehensive_status.pack()

        # Initial welcome message
        self.append_comprehensive_output("info")
        self.append_comprehensive_output("🎯 COMPREHENSIVE DESKTOP CONTROLLER\n", "highlight")
        self.append_comprehensive_output("\n", "info")
        self.append_comprehensive_output("Welcome! This system:\n", "info")
        self.append_comprehensive_output("  🧠 Phase 1: ", "phase1")
        self.append_comprehensive_output("Understands your prompt deeply\n", "info")
        self.append_comprehensive_output("  📋 Phase 2: ", "phase2")
        self.append_comprehensive_output("Breaks it into executable steps\n", "info")
        self.append_comprehensive_output("  👁️  Phase 3: ", "phase3")
        self.append_comprehensive_output("Monitors screen in real-time\n\n", "info")
        self.append_comprehensive_output("💡 Try a command above or use Quick Actions!\n", "highlight")
        self.append_comprehensive_output("\n", "info")

    def create_vlm_tab(self, notebook):
        """
        Virtual Language Model GUI Tab
        Self-learning AI that observes, learns, and controls
        """
        tab = tk.Frame(notebook, bg="#1a1d2e")
        notebook.add(tab, text="🧠 Learning AI")

        # Header
        header_frame = tk.Frame(tab, bg="#252941")
        header_frame.pack(fill="x", pady=(10, 0), padx=10)

        header = tk.Label(header_frame,
                          text="🧠 Virtual Language Model",
                          bg="#252941",
                          fg="#cba6f7",
                          font=("Segoe UI", 14, "bold"))
        header.pack(pady=12)

        info = tk.Label(header_frame,
                        text="👁️ Observes Screen → 📚 Learns Patterns → 🎯 Controls Desktop",
                        bg="#252941",
                        fg="#b0b0b0",
                        font=("Segoe UI", 9, "italic"))
        info.pack(pady=(0, 12))

        # Main container with two columns
        main_container = tk.Frame(tab, bg="#1a1d2e")
        main_container.pack(fill="both", expand=True, padx=10, pady=5)

        # Left column - Controls
        left_column = tk.Frame(main_container, bg="#1a1d2e")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Learning stats
        stats_frame = tk.Frame(left_column, bg="#2e3350", relief="flat")
        stats_frame.pack(fill="x", pady=5, padx=5)

        stats_title = tk.Label(stats_frame,
                               text="📊 Learning Statistics",
                               bg="#2e3350",
                               fg="#cba6f7",
                               font=("Segoe UI", 10, "bold"))
        stats_title.pack(pady=8)

        self.vlm_stats_display = tk.Text(stats_frame,
                                         bg="#16182a",
                                         fg="#e0e0e0",
                                         font=("Consolas", 9),
                                         height=6,
                                         relief="flat",
                                         padx=10,
                                         pady=10,
                                         state='disabled')
        self.vlm_stats_display.pack(fill="x", padx=5, pady=(0, 8))

        # Goal input section
        goal_frame = tk.Frame(left_column, bg="#1a1d2e")
        goal_frame.pack(fill="x", pady=(10, 5))

        goal_label = tk.Label(goal_frame,
                              text="🎯 Goal for AI:",
                              bg="#1a1d2e",
                              fg="#b0b0b0",
                              font=("Segoe UI", 9, "bold"))
        goal_label.pack(anchor="w", padx=5, pady=(0, 5))

        goal_input_frame = tk.Frame(goal_frame, bg="#1a1d2e")
        goal_input_frame.pack(fill="x", padx=5)

        self.vlm_goal_input = tk.Entry(goal_input_frame,
                                       bg="#2e3350",
                                       fg="#e0e0e0",
                                       font=("Segoe UI", 11),
                                       relief="solid",
                                       bd=2,
                                       insertbackground="#cba6f7")
        self.vlm_goal_input.pack(side="left", fill="x", expand=True, ipady=8)

        # Action buttons
        actions_frame = tk.Frame(left_column, bg="#1a1d2e")
        actions_frame.pack(fill="x", pady=10, padx=5)

        actions_label = tk.Label(actions_frame,
                                 text="⚡ Actions:",
                                 bg="#1a1d2e",
                                 fg="#b0b0b0",
                                 font=("Segoe UI", 9, "bold"))
        actions_label.pack(anchor="w", pady=(0, 5))

        # Row 1
        row1 = tk.Frame(actions_frame, bg="#1a1d2e")
        row1.pack(fill="x", pady=2)

        observe_btn = tk.Button(row1,
                                text="👁️ Observe Screen",
                                bg="#00d4aa",
                                fg="#0f0f1e",
                                font=("Segoe UI", 9, "bold"),
                                relief="flat",
                                cursor="hand2",
                                command=self.vlm_observe,
                                padx=15,
                                pady=8)
        observe_btn.pack(side="left", expand=True, fill="x", padx=2)
        self.add_hover_effect(observe_btn, "#89b4fa", "#74c7ec")

        decide_btn = tk.Button(row1,
                               text="🤔 Decide Action",
                               bg="#f9e2af",
                               fg="#0f0f1e",
                               font=("Segoe UI", 9, "bold"),
                               relief="flat",
                               cursor="hand2",
                               command=self.vlm_decide,
                               padx=15,
                               pady=8)
        decide_btn.pack(side="left", expand=True, fill="x", padx=2)
        self.add_hover_effect(decide_btn, "#f9e2af", "#f5c2e7")

        # Row 2
        row2 = tk.Frame(actions_frame, bg="#1a1d2e")
        row2.pack(fill="x", pady=2)

        execute_btn = tk.Button(row2,
                                text="▶️ Execute",
                                bg="#00ff88",
                                fg="#0f0f1e",
                                font=("Segoe UI", 9, "bold"),
                                relief="flat",
                                cursor="hand2",
                                command=self.vlm_execute,
                                padx=15,
                                pady=8)
        execute_btn.pack(side="left", expand=True, fill="x", padx=2)
        self.add_hover_effect(execute_btn, "#a6e3a1", "#94e2d5")

        learn_btn = tk.Button(row2,
                              text="🧠 Learn Session",
                              bg="#cba6f7",
                              fg="#0f0f1e",
                              font=("Segoe UI", 9, "bold"),
                              relief="flat",
                              cursor="hand2",
                              command=self.vlm_learn_session,
                              padx=15,
                              pady=8)
        learn_btn.pack(side="left", expand=True, fill="x", padx=2)
        self.add_hover_effect(learn_btn, "#cba6f7", "#b4befe")

        # Row 3
        row3 = tk.Frame(actions_frame, bg="#1a1d2e")
        row3.pack(fill="x", pady=2)

        query_btn = tk.Button(row3,
                              text="💬 Query Knowledge",
                              bg="#2e3350",
                              fg="#e0e0e0",
                              font=("Segoe UI", 9, "bold"),
                              relief="flat",
                              cursor="hand2",
                              command=self.vlm_query,
                              padx=15,
                              pady=8)
        query_btn.pack(side="left", expand=True, fill="x", padx=2)
        self.add_hover_effect(query_btn, "#313244", "#45475a")

        refresh_btn = tk.Button(row3,
                                text="🔄 Refresh Stats",
                                bg="#2e3350",
                                fg="#e0e0e0",
                                font=("Segoe UI", 9, "bold"),
                                relief="flat",
                                cursor="hand2",
                                command=self.vlm_refresh_stats,
                                padx=15,
                                pady=8)
        refresh_btn.pack(side="left", expand=True, fill="x", padx=2)
        self.add_hover_effect(refresh_btn, "#313244", "#45475a")

        # Knowledge display
        knowledge_frame = tk.Frame(left_column, bg="#1a1d2e")
        knowledge_frame.pack(fill="both", expand=True, pady=(10, 5))

        knowledge_label = tk.Label(knowledge_frame,
                                   text="📚 Learned Knowledge:",
                                   bg="#1a1d2e",
                                   fg="#b0b0b0",
                                   font=("Segoe UI", 9, "bold"))
        knowledge_label.pack(anchor="w", padx=5, pady=(0, 5))

        self.vlm_knowledge_display = scrolledtext.ScrolledText(
            knowledge_frame,
            bg="#16182a",
            fg="#e0e0e0",
            font=("Consolas", 8),
            wrap=tk.WORD,
            state='disabled',
            relief="flat",
            padx=10,
            pady=10
        )
        self.vlm_knowledge_display.pack(fill="both", expand=True, padx=5, pady=5)

        # Right column - Output
        right_column = tk.Frame(main_container, bg="#1a1d2e")
        right_column.pack(side="right", fill="both", expand=True, padx=(5, 0))

        output_label = tk.Label(right_column,
                                text="📊 Activity Log:",
                                bg="#1a1d2e",
                                fg="#b0b0b0",
                                font=("Segoe UI", 9, "bold"))
        output_label.pack(anchor="w", padx=5, pady=(0, 5))

        self.vlm_output = scrolledtext.ScrolledText(
            right_column,
            bg="#16182a",
            fg="#e0e0e0",
            font=("Consolas", 9),
            wrap=tk.WORD,
            state='disabled',
            relief="flat",
            padx=10,
            pady=10
        )
        self.vlm_output.pack(fill="both", expand=True, padx=5, pady=5)

        # Configure text tags
        self.vlm_output.tag_config("success", foreground="#a6e3a1", font=("Consolas", 9, "bold"))
        self.vlm_output.tag_config("error", foreground="#f38ba8", font=("Consolas", 9, "bold"))
        self.vlm_output.tag_config("info", foreground="#89dceb")
        self.vlm_output.tag_config("highlight", foreground="#cba6f7", font=("Consolas", 9, "bold"))
        self.vlm_output.tag_config("decision", foreground="#f9e2af", font=("Consolas", 9, "bold"))

        # Bottom status
        bottom_frame = tk.Frame(tab, bg="#1a1d2e")
        bottom_frame.pack(fill="x", padx=10, pady=(5, 10))

        help_btn = tk.Button(bottom_frame,
                             text="📖 How It Works",
                             bg="#00d4aa",
                             fg="#0f0f1e",
                             font=("Segoe UI", 9, "bold"),
                             relief="flat",
                             cursor="hand2",
                             command=self.show_vlm_help,
                             padx=15,
                             pady=8)
        help_btn.pack(side="left", padx=5)
        self.add_hover_effect(help_btn, "#89b4fa", "#74c7ec")

        clear_btn = tk.Button(bottom_frame,
                              text="🗑️ Clear Output",
                              bg="#2e3350",
                              fg="#e0e0e0",
                              font=("Segoe UI", 9, "bold"),
                              relief="flat",
                              cursor="hand2",
                              command=self.vlm_clear_output,
                              padx=15,
                              pady=8)
        clear_btn.pack(side="left", padx=5)
        self.add_hover_effect(clear_btn, "#313244", "#45475a")

        # Status
        status_container = tk.Frame(bottom_frame, bg="#2e3350", relief="flat")
        status_container.pack(side="right", padx=5)

        self.vlm_status = tk.Label(status_container,
                                   text="✅ Ready to Learn",
                                   bg="#2e3350",
                                   fg="#00ff88",
                                   font=("Segoe UI", 9, "bold"),
                                   padx=15,
                                   pady=8)
        self.vlm_status.pack()

        # Initialize with welcome message
        self.vlm_append_output("\n", "info")
        self.vlm_append_output("🧠 VIRTUAL LANGUAGE MODEL\n", "highlight")
        self.vlm_append_output("\n\n", "info")
        self.vlm_append_output("Welcome to the self-learning AI system!\n\n", "info")
        self.vlm_append_output("This AI can:\n", "info")
        self.vlm_append_output("  👁️  Observe and analyze your screen\n", "info")
        self.vlm_append_output("  📚 Learn UI patterns and workflows\n", "info")
        self.vlm_append_output("  🤔 Make intelligent decisions\n", "info")
        self.vlm_append_output("  🎯 Execute actions based on learned knowledge\n", "info")
        self.vlm_append_output("  💬 Answer questions about what it learned\n\n", "info")
        self.vlm_append_output("💡 Try: Click 'Observe Screen' to let it see your desktop!\n", "highlight")
        self.vlm_append_output("\n", "info")

        # Load initial stats
        self.vlm_refresh_stats()

    def create_web_automation_tab(self, notebook):
        """Web Automation with Selenium"""
        tab = tk.Frame(notebook, bg="#1a1d2e")
        notebook.add(tab, text="🌐 Web Auto")

        header_frame = tk.Frame(tab, bg="#252941")
        header_frame.pack(fill="x", pady=(10, 0), padx=10)

        header = tk.Label(header_frame,
                          text="🌐 Intelligent Web Automation",
                          bg="#252941",
                          fg="#89dceb",
                          font=("Segoe UI", 14, "bold"))
        header.pack(pady=12)

        info = tk.Label(header_frame,
                        text="🤖 AI-Powered Browser Control • Works in Replit Cloud",
                        bg="#252941",
                        fg="#b0b0b0",
                        font=("Segoe UI", 9, "italic"))
        info.pack(pady=(0, 12))

        input_section = tk.Frame(tab, bg="#1a1d2e")
        input_section.pack(fill="x", padx=10, pady=10)

        input_label = tk.Label(input_section,
                               text="💬 Natural Language Command:",
                               bg="#1a1d2e",
                               fg="#b0b0b0",
                               font=("Segoe UI", 9, "bold"))
        input_label.pack(anchor="w", padx=5, pady=(5, 2))

        input_box_frame = tk.Frame(input_section, bg="#1a1d2e")
        input_box_frame.pack(fill="x", padx=5, pady=(0, 5))

        self.web_auto_input = tk.Entry(input_box_frame,
                                       bg="#2e3350",
                                       fg="#e0e0e0",
                                       font=("Segoe UI", 11),
                                       relief="solid",
                                       bd=2,
                                       insertbackground="#89dceb")
        self.web_auto_input.pack(side="left", fill="x", expand=True, ipady=8)
        self.web_auto_input.bind("<Return>", lambda e: self.execute_web_automation())

        execute_btn = tk.Button(input_box_frame,
                                text="🚀 Execute",
                                bg="#89dceb",
                                fg="#0f0f1e",
                                font=("Segoe UI", 10, "bold"),
                                relief="flat",
                                cursor="hand2",
                                command=self.execute_web_automation,
                                padx=20,
                                pady=8)
        execute_btn.pack(side="right", padx=(5, 0))
        self.add_hover_effect(execute_btn, "#89dceb", "#74c7ec")

        quick_frame = tk.Frame(tab, bg="#252941")
        quick_frame.pack(fill="both", expand=True, padx=10, pady=10)

        quick_label = tk.Label(quick_frame,
                               text="⚡ Quick Actions",
                               bg="#252941",
                               fg="#f9e2af",
                               font=("Segoe UI", 11, "bold"))
        quick_label.pack(pady=10)

        canvas = tk.Canvas(quick_frame, bg="#252941", highlightthickness=0)
        scrollbar = ttk.Scrollbar(quick_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#252941")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        quick_actions = [
            ("🎯 LeetCode Problem 34", "open leetcode problem 34"),
            ("🎯 LeetCode Problem 1", "open leetcode problem 1"),
            ("📚 LeetCode Problemset", "open https://leetcode.com/problemset/all/"),
            ("🔍 Search GitHub Python", "search github for python automation"),
            ("🌟 GitHub Trending Python", "open https://github.com/trending/python"),
            ("🌟 GitHub Trending", "open https://github.com/trending"),
            ("💡 Search Google ML", "search google for machine learning"),
            ("🔎 Search StackOverflow", "search stackoverflow for python async"),
            ("▶️ Play Python Tutorial", "play youtube video python tutorial"),
            ("▶️ Play Coding Tutorial", "play youtube video coding tutorials"),
        ]

        for text, command in quick_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 9),
                            relief="flat",
                            cursor="hand2",
                            command=lambda c=command: self.quick_web_automation(c),
                            anchor="w",
                            padx=15,
                            pady=8,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=2)
            self.add_hover_effect(btn, "#313244", "#45475a")

        control_frame = tk.Frame(tab, bg="#1a1d2e")
        control_frame.pack(fill="x", padx=10, pady=(0, 10))

        init_btn = tk.Button(control_frame,
                             text="▶️ Start Browser",
                             bg="#2e3350",
                             fg="#e0e0e0",
                             font=("Segoe UI", 9, "bold"),
                             relief="flat",
                             cursor="hand2",
                             command=self.initialize_web_browser,
                             padx=12,
                             pady=6)
        init_btn.pack(side="left", padx=5)
        self.add_hover_effect(init_btn, "#313244", "#45475a")

        close_btn = tk.Button(control_frame,
                              text="🔒 Close Browser",
                              bg="#2e3350",
                              fg="#e0e0e0",
                              font=("Segoe UI", 9, "bold"),
                              relief="flat",
                              cursor="hand2",
                              command=self.close_web_browser,
                              padx=12,
                              pady=6)
        close_btn.pack(side="left", padx=5)
        self.add_hover_effect(close_btn, "#313244", "#45475a")

        screenshot_btn = tk.Button(control_frame,
                                   text="📸 Screenshot",
                                   bg="#2e3350",
                                   fg="#e0e0e0",
                                   font=("Segoe UI", 9, "bold"),
                                   relief="flat",
                                   cursor="hand2",
                                   command=self.take_web_screenshot,
                                   padx=12,
                                   pady=6)
        screenshot_btn.pack(side="left", padx=5)
        self.add_hover_effect(screenshot_btn, "#313244", "#45475a")

    def create_code_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1a1d2e")
        notebook.add(tab, text="💻 Code")

        canvas = tk.Canvas(tab, bg="#1a1d2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1d2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        actions = [
            ("🤖 Generate Palindrome Checker", "Write code for checking palindrome"),
            ("🔢 Generate Bubble Sort", "Generate Python code for bubble sort"),
            ("🧮 Generate Calculator", "Create JavaScript code for calculator"),
            ("📊 Generate Data Analysis", "Write Python code for data analysis"),
            ("🔐 Generate Password Generator", "Create code for password generator"),
            ("🌐 Generate Web Scraper", "Write Python code for web scraping"),
            ("📝 Generate Todo App", "Create JavaScript todo app"),
            ("🎮 Generate Game Logic", "Write Python code for tic-tac-toe game"),
        ]

        for text, command in actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=lambda c=command: self.quick_command(c),
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def create_desktop_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1a1d2e")
        notebook.add(tab, text="🖥️ Desktop")

        canvas = tk.Canvas(tab, bg="#1a1d2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1d2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Label(scrollable_frame,
                 text="🗂️ Desktop File Controller",
                 bg="#1a1d2e",
                 fg="#f9e2af",
                 font=("Segoe UI", 12, "bold"),
                 pady=10).pack(fill="x", padx=8)

        file_controller_actions = [
            ("🗂️ Launch Batch Controller", lambda: self.launch_batch_controller()),
            ("📋 List Desktop Items", lambda: self.list_desktop_items()),
            ("➕ Create New Folder", lambda: self.create_desktop_folder()),
            ("📁 Organize Desktop", lambda: self.organize_desktop()),
            ("🔍 Search Desktop Files", lambda: self.search_desktop_files()),
        ]

        for text, command in file_controller_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#3d4466",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10, "bold"),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#585b70")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#45475a", "#585b70")

        tk.Label(scrollable_frame,
                 text="🖥️ Desktop Quick Actions",
                 bg="#1a1d2e",
                 fg="#f9e2af",
                 font=("Segoe UI", 12, "bold"),
                 pady=10).pack(fill="x", padx=8, pady=(15, 0))

        actions = [
            ("📝 Open Notepad", "Open notepad"),
            ("📸 Take Screenshot", "Take a screenshot"),
            ("🔍 Search Google", "Search Google for Python tutorials"),
            ("🌐 Open Browser", "Open chrome"),
            ("📋 Copy Text", "Copy text Hello World to clipboard"),
            ("📁 Create File", "Create file test.txt with content Hello"),
            ("⌨️ Type Text", "Type Hello World"),
            ("🖱️ Analyze Screen", "Analyze current screen"),
            ("📊 Get System Info", "Show system information"),
        ]

        for text, command in actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=lambda c=command: self.quick_command(c),
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def create_file_automation_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1a1d2e")
        notebook.add(tab, text="📁 File Auto")

        canvas = tk.Canvas(tab, bg="#1a1d2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1d2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        actions = [
            ("📅 Rename by Date", "Rename files in Downloads folder by date"),
            ("🔢 Rename Sequential", "Rename files sequentially with numbers"),
            ("📂 Rename by Type", "Rename files by their type"),
            ("📁 Rename by Project", "Rename files using folder name as prefix"),
            ("🔍 Start Folder Monitor", "Monitor Downloads folder for new files"),
            ("⏹️ Stop Folder Monitor", "Stop monitoring folder"),
            ("📊 View Active Monitors", "Show all active folder monitors"),
            ("🗜️ Compress Folder", "Compress Documents folder to ZIP"),
            ("📦 Extract ZIP", "Extract archive.zip to current folder"),
            ("🗂️ Compress Old Files", "Compress files older than 30 days"),
            ("📁 Batch Compress", "Compress multiple files into one archive"),
            ("🔄 Auto-Archive by Age", "Automatically archive old files"),
        ]

        for text, command in actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=lambda c=command: self.quick_command(c),
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def create_clipboard_text_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1a1d2e")
        notebook.add(tab, text="📋 Clipboard & Text")

        canvas = tk.Canvas(tab, bg="#1a1d2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1d2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        actions = [
            ("📋 Paste from Clipboard", "Get text from clipboard"),
            ("📊 Clipboard Info", "Show clipboard information"),
            ("🗑️ Clear Clipboard", "Clear clipboard content"),
            ("📜 Clipboard History", "View clipboard history"),
            ("🔠 UPPERCASE", "Convert clipboard text to uppercase"),
            ("🔡 lowercase", "Convert clipboard text to lowercase"),
            ("🔤 Title Case", "Convert clipboard text to title case"),
            ("✏️ Sentence case", "Convert clipboard text to sentence case"),
            ("🔄 Toggle Case", "Toggle case of clipboard text"),
            ("✂️ Trim Whitespace", "Remove leading and trailing spaces"),
            ("🧹 Remove Extra Spaces", "Remove multiple spaces"),
            ("↔️ Remove Line Breaks", "Remove all line breaks"),
            ("↕️ Add Line Breaks", "Add line breaks at intervals"),
            ("🚫 Remove Special Chars", "Remove special characters"),
            ("🔢 Remove Numbers", "Remove all numbers from text"),
            ("📖 Word Count", "Count words and characters"),
            ("🔄 Reverse Text", "Reverse the text"),
            ("📊 Sort Lines", "Sort lines alphabetically"),
            ("🔗 Extract URLs", "Extract all URLs from text"),
            ("📧 Extract Emails", "Extract all email addresses"),
        ]

        for text, command in actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=lambda c=command: self.quick_command(c),
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def create_messaging_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1a1d2e")
        notebook.add(tab, text="📱 Messaging")

        canvas = tk.Canvas(tab, bg="#1a1d2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1d2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        actions = [
            ("👥 Add Contact", "Add contact John with phone 555-1234"),
            ("📋 List Contacts", "List all contacts"),
            ("📧 Send Email", "Send email to example@email.com"),
            ("💬 Send WhatsApp", "Send WhatsApp message"),
            ("📨 Email with Template", "Send template email"),
            ("📎 Email with Attachment", "Send email with attachment"),
            ("🎥 Open YouTube", "Search YouTube for music"),
            ("▶️ Play YouTube Video", "Play YouTube video"),
        ]

        for text, command in actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=lambda c=command: self.quick_command(c),
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def create_system_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1a1d2e")
        notebook.add(tab, text="⚙️ System")

        canvas = tk.Canvas(tab, bg="#1a1d2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1d2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Direct action buttons (lock and shutdown)
        direct_actions = [
            ("🔒 Lock Computer", self.direct_lock_screen, "#f38ba8"),
            ("⚠️ Shutdown Computer", self.direct_shutdown_system, "#f38ba8"),
        ]

        for text, command_func, color in direct_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg=color,
                            fg="#e0e0e0",
                            font=("Segoe UI", 10, "bold"),
                            relief="flat",
                            cursor="hand2",
                            command=command_func,
                            anchor="w",
                            padx=15,
                            pady=12,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            hover_color = "#fab387" if color == "#f38ba8" else "#45475a"
            self.add_hover_effect(btn, color, hover_color)

        # Separator
        separator = tk.Frame(scrollable_frame, bg="#3d4466", height=2)
        separator.pack(fill="x", padx=8, pady=8)

        # AI-powered actions (through command parsing)
        actions = [
            ("📊 System Report", "Get full system report"),
            ("💾 Check Disk Usage", "Show disk usage"),
            ("🧠 Check Memory", "Show memory usage"),
            ("⚡ CPU Usage", "Get CPU usage"),
            ("📂 Organize Downloads", "Organize downloads folder"),
            ("🔍 Find Large Files", "Find large files"),
            ("📁 Find Duplicates", "Find duplicate files"),
            ("🗜️ Compress Old Files", "Compress files older than 90 days"),
            ("💤 Sleep Computer", "Put computer to sleep"),
            ("🔊 Volume Control", "Set volume to 50"),
        ]

        for text, command in actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=lambda c=command: self.quick_command(c),
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def create_productivity_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1a1d2e")
        notebook.add(tab, text="📈 Productivity")

        canvas = tk.Canvas(tab, bg="#1a1d2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1d2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        actions = [
            ("📊 Screen Time Dashboard", "Show screen time dashboard"),
            ("🎯 Enable Focus Mode", "Enable focus mode for 2 hours"),
            ("🚫 Block Distractions", "Block distracting websites"),
            ("📈 Productivity Score", "Get my productivity score"),
            ("💧 Water Reminder", "Send water reminder"),
            ("📋 Daily Summary", "Generate daily summary"),
            ("📝 Smart Reply", "Generate smart reply"),
            ("✉️ Email Template", "Generate professional email template"),
            ("📊 Workflow Dashboard", "Show workflow dashboard"),
        ]

        for text, command in actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=lambda c=command: self.quick_command(c),
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def create_utilities_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1a1d2e")
        notebook.add(tab, text="🔧 Utilities")

        canvas = tk.Canvas(tab, bg="#1a1d2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1d2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        actions = [
            ("🌤️ Get Weather", "Get weather for New York"),
            ("📰 Get News", "Get latest technology news"),
            ("🌍 Translate to Spanish", "Translate 'Hello, how are you?' to Spanish"),
            ("🧮 Calculate", "Calculate 2 + 2 * 5"),
            ("💱 Currency Conversion", "Convert 100 USD to EUR"),
            ("🔐 Generate Password", "Generate a strong password"),
            ("🗝️ List Passwords", "List all saved passwords"),
            ("📝 Add Note", "Add note: Meeting tomorrow at 3 PM"),
            ("📋 List Notes", "List all my notes"),
            ("📅 Add Event", "Add event: Team meeting tomorrow at 2 PM"),
            ("📆 Today's Events", "Show today's events"),
            ("🗓️ Upcoming Events", "Show upcoming events"),
        ]

        for text, command in actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=lambda c=command: self.quick_command(c),
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def create_ecosystem_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1a1d2e")
        notebook.add(tab, text="🌐 Ecosystem")

        canvas = tk.Canvas(tab, bg="#1a1d2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1d2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        actions = [
            ("📊 Unified Dashboard", "Show ecosystem dashboard"),
            ("☀️ Morning Briefing", "Give me morning briefing"),
            ("🌙 Evening Summary", "Show evening summary"),
            ("💡 Smart Suggestions", "Give me smart suggestions"),
            ("🔍 Smart Search", "Smart search for meeting"),
            ("📈 Productivity Insights", "Show productivity insights"),
            ("🧹 Auto Organize", "Auto organize ecosystem"),
            ("⚡ Create Workflow", "Create workflow: Morning Routine"),
            ("📋 List Workflows", "List all workflows"),
            ("🚀 Run Workflow", "Run workflow: Morning Routine"),
            ("🔗 Cross-Module Search", "Search everywhere for project"),
            ("📅 Today Overview", "What's my schedule today?"),
            ("🎯 Daily Goals", "Show my daily goals"),
            ("📊 Weekly Summary", "Generate weekly summary"),
        ]

        for text, command in actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=lambda c=command: self.quick_command(c),
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def create_ai_features_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1a1d2e")
        notebook.add(tab, text="🤖 AI Features")

        canvas = tk.Canvas(tab, bg="#1a1d2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1d2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        header = tk.Label(scrollable_frame,
                          text="🤖 ADVANCED AI CAPABILITIES",
                          bg="#1a1d2e",
                          fg="#00d4aa",
                          font=("Segoe UI", 12, "bold"))
        header.pack(pady=12)

        info = tk.Label(scrollable_frame,
                        text="80+ AI-powered features available",
                        bg="#1a1d2e",
                        fg="#b0b0b0",
                        font=("Segoe UI", 9))
        info.pack(pady=(0, 15))

        screen_monitor_section = tk.Label(scrollable_frame,
                                          text="👁️ AI SCREEN MONITORING SYSTEM (Next-Gen)",
                                          bg="#1a1d2e",
                                          fg="#f9e2af",
                                          font=("Segoe UI", 11, "bold"))
        screen_monitor_section.pack(pady=(10, 8), anchor="w", padx=8)

        info_label = tk.Label(scrollable_frame,
                              text="Real-time AI monitoring with intelligent triggers, analytics, and automated actions",
                              bg="#1a1d2e",
                              fg="#b0b0b0",
                              font=("Segoe UI", 9, "italic"))
        info_label.pack(pady=(0, 8), anchor="w", padx=8)

        screen_monitor_actions = [
            ("📊 Productivity Analysis (Instant)", self.ai_monitor_productivity),
            ("🔒 Security Scan (Instant)", self.ai_monitor_security),
            ("⚡ Performance Analysis (Instant)", self.ai_monitor_performance),
            ("🐛 Error Detection (Instant)", self.ai_monitor_errors),
            ("🎨 UX/Design Review (Instant)", self.ai_monitor_ux),
            ("♿ Accessibility Audit (Instant)", self.ai_monitor_accessibility),
            ("💻 Code Review (Instant)", self.ai_monitor_code),
            ("🤖 Automation Discovery (Instant)", self.ai_monitor_automation),
            ("", None),
            ("🔄 Start Continuous Monitoring", self.ai_monitor_start_continuous),
            ("⏸️ Pause/Resume Monitoring", self.ai_monitor_pause_resume),
            ("🛑 Stop Monitoring", self.ai_monitor_stop),
            ("", None),
            ("📈 View Analytics Dashboard", self.ai_monitor_view_analytics),
            ("📊 Productivity Trends", self.ai_monitor_productivity_trends),
            ("🚨 Recent Alerts", self.ai_monitor_view_alerts),
            ("⚙️ Configure Settings", self.ai_monitor_configure),
            ("🧹 Clear Analytics Data", self.ai_monitor_clear_analytics),
        ]

        for text, command in screen_monitor_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

        rag_section = tk.Label(scrollable_frame,
                               text="🧠 DESKTOP RAG - SMART FILE INTELLIGENCE",
                               bg="#1a1d2e",
                               fg="#f9e2af",
                               font=("Segoe UI", 11, "bold"))
        rag_section.pack(pady=(15, 8), anchor="w", padx=8)

        rag_actions = [
            ("🚀 Quick Index My Files", "Index my desktop files"),
            ("📂 Index Specific Folder", "Index C:\\Users folder"),
            ("🔍 Search Files", "Search files for Python"),
            ("💬 Ask About My Files", "What Python projects do I have?"),
            ("📊 Summarize Folder", "Summarize my Documents folder"),
            ("🔎 Find Duplicate Files", "Find duplicate files in my computer"),
            ("📈 Show RAG Statistics", "Show desktop index statistics"),
        ]

        for text, command in rag_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=lambda c=command: self.quick_command(c),
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

        smart_automation_section = tk.Label(scrollable_frame,
                                            text="🎯 SMART AUTOMATION & AI",
                                            bg="#1a1d2e",
                                            fg="#f9e2af",
                                            font=("Segoe UI", 11, "bold"))
        smart_automation_section.pack(pady=(15, 8), anchor="w", padx=8)

        smart_info = tk.Label(scrollable_frame,
                              text="9 intelligent automation features powered by AI",
                              bg="#1a1d2e",
                              fg="#b0b0b0",
                              font=("Segoe UI", 9, "italic"))
        smart_info.pack(pady=(0, 8), anchor="w", padx=8)

        smart_actions = [
            ("🐛 Auto-Bug Fixer", self.smart_auto_bug_fixer),
            ("📅 Meeting Scheduler AI", self.smart_meeting_scheduler),
            ("📁 Smart File Recommendations", self.smart_file_recommender),
            ("📝 Auto-Documentation Generator", self.smart_doc_generator),
            ("⚡ Intelligent Command Shortcuts", self.smart_command_shortcuts),
            ("🔀 Project Context Switcher", self.smart_context_switcher),
            ("🎯 Task Auto-Prioritizer", self.smart_task_prioritizer),
            ("🔧 Workflow Auto-Optimizer", self.smart_workflow_optimizer),
            ("📋 Smart Template Generator", self.smart_template_generator),
            ("", None),
            ("📊 Smart Automation Dashboard", self.smart_automation_dashboard),
        ]

        for text, command in smart_actions:
            if text:
                btn = tk.Button(scrollable_frame,
                                text=text,
                                bg="#2e3350",
                                fg="#e0e0e0",
                                font=("Segoe UI", 10),
                                relief="flat",
                                cursor="hand2",
                                command=command,
                                anchor="w",
                                padx=15,
                                pady=10,
                                activebackground="#3d4466")
                btn.pack(fill="x", padx=8, pady=3)
                self.add_hover_effect(btn, "#313244", "#45475a")

        ai_section = tk.Label(scrollable_frame,
                              text="💬 AI ASSISTANTS & TEXT GENERATION",
                              bg="#1a1d2e",
                              fg="#f9e2af",
                              font=("Segoe UI", 11, "bold"))
        ai_section.pack(pady=(15, 8), anchor="w", padx=8)

        actions = [
            ("📋 List All AI Features", "List all AI features"),
            ("💬 Conversational AI", "Chat with AI about the weather"),
            ("🎓 Educational Assistant", "Explain quantum physics simply"),
            ("👔 Customer Service Bot", "Help with customer inquiry about returns"),
            ("🎯 Domain Expert", "Ask expert about machine learning"),
            ("📖 Story Writer", "Write a short sci-fi story about robots"),
            ("✍️ Content Creator", "Create a blog post about productivity"),
            ("📰 Article Generator", "Generate article about AI trends"),
            ("🔍 Text Summarizer", "Summarize this text"),
            ("🎨 Creative Writer", "Write a creative poem about nature"),
        ]

        for text, command in actions:
            if text:
                btn = tk.Button(scrollable_frame,
                                text=text,
                                bg="#2e3350",
                                fg="#e0e0e0",
                                font=("Segoe UI", 10),
                                relief="flat",
                                cursor="hand2",
                                command=lambda c=command: self.quick_command(c),
                                anchor="w",
                                padx=15,
                                pady=10,
                                activebackground="#3d4466")
                btn.pack(fill="x", padx=8, pady=3)
                self.add_hover_effect(btn, "#313244", "#45475a")

    def create_fun_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1a1d2e")
        notebook.add(tab, text="🎉 Fun")

        canvas = tk.Canvas(tab, bg="#1a1d2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1d2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        actions = [
            ("💪 Get Motivation", "Give me motivation"),
            ("🎯 Daily Quote", "Send me a quote"),
            ("😄 Tell a Joke", "Tell me a joke"),
            ("🎲 Random Fact", "Tell me a random fact"),
            ("🎮 Play Trivia", "Ask me a trivia question"),
            ("🎨 Generate Art Prompt", "Generate art prompt"),
            ("📚 Book Recommendation", "Recommend a book"),
            ("🎬 Movie Suggestion", "Suggest a movie"),
        ]

        for text, command in actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=lambda c=command: self.quick_command(c),
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def create_advanced_ai_tab(self, notebook):
        """Advanced AI Enhancements - Multi-modal, Memory, Learning, Predictions"""
        tab = tk.Frame(notebook, bg="#1a1d2e")
        notebook.add(tab, text="🧠 Advanced AI")

        header_frame = tk.Frame(tab, bg="#252941")
        header_frame.pack(fill="x", pady=(10, 0), padx=10)

        header = tk.Label(header_frame,
                          text="🧠 Advanced AI Enhancements",
                          bg="#252941",
                          fg="#cba6f7",
                          font=("Segoe UI", 14, "bold"))
        header.pack(pady=12)

        info = tk.Label(header_frame,
                        text="👁️ Multi-Modal • 🧠 Contextual Memory • 📚 Learning from Corrections • 🔮 Predictive Actions",
                        bg="#252941",
                        fg="#b0b0b0",
                        font=("Segoe UI", 9, "italic"))
        info.pack(pady=(0, 12))

        main_container = tk.Frame(tab, bg="#1a1d2e")
        main_container.pack(fill="both", expand=True, padx=10, pady=5)

        left_column = tk.Frame(main_container, bg="#1a1d2e")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 5))

        multi_modal_section = tk.Label(left_column,
                                       text="👁️ MULTI-MODAL AI",
                                       bg="#1a1d2e",
                                       fg="#cba6f7",
                                       font=("Segoe UI", 11, "bold"))
        multi_modal_section.pack(pady=(10, 8), anchor="w", padx=8)

        mm_buttons = [
            ("🧠 Analyze Current Screen", lambda: self.advanced_ai_analyze_screen()),
            ("🎤 Voice + Vision Analysis", lambda: self.advanced_ai_voice_vision()),
            ("📊 Multi-Modal Statistics", lambda: self.advanced_ai_mm_stats())
        ]

        for text, command in mm_buttons:
            btn = tk.Button(left_column,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

        memory_section = tk.Label(left_column,
                                  text="🧠 CONTEXTUAL MEMORY",
                                  bg="#1a1d2e",
                                  fg="#00d4aa",
                                  font=("Segoe UI", 11, "bold"))
        memory_section.pack(pady=(15, 8), anchor="w", padx=8)

        memory_buttons = [
            ("📝 Remember Something", lambda: self.advanced_ai_remember()),
            ("🔍 Recall Memories", lambda: self.advanced_ai_recall()),
            ("⚙️ Update Preferences", lambda: self.advanced_ai_preferences()),
            ("📊 Memory Statistics", lambda: self.advanced_ai_memory_stats())
        ]

        for text, command in memory_buttons:
            btn = tk.Button(left_column,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

        learning_section = tk.Label(left_column,
                                    text="📚 CORRECTION LEARNING",
                                    bg="#1a1d2e",
                                    fg="#00ff88",
                                    font=("Segoe UI", 11, "bold"))
        learning_section.pack(pady=(15, 8), anchor="w", padx=8)

        learning_buttons = [
            ("✏️ Record Correction", lambda: self.advanced_ai_record_correction()),
            ("📈 Learning Report", lambda: self.advanced_ai_learning_report()),
            ("🎯 Apply Learning", lambda: self.advanced_ai_apply_learning())
        ]

        for text, command in learning_buttons:
            btn = tk.Button(left_column,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

        predictions_section = tk.Label(left_column,
                                       text="🔮 PREDICTIVE ACTIONS",
                                       bg="#1a1d2e",
                                       fg="#f9e2af",
                                       font=("Segoe UI", 11, "bold"))
        predictions_section.pack(pady=(15, 8), anchor="w", padx=8)

        pred_buttons = [
            ("🔮 Get Predictions", lambda: self.advanced_ai_predictions()),
            ("💡 Proactive Suggestions", lambda: self.advanced_ai_suggestions()),
            ("📊 Prediction Accuracy", lambda: self.advanced_ai_accuracy())
        ]

        for text, command in pred_buttons:
            btn = tk.Button(left_column,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

        right_column = tk.Frame(main_container, bg="#1a1d2e")
        right_column.pack(side="right", fill="both", expand=True, padx=(5, 0))

        output_label = tk.Label(right_column,
                                text="📋 Output Console",
                                bg="#1a1d2e",
                                fg="#e0e0e0",
                                font=("Segoe UI", 11, "bold"))
        output_label.pack(pady=(10, 5), anchor="w", padx=8)

        self.advanced_ai_output = scrolledtext.ScrolledText(
            right_column,
            bg="#16182a",
            fg="#e0e0e0",
            font=("Consolas", 10),
            wrap=tk.WORD,
            height=25,
            state='disabled',
            relief="flat",
            padx=10,
            pady=10
        )
        self.advanced_ai_output.pack(fill="both", expand=True, padx=8, pady=(0, 10))

        self.advanced_ai_output.tag_config("success", foreground="#a6e3a1")
        self.advanced_ai_output.tag_config("error", foreground="#f38ba8")
        self.advanced_ai_output.tag_config("warning", foreground="#f9e2af")
        self.advanced_ai_output.tag_config("info", foreground="#89b4fa")
        self.advanced_ai_output.tag_config("prediction", foreground="#cba6f7")

        clear_btn = tk.Button(right_column,
                              text="🗑️ Clear Output",
                              bg="#3d4466",
                              fg="#e0e0e0",
                              font=("Segoe UI", 9),
                              relief="flat",
                              cursor="hand2",
                              command=lambda: self.advanced_ai_clear_output(),
                              padx=15,
                              pady=8)
        clear_btn.pack(pady=(0, 10), padx=8)
        self.add_hover_effect(clear_btn, "#45475a", "#585b70")

    def create_web_tools_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1a1d2e")
        notebook.add(tab, text="🌐 Web")

        canvas = tk.Canvas(tab, bg="#1a1d2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1d2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        actions = [
            ("🌐 Launch Web App", "Open In-One-Box web application"),
            ("🔗 Open GitHub", "Open GitHub repository"),
            ("📊 Dashboard View", "Show web dashboard"),
            ("⚙️ Settings Panel", "Open web settings"),
        ]

        for text, command in actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=lambda c=command: self.quick_command(c),
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def create_productivity_hub_tab(self, notebook):
        """Create comprehensive productivity hub tab with all productivity features"""
        tab = tk.Frame(notebook, bg="#1a1d2e")
        notebook.add(tab, text="📊 Productivity Hub")

        canvas = tk.Canvas(tab, bg="#1a1d2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1d2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Pomodoro Section
        pomodoro_section = tk.Label(scrollable_frame,
                                    text="🍅 POMODORO AI COACH",
                                    bg="#1a1d2e",
                                    fg="#f9e2af",
                                    font=("Segoe UI", 11, "bold"))
        pomodoro_section.pack(pady=(10, 8), anchor="w", padx=8)

        pomodoro_actions = [
            ("🍅 Start Pomodoro (25 min)", lambda: self.start_pomodoro_session()),
            ("☕ Take Short Break (5 min)", lambda: self.start_short_break()),
            ("🌳 Take Long Break (15 min)", lambda: self.start_long_break()),
            ("⏸️ Pause/Resume Session", lambda: self.toggle_pomodoro()),
            ("🛑 Stop Session", lambda: self.stop_pomodoro()),
            ("📊 View Pomodoro Stats", lambda: self.view_pomodoro_stats()),
        ]

        for text, command in pomodoro_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

        # Task Time Predictor Section
        task_section = tk.Label(scrollable_frame,
                                text="⏱️ TASK TIME PREDICTOR",
                                bg="#1a1d2e",
                                fg="#f9e2af",
                                font=("Segoe UI", 11, "bold"))
        task_section.pack(pady=(15, 8), anchor="w", padx=8)

        task_actions = [
            ("▶️ Start Task Tracking", lambda: self.start_task_tracking()),
            ("✅ Complete Current Task", lambda: self.complete_task()),
            ("📈 View Task Predictions", lambda: self.view_task_predictions()),
            ("📊 Task Analytics", lambda: self.view_task_analytics()),
        ]

        for text, command in task_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

        # Energy & Focus Section
        energy_section = tk.Label(scrollable_frame,
                                  text="🔋 ENERGY & FOCUS TRACKING",
                                  bg="#1a1d2e",
                                  fg="#f9e2af",
                                  font=("Segoe UI", 11, "bold"))
        energy_section.pack(pady=(15, 8), anchor="w", padx=8)

        energy_actions = [
            ("🔋 Check Energy Level", lambda: self.check_energy_level()),
            ("📈 Energy Trends", lambda: self.view_energy_trends()),
            ("🎯 Get Break Suggestion", lambda: self.get_break_suggestion()),
            ("⚠️ Distraction Check", lambda: self.check_distractions()),
            ("📊 Focus Report", lambda: self.view_focus_report()),
        ]

        for text, command in energy_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

        # Productivity Dashboard Section
        dashboard_section = tk.Label(scrollable_frame,
                                     text="📊 PRODUCTIVITY DASHBOARD",
                                     bg="#1a1d2e",
                                     fg="#f9e2af",
                                     font=("Segoe UI", 11, "bold"))
        dashboard_section.pack(pady=(15, 8), anchor="w", padx=8)

        dashboard_actions = [
            ("📊 View Complete Dashboard", lambda: self.view_productivity_dashboard()),
            ("📅 Weekly Summary", lambda: self.view_weekly_summary()),
            ("📈 Productivity Trends", lambda: self.view_productivity_trends()),
            ("🎯 Get Recommendations", lambda: self.get_productivity_recommendations()),
        ]

        for text, command in dashboard_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def create_tools_utilities_tab(self, notebook):
        """Create tools & utilities tab with password vault, notes, calendar, etc."""
        tab = tk.Frame(notebook, bg="#1a1d2e")
        notebook.add(tab, text="🛠️ Tools & Utilities")

        canvas = tk.Canvas(tab, bg="#1a1d2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1d2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Password Vault Section
        password_section = tk.Label(scrollable_frame,
                                    text="🔐 PASSWORD VAULT",
                                    bg="#1a1d2e",
                                    fg="#f9e2af",
                                    font=("Segoe UI", 11, "bold"))
        password_section.pack(pady=(10, 8), anchor="w", padx=8)

        password_actions = [
            ("➕ Add Password", lambda: self.add_password_dialog()),
            ("🔍 View Password", lambda: self.view_password_dialog()),
            ("📋 List All Passwords", lambda: self.list_passwords()),
            ("🔑 Generate Secure Password", lambda: self.generate_password()),
        ]

        for text, command in password_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

        # Quick Notes Section
        notes_section = tk.Label(scrollable_frame,
                                 text="📝 QUICK NOTES",
                                 bg="#1a1d2e",
                                 fg="#f9e2af",
                                 font=("Segoe UI", 11, "bold"))
        notes_section.pack(pady=(15, 8), anchor="w", padx=8)

        notes_actions = [
            ("➕ New Note", lambda: self.add_note_dialog()),
            ("📋 View All Notes", lambda: self.list_notes()),
            ("🔍 Search Notes", lambda: self.search_notes_dialog()),
            ("📌 Pinned Notes", lambda: self.view_pinned_notes()),
        ]

        for text, command in notes_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

        # Calendar Section
        calendar_section = tk.Label(scrollable_frame,
                                    text="📅 CALENDAR MANAGER",
                                    bg="#1a1d2e",
                                    fg="#f9e2af",
                                    font=("Segoe UI", 11, "bold"))
        calendar_section.pack(pady=(15, 8), anchor="w", padx=8)

        calendar_actions = [
            ("➕ Add Event", lambda: self.add_event_dialog()),
            ("📅 Today's Events", lambda: self.view_today_events()),
            ("📆 This Week", lambda: self.view_week_events()),
            ("🔔 Upcoming Reminders", lambda: self.view_reminders()),
        ]

        for text, command in calendar_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

        # Weather & News Section
        weather_section = tk.Label(scrollable_frame,
                                   text="🌤️ WEATHER & NEWS",
                                   bg="#1a1d2e",
                                   fg="#f9e2af",
                                   font=("Segoe UI", 11, "bold"))
        weather_section.pack(pady=(15, 8), anchor="w", padx=8)

        weather_actions = [
            ("🌤️ Get Weather", lambda: self.get_weather_dialog()),
            ("📅 3-Day Forecast", lambda: self.get_forecast()),
            ("📰 Latest News Headlines", lambda: self.get_news()),
            ("💼 Tech News", lambda: self.get_tech_news()),
        ]

        for text, command in weather_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

        # Translation Section
        translation_section = tk.Label(scrollable_frame,
                                       text="🌐 TRANSLATION SERVICE",
                                       bg="#1a1d2e",
                                       fg="#f9e2af",
                                       font=("Segoe UI", 11, "bold"))
        translation_section.pack(pady=(15, 8), anchor="w", padx=8)

        translation_actions = [
            ("🌐 Translate Text", lambda: self.translate_text_dialog()),
            ("🔍 Detect Language", lambda: self.detect_language_dialog()),
            ("📚 Supported Languages", lambda: self.show_supported_languages()),
        ]

        for text, command in translation_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#3d4466")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def toggle_boi_mode(self):
        """Toggle BOI personality mode"""
        self.boi_mode = not self.boi_mode
        if self.boi_mode:
            self.boi_toggle_btn.config(text="🤖 BOI Mode: ON", bg="#00d4aa")
            self.update_output("\n", "info")
            self.update_output("🤖 BOI Mode Activated\n", "success")
            self.update_output(self.boi.get_status_update('ready') + "\n", "info")
            self.update_output("\n\n", "info")
        else:
            self.boi_toggle_btn.config(text="🤖 BOI Mode: OFF", bg="#3d4466")
            self.update_output("\n", "info")
            self.update_output("Standard Mode Activated\n", "warning")
            self.update_output("\n\n", "info")

    def toggle_self_operating_mode(self):
        """Toggle Self-Operating Computer feature on/off"""
        self.self_operating_mode = not self.self_operating_mode
        if self.self_operating_mode:
            self.self_operating_toggle_btn.config(text="🎮 Self-Operating: ON", bg="#cba6f7")
            self.update_output("\n", "info")
            self.update_output("🎮 Self-Operating Computer Mode: ENABLED\n", "success")
            self.update_output("AI can now autonomously control your computer based on prompts.\n", "info")
            self.update_output("Use the 🎮 Self-Operating tab to give objectives.\n", "info")
            self.update_output("\n\n", "info")
        else:
            self.self_operating_toggle_btn.config(text="🎮 Self-Operating: OFF", bg="#3d4466")
            self.update_output("\n", "info")
            self.update_output("🎮 Self-Operating Computer Mode: DISABLED\n", "warning")
            self.update_output("Self-operating features are now turned off.\n", "info")
            self.update_output("\n\n", "info")

    def open_user_settings(self):
        """Open user profile settings dialog"""
        try:
            open_user_settings(self.root)
        except Exception as e:
            self.update_output(f"❌ Error opening user settings: {e}\n", "error")

    def show_boi_greeting(self):
        """Show BOI greeting message"""
        # Use personalized greeting from user profile
        personalized_greeting = self.user_profile.get_greeting()
        greeting = self.boi.get_greeting()

        self.update_output("\n", "info")
        self.update_output("🤖 Vatsal AI Assistant (Powered by BOI)\n", "success")
        self.update_output("\n", "info")
        self.update_output(f"{personalized_greeting}\n", "success")
        self.update_output(f"{greeting}\n\n", "info")

        # Show proactive suggestion
        suggestion = self.boi.get_proactive_suggestion()
        self.update_output(f"{suggestion}\n\n", "command")

        # Record interaction
        self.user_profile.record_interaction()

    def get_boi_response(self, user_input, command_result=None):
        """Get BOI personality response"""
        if self.boi_mode and self.boi.ai_available:
            return self.boi.process_with_personality(user_input, command_result)
        return command_result

    def start_boi_ai_conversation(self):
        """Start conversation with Simple Chat"""
        if self.simple_chatbot:
            greeting = self.simple_chatbot.greeting()
        else:
            greeting = "Hello! I'm Vatsal, your AI assistant. How can I help you today?"

        self._add_boi_ai_message("Vatsal", greeting)
        self.boi_conversation_active = True

    def send_to_boi_ai(self):
        """Send message to BOI"""
        user_message = self.boi_input.get().strip()
        if not user_message:
            return

        self.boi_input.delete(0, tk.END)
        self._add_boi_ai_message("YOU", user_message)

        thread = threading.Thread(target=self._process_boi_ai_message, args=(user_message,))
        thread.start()

    def _process_boi_ai_message(self, user_message):
        """Process message with Simple Chat in background with autonomous execution"""
        try:
            if self.simple_chatbot:
                response = self.simple_chatbot.chat(user_message)
            else:
                response = "Chatbot not available. Please check your Gemini API key configuration."

            self._add_boi_ai_message("BOI", response)

            # Autonomous mode: Detect and execute tasks
            if self.self_operating_mode and self.automation_orchestrator:
                autonomous_suggestions = self._detect_autonomous_actions(user_message, response)

                if autonomous_suggestions:
                    # Show suggestions
                    suggestion_text = "\n💡 Autonomous Suggestions:\n" + "\n".join(
                        f"  • {s}" for s in autonomous_suggestions
                    )
                    self._add_boi_ai_message("BOI", suggestion_text)

                    # Auto-execute if user explicitly requested execution
                    if any(word in user_message.lower() for word in ['execute', 'run', 'do it', 'perform', 'start']):
                        self._execute_autonomous_task(user_message, response)

        except Exception as e:
            self._add_boi_ai_message("BOI", f"Sorry, I encountered an error: {str(e)}")

    def _detect_autonomous_actions(self, user_msg, ai_response):
        """Detect potential autonomous actions from conversation"""
        suggestions = []
        msg_lower = user_msg.lower()

        # Code execution
        if any(word in msg_lower for word in ['code', 'program', 'script', 'function']):
            suggestions.append("I can execute code in a sandbox environment")
            if self.self_operating_computer:
                suggestions.append("Self-operating mode can test this code")

        # File operations
        elif any(word in msg_lower for word in ['file', 'folder', 'organize', 'clean']):
            suggestions.append("I can organize files automatically")
            suggestions.append("Ready to execute file operations")

        # System tasks
        elif any(word in msg_lower for word in ['open', 'launch', 'start', 'close']):
            suggestions.append("I can execute system commands")
            if self.executor:
                suggestions.append("Command executor ready")

        # Task automation
        elif any(word in msg_lower for word in ['automate', 'schedule', 'workflow']):
            suggestions.append("I can create automated workflows")
            suggestions.append("Self-operating mode available")

        return suggestions[:3]

    def _execute_autonomous_task(self, user_msg, ai_response):
        """Execute autonomous task using the orchestrator"""
        if not self.automation_orchestrator:
            return

        msg_lower = user_msg.lower()

        # Determine task type and create task
        if 'self' in msg_lower or 'auto' in msg_lower:
            task_type = "self_operating"
            intent = "Self-operating task"
        else:
            task_type = "command"
            intent = "Command execution task"

        # Submit task to orchestrator
        task_id = self.automation_orchestrator.submit_task(
            intent=intent,
            command=user_msg,
            task_type=task_type,
            require_confirmation=False  # Confirmation handled by callback
        )

        if task_id:
            self._add_boi_ai_message("BOI", f"🤖 Autonomous task queued: {task_id}")

    def _add_boi_ai_message(self, sender, message):
        """Add message to BOI conversation display"""
        self.boi_conversation_display.config(state='normal')

        timestamp = datetime.now().strftime("%I:%M:%S %p")

        if sender == "BOI":
            self.boi_conversation_display.insert(tk.END, f"\n🤖 BOI", "boi")
            self.boi_conversation_display.insert(tk.END, f" ({timestamp})\n", "timestamp")
            self.boi_conversation_display.insert(tk.END, f"{message}\n", "")
        else:
            self.boi_conversation_display.insert(tk.END, f"\n👤 {sender}", "user")
            self.boi_conversation_display.insert(tk.END, f" ({timestamp})\n", "timestamp")
            self.boi_conversation_display.insert(tk.END, f"{message}\n", "")

        self.boi_conversation_display.config(state='disabled')
        self.boi_conversation_display.see(tk.END)

    def boi_ai_get_suggestion(self):
        """Get a friendly prompt from BOI"""
        suggestions = [
            "💡 Try asking me: 'What's the weather like in programming?'",
            "💡 I can help with: General questions, coding, math, science, and more!",
            "💡 Ask me anything! From 'How do loops work?' to 'Tell me a joke'",
            "💡 Need help? Try: 'Explain Python functions' or 'What's 5+5?'",
            "💡 I'm here to chat! Ask me about any topic you're curious about."
        ]
        import random
        self._add_boi_ai_message("BOI", random.choice(suggestions))

    def clear_boi_ai_conversation(self):
        """Clear conversation history"""
        if self.simple_chatbot:
            self.simple_chatbot.reset()

        self.boi_conversation_display.config(state='normal')
        self.boi_conversation_display.delete(1.0, tk.END)
        self.boi_conversation_display.config(state='disabled')
        self.boi_conversation_active = False
        messagebox.showinfo("Cleared", "Chat cleared! Ready for a fresh conversation.")

    def show_boi_ai_stats(self):
        """Show comprehensive chatbot and autonomous system statistics"""
        # Chatbot stats
        if self.simple_chatbot:
            conv_count = len(self.simple_chatbot.conversation_history)
            chatbot_status = f"""💬 Chat Session:
  • Conversation: {conv_count // 2} exchanges
  • Model: Gemini 2.5 Flash (Latest)
  • Memory: Last 10 exchanges
  • Status: ✅ Active"""
        else:
            chatbot_status = "💬 Chat: ❌ Not available"

        # Autonomous system stats
        if self.automation_orchestrator:
            orch_stats = self.automation_orchestrator.get_statistics()
            autonomous_status = f"""
🤖 Autonomous System:
  • Autonomous Mode: {'✅ ON' if self.self_operating_mode else '❌ OFF'}
  • Orchestrator: {'✅ Running' if orch_stats['orchestrator_running'] else '❌ Stopped'}
  • Total Tasks: {orch_stats['total_tasks']}
  • Successful: {orch_stats['successful_tasks']}
  • Failed: {orch_stats['failed_tasks']}
  • Running: {orch_stats['running_tasks']}
  • Pending: {orch_stats['pending_tasks']}"""
        else:
            autonomous_status = "\n🤖 Autonomous: ❌ Not available"

        # Self-operating status
        if self.self_operating_computer:
            self_op_status = "\n🎮 Self-Operating: ✅ Ready"
        else:
            self_op_status = "\n🎮 Self-Operating: ❌ Not available"

        # Executor status
        if self.executor:
            exec_status = "\n⚡ Command Executor: ✅ Ready"
        else:
            exec_status = "\n⚡ Command Executor: ❌ Not available"

        stats_message = f"""📊 BOI (Barely Obeys Instructions) System Statistics

{chatbot_status}{autonomous_status}{self_op_status}{exec_status}

🎯 Features Available:
  • Real-time AI conversation
  • Context-aware autonomous suggestions
  • Proactive task execution
  • Self-operating capabilities
"""

        messagebox.showinfo("BOI (Barely Obeys Instructions) Stats", stats_message)

    def execute_boi_automator_command(self):
        """Execute command using BOI automator"""
        if not self.boi_automator:
            self._update_boi_automator_output("❌ BOI Automator not available. Check Gemini API key.\n", "error")
            return

        command = self.boi_automator_input.get().strip()
        if not command:
            return

        self.boi_automator_input.delete(0, tk.END)
        self._update_boi_automator_output(f"\n🎯 Command: {command}\n", "info")

        thread = threading.Thread(target=self._process_boi_automator_command, args=(command,))
        thread.start()

    def _boi_confirmation_callback(self, intent, risk_level):
        """Confirmation callback for destructive BOI actions"""
        result = messagebox.askyesno(
            "⚠️ Confirmation Required",
            f"Risk Level: {risk_level.upper()}\n\nAction: {intent}\n\nDo you want to proceed?",
            icon='warning'
        )
        return result

    def _process_boi_automator_command(self, command):
        """Process BOI automator command in background"""
        try:
            self._update_boi_automator_output("🤔 Understanding command...\n", "info")
            result = self.boi_automator.execute_command(command,
                                                           confirmation_callback=self._boi_confirmation_callback)

            if "✓" in result:
                self._update_boi_automator_output(f"\n{result}\n", "success")
            elif "✗" in result or "❌" in result:
                self._update_boi_automator_output(f"\n{result}\n", "error")
            elif "⚠️" in result:
                self._update_boi_automator_output(f"\n{result}\n", "warning")
            else:
                self._update_boi_automator_output(f"\n{result}\n", "info")

        except Exception as e:
            self._update_boi_automator_output(f"\n❌ Error: {str(e)}\n", "error")

    def _update_boi_automator_output(self, message, tag=""):
        """Update BOI automator output display"""
        self.boi_automator_output.config(state='normal')
        self.boi_automator_output.insert(tk.END, message, tag)
        self.boi_automator_output.config(state='disabled')
        self.boi_automator_output.see(tk.END)

    def boi_quick_action(self, command):
        """Execute quick action or clear output"""
        if command is None:
            self.boi_automator_output.config(state='normal')
            self.boi_automator_output.delete(1.0, tk.END)
            self.boi_automator_output.config(state='disabled')
            return

        self.boi_automator_input.delete(0, tk.END)
        self.boi_automator_input.insert(0, command)
        self.execute_boi_automator_command()

    def start_self_operating_text(self):
        """Start self-operating computer with text objective"""
        if not self.self_operating_mode:
            messagebox.showwarning(
                "Feature Disabled",
                "🎮 Self-Operating Computer mode is currently DISABLED.\n\n"
                "Please enable it using the '🎮 Self-Operating: OFF' toggle button in the header to use this feature."
            )
            self._update_soc_output("⚠️ Self-Operating mode is disabled. Enable it from the header toggle.\n",
                                    "warning")
            return

        if not self.self_operating_computer:
            self._update_soc_output("❌ Self-Operating Computer not available. Check Gemini API key.\n", "error")
            return

        if self.soc_running:
            messagebox.showwarning("Already Running", "Self-operating mode is already active!")
            return

        objective = self.soc_objective.get("1.0", tk.END).strip()
        if not objective:
            messagebox.showwarning("No Objective", "Please enter an objective first!")
            return

        self.soc_running = True
        self.soc_status_label.config(text=f"Status: Running...", fg="#f9e2af")
        self._update_soc_output(f"\n🎯 Starting self-operating mode...\n", "success")
        self._update_soc_output(f"📋 Objective: {objective}\n\n", "progress")

        self.soc_thread = threading.Thread(target=self._run_self_operating, args=(objective,), daemon=True)
        self.soc_thread.start()

        # Auto-minimize window so user can see AI working on desktop
        self.root.after(500, self.root.iconify)

    def start_self_operating_voice(self):
        """Start self-operating computer with voice objective"""
        if not self.self_operating_mode:
            messagebox.showwarning(
                "Feature Disabled",
                "🎮 Self-Operating Computer mode is currently DISABLED.\n\n"
                "Please enable it using the '🎮 Self-Operating: OFF' toggle button in the header to use this feature."
            )
            self._update_soc_output("⚠️ Self-Operating mode is disabled. Enable it from the header toggle.\n",
                                    "warning")
            return

        if not self.self_operating_computer:
            self._update_soc_output("❌ Self-Operating Computer not available. Check Gemini API key.\n", "error")
            return

        if self.soc_running:
            messagebox.showwarning("Already Running", "Self-operating mode is already active!")
            return

        self.soc_running = True
        self.soc_status_label.config(text="Status: Listening...", fg="#00d4aa")
        self._update_soc_output("\n🎤 Voice input mode activated...\n", "success")
        self._update_soc_output("Please state your objective clearly.\n\n", "progress")

        self.soc_thread = threading.Thread(target=self._run_self_operating_voice, daemon=True)
        self.soc_thread.start()

        # Auto-minimize window so user can see AI working on desktop
        self.root.after(500, self.root.iconify)

    def stop_self_operating(self):
        """Stop the self-operating computer"""
        if not self.soc_running:
            messagebox.showinfo("Not Running", "Self-operating mode is not currently active.")
            return

        self.soc_running = False
        self.soc_status_label.config(text="Status: Stopped", fg="#00d4aa")
        self._update_soc_output("\n🛑 Self-operating mode stopped by user.\n", "warning")

    def _run_self_operating(self, objective):
        """Run self-operating computer in background"""
        try:
            import sys
            from io import StringIO

            old_stdout = sys.stdout
            sys.stdout = StringIO()

            class GUILogger:
                def __init__(self, gui):
                    self.gui = gui

                def log(self, message, level="INFO"):
                    if "🔍" in message or "Analyzing" in message:
                        tag = "iteration"
                    elif "💭" in message or "Thought:" in message:
                        tag = "thought"
                    elif "⚡" in message or "Action:" in message:
                        tag = "action"
                    elif "📊" in message or "Progress:" in message:
                        tag = "progress"
                    elif "✅" in message or "COMPLETE" in message:
                        tag = "success"
                    elif "❌" in message or "ERROR" in level:
                        tag = "error"
                    elif "⚠️" in message or "WARN" in level:
                        tag = "warning"
                    else:
                        tag = ""

                    self.gui._update_soc_output(message + "\n", tag)

            logger = GUILogger(self)
            self.self_operating_computer._log = lambda msg, level="INFO": logger.log(msg, level)

            result = self.self_operating_computer.operate(objective)

            sys.stdout = old_stdout

            if result.get("completed"):
                self._update_soc_output(f"\n✅ Objective completed in {result['duration_seconds']}s!\n", "success")
                self._update_soc_output(f"📊 Total iterations: {result['iterations']}\n", "progress")
                self.soc_status_label.config(text="Status: Completed ✅", fg="#00ff88")
            else:
                self._update_soc_output(f"\n⏸️ Session ended (max iterations reached)\n", "warning")
                self._update_soc_output(f"📊 Total iterations: {result['iterations']}\n", "progress")
                self.soc_status_label.config(text="Status: Incomplete", fg="#f9e2af")

            self.soc_running = False

        except Exception as e:
            self._update_soc_output(f"\n❌ Error: {str(e)}\n", "error")
            self.soc_status_label.config(text="Status: Error", fg="#00d4aa")
            self.soc_running = False

    def _run_self_operating_voice(self):
        """Run self-operating computer with voice input"""
        try:
            result = self.self_operating_computer.operate_with_voice()

            if not result:
                self._update_soc_output("❌ Voice input failed. Please try again.\n", "error")
                self.soc_status_label.config(text="Status: Ready", fg="#00ff88")
                self.soc_running = False
                return

            if result.get("completed"):
                self._update_soc_output(f"\n✅ Objective completed!\n", "success")
                self.soc_status_label.config(text="Status: Completed ✅", fg="#00ff88")
            else:
                self._update_soc_output(f"\n⏸️ Session ended\n", "warning")
                self.soc_status_label.config(text="Status: Incomplete", fg="#f9e2af")

            self.soc_running = False

        except Exception as e:
            self._update_soc_output(f"\n❌ Error: {str(e)}\n", "error")
            self.soc_status_label.config(text="Status: Error", fg="#00d4aa")
            self.soc_running = False

    def _update_soc_output(self, message, tag=""):
        """Update self-operating computer output display"""
        self.soc_output.config(state='normal')
        self.soc_output.insert(tk.END, message, tag)
        self.soc_output.config(state='disabled')
        self.soc_output.see(tk.END)

    def clear_soc_output(self):
        """Clear self-operating computer output"""
        self.soc_output.config(state='normal')
        self.soc_output.delete(1.0, tk.END)
        self.soc_output.config(state='disabled')
        messagebox.showinfo("Cleared", "Output cleared!")

    def show_soc_guide(self):
        """Show self-operating computer guide"""
        guide = """
🎮 SELF-OPERATING COMPUTER GUIDE

Powered by Gemini Vision, this feature lets AI autonomously control
your computer to accomplish objectives.

HOW IT WORKS:
1. AI views your screen (takes screenshots)
2. Analyzes what it sees using Gemini Vision
3. Decides the next mouse/keyboard action
4. Executes the action
5. Repeats until objective is complete

INPUT MODES:
▶️ Text Mode: Type your objective and click Start
🎤 Voice Mode: Speak your objective when prompted

EXAMPLE OBJECTIVES:
• Open Google Chrome and search for Python tutorials
• Go to YouTube and play a video about AI
• Open Calculator and calculate 25 × 47
• Create a new folder on Desktop named 'AI Projects'
• Open Notepad and write 'Hello World'

TIPS:
✓ Be specific and clear with objectives
✓ Simple tasks work best (1-3 steps)
✓ AI can see and interact with visible UI elements
✓ Click Stop if you need to interrupt
✓ Check screenshots/ folder to see what AI saw

SAFETY:
⚠️ AI will not perform destructive actions without context
⚠️ Move mouse to corner to trigger failsafe (PyAutoGUI)
⚠️ Maximum 30 iterations per session

Based on OthersideAI's self-operating-computer framework
"""
        messagebox.showinfo("Self-Operating Computer Guide", guide)

    def view_soc_screenshots(self):
        """Open screenshots folder"""
        import subprocess
        import platform

        screenshots_dir = Path("screenshots")
        if not screenshots_dir.exists():
            messagebox.showinfo("No Screenshots", "No screenshots have been taken yet.")
            return

        try:
            if platform.system() == "Windows":
                os.startfile(screenshots_dir)
            elif platform.system() == "Darwin":
                subprocess.run(["open", screenshots_dir])
            else:
                subprocess.run(["xdg-open", screenshots_dir])

            self._update_soc_output("📸 Opened screenshots folder\n", "success")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder: {str(e)}")

    def auto_start_if_enabled(self):
        """Auto-start self-operating mode if enabled"""
        if self.auto_control_enabled:
            self._update_soc_output("\n🚀 Auto-starting self-operating mode...\n", "success")
            self.start_self_operating_text()
        else:
            messagebox.showinfo(
                "Auto Mode Disabled",
                "Auto Self-Control Mode is currently disabled.\n\n"
                "Enable it using the toggle button to use Ctrl+Enter quick-start."
            )

    def toggle_auto_control(self):
        """Toggle auto self-control mode on/off"""
        self.auto_control_enabled = not self.auto_control_enabled

        if self.auto_control_enabled:
            self.auto_control_btn.config(
                text="✅ Enabled",
                fg="#00ff88",
                bg="#3d4466"
            )
            self._update_soc_output("\n🔄 Auto Self-Control Mode: ENABLED\n", "success")
            self._update_soc_output("AI will automatically start self-operating mode after commands.\n", "progress")
            messagebox.showinfo(
                "Auto Mode Enabled",
                "✅ Auto Self-Control Mode is now ENABLED!\n\n"
                "When you give a command, AI will automatically:\n"
                "1. Understand the command\n"
                "2. Enter self-operating mode\n"
                "3. View the screen and perform actions\n"
                "4. Complete the objective autonomously\n\n"
                "You can toggle this off anytime."
            )
        else:
            self.auto_control_btn.config(
                text="❌ Disabled",
                fg="#00d4aa",
                bg="#2e3350"
            )
            self._update_soc_output("\n🔄 Auto Self-Control Mode: DISABLED\n", "warning")
            self._update_soc_output("Manual control restored. Use Start buttons to begin.\n", "progress")
            messagebox.showinfo(
                "Auto Mode Disabled",
                "❌ Auto Self-Control Mode is now DISABLED.\n\n"
                "Use the Start buttons to manually begin self-operating mode."
            )

    def execute_web_automation(self):
        """Execute web automation from input"""
        if not self.web_automator:
            self.update_output("❌ Web automation not available\n", "error")
            return

        command = self.web_auto_input.get().strip()
        if not command:
            self.update_output("⚠️  Please enter a command\n", "warning")
            return

        self.update_output(f"\n🤖 EXECUTING WEB AUTOMATION\n", "info")
        self.update_output(f"📋 Command: {command}\n", "info")

        def run_automation():
            try:
                result = self.web_automator.execute_task(command, interactive=False)

                if result.get('success'):
                    self.update_output(f"\n✅ Task completed successfully!\n", "success")
                    self.update_output(f"📊 Success rate: {result['successful_steps']}/{result['total_steps']}\n",
                                       "info")
                else:
                    self.update_output(f"\n⚠️  Task completed with issues\n", "warning")

                for i, step_result in enumerate(result.get('results', []), 1):
                    if step_result.get('success'):
                        self.update_output(f"   Step {i}: ✅ {step_result.get('message', 'Done')}\n", "success")
                    else:
                        self.update_output(f"   Step {i}: ❌ {step_result.get('error', 'Failed')}\n", "error")

                self.web_auto_input.delete(0, tk.END)

            except Exception as e:
                self.update_output(f"❌ Error: {str(e)}\n", "error")

        thread = threading.Thread(target=run_automation, daemon=True)
        thread.start()

    def quick_web_automation(self, command):
        """Quick web automation action"""
        if not self.web_automator:
            self.update_output("❌ Web automation not available\n", "error")
            return

        self.web_auto_input.delete(0, tk.END)
        self.web_auto_input.insert(0, command)
        self.execute_web_automation()

    def initialize_web_browser(self):
        """Initialize the web browser"""
        if not self.web_automator:
            self.update_output("❌ Web automation not available\n", "error")
            return

        self.update_output("🌐 Initializing browser...\n", "info")

        def init():
            try:
                if self.web_automator.initialize_browser():
                    self.update_output("✅ Browser initialized successfully!\n", "success")
                    self.update_output(f"📍 Ready for automation commands\n", "info")
                else:
                    self.update_output("❌ Failed to initialize browser\n", "error")
            except Exception as e:
                self.update_output(f"❌ Error: {str(e)}\n", "error")

        thread = threading.Thread(target=init, daemon=True)
        thread.start()

    def close_web_browser(self):
        """Close the web browser"""
        if not self.web_automator:
            self.update_output("❌ Web automation not available\n", "error")
            return

        try:
            self.web_automator.close_browser()
            self.update_output("🔒 Browser closed\n", "info")
        except Exception as e:
            self.update_output(f"❌ Error closing browser: {str(e)}\n", "error")

    def take_web_screenshot(self):
        """Take a screenshot of the current page"""
        import time
        if not self.web_automator:
            self.update_output("❌ Web automation not available\n", "error")
            return

        try:
            filename = f"web_screenshot_{int(time.time())}.png"
            if self.web_automator.take_screenshot(filename):
                self.update_output(f"📸 Screenshot saved: {filename}\n", "success")
                self.update_output(f"📍 URL: {self.web_automator.get_current_url()}\n", "info")
            else:
                self.update_output("❌ Screenshot failed - browser not initialized\n", "error")
        except Exception as e:
            self.update_output(f"❌ Error: {str(e)}\n", "error")

    def select_command_text(self):
        """Select all text in command input for easy editing"""
        self.command_input.select_range(0, tk.END)
        self.command_input.icursor(tk.END)

    def check_api_key(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            self.update_output("⚠️ WARNING: GEMINI_API_KEY not found in environment variables.\n", "warning")
            self.update_output("Please set your Gemini API key to use AI features.\n\n", "info")
            self.update_status("⚠️ API Key Missing", "#f9e2af")
        else:
            self.update_output("✅ Gemini AI is ready!\n", "success")
            self.update_output("Type a command or click a Quick Action button to get started.\n\n", "info")

    def quick_command(self, command):
        self.command_input.delete(0, tk.END)
        self.command_input.insert(0, command)
        self.execute_command()

    def direct_lock_screen(self):
        """Directly lock the screen without going through AI parsing"""
        if self.processing:
            messagebox.showwarning("Busy", "Please wait for the current command to finish.")
            return

        self.processing = True
        self.update_status("🔒 Locking...", "#f9e2af")

        def lock_thread():
            try:
                self.update_output(f"\n", "info")
                self.update_output("🔒 Locking the computer...\n", "info")
                result = self.system_controller.lock_screen()
                self.update_output(f"{result}\n", "success")
                self.update_status("✅ Ready", "#a6e3a1")
            except Exception as e:
                self.update_output(f"❌ Error locking screen: {str(e)}\n", "error")
                self.update_status("❌ Error", "#f38ba8")
            finally:
                self.processing = False

        threading.Thread(target=lock_thread, daemon=True).start()

    def direct_shutdown_system(self):
        """Directly shutdown the system without going through AI parsing"""
        if self.processing:
            messagebox.showwarning("Busy", "Please wait for the current command to finish.")
            return

        # Confirm shutdown action
        confirm = messagebox.askyesno(
            "Confirm Shutdown",
            "Are you sure you want to shutdown the computer?\n\nThe system will shutdown in 10 seconds."
        )

        if not confirm:
            return

        self.processing = True
        self.update_status("⚠️ Shutting down...", "#f38ba8")

        def shutdown_thread():
            try:
                self.update_output(f"\n", "info")
                self.update_output("⚠️ Initiating shutdown...\n", "warning")
                result = self.system_controller.shutdown_system(delay_seconds=10)
                self.update_output(f"{result}\n", "warning")
                self.update_status("⚠️ Shutting down", "#f38ba8")
            except Exception as e:
                self.update_output(f"❌ Error during shutdown: {str(e)}\n", "error")
                self.update_status("❌ Error", "#f38ba8")
            finally:
                self.processing = False

        threading.Thread(target=shutdown_thread, daemon=True).start()

    def execute_command(self):
        if self.processing:
            messagebox.showwarning("Busy", "Please wait for the current command to finish.")
            return

        command = self.command_input.get().strip()
        if not command:
            messagebox.showwarning("Empty Command", "Please enter a command.")
            return

        # Clear the input box immediately
        self.command_input.delete(0, tk.END)

        self.processing = True
        self.update_status("⚙️ Running...", "#f9e2af")
        self.execute_btn.config(state="disabled", text="⏳ Running...")

        thread = threading.Thread(target=self._execute_in_thread, args=(command,))
        thread.start()

    def _execute_in_thread(self, command):
        try:
            # Broadcast command started
            if self.ws_client and self.ws_client.connected:
                self.ws_client.emit('command_started', {
                    'command': command,
                    'timestamp': datetime.now().isoformat()
                })

            self.update_output(f"\n", "info")
            self.update_output(f"📝 You: {command}\n", "command")
            self.update_output(f"\n", "info")

            # BOI acknowledgment
            if self.boi_mode:
                ack = self.boi.acknowledge_command(command)
                self.update_output(f"🤖 BOI: {ack}\n\n", "info")

            command_dict = parse_command(command)

            if command_dict.get("action") == "error":
                error_msg = command_dict.get('description', 'Error processing command')

                if self.boi_mode:
                    boi_response = self.boi.process_with_personality(
                        command,
                        f"Error: {error_msg}"
                    )
                    self.update_output(f"🤖 BOI: {boi_response}\n", "error")

                    # Speak error response if voice is enabled
                    if self.voice_commander and self.voice_enabled:
                        self.voice_commander.speak(boi_response)
                else:
                    self.update_output(f"❌ {error_msg}\n", "error")
                    suggestion = get_ai_suggestion(f"User tried: {command}, but got error. Suggest alternatives.")
                    self.update_output(f"\n💡 Suggestion: {suggestion}\n", "info")

                self.update_status("❌ Error", "#f38ba8")
                return

            result = self.executor.execute(command_dict)

            if result["success"]:
                # Broadcast command completed
                if self.ws_client and self.ws_client.connected:
                    self.ws_client.emit('command_completed', {
                        'command': command,
                        'result': str(result['message']),
                        'timestamp': datetime.now().isoformat()
                    })

                # Get BOI response if mode is enabled
                if self.boi_mode:
                    boi_response = self.get_boi_response(command, result['message'])
                    self.update_output(f"🤖 BOI:\n{boi_response}\n\n", "success")

                    # Speak BOI's response if voice is enabled
                    if self.voice_commander and self.voice_enabled:
                        self.voice_commander.speak(boi_response)

                    # Show technical result in smaller text
                    self.update_output(f"📊 Technical Details:\n{result['message']}\n", "info")
                else:
                    self.update_output(f"✅ Result:\n{result['message']}\n", "success")

                self.update_status("✅ Ready", "#a6e3a1")

                # Occasionally show proactive suggestions
                import random
                if random.random() < 0.3 and self.boi_mode:  # 30% chance
                    suggestion = self.boi.get_proactive_suggestion()
                    self.update_output(f"\n{suggestion}\n", "command")

            else:
                # Broadcast command failed
                if self.ws_client and self.ws_client.connected:
                    self.ws_client.emit('command_failed', {
                        'command': command,
                        'error': str(result['message']),
                        'timestamp': datetime.now().isoformat()
                    })

                if self.boi_mode:
                    boi_response = self.boi.process_with_personality(
                        command,
                        f"Error: {result['message']}"
                    )
                    self.update_output(f"🤖 BOI: {boi_response}\n", "error")

                    # Speak error response if voice is enabled
                    if self.voice_commander and self.voice_enabled:
                        self.voice_commander.speak(boi_response)
                else:
                    self.update_output(f"❌ Error:\n{result['message']}\n", "error")

                self.update_status("❌ Error", "#f38ba8")

        except Exception as e:
            # Broadcast exception
            if self.ws_client and self.ws_client.connected:
                self.ws_client.emit('command_failed', {
                    'command': command,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })

            if self.boi_mode:
                self.update_output(f"🤖 BOI: Apologies, Sir. Encountered an unexpected error: {str(e)}\n", "error")
            else:
                self.update_output(f"❌ Error: {str(e)}\n", "error")
            self.update_status("❌ Error", "#f38ba8")

        finally:
            self.processing = False
            self.root.after(0, lambda: self.execute_btn.config(state="normal", text="▶ Execute"))

    def update_status(self, text, color):
        def _update():
            if hasattr(self, 'status_label'):
                self.status_label.config(text=text, fg=color)

        self.root.after(0, _update)

    def start_voice_listen(self):
        """Start push-to-talk voice command"""
        if not self.voice_commander:
            messagebox.showerror("Voice Error", "Voice commander not available")
            return

        if self.processing:
            messagebox.showwarning("Busy", "Please wait for the current command to finish.")
            return

        def voice_thread():
            self.update_output("\n🎤 Listening for voice command...\n", "info")
            self.update_status("🎤 Listening...", "#f9e2af")
            # self.root.after(0, lambda: self.voice_listen_btn.config(bg="#00d4aa"))

            result = self.voice_commander.listen_once(timeout=10)

            # self.root.after(0, lambda: self.voice_listen_btn.config(bg="#00ff88"))

            if result['success'] and result['command']:
                self.update_output(f"✅ Heard: {result['command']}\n\n", "success")

                # Execute the command
                self.command_input.delete(0, tk.END)
                self.command_input.insert(0, result['command'])
                self.execute_command()

            else:
                self.update_output(f"❌ {result['message']}\n", "error")
                self.update_status("✅ Ready", "#a6e3a1")

        thread = threading.Thread(target=voice_thread, daemon=True)
        thread.start()

    def toggle_continuous_listening(self):
        """Toggle continuous voice listening mode"""
        if not self.voice_commander:
            messagebox.showerror("Voice Error", "Voice commander not available")
            return

        if not self.voice_listening:
            # Start continuous listening (callback already set during init)
            result = self.voice_commander.start_continuous_listening()

            if result['success']:
                self.voice_listening = True
                # self.voice_continuous_btn.config(bg="#00ff88", text="🔇")

                # Show wake word status
                wake_words = ", ".join(self.voice_commander.get_wake_words()[:3])
                wake_status = ""
                if self.voice_commander.wake_word_enabled:
                    wake_status = f"\n💬 Wake words: {wake_words}\n"

                self.update_output("\n🔊 Continuous voice listening ENABLED\n", "success")
                self.update_output(wake_status, "info")
                self.update_output("Say 'stop listening' to disable\n\n", "info")
                self.update_status("🎤 Voice Active", "#a6e3a1")
            else:
                messagebox.showerror("Voice Error", result['message'])
        else:
            # Stop continuous listening
            result = self.voice_commander.stop_continuous_listening()

            if result['success']:
                self.voice_listening = False
                # self.voice_continuous_btn.config(bg="#3d4466", text="🔊")
                self.update_output("\n🔇 Continuous voice listening DISABLED\n", "warning")
                self.update_status("✅ Ready", "#a6e3a1")

    def toggle_wake_word(self):
        """Toggle wake word detection on/off"""
        if not self.voice_commander:
            messagebox.showerror("Voice Error", "Voice commander not available")
            return

        result = self.voice_commander.toggle_wake_word()

        if result['success']:
            if result['enabled']:
                self.wake_word_btn.config(bg="#00ff88")
                wake_words = ", ".join(self.voice_commander.get_wake_words()[:3])
                self.update_output(f"\n💬 Wake word ENABLED\n", "success")
                self.update_output(f"Say: {wake_words}\n", "info")
                self.update_output(f"Then your command (e.g., 'Hey Vatsal, what time is it')\n\n", "info")
            else:
                self.wake_word_btn.config(bg="#f9e2af")
                self.update_output(f"\n💬 Wake word DISABLED\n", "warning")
                self.update_output(f"Continuous listening will respond to all speech\n\n", "info")

    def handle_voice_command(self, command):
        """Handle voice command from continuous listening"""
        print(f"📞 Callback received command: '{command}'")
        # Execute on main thread for thread safety
        self.root.after(0, lambda: self._execute_voice_command(command))

    def _execute_voice_command(self, command):
        """Internal method to execute voice command on main thread"""
        print(f"🎯 Executing voice command on main thread: '{command}'")
        self.update_output(f"\n🎤 Voice Command: {command}\n", "info")

        # Insert command and execute
        self.command_input.delete(0, tk.END)
        self.command_input.insert(0, command)

        # Execute the command
        print(f"⚙️  Calling execute_command()...")
        self.execute_command()
        print(f"✅ execute_command() completed")

    def toggle_sound_effects(self):
        """Toggle voice sound effects on/off"""
        if not self.voice_commander:
            messagebox.showerror("Voice Error", "Voice commander not available")
            return

        result = self.voice_commander.toggle_sound_effects()

        if result['success']:
            if result['enabled']:
                # self.sound_fx_btn.config(bg="#00ff88", text="🔊")
                self.update_output(f"\n🔊 Voice sound effects ENABLED\n", "success")
                self.update_output(f"You'll hear beeps during voice interactions\n", "info")

                # Play success sound to demonstrate
                if self.voice_commander.sound_effects:
                    self.voice_commander.sound_effects.play_sound('success', async_play=True)
            else:
                # self.sound_fx_btn.config(bg="#3d4466", text="🔇")
                self.update_output(f"\n🔇 Voice sound effects DISABLED\n", "warning")
                self.update_output(f"Voice commands will work silently\n", "info")

    def toggle_gesture_voice(self):
        """Toggle gesture-activated voice listening (V sign → voice)"""
        if not self.gesture_voice_active:
            # Create fresh activator with callbacks
            try:
                self.gesture_voice_activator = create_gesture_voice_activator(
                    on_speech_callback=self.handle_gesture_speech
                )
                self.gesture_voice_activator.set_stop_callback(self._on_gesture_voice_stopped)
            except Exception as e:
                messagebox.showerror("Gesture Voice Error", f"Failed to initialize: {e}")
                return

            # Start gesture voice activator in background thread
            def run_gesture_voice():
                try:
                    self.gesture_voice_activator.run()
                except Exception as e:
                    print(f"❌ Gesture voice error: {e}")
                    self.root.after(0, self._on_gesture_voice_stopped)

            threading.Thread(target=run_gesture_voice, daemon=True).start()
            self.gesture_voice_active = True
            self.gesture_voice_btn.config(bg="#00ff88", text="✌️✌️")
            self.gesture_voice_btn.config(bg="#00ff88", text="✌️✌️")
            self.update_output("\n", "info")
            self.update_output("✌️  Gesture Voice & Hand Detection ENABLED\n", "success")

            self.update_output("📋 Available Gestures:\n", "info")
            self.update_output("  🖖 SPOCK - Activate listening mode\n", "info")
            self.update_output("  🤟 ROCK SIGN - Vatsal identified (ILoveYou)\n", "info")
            self.update_output("  ✋ OPEN PALM - Pause/Stop\n", "info")
            self.update_output("  👊 FIST - Wake/Resume\n", "info")
            self.update_output("  👆 ONE FINGER - Selection mode\n", "info")
            self.update_output("  ✌️ PEACE SIGN - Voice activation\n", "info")
            self.update_output("  👌 OK CIRCLE - Confirm/Execute\n", "info")
            self.update_output("  🫰 PINCH - Grab/Zoom\n", "info")
            self.update_output("  👍 THUMBS UP - Approval\n", "info")
            self.update_output("  👎 THUMBS DOWN - Rejection\n", "info")
            self.update_output("\n💡 Tips:\n", "info")
            self.update_output("  • Show TWO V SIGNS (both hands) for BOI greeting\n", "info")
            self.update_output("  • Camera window shows detected gestures\n", "info")
            self.update_output("  • Press 'q' in camera window to close\n\n", "info")
            self.update_status("✌️  Gesture Voice Active", "#00ff88")
        else:
            # Stop gesture voice activator
            if self.gesture_voice_activator:
                self.gesture_voice_activator.stop()
            self._on_gesture_voice_stopped()

    def _on_gesture_voice_stopped(self):
        """Callback when gesture voice activator stops (thread-safe)"""
        self.gesture_voice_active = False
        self.gesture_voice_btn.config(bg="#ffd700", text="✌️")
        self.update_output("\n✌️  Gesture Voice Activator DISABLED\n", "warning")
        self.update_status("✅ Ready", "#a6e3a1")

    def handle_gesture_speech(self, speech_text):
        """Handle speech recognized from gesture activation (thread-safe)"""
        print(f"✌️ Gesture speech received: '{speech_text}'")
        # Route to existing voice command handler on main thread
        self.root.after(0, lambda: self.handle_voice_command(speech_text))

    # REMOVED: Separate gesture button functionality merged into toggle_gesture_voice
    # def toggle_gesture(self):
    #     """Toggle gesture recognition on/off (Two V signs for BOI greeting)"""
    #     # This functionality is now part of the V sign gesture voice feature

    def _handle_gesture_command(self, command):
        """
        Handle voice command from gesture detection.

        THREAD SAFETY: This is called from the detection worker thread,
        so we use root.after(0, ...) to marshal execution to the main thread
        before touching any Tkinter widgets.
        """
        print(f"✋ Gesture command received: '{command}'")
        # Marshal to main thread for thread-safe widget manipulation
        self.root.after(0, lambda: self._execute_voice_command(command))

    def show_sound_settings(self):
        """Show sound effects settings dialog"""
        if not self.voice_commander or not self.voice_commander.sound_effects:
            messagebox.showerror("Sound Error", "Sound effects not available")
            return

        settings_window = tk.Toplevel(self.root)
        settings_window.title("🔊 Sound Effects Settings")
        settings_window.geometry("500x450")
        settings_window.configure(bg="#252941")

        header = tk.Label(settings_window,
                          text="🔊 Voice Sound Effects Settings",
                          bg="#252941",
                          fg="#e0e0e0",
                          font=("Segoe UI", 16, "bold"),
                          pady=20)
        header.pack()

        # Sound effects status
        status_frame = tk.Frame(settings_window, bg="#2a2a3e", relief="flat")
        status_frame.pack(fill="x", padx=20, pady=10)

        sounds_list = self.voice_commander.list_sound_effects()
        status_text = "🎵 Available Sound Effects:\n\n"

        if sounds_list['success']:
            for name, info in sounds_list['sounds'].items():
                status = "✅" if info['exists'] else "❌"
                status_text += f"{status} {name.replace('_', ' ').title()}\n"

        status_label = tk.Label(status_frame,
                                text=status_text,
                                bg="#2a2a3e",
                                fg="#e0e0e0",
                                font=("Segoe UI", 11),
                                justify="left",
                                pady=15,
                                padx=15)
        status_label.pack()

        # Volume control
        volume_frame = tk.Frame(settings_window, bg="#252941")
        volume_frame.pack(fill="x", padx=20, pady=15)

        volume_label = tk.Label(volume_frame,
                                text="🎚️ Volume:",
                                bg="#252941",
                                fg="#e0e0e0",
                                font=("Segoe UI", 12, "bold"))
        volume_label.pack(side="left", padx=10)

        current_volume = self.voice_commander.sound_effects.volume if self.voice_commander.sound_effects else 0.8

        def update_volume(val):
            volume = float(val)
            self.voice_commander.set_sound_volume(volume)
            volume_value.config(text=f"{int(volume * 100)}%")

        volume_slider = tk.Scale(volume_frame,
                                 from_=0.0,
                                 to=1.0,
                                 resolution=0.1,
                                 orient="horizontal",
                                 bg="#2e3350",
                                 fg="#e0e0e0",
                                 highlightthickness=0,
                                 command=update_volume,
                                 length=250)
        volume_slider.set(current_volume)
        volume_slider.pack(side="left", padx=10)

        volume_value = tk.Label(volume_frame,
                                text=f"{int(current_volume * 100)}%",
                                bg="#252941",
                                fg="#00ff88",
                                font=("Segoe UI", 11, "bold"))
        volume_value.pack(side="left", padx=10)

        # Test sounds section
        test_frame = tk.Frame(settings_window, bg="#2a2a3e", relief="flat")
        test_frame.pack(fill="x", padx=20, pady=15)

        test_header = tk.Label(test_frame,
                               text="🎵 Test Sounds:",
                               bg="#2a2a3e",
                               fg="#f9e2af",
                               font=("Segoe UI", 12, "bold"),
                               pady=10)
        test_header.pack()

        test_buttons_frame = tk.Frame(test_frame, bg="#2a2a3e")
        test_buttons_frame.pack(pady=10)

        sound_names = ['wake_word', 'listening', 'processing', 'success', 'error']

        def play_test_sound(sound_name):
            self.voice_commander.sound_effects.play_sound(sound_name, async_play=True)

        for sound_name in sound_names:
            btn_text = sound_name.replace('_', ' ').title()
            test_btn = tk.Button(test_buttons_frame,
                                 text=btn_text,
                                 bg="#2e3350",
                                 fg="#e0e0e0",
                                 font=("Segoe UI", 9),
                                 relief="flat",
                                 cursor="hand2",
                                 command=lambda s=sound_name: play_test_sound(s),
                                 padx=15,
                                 pady=8)
            test_btn.pack(side="left", padx=5)
            self.add_hover_effect(test_btn, "#313244", "#45475a")

        # Info section
        info_frame = tk.Frame(settings_window, bg="#252941")
        info_frame.pack(fill="x", padx=20, pady=15)

        info_text = """
💡 Tips:
• Click sound names above to test them
• Adjust volume slider to your preference
• Sound effects play during voice interactions
• Toggle 🔊 button to enable/disable sounds
        """

        info_label = tk.Label(info_frame,
                              text=info_text,
                              bg="#252941",
                              fg="#b0b0b0",
                              font=("Segoe UI", 10),
                              justify="left")
        info_label.pack()

        # Close button
        close_btn = tk.Button(settings_window,
                              text="✅ Done",
                              bg="#00d4aa",
                              fg="#0f0f1e",
                              font=("Segoe UI", 11, "bold"),
                              relief="flat",
                              cursor="hand2",
                              command=settings_window.destroy,
                              padx=30,
                              pady=10)
        close_btn.pack(pady=15)
        self.add_hover_effect(close_btn, "#89b4fa", "#74c7ec")

    def show_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("❓ Help Guide")
        help_window.geometry("900x700")
        help_window.configure(bg="#252941")

        header = tk.Label(help_window,
                          text="🤖 AI Desktop Automation Controller - Help Guide",
                          bg="#252941",
                          fg="#e0e0e0",
                          font=("Segoe UI", 16, "bold"),
                          pady=20)
        header.pack()

        text_area = scrolledtext.ScrolledText(help_window,
                                              bg="#2a2a3e",
                                              fg="#e0e0e0",
                                              font=("Segoe UI", 11),
                                              wrap="word",
                                              padx=20,
                                              pady=20)
        text_area.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        help_text = """
🎯 QUICK START GUIDE

The AI Desktop Automation Controller is your personal AI-powered assistant for automating tasks on your computer.

📋 HOW TO USE:

1. Click any button in the Quick Actions panel
2. Or type a natural language command in the input field
3. Press Enter or click the Execute button
4. View the results in the Output Console

💡 EXAMPLE COMMANDS:

Desktop Control:
• "Take a screenshot"
• "Open notepad"
• "Search Google for Python tutorials"

Code Generation:
• "Write Python code for bubble sort"
• "Generate a calculator in JavaScript"

Messaging:
• "Send email to example@email.com"
• "Add contact John with phone 555-1234"

System Management:
• "Show system information"
• "Check disk usage"
• "Organize downloads folder"

AI Features:
• "Write a story about robots"
• "Explain quantum physics"
• "Generate a professional email template"

And much more! Explore all tabs for 80+ features.

🔑 REQUIREMENTS:

• Gemini API key (set GEMINI_API_KEY environment variable)
• Various system permissions for automation features

⚡ TIPS:

• Use natural language - the AI understands context
• Check the Output Console for detailed results
• Use Quick Actions for common tasks
• Explore all tabs to discover features

For more information, visit the documentation or contact support.
        """

        text_area.insert(1.0, help_text.strip())
        text_area.config(state="disabled")

        close_btn = tk.Button(help_window,
                              text="Close",
                              bg="#00d4aa",
                              fg="#0f0f1e",
                              font=("Segoe UI", 11, "bold"),
                              relief="flat",
                              cursor="hand2",
                              command=help_window.destroy,
                              padx=30,
                              pady=10)
        close_btn.pack(pady=(0, 20))

    def show_contacts(self):
        contacts_window = tk.Toplevel(self.root)
        contacts_window.title("👥 Contacts Manager")
        contacts_window.geometry("700x600")
        contacts_window.configure(bg="#252941")

        header = tk.Label(contacts_window,
                          text="👥 Contact Manager",
                          bg="#252941",
                          fg="#e0e0e0",
                          font=("Segoe UI", 16, "bold"),
                          pady=20)
        header.pack()

        info = tk.Label(contacts_window,
                        text="Manage your contacts for email and messaging automation",
                        bg="#252941",
                        fg="#b0b0b0",
                        font=("Segoe UI", 10))
        info.pack()

        text_area = scrolledtext.ScrolledText(contacts_window,
                                              bg="#2a2a3e",
                                              fg="#e0e0e0",
                                              font=("Segoe UI", 11),
                                              wrap="word",
                                              padx=20,
                                              pady=20)
        text_area.pack(fill="both", expand=True, padx=20, pady=20)

        try:
            command_dict = parse_command("List all contacts")
            result = self.executor.execute(command_dict)
            if result["success"]:
                text_area.insert(1.0, result["message"])
            else:
                text_area.insert(1.0, f"Error: {result['message']}")
        except Exception as e:
            text_area.insert(1.0,
                             f"No contacts found or error loading contacts.\n\nUse the command:\n'Add contact NAME with phone NUMBER and email EMAIL'\n\nError details: {str(e)}")

        text_area.config(state="disabled")

        close_btn = tk.Button(contacts_window,
                              text="Close",
                              bg="#00d4aa",
                              fg="#0f0f1e",
                              font=("Segoe UI", 11, "bold"),
                              relief="flat",
                              cursor="hand2",
                              command=contacts_window.destroy,
                              padx=30,
                              pady=10)
        close_btn.pack(pady=(0, 20))

    def show_suggestion(self):
        """Show BOI proactive suggestion"""
        suggestion = self.boi.get_proactive_suggestion()
        self.update_output(f"{suggestion}", "command")

    def show_about(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("ℹ️ About Vatsal")
        about_window.geometry("700x600")
        about_window.configure(bg="#252941")

        header = tk.Label(about_window,
                          text="🤖 Vatsal - AI Desktop Assistant",
                          bg="#252941",
                          fg="#e0e0e0",
                          font=("Segoe UI", 18, "bold"),
                          pady=20)
        header.pack()

        version = tk.Label(about_window,
                           text="Version 2.1.0 - Vatsal Edition (Powered by BOI)",
                           bg="#252941",
                           fg="#00d4aa",
                           font=("Segoe UI", 11))
        version.pack()

        description_frame = tk.Frame(about_window, bg="#2a2a3e")
        description_frame.pack(fill="both", expand=True, padx=30, pady=30)

        description = tk.Label(description_frame,
                               text="""
⚡ Vatsal - Your Intelligent Desktop AI Assistant

Powered by Google Gemini AI & BOI Framework

Vatsal is your intelligent AI assistant with sophisticated 
personality and advanced voice control capabilities.

✓ 80+ AI-powered features
✓ Advanced wake word detection ("Vatsal", "Hey Vatsal", etc.)
✓ Context-aware responses with memory
✓ Proactive suggestions & assistance
✓ Natural language command processing
✓ Desktop automation & control
✓ Code generation assistance
✓ Email & messaging automation
✓ System management tools
✓ Productivity tracking
✓ Smart scheduling & workflows

BOI Mode Features:
• Personalized responses with wit and charm
• Contextual understanding of your commands
• Proactive suggestions based on time and usage
• Conversational memory across sessions
• Professional yet friendly communication

Toggle BOI Mode ON/OFF anytime from the header.

© 2025 AI Automation Suite
                              """,
                               bg="#2a2a3e",
                               fg="#e0e0e0",
                               font=("Segoe UI", 10),
                               justify="center")
        description.pack(expand=True)

        close_btn = tk.Button(about_window,
                              text="Close",
                              bg="#00d4aa",
                              fg="#0f0f1e",
                              font=("Segoe UI", 11, "bold"),
                              relief="flat",
                              cursor="hand2",
                              command=about_window.destroy,
                              padx=30,
                              pady=10)
        close_btn.pack(pady=(0, 20))

    def show_security_dashboard(self):
        """Display AI-Powered Security Dashboard"""
        if not self.security_dashboard:
            messagebox.showerror("Error", "Security Dashboard not initialized")
            return

        sec_window = tk.Toplevel(self.root)
        sec_window.title("🛡️ AI-Powered Security Dashboard")
        sec_window.geometry("1000x700")
        sec_window.configure(bg="#252941")

        header_frame = tk.Frame(sec_window, bg="#16182a")
        header_frame.pack(fill="x", pady=(0, 10))

        header = tk.Label(header_frame,
                          text="🛡️ Security Dashboard with Gemini AI",
                          bg="#16182a",
                          fg="#00d4aa",
                          font=("Segoe UI", 18, "bold"),
                          pady=15)
        header.pack()

        subtitle = tk.Label(header_frame,
                            text="🤖 AI-Powered Threat Analysis • 🔐 Enhanced Security Features",
                            bg="#16182a",
                            fg="#b0b0b0",
                            font=("Segoe UI", 10, "italic"))
        subtitle.pack()

        # Main content area
        main_frame = tk.Frame(sec_window, bg="#252941")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Left panel - Actions
        left_panel = tk.Frame(main_frame, bg="#1a1d2e", width=300)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)

        actions_label = tk.Label(left_panel,
                                 text="🎯 Security Actions",
                                 bg="#1a1d2e",
                                 fg="#f9e2af",
                                 font=("Segoe UI", 12, "bold"),
                                 pady=10)
        actions_label.pack()

        # Security action buttons
        security_actions = [
            ("📊 Security Status", self.show_security_status),
            ("🤖 AI Threat Analysis", self.show_ai_threat_analysis),
            ("💡 AI Recommendations", self.show_ai_security_recommendations),
            ("🔍 Anomaly Detection", self.show_ai_anomaly_detection),
            ("📄 Full AI Report", self.show_ai_security_report),
            ("❓ Ask Security Question", self.ask_security_question)
        ]

        for text, command in security_actions:
            btn = tk.Button(left_panel,
                            text=text,
                            bg="#2e3350",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=12)
            btn.pack(fill="x", padx=10, pady=5)

        # Right panel - Display area
        right_panel = tk.Frame(main_frame, bg="#1a1d2e")
        right_panel.pack(side="right", fill="both", expand=True)

        display_label = tk.Label(right_panel,
                                 text="📋 Security Information",
                                 bg="#1a1d2e",
                                 fg="#f9e2af",
                                 font=("Segoe UI", 12, "bold"),
                                 pady=10)
        display_label.pack()

        # Display area
        self.security_display = scrolledtext.ScrolledText(
            right_panel,
            bg="#16182a",
            fg="#e0e0e0",
            font=("Consolas", 10),
            wrap=tk.WORD,
            relief="flat",
            padx=15,
            pady=15
        )
        self.security_display.pack(fill="both", expand=True, padx=10, pady=10)

        # Show initial status
        status = self.security_dashboard.get_comprehensive_security_status()
        status_text = f"""
🛡️ SECURITY DASHBOARD STATUS

Security Level: {status['dashboard_info']['security_level'].upper()}
Current User: {status['dashboard_info']['current_user'] or 'Not Authenticated'}
Authenticated: {status['dashboard_info']['authenticated']}

🔐 BIOMETRIC AUTHENTICATION
  • Enrolled Users: {status['biometric_authentication']['enrolled_users']}
  • Success Rate: {status['biometric_authentication']['success_rate']:.1f}%

🔑 TWO-FACTOR AUTHENTICATION
  • Enabled Users: {status['two_factor_authentication']['enabled_users']}
  • Success Rate: {status['two_factor_authentication']['success_rate']:.1f}%

🔒 ENCRYPTED STORAGE
  • Status: {'ENABLED' if status['encrypted_storage']['enabled'] else 'DISABLED'}
  • Encrypted Files: {status['encrypted_storage']['encrypted_files']}

🛡️ ACTIVITY MONITORING
  • Status: {'ACTIVE' if status['activity_monitoring']['active'] else 'INACTIVE'}
  • Total Activities: {status['activity_monitoring']['total_activities']}
  • Threats Detected: {status['activity_monitoring']['threats_detected']}

⚠️ THREATS (24H)
  • Total: {status['threat_summary_24h']['total_threats']}
  • Critical: {status['threat_summary_24h']['critical']}
  • High: {status['threat_summary_24h']['high']}

Click the buttons on the left to access AI-powered security features.
        """
        self.security_display.insert("1.0", status_text)

        close_btn = tk.Button(sec_window,
                              text="Close",
                              bg="#00d4aa",
                              fg="#0f0f1e",
                              font=("Segoe UI", 11, "bold"),
                              relief="flat",
                              cursor="hand2",
                              command=sec_window.destroy,
                              padx=30,
                              pady=10)
        close_btn.pack(pady=20)

    def show_security_status(self):
        """Show current security status"""
        if not hasattr(self, 'security_display'):
            messagebox.showinfo("Info", "Please open Security Dashboard first")
            return

        self.security_display.delete("1.0", "end")
        self.security_display.insert("1.0", "Loading security status...\n")
        self.security_display.update()

        status = self.security_dashboard.get_comprehensive_security_status()
        report = self.security_dashboard.generate_security_report()

        self.security_display.delete("1.0", "end")
        self.security_display.insert("1.0", report)

    def show_ai_threat_analysis(self):
        """Show AI-powered threat analysis"""
        if not hasattr(self, 'security_display'):
            messagebox.showinfo("Info", "Please open Security Dashboard first")
            return

        self.security_display.delete("1.0", "end")
        self.security_display.insert("1.0", "🤖 Analyzing threats with Gemini AI...\nThis may take a moment...\n")
        self.security_display.update()

        result = self.security_dashboard.ai_analyze_threats()

        self.security_display.delete("1.0", "end")
        if result.get("success"):
            self.security_display.insert("1.0", f"""
🤖 AI-POWERED THREAT ANALYSIS

Threat Count: {result.get('threat_count', 0)}
Analysis Time: {result.get('timestamp', 'N/A')}

{result['analysis']}
            """)
        else:
            self.security_display.insert("1.0", f"⚠️ Error: {result.get('message', 'Unknown error')}")

    def show_ai_security_recommendations(self):
        """Show AI-powered security recommendations"""
        if not hasattr(self, 'security_display'):
            messagebox.showinfo("Info", "Please open Security Dashboard first")
            return

        self.security_display.delete("1.0", "end")
        self.security_display.insert("1.0", "🤖 Generating security recommendations with Gemini AI...\n")
        self.security_display.update()

        result = self.security_dashboard.ai_security_recommendations()

        self.security_display.delete("1.0", "end")
        if result.get("success"):
            self.security_display.insert("1.0", f"""
💡 AI-POWERED SECURITY RECOMMENDATIONS

Current Security Level: {result.get('security_level', 'N/A').upper()}
Analysis Time: {result.get('timestamp', 'N/A')}

{result['recommendations']}
            """)
        else:
            self.security_display.insert("1.0", f"⚠️ Error: {result.get('message', 'Unknown error')}")

    def show_ai_anomaly_detection(self):
        """Show AI-powered anomaly detection"""
        if not hasattr(self, 'security_display'):
            messagebox.showinfo("Info", "Please open Security Dashboard first")
            return

        self.security_display.delete("1.0", "end")
        self.security_display.insert("1.0", "🤖 Detecting anomalies with Gemini AI...\n")
        self.security_display.update()

        result = self.security_dashboard.ai_detect_anomalies()

        self.security_display.delete("1.0", "end")
        if result.get("success"):
            self.security_display.insert("1.0", f"""
🔍 AI-POWERED ANOMALY DETECTION

Activities Analyzed: {result.get('activities_analyzed', 0)}
Analysis Time: {result.get('timestamp', 'N/A')}

{result['anomalies']}
            """)
        else:
            self.security_display.insert("1.0", f"⚠️ Error: {result.get('message', 'Unknown error')}")

    def show_ai_security_report(self):
        """Show comprehensive AI-enhanced security report"""
        if not hasattr(self, 'security_display'):
            messagebox.showinfo("Info", "Please open Security Dashboard first")
            return

        self.security_display.delete("1.0", "end")
        self.security_display.insert("1.0",
                                     "🤖 Generating comprehensive AI security report...\nThis may take a moment...\n")
        self.security_display.update()

        report = self.security_dashboard.ai_generate_security_report()

        self.security_display.delete("1.0", "end")
        self.security_display.insert("1.0", report)

    def ask_security_question(self):
        """Ask a natural language security question"""
        if not hasattr(self, 'security_display'):
            messagebox.showinfo("Info", "Please open Security Dashboard first")
            return

        question = simpledialog.askstring(
            "Security Question",
            "Ask me anything about your security status:",
            parent=self.root
        )

        if not question:
            return

        self.security_display.delete("1.0", "end")
        self.security_display.insert("1.0", f"❓ Question: {question}\n\n🤖 Thinking...\n")
        self.security_display.update()

        result = self.security_dashboard.ai_natural_language_query(question)

        self.security_display.delete("1.0", "end")
        if result.get("success"):
            self.security_display.insert("1.0", f"""
❓ SECURITY QUESTION & ANSWER

Question: {result.get('question', question)}
Answered: {result.get('timestamp', 'N/A')}

{result['answer']}
            """)
        else:
            self.security_display.insert("1.0", f"⚠️ Error: {result.get('message', 'Unknown error')}")

    def run_comprehensive_analysis(self):
        """Run comprehensive AI screen analysis"""

        def execute():
            self.update_output("\n🧠 Running Comprehensive AI Analysis...\n", "command")
            result = self.advanced_monitor.advanced_screen_analysis("comprehensive")
            if result["success"]:
                self.update_output(result["analysis"], "success")
                if result.get("structured_data"):
                    scores = result["structured_data"].get("scores", {})
                    if scores:
                        self.update_output(f"\n📊 Scores: {scores}", "info")
            else:
                self.update_output(f"Error: {result.get('error', 'Unknown error')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def run_security_scan(self):
        """Run security scan"""

        def execute():
            self.update_output("\n🛡️ Running Security Scan...\n", "command")
            result = self.advanced_monitor.security_scan()
            if result["success"]:
                self.update_output(result["analysis"], "success")
            else:
                self.update_output(f"Error: {result.get('error', 'Unknown error')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def run_performance_audit(self):
        """Run performance audit"""

        def execute():
            self.update_output("\n⚡ Running Performance Audit...\n", "command")
            result = self.advanced_monitor.performance_audit()
            if result["success"]:
                self.update_output(result["analysis"], "success")
            else:
                self.update_output(f"Error: {result.get('error', 'Unknown error')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def run_ux_review(self):
        """Run UX expert review"""

        def execute():
            self.update_output("\n🎨 Running UX Expert Review...\n", "command")
            result = self.advanced_monitor.ux_expert_review()
            if result["success"]:
                self.update_output(result["analysis"], "success")
            else:
                self.update_output(f"Error: {result.get('error', 'Unknown error')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def run_accessibility_audit(self):
        """Run accessibility audit"""

        def execute():
            self.update_output("\n♿ Running Accessibility Audit...\n", "command")
            result = self.advanced_monitor.accessibility_audit()
            if result["success"]:
                self.update_output(result["analysis"], "success")
            else:
                self.update_output(f"Error: {result.get('error', 'Unknown error')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def run_code_review(self):
        """Run code review"""

        def execute():
            self.update_output("\n💻 Running Code Review...\n", "command")
            result = self.advanced_monitor.code_review()
            if result["success"]:
                self.update_output(result["analysis"], "success")
            else:
                self.update_output(f"Error: {result.get('error', 'Unknown error')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def run_design_critique(self):
        """Run design critique"""

        def execute():
            self.update_output("\n🎭 Running Design Critique...\n", "command")
            result = self.advanced_monitor.design_critique()
            if result["success"]:
                self.update_output(result["analysis"], "success")
            else:
                self.update_output(f"Error: {result.get('error', 'Unknown error')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def run_automation_discovery(self):
        """Find automation opportunities"""

        def execute():
            self.update_output("\n🤖 Finding Automation Opportunities...\n", "command")
            result = self.advanced_monitor.find_automation_opportunities()
            if result["success"]:
                self.update_output(result["analysis"], "success")
            else:
                self.update_output(f"Error: {result.get('error', 'Unknown error')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def view_analytics_report(self):
        """View analytics report"""

        def execute():
            self.update_output("\n📊 Generating Analytics Report...\n", "command")
            result = self.advanced_monitor.get_analytics_report()
            if result["success"]:
                self.update_output(result["report"], "success")
            else:
                self.update_output(f"Error: {result.get('error', 'Unknown error')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def start_continuous_monitoring(self):
        """Start continuous monitoring with dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("🔄 Continuous Monitoring Setup")
        dialog.geometry("500x400")
        dialog.configure(bg="#252941")

        tk.Label(dialog, text="⚙️ Configure Continuous Monitoring",
                 bg="#252941", fg="#e0e0e0",
                 font=("Segoe UI", 14, "bold")).pack(pady=15)

        tk.Label(dialog, text="Duration (minutes):",
                 bg="#252941", fg="#b0b0b0",
                 font=("Segoe UI", 10)).pack(pady=(10, 5))
        duration_entry = tk.Entry(dialog, font=("Segoe UI", 11), width=20)
        duration_entry.insert(0, "60")
        duration_entry.pack()

        tk.Label(dialog, text="Check Interval (seconds):",
                 bg="#252941", fg="#b0b0b0",
                 font=("Segoe UI", 10)).pack(pady=(10, 5))
        interval_entry = tk.Entry(dialog, font=("Segoe UI", 11), width=20)
        interval_entry.insert(0, "30")
        interval_entry.pack()

        triggers_frame = tk.Frame(dialog, bg="#252941")
        triggers_frame.pack(pady=15)

        tk.Label(triggers_frame, text="Triggers:",
                 bg="#252941", fg="#b0b0b0",
                 font=("Segoe UI", 10, "bold")).pack()

        error_var = tk.BooleanVar(value=True)
        security_var = tk.BooleanVar(value=True)
        perf_var = tk.BooleanVar(value=True)

        tk.Checkbutton(triggers_frame, text="Error Detection",
                       variable=error_var, bg="#252941", fg="#e0e0e0",
                       selectcolor="#313244", font=("Segoe UI", 9)).pack(anchor="w")
        tk.Checkbutton(triggers_frame, text="Security Monitoring",
                       variable=security_var, bg="#252941", fg="#e0e0e0",
                       selectcolor="#313244", font=("Segoe UI", 9)).pack(anchor="w")
        tk.Checkbutton(triggers_frame, text="Performance Issues",
                       variable=perf_var, bg="#252941", fg="#e0e0e0",
                       selectcolor="#313244", font=("Segoe UI", 9)).pack(anchor="w")

        def start_monitoring():
            duration = int(duration_entry.get())
            interval = int(interval_entry.get())
            triggers = {
                "errors": error_var.get(),
                "security": security_var.get(),
                "performance_issues": perf_var.get()
            }
            dialog.destroy()

            def execute():
                self.update_output(f"\n🔄 Starting Continuous Monitoring for {duration} minutes...\n", "command")
                result = self.advanced_monitor.continuous_monitoring(
                    duration_minutes=duration,
                    check_interval=interval,
                    triggers=triggers
                )
                if result["success"]:
                    self.update_output(
                        f"✅ Monitoring completed! {result['total_checks']} checks performed, {result['alerts_triggered']} alerts triggered.",
                        "success")
                else:
                    self.update_output(f"Error: {result.get('error', 'Unknown error')}", "error")

            threading.Thread(target=execute, daemon=True).start()

        tk.Button(dialog, text="▶️ Start Monitoring",
                  bg="#00d4aa", fg="#0f0f1e",
                  font=("Segoe UI", 11, "bold"),
                  command=start_monitoring, padx=20, pady=8).pack(pady=15)

    def ai_monitor_productivity(self):
        """Run instant productivity analysis with new AI monitor"""

        def execute():
            self.update_output("\n📊 Analyzing Productivity...\n", "command")
            result = self.ai_monitor.analyze_now("productivity")
            if result.get("success"):
                data = result.get("data", {})
                analysis = result.get("analysis", "")
                score = data.get("productivity_score", 0)

                self.update_output(f"⭐ Productivity Score: {score}/10\n", "info")
                self.update_output(f"{analysis}\n", "success")
            else:
                self.update_output(f"❌ {result.get('message', 'Analysis failed')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def ai_monitor_security(self):
        """Run instant security scan"""

        def execute():
            self.update_output("\n🔒 Running Security Scan...\n", "command")
            result = self.ai_monitor.analyze_now("security")
            if result.get("success"):
                data = result.get("data", {})
                analysis = result.get("analysis", "")
                risk_level = data.get("risk_level", "UNKNOWN")

                self.update_output(f"🛡️ Risk Level: {risk_level}\n", "info")
                self.update_output(f"{analysis}\n", "success")
            else:
                self.update_output(f"❌ {result.get('message', 'Scan failed')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def ai_monitor_performance(self):
        """Run instant performance analysis"""

        def execute():
            self.update_output("\n⚡ Analyzing Performance...\n", "command")
            result = self.ai_monitor.analyze_now("performance")
            if result.get("success"):
                data = result.get("data", {})
                analysis = result.get("analysis", "")
                score = data.get("performance_score", 0)

                self.update_output(f"⚡ Performance Score: {score}/10\n", "info")
                self.update_output(f"{analysis}\n", "success")
            else:
                self.update_output(f"❌ {result.get('message', 'Analysis failed')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def ai_monitor_errors(self):
        """Run instant error detection"""

        def execute():
            self.update_output("\n🐛 Detecting Errors...\n", "command")
            result = self.ai_monitor.analyze_now("errors")
            if result.get("success"):
                data = result.get("data", {})
                analysis = result.get("analysis", "")
                errors_found = data.get("errors_found", False)
                error_count = data.get("error_count", 0)

                if errors_found:
                    self.update_output(f"⚠️ {error_count} Error(s) Detected!\n", "info")
                else:
                    self.update_output(f"✅ No Errors Detected\n", "info")

                self.update_output(f"{analysis}\n", "success")
            else:
                self.update_output(f"❌ {result.get('message', 'Detection failed')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def ai_monitor_ux(self):
        """Run instant UX/Design review"""

        def execute():
            self.update_output("\n🎨 Reviewing UX/Design...\n", "command")
            result = self.ai_monitor.analyze_now("ux")
            if result.get("success"):
                data = result.get("data", {})
                analysis = result.get("analysis", "")
                ux_score = data.get("ux_score", 0)

                self.update_output(f"🎨 UX Score: {ux_score}/10\n", "info")
                self.update_output(f"{analysis}\n", "success")
            else:
                self.update_output(f"❌ {result.get('message', 'Review failed')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def ai_monitor_accessibility(self):
        """Run instant accessibility audit"""

        def execute():
            self.update_output("\n♿ Running Accessibility Audit...\n", "command")
            result = self.ai_monitor.analyze_now("accessibility")
            if result.get("success"):
                data = result.get("data", {})
                analysis = result.get("analysis", "")
                acc_score = data.get("accessibility_score", 0)

                self.update_output(f"♿ Accessibility Score: {acc_score}/10\n", "info")
                self.update_output(f"{analysis}\n", "success")
            else:
                self.update_output(f"❌ {result.get('message', 'Audit failed')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def ai_monitor_code(self):
        """Run instant code review"""

        def execute():
            self.update_output("\n💻 Reviewing Code...\n", "command")
            result = self.ai_monitor.analyze_now("code")
            if result.get("success"):
                data = result.get("data", {})
                analysis = result.get("analysis", "")
                code_detected = data.get("code_detected", False)

                if code_detected:
                    quality_score = data.get("code_quality_score", 0)
                    self.update_output(f"💻 Code Quality Score: {quality_score}/10\n", "info")
                else:
                    self.update_output(f"ℹ️ No Code Detected\n", "info")

                self.update_output(f"{analysis}\n", "success")
            else:
                self.update_output(f"❌ {result.get('message', 'Review failed')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def ai_monitor_automation(self):
        """Run instant automation discovery"""

        def execute():
            self.update_output("\n🤖 Finding Automation Opportunities...\n", "command")
            result = self.ai_monitor.analyze_now("automation")
            if result.get("success"):
                data = result.get("data", {})
                analysis = result.get("analysis", "")
                opportunities = data.get("automation_opportunities", [])

                self.update_output(f"🤖 {len(opportunities)} Automation Opportunity(ies) Found\n", "info")
                self.update_output(f"{analysis}\n", "success")
            else:
                self.update_output(f"❌ {result.get('message', 'Discovery failed')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def ai_monitor_start_continuous(self):
        """Start continuous AI monitoring"""
        dialog = tk.Toplevel(self.root)
        dialog.title("🔄 Start Continuous Monitoring")
        dialog.geometry("550x500")
        dialog.configure(bg="#252941")

        tk.Label(dialog, text="🔄 Continuous AI Monitoring",
                 bg="#252941", fg="#e0e0e0",
                 font=("Segoe UI", 14, "bold")).pack(pady=15)

        tk.Label(dialog, text="Select monitoring modes:",
                 bg="#252941", fg="#b0b0b0",
                 font=("Segoe UI", 10, "bold")).pack(pady=(10, 5))

        modes_frame = tk.Frame(dialog, bg="#252941")
        modes_frame.pack(pady=10)

        mode_vars = {}
        for mode_id, mode_info in self.ai_monitor.ANALYSIS_MODES.items():
            var = tk.BooleanVar(value=mode_id in ["productivity", "errors", "security"])
            tk.Checkbutton(modes_frame, text=f"{mode_info['icon']} {mode_info['name']}",
                           variable=var, bg="#252941", fg="#e0e0e0",
                           selectcolor="#313244", font=("Segoe UI", 9)).pack(anchor="w")
            mode_vars[mode_id] = var

        tk.Label(dialog, text="Check interval (seconds):",
                 bg="#252941", fg="#b0b0b0",
                 font=("Segoe UI", 10)).pack(pady=(15, 5))
        interval_entry = tk.Entry(dialog, font=("Segoe UI", 11), width=20)
        interval_entry.insert(0, "30")
        interval_entry.pack()

        def start():
            selected_modes = [mode for mode, var in mode_vars.items() if var.get()]
            interval = int(interval_entry.get())
            dialog.destroy()

            def execute():
                self.update_output(f"\n🔄 Starting Continuous Monitoring...\n", "command")
                self.update_output(f"   📊 Modes: {', '.join(selected_modes)}\n", "info")
                self.update_output(f"   ⏱️  Interval: {interval}s\n", "info")

                result = self.ai_monitor.start_monitoring(modes=selected_modes, interval=interval)
                if result.get("success"):
                    self.update_output(f"✅ {result['message']}\n", "success")
                    self.update_output(f"   ℹ️ Monitoring is running in background. Use 'Stop Monitoring' to end.\n",
                                       "info")
                else:
                    self.update_output(f"❌ {result.get('message')}", "error")

            threading.Thread(target=execute, daemon=True).start()

        tk.Button(dialog, text="▶️ Start Monitoring",
                  bg="#00d4aa", fg="#0f0f1e",
                  font=("Segoe UI", 11, "bold"),
                  command=start, padx=20, pady=8).pack(pady=15)

    def ai_monitor_pause_resume(self):
        """Pause or resume monitoring"""
        if self.ai_monitor.paused:
            result = self.ai_monitor.resume_monitoring()
            self.update_output(f"▶️ {result['message']}\n", "success")
        else:
            result = self.ai_monitor.pause_monitoring()
            self.update_output(f"⏸️ {result['message']}\n", "success")

    def ai_monitor_stop(self):
        """Stop continuous monitoring"""
        result = self.ai_monitor.stop_monitoring()
        if result.get("success"):
            stats = result.get("stats", {})
            self.update_output(f"\n✅ {result['message']}\n", "success")
            self.update_output(f"   📊 Session Statistics:\n", "info")
            self.update_output(f"      • Screenshots: {stats.get('total_screenshots', 0)}\n", "info")
            self.update_output(f"      • AI Analyses: {stats.get('ai_analyses', 0)}\n", "info")
            self.update_output(f"      • Changes Detected: {stats.get('changes_detected', 0)}\n", "info")
            self.update_output(f"      • Alerts Triggered: {stats.get('alerts_triggered', 0)}\n", "info")
        else:
            self.update_output(f"❌ {result.get('message')}", "error")

    def ai_monitor_view_analytics(self):
        """View analytics dashboard"""

        def execute():
            self.update_output("\n📈 Analytics Dashboard\n", "command")

            summary = self.ai_monitor.get_analytics_summary()

            prod = summary.get("productivity", {})
            sec = summary.get("security", {})
            err = summary.get("errors", {})
            perf = summary.get("performance", {})
            patterns = summary.get("patterns", {})
            session = summary.get("session", {})

            self.update_output(f"\n📊 Productivity Analytics:\n", "info")
            self.update_output(f"   • Average Score: {prod.get('average_score', 0)}/10\n", "success")
            self.update_output(f"   • Total Measurements: {prod.get('total_measurements', 0)}\n", "success")

            self.update_output(f"\n🔒 Security Analytics:\n", "info")
            self.update_output(f"   • Total Issues: {sec.get('total_issues', 0)}\n", "success")
            self.update_output(f"   • Critical Issues: {sec.get('critical_issues', 0)}\n", "success")

            self.update_output(f"\n🐛 Error Analytics:\n", "info")
            self.update_output(f"   • Total Errors: {err.get('total_errors', 0)}\n", "success")

            self.update_output(f"\n⚡ Performance Analytics:\n", "info")
            self.update_output(f"   • Measurements: {perf.get('measurements', 0)}\n", "success")

            self.update_output(f"\n🧠 Pattern Learning:\n", "info")
            self.update_output(f"   • Patterns Learned: {patterns.get('patterns_learned', 0)}\n", "success")

            self.update_output(f"\n📊 Current Session:\n", "info")
            self.update_output(f"   • Screenshots: {session.get('total_screenshots', 0)}\n", "success")
            self.update_output(f"   • AI Analyses: {session.get('ai_analyses', 0)}\n", "success")
            self.update_output(f"   • Changes Detected: {session.get('changes_detected', 0)}\n", "success")
            self.update_output(f"   • Alerts: {session.get('alerts_triggered', 0)}\n", "success")

            self.update_output("\n", "info")

        threading.Thread(target=execute, daemon=True).start()

    def ai_monitor_productivity_trends(self):
        """View productivity trends"""

        def execute():
            self.update_output("\n📊 Productivity Trends Analysis\n", "command")

            trends = self.ai_monitor.get_productivity_trends()

            if "message" in trends:
                self.update_output(f"{trends['message']}\n", "info")
            else:
                hourly = trends.get("hourly_averages", {})
                peak_hour = trends.get("peak_productivity_hour", 0)
                peak_score = trends.get("peak_productivity_score", 0)
                low_hour = trends.get("lowest_productivity_hour", 0)
                low_score = trends.get("lowest_productivity_score", 0)

                self.update_output(f"📈 Hourly Productivity Averages:\n", "info")
                for hour in sorted(hourly.keys()):
                    score = hourly[hour]
                    bar = "█" * int(score)
                    self.update_output(f"   {hour:02d}:00 | {bar} {score:.1f}/10\n", "success")

                self.update_output(f"\n🌟 Peak Productivity:\n", "info")
                self.update_output(f"   • Hour: {peak_hour:02d}:00\n", "success")
                self.update_output(f"   • Score: {peak_score:.1f}/10\n", "success")

                self.update_output(f"\n📉 Lowest Productivity:\n", "info")
                self.update_output(f"   • Hour: {low_hour:02d}:00\n", "success")
                self.update_output(f"   • Score: {low_score:.1f}/10\n", "success")

            self.update_output("\n", "info")

        threading.Thread(target=execute, daemon=True).start()

    def ai_monitor_view_alerts(self):
        """View recent alerts"""

        def execute():
            self.update_output("\n🚨 Recent Alerts\n", "command")

            alerts = self.ai_monitor.get_recent_alerts(limit=10)

            if not alerts:
                self.update_output("ℹ️ No alerts yet\n", "info")
            else:
                for i, alert in enumerate(alerts, 1):
                    severity = alert.get("severity", "UNKNOWN")
                    alert_type = alert.get("type", "UNKNOWN")
                    message = alert.get("message", "")
                    timestamp = alert.get("timestamp", "")

                    icon = "🔴" if severity == "CRITICAL" else "🟡" if severity == "HIGH" else "🟢"

                    self.update_output(f"\n{i}. {icon} [{severity}] {alert_type}\n", "info")
                    self.update_output(f"   {message}\n", "success")
                    self.update_output(f"   ⏰ {timestamp}\n", "success")

            self.update_output("\n", "info")

        threading.Thread(target=execute, daemon=True).start()

    def ai_monitor_configure(self):
        """Configure monitoring settings"""
        dialog = tk.Toplevel(self.root)
        dialog.title("⚙️ Monitoring Configuration")
        dialog.geometry("500x550")
        dialog.configure(bg="#252941")

        tk.Label(dialog, text="⚙️ Monitoring Settings",
                 bg="#252941", fg="#e0e0e0",
                 font=("Segoe UI", 14, "bold")).pack(pady=15)

        config = self.ai_monitor.get_config()

        tk.Label(dialog, text="Default check interval (seconds):",
                 bg="#252941", fg="#b0b0b0",
                 font=("Segoe UI", 10)).pack(pady=(10, 5))
        interval_entry = tk.Entry(dialog, font=("Segoe UI", 11), width=20)
        interval_entry.insert(0, str(config.get("default_interval", 30)))
        interval_entry.pack()

        change_detection_var = tk.BooleanVar(value=config.get("change_detection", True))
        tk.Checkbutton(dialog, text="Enable change detection (skip identical screens)",
                       variable=change_detection_var, bg="#252941", fg="#e0e0e0",
                       selectcolor="#313244", font=("Segoe UI", 9)).pack(pady=5)

        smart_scheduling_var = tk.BooleanVar(value=config.get("smart_scheduling", True))
        tk.Checkbutton(dialog, text="Enable smart scheduling",
                       variable=smart_scheduling_var, bg="#252941", fg="#e0e0e0",
                       selectcolor="#313244", font=("Segoe UI", 9)).pack(pady=5)

        privacy_mode_var = tk.BooleanVar(value=config.get("privacy_mode", False))
        tk.Checkbutton(dialog, text="Privacy mode (no screenshots saved)",
                       variable=privacy_mode_var, bg="#252941", fg="#e0e0e0",
                       selectcolor="#313244", font=("Segoe UI", 9)).pack(pady=5)

        tk.Label(dialog, text="Auto Actions:",
                 bg="#252941", fg="#b0b0b0",
                 font=("Segoe UI", 10, "bold")).pack(pady=(15, 5))

        auto_actions = config.get("auto_actions", {})

        screenshot_on_error_var = tk.BooleanVar(value=auto_actions.get("screenshot_on_error", True))
        tk.Checkbutton(dialog, text="Auto-screenshot on errors",
                       variable=screenshot_on_error_var, bg="#252941", fg="#e0e0e0",
                       selectcolor="#313244", font=("Segoe UI", 9)).pack(pady=2)

        alert_on_security_var = tk.BooleanVar(value=auto_actions.get("alert_on_security", True))
        tk.Checkbutton(dialog, text="Alert on security issues",
                       variable=alert_on_security_var, bg="#252941", fg="#e0e0e0",
                       selectcolor="#313244", font=("Segoe UI", 9)).pack(pady=2)

        log_productivity_var = tk.BooleanVar(value=auto_actions.get("log_productivity", True))
        tk.Checkbutton(dialog, text="Log productivity metrics",
                       variable=log_productivity_var, bg="#252941", fg="#e0e0e0",
                       selectcolor="#313244", font=("Segoe UI", 9)).pack(pady=2)

        def save_settings():
            updates = {
                "default_interval": int(interval_entry.get()),
                "change_detection": change_detection_var.get(),
                "smart_scheduling": smart_scheduling_var.get(),
                "privacy_mode": privacy_mode_var.get(),
                "auto_actions": {
                    "screenshot_on_error": screenshot_on_error_var.get(),
                    "alert_on_security": alert_on_security_var.get(),
                    "log_productivity": log_productivity_var.get()
                }
            }

            result = self.ai_monitor.update_config(updates)
            self.update_output(f"✅ {result['message']}\n", "success")
            dialog.destroy()

        tk.Button(dialog, text="💾 Save Settings",
                  bg="#00d4aa", fg="#0f0f1e",
                  font=("Segoe UI", 11, "bold"),
                  command=save_settings, padx=20, pady=8).pack(pady=20)

    def ai_monitor_clear_analytics(self):
        """Clear analytics data"""
        response = messagebox.askyesno(
            "Confirm Clear Analytics",
            "Are you sure you want to clear all analytics data?\n\nThis will delete:\n• Productivity history\n• Security issues log\n• Error history\n• Performance metrics\n• Learned patterns\n\nThis action cannot be undone."
        )

        if response:
            result = self.ai_monitor.clear_analytics()
            self.update_output(f"✅ {result['message']}\n", "success")

    def smart_auto_bug_fixer(self):
        """Auto-Bug Fixer interface"""

        def execute():
            self.update_output("\n🐛 Auto-Bug Fixer\n", "command")

            error_text = self.show_input_dialog(
                "Auto-Bug Fixer",
                "Enter error log or error message to analyze:"
            )

            if error_text:
                self.update_output(f"Analyzing error...\n", "info")
                analysis = self.smart_automation.bug_fixer.analyze_error_log(error_text)

                self.update_output(f"\n📋 Error Analysis\n", "success")
                self.update_output(f"Type: {analysis.get('error_type', 'Unknown')}\n", "info")
                self.update_output(f"Severity: {analysis.get('severity', 'Unknown')}\n", "info")
                self.update_output(f"\n🔍 Root Cause:\n{analysis.get('root_cause', 'N/A')}\n", "info")

                if analysis.get('fix_steps'):
                    self.update_output(f"\n✅ Fix Steps:\n", "success")
                    for i, step in enumerate(analysis.get('fix_steps', []), 1):
                        self.update_output(f"{i}. {step}\n", "info")

                if analysis.get('prevention_tips'):
                    self.update_output(f"\n💡 Prevention Tips:\n", "success")
                    for tip in analysis.get('prevention_tips', []):
                        self.update_output(f"• {tip}\n", "info")

        threading.Thread(target=execute, daemon=True).start()

    def smart_meeting_scheduler(self):
        """Meeting Scheduler AI interface"""

        def execute():
            self.update_output("\n📅 Meeting Scheduler AI\n", "command")

            title = self.show_input_dialog("Meeting Title", "Enter meeting title:")
            if not title:
                return

            duration = self.show_input_dialog("Duration", "Duration in minutes (e.g., 30):")
            if not duration:
                return

            attendees = self.show_input_dialog("Attendees", "Enter attendee emails (comma-separated):")
            if not attendees:
                return

            attendee_list = [a.strip() for a in attendees.split(',') if a.strip()]

            self.update_output("Finding optimal meeting time...\n", "info")
            result = self.smart_automation.meeting_scheduler.schedule_meeting(
                title, int(duration), attendee_list
            )

            if result.get('success'):
                time_slot = result['scheduled_time']
                self.update_output(f"\n✅ Meeting Scheduled!\n", "success")
                self.update_output(f"Title: {title}\n", "info")
                self.update_output(f"Time: {time_slot.get('start', 'N/A')}\n", "info")
                self.update_output(f"Duration: {duration} minutes\n", "info")
                self.update_output(f"Event ID: {result.get('event_id', 'N/A')}\n", "info")

                if result.get('alternatives'):
                    self.update_output(f"\n📋 Alternative Times:\n", "success")
                    for alt in result['alternatives']:
                        self.update_output(f"• {alt.get('start', 'N/A')}\n", "info")
            else:
                self.update_output(f"❌ {result.get('message', 'Failed to schedule')}\n", "error")

        threading.Thread(target=execute, daemon=True).start()

    def smart_file_recommender(self):
        """Smart File Recommendations interface"""

        def execute():
            self.update_output("\n📁 Smart File Recommendations\n", "command")

            task = self.show_input_dialog(
                "Current Task",
                "What are you working on? (optional, press Enter to skip):"
            )

            self.update_output("Analyzing file patterns...\n", "info")
            recommendations = self.smart_automation.file_recommender.recommend_files(
                current_task=task if task else None,
                limit=10
            )

            if recommendations:
                self.update_output(f"\n✅ Recommended Files ({len(recommendations)}):\n", "success")
                for i, rec in enumerate(recommendations, 1):
                    self.update_output(f"\n{i}. {rec.get('file', 'Unknown')}\n", "info")
                    self.update_output(f"   Reason: {rec.get('reason', 'N/A')}\n", "success")
                    self.update_output(f"   Score: {rec.get('score', 0)}/100\n", "info")
            else:
                self.update_output("ℹ️ No recommendations available yet. Start working with files to build patterns!\n",
                                   "info")

        threading.Thread(target=execute, daemon=True).start()

    def smart_doc_generator(self):
        """Auto-Documentation Generator interface"""

        def execute():
            self.update_output("\n📝 Auto-Documentation Generator\n", "command")

            doc_type = self.show_input_dialog(
                "Documentation Type",
                "What to generate?\n1. README for project\n2. Function documentation\n3. API documentation\n\nEnter number (1-3):"
            )

            if doc_type == "1":
                self.update_output("Generating README.md...\n", "info")
                readme = self.smart_automation.doc_generator.generate_readme(".")
                self.update_output(f"\n✅ README Generated!\n", "success")
                self.update_output(f"{readme[:500]}...\n", "info")
                self.update_output(f"\nSaved to: auto_generated_docs/README_generated.md\n", "success")
            elif doc_type == "2":
                file_path = self.show_input_dialog("File Path", "Enter file path to document:")
                if file_path:
                    self.update_output(f"Generating documentation for {file_path}...\n", "info")
                    result = self.smart_automation.doc_generator.document_file(file_path)
                    if result.get('success'):
                        self.update_output(f"\n✅ Documentation Generated!\n", "success")
                        self.update_output(f"Saved to: {result.get('docs_path', 'N/A')}\n", "info")
                    else:
                        self.update_output(f"❌ {result.get('error', 'Failed')}\n", "error")
            elif doc_type == "3":
                self.update_output("API documentation feature requires code input.\n", "info")
                self.update_output("Use 'Function documentation' option instead.\n", "info")

        threading.Thread(target=execute, daemon=True).start()

    def smart_command_shortcuts(self):
        """Intelligent Command Shortcuts interface"""

        def execute():
            self.update_output("\n⚡ Intelligent Command Shortcuts\n", "command")

            action = self.show_input_dialog(
                "Command Shortcuts",
                "What would you like to do?\n1. View suggestions\n2. Create shortcut\n3. View most used\n\nEnter number (1-3):"
            )

            if action == "1":
                self.update_output("Analyzing command patterns...\n", "info")
                suggestions = self.smart_automation.command_shortcuts.suggest_shortcuts()

                if suggestions:
                    self.update_output(f"\n✅ Shortcut Suggestions ({len(suggestions)}):\n", "success")
                    for i, sug in enumerate(suggestions, 1):
                        self.update_output(f"\n{i}. {sug.get('shortcut', 'N/A')}\n", "info")
                        self.update_output(f"   {sug.get('description', 'N/A')}\n", "success")
                        self.update_output(f"   Commands: {', '.join(sug.get('commands', []))}\n", "info")
                else:
                    self.update_output("ℹ️ No patterns detected yet. Keep using commands!\n", "info")

            elif action == "2":
                name = self.show_input_dialog("Shortcut Name", "Enter shortcut name:")
                if name:
                    self.update_output(f"Shortcut '{name}' created!\n", "success")

            elif action == "3":
                shortcuts = self.smart_automation.command_shortcuts.get_most_used_shortcuts(5)
                if shortcuts:
                    self.update_output(f"\n✅ Most Used Shortcuts:\n", "success")
                    for i, shortcut in enumerate(shortcuts, 1):
                        self.update_output(f"\n{i}. {shortcut.get('name', 'N/A')}\n", "info")
                        self.update_output(f"   Used: {shortcut.get('usage_count', 0)} times\n", "success")
                else:
                    self.update_output("ℹ️ No shortcuts created yet.\n", "info")

        threading.Thread(target=execute, daemon=True).start()

    def smart_context_switcher(self):
        """Project Context Switcher interface"""

        def execute():
            self.update_output("\n🔀 Project Context Switcher\n", "command")

            contexts = self.smart_automation.context_switcher.list_contexts()

            if contexts:
                self.update_output(f"\n📋 Saved Contexts ({len(contexts)}):\n", "success")
                for i, ctx in enumerate(contexts, 1):
                    self.update_output(f"\n{i}. {ctx.get('name', 'N/A')}\n", "info")
                    self.update_output(f"   Path: {ctx.get('project_path', 'N/A')}\n", "success")
                    self.update_output(f"   Files: {ctx.get('file_count', 0)}\n", "info")
                    self.update_output(f"   Last accessed: {ctx.get('last_accessed', 'N/A')[:19]}\n", "info")
            else:
                self.update_output("ℹ️ No saved contexts yet.\n", "info")

            current = self.smart_automation.context_switcher.get_current_context()
            if current:
                self.update_output(f"\n✅ Current Context: {current.get('name', 'None')}\n", "success")

        threading.Thread(target=execute, daemon=True).start()

    def smart_task_prioritizer(self):
        """Task Auto-Prioritizer interface"""

        def execute():
            self.update_output("\n🎯 Task Auto-Prioritizer\n", "command")

            self.update_output("Prioritizing tasks with AI...\n", "info")
            prioritized = self.smart_automation.task_prioritizer.prioritize_tasks()

            if prioritized:
                self.update_output(f"\n✅ Prioritized Tasks ({len(prioritized)}):\n", "success")
                for i, task in enumerate(prioritized[:10], 1):
                    score = task.get('priority_score', 0)
                    self.update_output(f"\n{i}. [{score:.0f}/100] {task.get('title', 'N/A')}\n", "info")
                    if task.get('deadline'):
                        self.update_output(f"   Deadline: {task['deadline'][:10]}\n", "success")
                    if task.get('priority_reason'):
                        self.update_output(f"   Why: {task['priority_reason']}\n", "info")

                suggestions = self.smart_automation.task_prioritizer.get_task_suggestions()
                if suggestions:
                    self.update_output(f"\n💡 Suggestions:\n", "success")
                    for suggestion in suggestions:
                        self.update_output(f"• {suggestion}\n", "info")
            else:
                self.update_output("ℹ️ No tasks to prioritize. Add tasks first!\n", "info")

        threading.Thread(target=execute, daemon=True).start()

    def smart_workflow_optimizer(self):
        """Workflow Auto-Optimizer interface"""

        def execute():
            self.update_output("\n🔧 Workflow Auto-Optimizer\n", "command")

            self.update_output("Analyzing workflow patterns...\n", "info")
            report = self.smart_automation.workflow_optimizer.get_efficiency_report()

            self.update_output(f"\n📊 Efficiency Report\n", "success")
            self.update_output(f"Total Actions: {report.get('total_actions', 0)}\n", "info")
            self.update_output(f"Detected Patterns: {report.get('detected_patterns', 0)}\n", "info")
            self.update_output(f"Optimizable Actions: {report.get('optimizable_actions', 0)}\n", "info")
            self.update_output(f"Efficiency Score: {report.get('efficiency_score', 0)}/100\n", "success")

            if report.get('top_patterns'):
                self.update_output(f"\n🔄 Top Repeated Patterns:\n", "success")
                for pattern in report['top_patterns'][:5]:
                    self.update_output(f"• {pattern.get('pattern', 'N/A')} ({pattern.get('occurrences', 0)}x)\n",
                                       "info")

            if report.get('recommendations'):
                self.update_output(f"\n💡 Recommendations:\n", "success")
                for rec in report['recommendations']:
                    self.update_output(f"• {rec}\n", "info")

            self.update_output("\nGenerating optimization suggestions...\n", "info")
            optimizations = self.smart_automation.workflow_optimizer.suggest_optimizations()

            if optimizations:
                self.update_output(f"\n✅ Optimization Suggestions:\n", "success")
                for i, opt in enumerate(optimizations[:5], 1):
                    self.update_output(f"\n{i}. Pattern: {opt.get('pattern', 'N/A')}\n", "info")
                    self.update_output(f"   Suggestion: {opt.get('suggestion', 'N/A')}\n", "success")
                    self.update_output(f"   Time Saved: {opt.get('time_saved', 'N/A')}\n", "info")
                    self.update_output(f"   Difficulty: {opt.get('difficulty', 'N/A')}\n", "info")

        threading.Thread(target=execute, daemon=True).start()

    def smart_template_generator(self):
        """Smart Template Generator interface"""

        def execute():
            self.update_output("\n📋 Smart Template Generator\n", "command")

            template_type = self.show_input_dialog(
                "Template Type",
                "What type of template?\n1. Code template\n2. Email template\n3. Document template\n\nEnter number (1-3):"
            )

            if template_type == "1":
                language = self.show_input_dialog("Language", "Programming language (e.g., python, javascript):")
                template_kind = self.show_input_dialog("Type", "Template type (e.g., class, function, api):")

                if language and template_kind:
                    self.update_output(f"Generating {language} {template_kind} template...\n", "info")
                    template = self.smart_automation.template_generator.generate_code_template(
                        language, template_kind
                    )
                    self.update_output(f"\n✅ Code Template Generated!\n", "success")
                    self.update_output(f"{template[:500]}...\n", "info")

            elif template_type == "2":
                purpose = self.show_input_dialog("Purpose", "Email purpose (e.g., job application, follow-up):")
                tone = self.show_input_dialog("Tone", "Tone (professional/casual/friendly):", "professional")

                if purpose:
                    self.update_output(f"Generating email template...\n", "info")
                    template = self.smart_automation.template_generator.generate_email_template(
                        purpose, tone if tone else "professional"
                    )
                    self.update_output(f"\n✅ Email Template Generated!\n", "success")
                    self.update_output(f"{template[:400]}...\n", "info")

            elif template_type == "3":
                doc_type = self.show_input_dialog("Document Type", "Document type (e.g., proposal, report):")

                if doc_type:
                    self.update_output(f"Generating document template...\n", "info")
                    template = self.smart_automation.template_generator.generate_document_template(doc_type)
                    self.update_output(f"\n✅ Document Template Generated!\n", "success")
                    self.update_output(f"{template[:400]}...\n", "info")

            templates = self.smart_automation.template_generator.list_templates()
            self.update_output(f"\n📋 Total Templates Created: {len(templates)}\n", "success")

        threading.Thread(target=execute, daemon=True).start()

    def smart_automation_dashboard(self):
        """Show Smart Automation Dashboard"""

        def execute():
            self.update_output("\n📊 Smart Automation Dashboard\n", "command")

            summary = self.smart_automation.get_dashboard_summary()

            self.update_output(f"\n🐛 Auto-Bug Fixer\n", "success")
            self.update_output(f"Fixes Applied: {summary['auto_bug_fixer']['fixes_applied']}\n", "info")

            self.update_output(f"\n📅 Meeting Scheduler\n", "success")
            self.update_output(f"Upcoming Meetings: {summary['meeting_scheduler']['upcoming_meetings']}\n", "info")

            self.update_output(f"\n📁 File Recommender\n", "success")
            self.update_output(f"Tracked Files: {summary['file_recommender']['tracked_files']}\n", "info")

            self.update_output(f"\n⚡ Command Shortcuts\n", "success")
            self.update_output(f"Shortcuts Created: {summary['command_shortcuts']['shortcuts_created']}\n", "info")

            self.update_output(f"\n🔀 Project Contexts\n", "success")
            self.update_output(f"Saved Contexts: {summary['project_contexts']['saved_contexts']}\n", "info")

            self.update_output(f"\n🎯 Task Prioritizer\n", "success")
            self.update_output(f"Pending Tasks: {summary['task_prioritizer']['pending_tasks']}\n", "info")

            self.update_output(f"\n🔧 Workflow Optimizer\n", "success")
            self.update_output(f"Patterns Detected: {summary['workflow_optimizer']['patterns_detected']}\n", "info")
            self.update_output(f"Efficiency Score: {summary['workflow_optimizer']['efficiency_score']}/100\n", "info")

            self.update_output(f"\n📋 Template Generator\n", "success")
            self.update_output(f"Templates Created: {summary['template_generator']['templates_created']}\n", "info")

            self.update_output("\n", "info")

        threading.Thread(target=execute, daemon=True).start()

    def show_input_dialog(self, title, prompt, default=""):
        """Helper method to show input dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("500x200")
        dialog.configure(bg="#252941")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text=prompt,
                 bg="#252941", fg="#e0e0e0",
                 font=("Segoe UI", 10),
                 wraplength=450).pack(pady=20, padx=20)

        entry = tk.Entry(dialog, font=("Segoe UI", 11), width=40)
        entry.insert(0, default)
        entry.pack(pady=10)
        entry.focus()

        result: list = [None]

        def on_ok():
            result[0] = entry.get()
            dialog.destroy()

        def on_cancel():
            dialog.destroy()

        entry.bind("<Return>", lambda e: on_ok())
        entry.bind("<Escape>", lambda e: on_cancel())

        btn_frame = tk.Frame(dialog, bg="#252941")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="OK", command=on_ok,
                  bg="#00d4aa", fg="#0f0f1e",
                  font=("Segoe UI", 10, "bold"),
                  padx=20, pady=5).pack(side="left", padx=5)

        tk.Button(btn_frame, text="Cancel", command=on_cancel,
                  bg="#2e3350", fg="#e0e0e0",
                  font=("Segoe UI", 10),
                  padx=20, pady=5).pack(side="left", padx=5)

        dialog.wait_window()
        return result[0]

    def launch_batch_controller(self):
        """Launch Windows batch file controller"""

        def execute():
            self.update_output("\n🗂️ Desktop File Controller\n", "command")

            result = self.desktop_controller.launch_batch_controller()

            if result["success"]:
                self.update_output(f"✅ {result['message']}\n", "success")
                self.update_output("The batch file controller window has been opened.\n", "info")
            else:
                self.update_output(f"ℹ️ {result['message']}\n", "info")
                self.update_output("\nYou can use the Python-based buttons below instead:\n", "info")
                self.update_output("• List Desktop Items\n", "info")
                self.update_output("• Create New Folder\n", "info")
                self.update_output("• Organize Desktop\n", "info")
                self.update_output("• Search Desktop Files\n", "info")

        threading.Thread(target=execute, daemon=True).start()

    def list_desktop_items(self):
        """List all items on desktop"""

        def execute():
            self.update_output("\n📋 Desktop Contents\n", "command")

            result = self.desktop_controller.list_items()

            if result["success"]:
                self.update_output(f"📁 Total items: {result['count']}\n\n", "success")

                folders = [item for item in result["items"] if item["type"] == "Folder"]
                files = [item for item in result["items"] if item["type"] == "File"]

                if folders:
                    self.update_output(f"📂 Folders ({len(folders)}):\n", "success")
                    for item in folders[:15]:
                        self.update_output(f"  📁 {item['name']}\n", "info")
                    if len(folders) > 15:
                        self.update_output(f"  ... and {len(folders) - 15} more folders\n", "info")
                    self.update_output("\n", "info")

                if files:
                    self.update_output(f"📄 Files ({len(files)}):\n", "success")
                    for item in files[:15]:
                        self.update_output(f"  📄 {item['name']}\n", "info")
                    if len(files) > 15:
                        self.update_output(f"  ... and {len(files) - 15} more files\n", "info")

                self.update_output(f"\n📊 Desktop Path: {self.desktop_controller.desktop_path}\n", "info")
            else:
                self.update_output(f"❌ {result['message']}\n", "error")

        threading.Thread(target=execute, daemon=True).start()

    def create_desktop_folder(self):
        """Create a new folder on desktop"""

        def execute():
            folder_name = self.show_input_dialog(
                "Create Folder",
                "Enter the name for the new folder:"
            )

            if folder_name:
                self.update_output("\n➕ Creating Folder...\n", "command")

                result = self.desktop_controller.create_folder(folder_name)

                if result["success"]:
                    self.update_output(f"✅ {result['message']}\n", "success")
                    self.update_output(f"📁 Path: {result['path']}\n", "info")
                else:
                    self.update_output(f"❌ {result['message']}\n", "error")
            else:
                self.update_output("ℹ️ Folder creation cancelled.\n", "info")

        threading.Thread(target=execute, daemon=True).start()

    def organize_desktop(self):
        """Organize desktop files by type"""

        def execute():
            self.update_output("\n📁 Organizing Desktop...\n", "command")

            self.update_output("Sorting files into folders by type...\n", "info")
            self.update_output("• Documents (txt, pdf, doc, xls, ppt)\n", "info")
            self.update_output("• Images (jpg, png, gif, bmp, svg)\n", "info")
            self.update_output("• Videos (mp4, avi, mkv, mov)\n", "info")
            self.update_output("• Music (mp3, wav, flac)\n", "info")
            self.update_output("• Archives (zip, rar, 7z)\n", "info")
            self.update_output("• Programs (exe, msi)\n\n", "info")

            result = self.desktop_controller.organize_by_type()

            if result["success"]:
                self.update_output(f"✅ {result['message']}\n", "success")
                self.update_output("Your desktop is now organized!\n", "info")
            else:
                self.update_output(f"❌ {result['message']}\n", "error")

        threading.Thread(target=execute, daemon=True).start()

    def search_desktop_files(self):
        """Search for files on desktop"""

        def execute():
            search_term = self.show_input_dialog(
                "Search Desktop",
                "Enter search term (filename or part of filename):"
            )

            if search_term:
                self.update_output(f"\n🔍 Searching Desktop for '{search_term}'...\n", "command")

                result = self.desktop_controller.search_files(search_term)

                if result["success"]:
                    if result["count"] > 0:
                        self.update_output(f"✅ Found {result['count']} matching items:\n\n", "success")

                        for item in result["results"][:20]:
                            icon = "📁" if item["type"] == "Folder" else "📄"
                            self.update_output(f"{icon} {item['name']}\n", "info")
                            self.update_output(f"   Path: {item['path']}\n", "info")

                        if result['count'] > 20:
                            self.update_output(f"\n... and {result['count'] - 20} more results\n", "info")
                    else:
                        self.update_output(f"ℹ️ No files found matching '{search_term}'\n", "info")
                else:
                    self.update_output(f"❌ {result['message']}\n", "error")
            else:
                self.update_output("ℹ️ Search cancelled.\n", "info")

        threading.Thread(target=execute, daemon=True).start()

    # ===== PRODUCTIVITY HUB METHODS =====

    def start_pomodoro_session(self):
        """Start a new Pomodoro session"""
        task_name = self.show_input_dialog("Pomodoro Task", "What are you working on?", "Focused Work")
        if task_name:
            result = self.pomodoro_coach.start_pomodoro(task_name)
            self.update_output(f"\n🍅 Pomodoro Started!\n", "success")
            self.update_output(f"Task: {task_name}\n", "info")
            self.update_output(f"Duration: {result['duration']} minutes\n", "info")
            if result.get('ai_coach'):
                self.update_output(f"\n💬 AI Coach: {result['ai_coach']}\n", "command")

    def start_short_break(self):
        """Start a short break"""
        result = self.pomodoro_coach.start_break(is_long=False)
        self.update_output(f"\n☕ {result['message']}\n", "success")
        if result.get('ai_coach'):
            self.update_output(f"💬 AI Coach: {result['ai_coach']}\n", "info")

    def start_long_break(self):
        """Start a long break"""
        result = self.pomodoro_coach.start_break(is_long=True)
        self.update_output(f"\n🌳 {result['message']}\n", "success")
        if result.get('ai_coach'):
            self.update_output(f"💬 AI Coach: {result['ai_coach']}\n", "info")

    def toggle_pomodoro(self):
        """Pause/resume Pomodoro"""
        result = self.pomodoro_coach.pause_session()
        self.update_output(f"\n⏸️ {result['message']}\n", "info")

    def stop_pomodoro(self):
        """Stop current Pomodoro session"""
        result = self.pomodoro_coach.stop_session()
        self.update_output(f"\n🛑 {result['message']}\n", "info")

    def view_pomodoro_stats(self):
        """View Pomodoro statistics"""
        stats = self.pomodoro_coach.get_statistics()
        self.update_output(f"\n📊 POMODORO STATISTICS\n", "success")

        self.update_output(f"Total Pomodoros: {stats['total_pomodoros']}\n", "info")
        self.update_output(f"Completed Today: {stats['pomodoros_today']}\n", "info")
        self.update_output(f"Total Work Time: {stats['total_work_hours']:.1f} hours\n", "info")
        self.update_output(f"Completion Rate: {stats['completion_rate']:.1f}%\n", "success")

    def start_task_tracking(self):
        """Start tracking a new task"""
        task_name = self.show_input_dialog("Task Name", "What task are you starting?")
        if task_name:
            category = self.show_input_dialog("Task Category", "Category (coding/meeting/email/documentation/etc):",
                                              "general")
            result = self.task_predictor.start_task(task_name, category or "general")
            self.update_output(f"\n▶️ Task Started: {task_name}\n", "success")
            self.update_output(f"Task ID: #{result['task_id']}\n", "info")
            self.update_output(f"Estimated Time: {result['estimated_minutes']} minutes\n", "info")
            self.update_output(f"Predicted Time: {result['predicted_minutes']} minutes\n", "command")
            self.update_output(f"Confidence: {result['confidence']}\n", "info")

    def complete_task(self):
        """Complete current task"""
        task_id = self.show_input_dialog("Task ID", "Enter task ID to complete:")
        if task_id:
            try:
                result = self.task_predictor.complete_task(int(task_id))
                if result['success']:
                    self.update_output(f"\n✅ Task Completed!\n", "success")
                    self.update_output(f"Task: {result['task_name']}\n", "info")
                    self.update_output(f"Estimated: {result['estimated_minutes']:.0f} min\n", "info")
                    self.update_output(f"Actual: {result['actual_minutes']:.0f} min\n", "info")
                    self.update_output(f"Accuracy: {result['accuracy']:.1f}%\n", "success")
                else:
                    self.update_output(f"❌ {result['message']}\n", "error")
            except ValueError:
                self.update_output("❌ Invalid task ID\n", "error")

    def view_task_predictions(self):
        """View task time predictions"""
        report = self.task_predictor.get_accuracy_report()
        self.update_output(f"\n📈 TASK PREDICTION REPORT\n", "success")

        self.update_output(f"Total Tasks: {report['total_tasks']}\n", "info")
        self.update_output(f"Average Accuracy: {report['average_accuracy']:.1f}%\n", "success")
        self.update_output(f"Best Category: {report['best_category']}\n", "info")

    def view_task_analytics(self):
        """View task analytics"""
        insights = self.task_predictor.get_insights()
        self.update_output(f"\n📊 TASK ANALYTICS\n", "success")

        for insight in insights:
            self.update_output(f"• {insight}\n", "info")

    def check_energy_level(self):
        """Check current energy level"""
        energy = self.energy_tracker.get_current_energy()
        self.update_output(f"\n🔋 CURRENT ENERGY LEVEL\n", "success")

        self.update_output(f"Level: {energy['level']:.0f}/100 {energy['emoji']}\n", "info")
        self.update_output(f"Status: {energy['category']}\n", "success")
        self.update_output(f"Trend: {energy['trend']}\n", "info")
        if energy.get('suggestion'):
            self.update_output(f"\n💡 {energy['suggestion']}\n", "command")

    def view_energy_trends(self):
        """View energy trends"""
        trends = self.energy_tracker.get_daily_summary()
        self.update_output(f"\n📈 ENERGY TRENDS\n", "success")

        self.update_output(f"Average Energy: {trends['average_energy']:.0f}/100\n", "info")
        self.update_output(f"Peak Time: {trends['peak_hour']}:00\n", "success")
        self.update_output(f"Low Time: {trends['low_hour']}:00\n", "info")

    def get_break_suggestion(self):
        """Get AI break suggestion"""
        suggestion = self.break_suggester.should_take_break()
        self.update_output(f"\n🎯 BREAK SUGGESTION\n", "success")

        self.update_output(f"{suggestion['message']}\n", "info")
        if suggestion['should_break']:
            self.update_output(f"\n💡 Suggested break type: {suggestion['break_type']}\n", "command")
            self.update_output(f"Duration: {suggestion['duration']} minutes\n", "info")

    def check_distractions(self):
        """Check for distractions"""
        result = self.distraction_detector.detect_distraction()
        self.update_output(f"\n⚠️ DISTRACTION CHECK\n", "success")

        if result['is_distracted']:
            self.update_output(f"Status: Distracted ⚠️\n", "error")
            self.update_output(f"App: {result['app']}\n", "info")
            self.update_output(f"Category: {result['category']}\n", "info")
        else:
            self.update_output(f"Status: Focused ✅\n", "success")

    def view_focus_report(self):
        """View focus report"""
        report = self.distraction_detector.get_daily_report()
        self.update_output(f"\n📊 FOCUS REPORT\n", "success")

        self.update_output(f"Distractions Today: {report['distractions_today']}\n", "info")
        self.update_output(f"Focus Time: {report['focus_time']} minutes\n", "success")
        self.update_output(f"Distraction Time: {report['distraction_time']} minutes\n", "error")

    def view_productivity_dashboard(self):
        """View complete productivity dashboard"""
        dashboard = self.productivity_dashboard.get_comprehensive_dashboard()
        self.update_output(f"\n📊 PRODUCTIVITY DASHBOARD\n", "success")

        self.update_output(f"Period: {dashboard['period']}\n", "info")
        overview = dashboard['overview']
        self.update_output(f"\nWork Sessions: {overview['total_work_sessions']}\n", "info")
        self.update_output(f"Tasks Completed: {overview['total_tasks_completed']}\n", "info")
        self.update_output(f"Productivity Score: {overview['productivity_score']:.0f}/100\n", "success")

    def view_weekly_summary(self):
        """View weekly summary"""
        dashboard = self.productivity_dashboard.get_comprehensive_dashboard(days=7)
        self.update_output(f"\n📅 WEEKLY SUMMARY\n", "success")

        time_analysis = dashboard['time_analysis']
        if not time_analysis.get('no_data'):
            self.update_output(f"Total Work Time: {time_analysis['total_work_minutes']} minutes\n", "info")
            self.update_output(f"Daily Average: {time_analysis['avg_work_minutes_per_day']:.0f} minutes\n", "info")
            self.update_output(f"Most Productive Hour: {time_analysis['most_productive_hour']}:00\n", "success")

    def view_productivity_trends(self):
        """View productivity trends"""
        self.update_output(f"\n📈 PRODUCTIVITY TRENDS\n", "success")
        self.update_output(f"Analyzing your productivity patterns...\n", "info")
        dashboard = self.productivity_dashboard.get_comprehensive_dashboard(days=30)
        for rec in dashboard['recommendations']:
            self.update_output(f"💡 {rec}\n", "command")

    def get_productivity_recommendations(self):
        """Get productivity recommendations"""
        dashboard = self.productivity_dashboard.get_comprehensive_dashboard()
        self.update_output(f"\n🎯 PRODUCTIVITY RECOMMENDATIONS\n", "success")

        for i, rec in enumerate(dashboard['recommendations'], 1):
            self.update_output(f"{i}. {rec}\n", "info")

    # ===== TOOLS & UTILITIES METHODS =====

    def add_password_dialog(self):
        """Add new password to vault"""
        name = self.show_input_dialog("Service Name", "Service name (e.g., Gmail, GitHub):")
        if name:
            username = self.show_input_dialog("Username", "Username or email:")
            password = self.show_input_dialog("Password", "Password:")
            url = self.show_input_dialog("URL (Optional)", "Service URL:", "")
            if username and password:
                result = self.password_vault.add_password(name, username, password, url)
                self.update_output(result, "success")

    def view_password_dialog(self):
        """View a password from vault"""
        name = self.show_input_dialog("Service Name", "Which service password to view?")
        if name:
            result = self.password_vault.get_password(name)
            self.update_output(result, "info")

    def list_passwords(self):
        """List all saved passwords"""
        result = self.password_vault.list_passwords()
        self.update_output(result, "info")

    def generate_password(self):
        """Generate a secure password"""
        length = self.show_input_dialog("Password Length", "Length (8-32 characters):", "16")
        try:
            length = int(length) if length else 16
            result = self.password_vault.generate_secure_password(length)
            self.update_output(result, "success")
        except:
            self.update_output("❌ Invalid length\n", "error")

    def add_note_dialog(self):
        """Add a new note"""
        content = self.show_input_dialog("Note Content", "Enter your note:")
        if content:
            category = self.show_input_dialog("Category", "Category (optional):", "general")
            result = self.notes.add_note(content, category or "general")
            self.update_output(result, "success")

    def list_notes(self):
        """List all notes"""
        result = self.notes.list_notes()
        self.update_output(result, "info")

    def search_notes_dialog(self):
        """Search notes"""
        query = self.show_input_dialog("Search Notes", "Search term:")
        if query:
            result = self.notes.search_notes(query)
            self.update_output(result, "info")

    def view_pinned_notes(self):
        """View pinned notes"""
        result = self.notes.get_pinned_notes()
        self.update_output(result, "info")

    def add_event_dialog(self):
        """Add a calendar event"""
        title = self.show_input_dialog("Event Title", "Event name:")
        if title:
            date = self.show_input_dialog("Date", "Date (YYYY-MM-DD):")
            time = self.show_input_dialog("Time (Optional)", "Time (HH:MM):", "")
            if date:
                result = self.calendar.add_event(title, date, time)
                self.update_output(result, "success")

    def view_today_events(self):
        """View today's events"""
        result = self.calendar.get_today_events()
        self.update_output(result, "info")

    def view_week_events(self):
        """View this week's events"""
        result = self.calendar.get_week_events()
        self.update_output(result, "info")

    def view_reminders(self):
        """View upcoming reminders"""
        result = self.calendar.get_upcoming_reminders()
        self.update_output(result, "info")

    def get_weather_dialog(self):
        """Get weather for a city"""
        city = self.show_input_dialog("City", "Enter city name:", "New York")
        if city:
            result = self.weather_news.get_weather(city)
            self.update_output(result, "info")

    def get_forecast(self):
        """Get weather forecast"""
        city = self.show_input_dialog("City", "Enter city name:", "New York")
        if city:
            result = self.weather_news.get_forecast(city, days=3)
            self.update_output(result, "info")

    def get_news(self):
        """Get latest news"""
        result = self.weather_news.get_news_headlines("general", 5)
        self.update_output(result, "info")

    def get_tech_news(self):
        """Get tech news"""
        result = self.weather_news.get_news_headlines("technology", 5)
        self.update_output(result, "info")

    def translate_text_dialog(self):
        """Translate text"""
        text = self.show_input_dialog("Text to Translate", "Enter text:")
        if text:
            target = self.show_input_dialog("Target Language", "Language code (e.g., es, fr, de):", "es")
            if target:
                result = self.translator.translate(text, target)
                self.update_output(result, "info")

    def detect_language_dialog(self):
        """Detect text language"""
        text = self.show_input_dialog("Text", "Enter text to detect language:")
        if text:
            result = self.translator.detect_language(text)
            self.update_output(result, "info")

    def show_supported_languages(self):
        """Show supported languages"""
        result = self.translator.get_supported_languages()
        self.update_output(result, "info")

    def auto_desktop_sync(self):
        """Auto-initialize desktop sync on GUI startup - Scans and stores desktop data"""
        import time
        time.sleep(2)  # Wait for GUI to fully load

        try:
            self.update_output("\n", "info")
            self.update_output("🚀 DESKTOP FILE & FOLDER AUTOMATOR - STARTING\n", "command")

            # Create Desktop Sync Manager instance
            manager = DesktopSyncManager()

            # Step 1: Scan the desktop
            self.update_output("\n🔍 Scanning your desktop...\n", "command")
            scan_result = manager.scan_desktop()

            if not scan_result["success"]:
                self.update_output(f"❌ Error: {scan_result['message']}\n", "error")
                return

            scan_data = scan_result["data"]
            stats = scan_data["statistics"]

            # Step 2: Display summary in GUI
            self.update_output("\n📊 DESKTOP ANALYSIS SUMMARY\n", "success")

            self.update_output(f"📂 Desktop Location: {scan_data['desktop_path']}\n", "info")
            self.update_output(
                f"📅 Scanned: {datetime.fromisoformat(scan_data['scan_time']).strftime('%Y-%m-%d %H:%M:%S')}\n\n",
                "info")

            self.update_output(f"📁 Total Folders: {stats['total_folders']}\n", "info")
            self.update_output(f"📄 Total Files: {stats['total_files']}\n", "info")

            # Format file size
            total_size = stats['total_size_bytes']
            size_str = manager.format_size(total_size)
            self.update_output(f"💾 Total Size: {size_str}\n", "info")

            # Show file types
            if stats["file_types"]:
                self.update_output(f"\n📑 File Types Found:\n", "command")
                for ext, count in sorted(stats["file_types"].items(), key=lambda x: x[1], reverse=True)[:10]:
                    ext_display = ext if ext != "no_extension" else "(no extension)"
                    self.update_output(f"   {ext_display}: {count} file(s)\n", "info")

            # Show top folders
            if scan_data["folders"]:
                self.update_output(f"\n📂 Folders on Desktop:\n", "command")
                for folder in scan_data["folders"][:10]:
                    self.update_output(f"   • {folder['name']} ({folder['item_count']} items)\n", "info")
                if len(scan_data["folders"]) > 10:
                    self.update_output(f"   ... and {len(scan_data['folders']) - 10} more folders\n", "info")

            # Step 3: Save the data
            self.update_output("\n💾 Saving desktop data...\n", "command")
            save_result = manager.save_desktop_data(scan_data)

            if save_result["success"]:
                self.update_output(f"✅ Data saved to: {save_result['file']}\n", "success")
            else:
                self.update_output(f"⚠️  Could not save data: {save_result['message']}\n", "error")

            # Step 4: Check batch file
            batch_result = manager.prepare_batch_file_download()
            if batch_result["success"]:
                self.update_output("\n📥 BATCH FILE READY:\n", "success")
                self.update_output(f"   Location: {batch_result['batch_file']}\n", "info")
                if manager.is_windows:
                    self.update_output("   🚀 Double-click to launch desktop automation!\n", "info")
                else:
                    self.update_output("   📥 Download to your Windows PC to use\n", "info")
            else:
                self.update_output("\n📥 BATCH FILE SETUP:\n", "command")
                self.update_output("   Download 'desktop_file_controller.bat' from Replit\n", "info")
                self.update_output(f"   Place in: {manager.script_dir}\n", "info")

            self.update_output("\n", "info")
            self.update_output("✅ DESKTOP SCAN COMPLETE!\n", "success")
            self.update_output("💡 All desktop data has been analyzed and saved\n", "info")
            self.update_output("🗂️  Use the Desktop tab buttons to manage your files\n", "info")
            self.update_output("\n\n", "info")

        except Exception as e:
            self.update_output(f"\n⚠️  Desktop sync error: {str(e)}\n", "error")
            import traceback
            self.update_output(f"Details: {traceback.format_exc()}\n", "error")

    # ==================== Comprehensive Controller Methods ====================

    def load_comprehensive_command(self, command):
        """Load a predefined command into the input"""
        self.comprehensive_input.delete(0, tk.END)
        self.comprehensive_input.insert(0, command)
        self.comprehensive_input.focus()

    def show_quick_actions_menu(self):
        """Show the main quick actions menu"""
        self.quick_feature_view.pack_forget()
        self.quick_menu_view.pack(fill="both", expand=True)

    def toggle_sidebar(self):
        """Toggle sidebar expanded/collapsed state"""
        if self.sidebar_expanded:
            # Collapse sidebar
            self.sidebar.config(width=50)
            self.sidebar_toggle_btn.config(text="▶")
            self.sidebar_title.pack_forget()

            # Update button text to show only icons
            for btn, name, color in self.sidebar_buttons:
                icon = [c for c in self.sidebar_categories if c[1] == name][0][0]
                btn.config(text=icon, width=3)

            self.sidebar_expanded = False
        else:
            # Expand sidebar
            self.sidebar.config(width=120)
            self.sidebar_toggle_btn.config(text="◀")
            self.sidebar_title.pack(pady=(5, 10))

            # Restore full text
            for btn, name, color in self.sidebar_buttons:
                icon = [c for c in self.sidebar_categories if c[1] == name][0][0]
                btn.config(text=f"{icon}\n{name}", width=10)

            self.sidebar_expanded = True

    def scroll_to_category(self, category):
        """Scroll to and highlight a specific category"""
        # Update active category highlighting
        for btn, name, color in self.sidebar_buttons:
            if name == category:
                btn.config(bg="#3d4466", relief="solid", bd=2)
                self.active_sidebar_category = category
            else:
                btn.config(bg="#2e3350", relief="flat", bd=0)

        # Map category names to quick actions headers
        category_map = {
            "SYSTEM": "🖥️ SYSTEM",
            "WEB": "🌐 WEB & APPS",
            "WORK": "📁 PRODUCTIVITY",
            "MEDIA": "🎵 MEDIA"
        }

        target_header = category_map.get(category, "")

        # Scroll to the category header
        if target_header in self.category_headers:
            header_widget = self.category_headers[target_header]
            # Get the y position of the header
            try:
                self.menu_canvas.update_idletasks()
                # Get the widget's bbox
                bbox = self.menu_canvas.bbox("all")
                if bbox:
                    # Calculate position
                    y_pos = header_widget.winfo_y()
                    canvas_height = self.menu_canvas.winfo_height()
                    scroll_region = bbox[3]  # Total height

                    if scroll_region > canvas_height:
                        # Scroll to position
                        fraction = y_pos / scroll_region
                        self.menu_canvas.yview_moveto(fraction)
            except Exception as e:
                print(f"Scroll error: {e}")

    def show_quick_action_feature(self, title, description, color, feature_id):
        """Show the selected quick action feature"""
        # Hide menu, show feature view
        self.quick_menu_view.pack_forget()
        self.quick_feature_view.pack(fill="both", expand=True)

        # Update title
        self.feature_title.config(text=title, fg=color)

        # Clear previous content
        for widget in self.feature_content.winfo_children():
            widget.destroy()

        # Create feature-specific content
        content_inner = tk.Frame(self.feature_content, bg="#181825")
        content_inner.pack(fill="both", expand=True, padx=15, pady=15)

        # Description
        desc_label = tk.Label(content_inner,
                              text=description,
                              bg="#181825",
                              fg="#b0b0b0",
                              font=("Segoe UI", 10),
                              wraplength=350)
        desc_label.pack(pady=(0, 20))

        # Feature-specific content
        if feature_id == "screenshot":
            self.create_screenshot_feature(content_inner, color)
        elif feature_id == "lock":
            self.create_lock_feature(content_inner, color)
        elif feature_id == "taskmanager":
            self.create_taskmanager_feature(content_inner, color)
        elif feature_id == "chrome":
            self.create_chrome_feature(content_inner, color)
        elif feature_id == "google":
            self.create_google_feature(content_inner, color)
        elif feature_id == "gmail":
            self.create_gmail_feature(content_inner, color)
        elif feature_id == "whatsapp":
            self.create_whatsapp_feature(content_inner, color)
        elif feature_id == "vscode":
            self.create_vscode_feature(content_inner, color)
        elif feature_id == "explorer":
            self.create_explorer_feature(content_inner, color)
        elif feature_id == "notepad":
            self.create_notepad_feature(content_inner, color)
        elif feature_id == "spotify":
            self.create_spotify_feature(content_inner, color)
        elif feature_id == "youtube":
            self.create_youtube_feature(content_inner, color)
        elif feature_id == "volume":
            self.create_volume_feature(content_inner, color)
        elif feature_id == "workflow_builder":
            self.create_workflow_builder_feature(content_inner, color)
        elif feature_id == "macro_recorder":
            self.create_macro_recorder_feature(content_inner, color)
        elif feature_id == "mobile_control":
            self.create_mobile_control_feature(content_inner, color)

    def create_workflow_builder_feature(self, parent, color):
        """Create workflow builder feature UI"""
        tk.Label(parent, text="💬 Workflow Builder", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        info_text = "Build complex automation workflows using plain English. The AI will convert your descriptions into executable steps."
        tk.Label(parent, text=info_text, bg="#181825", fg="#b0b0b0",
                 font=("Segoe UI", 9), wraplength=350, justify="left").pack(pady=(0, 20))

        btn = tk.Button(parent, text="💬 Open Workflow Builder",
                        bg=color, fg="#0f0f1e",
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                        command=self.show_workflow_builder,
                        padx=30, pady=12)
        btn.pack(pady=10)

    def create_macro_recorder_feature(self, parent, color):
        """Create macro recorder feature placeholder"""
        tk.Label(parent, text="🎬 Macro Recorder", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))
        tk.Label(parent, text="Record and playback mouse & keyboard actions",
                 bg="#181825", fg="#b0b0b0", font=("Segoe UI", 9)).pack(pady=(0, 20))
        tk.Label(parent, text="Use the Macro Recorder tab for full access",
                 bg="#181825", fg="#b0b0b0", font=("Segoe UI", 9, "italic")).pack()

    def create_mobile_control_feature(self, parent, color):
        """Create mobile control feature placeholder"""
        tk.Label(parent, text="📱 Mobile Control", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))
        tk.Label(parent, text="Control your desktop from mobile devices",
                 bg="#181825", fg="#b0b0b0", font=("Segoe UI", 9)).pack(pady=(0, 20))
        tk.Label(parent, text="Use the Mobile Companion tab for full access",
                 bg="#181825", fg="#b0b0b0", font=("Segoe UI", 9, "italic")).pack()

    def create_hand_gesture_feature(self, parent, color):
        """Create hand gesture control feature UI"""
        tk.Label(parent, text="✋ Hand Gesture Control", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        info_text = "Control your mouse using hand gestures via webcam. Features 7 gestures: cursor movement, left/right click, scroll, drag, and volume control."
        tk.Label(parent, text=info_text, bg="#181825", fg="#b0b0b0",
                 font=("Segoe UI", 9), wraplength=350, justify="left").pack(pady=(0, 20))

        # Launch button
        btn = tk.Button(parent, text="🎥 Launch Hand Gesture Controller",
                        bg=color, fg="#0f0f1e",
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                        command=self.launch_hand_gesture_controller,
                        padx=30, pady=12)
        btn.pack(pady=10)

        # Info labels
        tk.Label(parent, text="📋 Requirements:", bg="#181825", fg="#89dceb",
                 font=("Segoe UI", 9, "bold")).pack(pady=(15, 5), anchor="w")
        tk.Label(parent, text="• Working webcam", bg="#181825", fg="#b0b0b0",
                 font=("Segoe UI", 8)).pack(anchor="w", padx=20)
        tk.Label(parent, text="• Good lighting conditions", bg="#181825", fg="#b0b0b0",
                 font=("Segoe UI", 8)).pack(anchor="w", padx=20)
        tk.Label(parent, text="• Plain background recommended", bg="#181825", fg="#b0b0b0",
                 font=("Segoe UI", 8)).pack(anchor="w", padx=20)

        tk.Label(parent, text="⌨️ Controls:", bg="#181825", fg="#89dceb",
                 font=("Segoe UI", 9, "bold")).pack(pady=(10, 5), anchor="w")
        tk.Label(parent, text="• Press 'Q' to quit", bg="#181825", fg="#b0b0b0",
                 font=("Segoe UI", 8)).pack(anchor="w", padx=20)
        tk.Label(parent, text="• Press 'S' to toggle stats", bg="#181825", fg="#b0b0b0",
                 font=("Segoe UI", 8)).pack(anchor="w", padx=20)

    def launch_hand_gesture_controller(self):
        """Launch the hand gesture controller in a separate thread"""

        def run_controller():
            try:
                from modules.automation.hand_gesture_controller import HandGestureController

                self.log_to_console("🎥 Initializing Hand Gesture Controller...")

                controller = HandGestureController()

                # Check dependencies
                deps = controller.check_dependencies()
                all_available = all(deps.values())

                if not all_available:
                    missing = [name for name, available in deps.items() if not available]
                    error_msg = f"Missing dependencies: {', '.join(missing)}\n"
                    error_msg += controller.get_missing_dependencies_message()
                    self.log_to_console(f"❌ {error_msg}")
                    messagebox.showerror("Missing Dependencies", error_msg)
                    return

                self.log_to_console("✅ All dependencies available")

                # Initialize controller
                result = controller.initialize()

                if not result["success"]:
                    error_msg = result.get("error", "Unknown error")
                    help_text = result.get("help", "")
                    full_msg = f"{error_msg}\n\n{help_text}" if help_text else error_msg
                    self.log_to_console(f"❌ Initialization failed: {error_msg}")
                    messagebox.showerror("Initialization Failed", full_msg)
                    return

                self.log_to_console(f"✅ {result['message']}")
                self.log_to_console(f"📺 Screen: {result['screen_size']}")
                self.log_to_console(f"🎥 {result['camera']}")
                self.log_to_console("✋ HAND GESTURE CONTROLS:")
                self.log_to_console("  👆 Index finger        → Move cursor")
                self.log_to_console("  🤏 Pinch               → Left click")
                self.log_to_console("  ✋ Open palm           → Scroll")
                self.log_to_console("  🤘 Thumb + Index       → Volume control")
                self.log_to_console("  🤙 Pinky only          → Right click")
                self.log_to_console("  ✊ Closed fist         → Drag & drop")
                self.log_to_console("\n⌨️  Press 'Q' to quit")

                # Start controller (this will open a VNC window)
                result = controller.start(show_video=True)

                if result["success"]:
                    stats = result["stats"]
                    self.log_to_console("✅ Hand Gesture Controller stopped")
                    self.log_to_console(f"📊 Statistics:")
                    self.log_to_console(f"  Total gestures: {stats['total_gestures']}")
                    self.log_to_console(f"  Clicks: {stats['clicks']}")
                    self.log_to_console(f"  Scrolls: {stats['scrolls']}")
                    self.log_to_console(f"  Drags: {stats['drags']}")
                else:
                    error_msg = result.get("error", "Unknown error")
                    self.log_to_console(f"❌ Error: {error_msg}")
                    messagebox.showerror("Runtime Error", error_msg)

            except Exception as e:
                error_msg = f"Failed to launch hand gesture controller: {str(e)}"
                self.log_to_console(f"❌ {error_msg}")
                messagebox.showerror("Error", error_msg)

        # Run in separate thread to avoid blocking GUI
        thread = threading.Thread(target=run_controller, daemon=True)
        thread.start()

    def create_screenshot_feature(self, parent, color):
        """Create screenshot feature UI"""
        tk.Label(parent, text="📸 Screenshot Options", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        btn = tk.Button(parent, text="📷 Capture Full Screen", bg="#2e3350", fg="#e0e0e0",
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                        command=lambda: self.load_comprehensive_command("Take a screenshot"),
                        padx=20, pady=12)
        btn.pack(fill="x", pady=5)
        self.add_hover_effect(btn, "#313244", "#45475a")

        btn2 = tk.Button(parent, text="🖼️ Capture Window", bg="#2e3350", fg="#e0e0e0",
                         font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                         command=lambda: self.load_comprehensive_command("Take screenshot of active window"),
                         padx=20, pady=12)
        btn2.pack(fill="x", pady=5)
        self.add_hover_effect(btn2, "#313244", "#45475a")

    def create_lock_feature(self, parent, color):
        """Create lock PC feature UI"""
        tk.Label(parent, text="🔒 System Lock", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        tk.Label(parent, text="⚠️ This will lock your computer", bg="#181825", fg="#00d4aa",
                 font=("Segoe UI", 9)).pack(pady=5)

        btn = tk.Button(parent, text="🔒 Lock Computer Now", bg="#00d4aa", fg="#0f0f1e",
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                        command=lambda: self.load_comprehensive_command("Lock the computer"),
                        padx=20, pady=12)
        btn.pack(fill="x", pady=10)
        self.add_hover_effect(btn, "#f38ba8", "#f5c2e7")

    def create_taskmanager_feature(self, parent, color):
        """Create task manager feature UI"""
        tk.Label(parent, text="📊 Task Manager", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        btn = tk.Button(parent, text="📊 Open Task Manager", bg="#2e3350", fg="#e0e0e0",
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                        command=lambda: self.load_comprehensive_command("Open Task Manager"),
                        padx=20, pady=12)
        btn.pack(fill="x", pady=5)
        self.add_hover_effect(btn, "#313244", "#45475a")

    def create_chrome_feature(self, parent, color):
        """Create Chrome feature UI"""
        tk.Label(parent, text="🌍 Chrome Browser", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        btn = tk.Button(parent, text="🌍 Open Chrome", bg="#2e3350", fg="#e0e0e0",
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                        command=lambda: self.load_comprehensive_command("Open Chrome and go to Google"),
                        padx=20, pady=12)
        btn.pack(fill="x", pady=5)
        self.add_hover_effect(btn, "#313244", "#45475a")

    def create_google_feature(self, parent, color):
        """Create Google search feature UI"""
        tk.Label(parent, text="🔍 Google Search", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        search_entry = tk.Entry(parent, bg="#2e3350", fg="#e0e0e0", font=("Segoe UI", 10),
                                relief="flat", insertbackground="#f9e2af")
        search_entry.insert(0, "Python tutorials")
        search_entry.pack(fill="x", pady=5, ipady=8)

        btn = tk.Button(parent, text="🔍 Search Google", bg="#00ff88", fg="#0f0f1e",
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                        command=lambda: self.load_comprehensive_command(f"Search Google for {search_entry.get()}"),
                        padx=20, pady=12)
        btn.pack(fill="x", pady=10)
        self.add_hover_effect(btn, "#a6e3a1", "#94e2d5")

    def create_gmail_feature(self, parent, color):
        """Create Gmail feature UI"""
        tk.Label(parent, text="📧 Gmail", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        btn = tk.Button(parent, text="📧 Open Gmail", bg="#2e3350", fg="#e0e0e0",
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                        command=lambda: self.load_comprehensive_command("Open Gmail in browser"),
                        padx=20, pady=12)
        btn.pack(fill="x", pady=5)
        self.add_hover_effect(btn, "#313244", "#45475a")

    def create_whatsapp_feature(self, parent, color):
        """Create WhatsApp feature UI"""
        tk.Label(parent, text="💬 WhatsApp", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        btn = tk.Button(parent, text="💬 Open WhatsApp Web", bg="#2e3350", fg="#e0e0e0",
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                        command=lambda: self.load_comprehensive_command("Open WhatsApp Web"),
                        padx=20, pady=12)
        btn.pack(fill="x", pady=5)
        self.add_hover_effect(btn, "#313244", "#45475a")

    def create_vscode_feature(self, parent, color):
        """Create VS Code feature UI"""
        tk.Label(parent, text="📝 VS Code", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        btn = tk.Button(parent, text="📝 Launch VS Code", bg="#2e3350", fg="#e0e0e0",
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                        command=lambda: self.load_comprehensive_command("Launch VS Code"),
                        padx=20, pady=12)
        btn.pack(fill="x", pady=5)
        self.add_hover_effect(btn, "#313244", "#45475a")

    def create_explorer_feature(self, parent, color):
        """Create File Explorer feature UI"""
        tk.Label(parent, text="📂 File Explorer", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        btn = tk.Button(parent, text="📂 Open File Explorer", bg="#2e3350", fg="#e0e0e0",
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                        command=lambda: self.load_comprehensive_command("Open File Explorer"),
                        padx=20, pady=12)
        btn.pack(fill="x", pady=5)
        self.add_hover_effect(btn, "#313244", "#45475a")

    def create_notepad_feature(self, parent, color):
        """Create Notepad feature UI"""
        tk.Label(parent, text="🗒️ Notepad", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        btn = tk.Button(parent, text="🗒️ Open Notepad", bg="#2e3350", fg="#e0e0e0",
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                        command=lambda: self.load_comprehensive_command("Open Notepad"),
                        padx=20, pady=12)
        btn.pack(fill="x", pady=5)
        self.add_hover_effect(btn, "#313244", "#45475a")

    def create_spotify_feature(self, parent, color):
        """Create Spotify feature UI"""
        tk.Label(parent, text="🎵 Spotify", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        btn = tk.Button(parent, text="🎵 Launch Spotify", bg="#2e3350", fg="#e0e0e0",
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                        command=lambda: self.load_comprehensive_command("Launch Spotify"),
                        padx=20, pady=12)
        btn.pack(fill="x", pady=5)
        self.add_hover_effect(btn, "#313244", "#45475a")

    def create_youtube_feature(self, parent, color):
        """Create YouTube feature UI with improved video playing"""
        tk.Label(parent, text="🎬 YouTube", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        # Search and Play input
        input_frame = tk.Frame(parent, bg="#181825")
        input_frame.pack(fill="x", pady=5)

        self.youtube_search_entry = tk.Entry(input_frame, bg="#2e3350", fg="#e0e0e0",
                                             font=("Segoe UI", 10), relief="flat",
                                             insertbackground="#e0e0e0")
        self.youtube_search_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.youtube_search_entry.insert(0, "Enter video search...")
        self.youtube_search_entry.bind("<FocusIn>", lambda e: self.youtube_search_entry.delete(0,
                                                                                               tk.END) if self.youtube_search_entry.get() == "Enter video search..." else None)
        self.youtube_search_entry.bind("<Return>", lambda e: self.play_youtube_from_input())

        play_btn = tk.Button(input_frame, text="▶️", bg="#00d4aa", fg="#0f0f1e",
                             font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                             command=self.play_youtube_from_input,
                             padx=12, pady=8)
        play_btn.pack(side="right")
        self.add_hover_effect(play_btn, "#a6e3a1", "#f5c2e7")

        # Quick action buttons
        btn1 = tk.Button(parent, text="🎬 Open YouTube", bg="#2e3350", fg="#e0e0e0",
                         font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                         command=lambda: self.load_comprehensive_command("Open YouTube"),
                         padx=20, pady=12)
        btn1.pack(fill="x", pady=5)
        self.add_hover_effect(btn1, "#313244", "#45475a")

        btn2 = tk.Button(parent, text="🎵 Play Music", bg="#2e3350", fg="#e0e0e0",
                         font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                         command=lambda: self.play_youtube_video("music"),
                         padx=20, pady=12)
        btn2.pack(fill="x", pady=5)
        self.add_hover_effect(btn2, "#313244", "#45475a")

        btn3 = tk.Button(parent, text="📚 Python Tutorial", bg="#2e3350", fg="#e0e0e0",
                         font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                         command=lambda: self.play_youtube_video("python tutorial"),
                         padx=20, pady=12)
        btn3.pack(fill="x", pady=5)
        self.add_hover_effect(btn3, "#313244", "#45475a")

    def play_youtube_from_input(self):
        """Play YouTube video from search input"""
        query = self.youtube_search_entry.get().strip()
        if query and query != "Enter video search...":
            self.play_youtube_video(query)
            self.youtube_search_entry.delete(0, tk.END)
            self.youtube_search_entry.insert(0, "Enter video search...")

    def play_youtube_video(self, query):
        """Play YouTube video using improved Selenium method"""

        def execute():
            try:
                self.append_comprehensive_output(f"\n🎬 Playing YouTube video: {query}\n", "info")
                self.append_comprehensive_output("⏳ Starting browser and finding video...\n", "info")

                # Use the selenium YouTube automation
                if not hasattr(self, 'selenium_youtube') or self.selenium_youtube is None:
                    from modules.web.selenium_web_automator import SeleniumWebAutomator
                    self.selenium_youtube = SeleniumWebAutomator(headless=False)

                result = self.selenium_youtube.youtube_play_video(query)

                if result.get("success"):
                    self.append_comprehensive_output(f"✅ {result.get('message')}\n", "success")
                else:
                    self.append_comprehensive_output(f"❌ {result.get('error')}\n", "error")
                    # Try fallback method
                    self.append_comprehensive_output("⚠️ Trying fallback method...\n", "info")
                    self.load_comprehensive_command(f"play youtube video {query}")

            except Exception as e:
                self.append_comprehensive_output(f"❌ Error: {str(e)}\n", "error")
                self.append_comprehensive_output("⚠️ Using fallback method...\n", "info")
                self.load_comprehensive_command(f"play youtube video {query}")

        thread = threading.Thread(target=execute, daemon=True)
        thread.start()

    def create_volume_feature(self, parent, color):
        """Create Volume control feature UI"""
        tk.Label(parent, text="🔊 Volume Control", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        btn1 = tk.Button(parent, text="🔊 Volume Up", bg="#2e3350", fg="#e0e0e0",
                         font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                         command=lambda: self.load_comprehensive_command("Increase volume by 10%"),
                         padx=20, pady=12)
        btn1.pack(fill="x", pady=5)
        self.add_hover_effect(btn1, "#313244", "#45475a")

        btn2 = tk.Button(parent, text="🔉 Volume Down", bg="#2e3350", fg="#e0e0e0",
                         font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                         command=lambda: self.load_comprehensive_command("Decrease volume by 10%"),
                         padx=20, pady=12)
        btn2.pack(fill="x", pady=5)
        self.add_hover_effect(btn2, "#313244", "#45475a")

        btn3 = tk.Button(parent, text="🔇 Mute", bg="#00d4aa", fg="#0f0f1e",
                         font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                         command=lambda: self.load_comprehensive_command("Mute system volume"),
                         padx=20, pady=12)
        btn3.pack(fill="x", pady=5)
        self.add_hover_effect(btn3, "#f38ba8", "#f5c2e7")

    def append_comprehensive_output(self, text, tag=None):
        """Append text to the comprehensive output display"""
        self.comprehensive_output.config(state='normal')
        if tag:
            self.comprehensive_output.insert(tk.END, text, tag)
        else:
            self.comprehensive_output.insert(tk.END, text)
        self.comprehensive_output.see(tk.END)
        self.comprehensive_output.config(state='disabled')
        self.root.update_idletasks()

    def clear_comprehensive_output(self):
        """Clear the comprehensive output display"""
        self.comprehensive_output.config(state='normal')
        self.comprehensive_output.delete(1.0, tk.END)
        self.comprehensive_output.config(state='disabled')

        # Reset welcome message
        self.append_comprehensive_output("\n", "info")
        self.append_comprehensive_output("🎯 COMPREHENSIVE DESKTOP CONTROLLER\n", "highlight")
        self.append_comprehensive_output("\n", "info")
        self.append_comprehensive_output("\n✅ Output cleared. Ready for new command!\n\n", "success")

    def update_comprehensive_phase(self, phase_name, status="active"):
        """Update the visual indicator for current phase"""
        colors = {
            "active": "#f9e2af",
            "complete": "#a6e3a1",
            "inactive": "#6c7086"
        }

        if phase_name in self.phase_labels:
            color = colors.get(status, colors["inactive"])
            self.phase_labels[phase_name].config(fg=color)

    def execute_comprehensive_command(self):
        """Execute a comprehensive desktop control command"""
        command = self.comprehensive_input.get().strip()

        if not command:
            messagebox.showwarning("Empty Command", "Please enter a command first!")
            return

        if not self.comprehensive_controller:
            self.append_comprehensive_output("\n⚠️  Comprehensive Controller not available\n", "error")
            self.append_comprehensive_output("This feature requires local execution with display access.\n", "info")
            self.append_comprehensive_output("Download and run locally for full functionality.\n", "info")
            return

        # Clear previous output
        self.comprehensive_output.config(state='normal')
        self.comprehensive_output.delete(1.0, tk.END)
        self.comprehensive_output.config(state='disabled')

        # Update status
        self.comprehensive_status.config(text="⚙️ Processing...", fg="#f9e2af")

        # Run in thread
        thread = threading.Thread(target=self._execute_comprehensive_task, args=(command,), daemon=True)
        thread.start()

    def _execute_comprehensive_task(self, command):
        """Execute comprehensive task in background thread"""
        try:
            self.append_comprehensive_output("\n", "info")
            self.append_comprehensive_output("🎯 COMPREHENSIVE DESKTOP CONTROLLER\n", "highlight")
            self.append_comprehensive_output("\n", "info")
            self.append_comprehensive_output(f"Command: {command}\n\n", "info")

            # Phase 1: Understand
            self.append_comprehensive_output("\n", "info")
            self.append_comprehensive_output("🧠 PHASE 1: UNDERSTANDING PROMPT\n", "phase1")
            self.append_comprehensive_output("\n", "info")
            self.update_comprehensive_phase("UNDERSTAND", "active")

            understanding = self.comprehensive_controller.understand_prompt(command)

            self.append_comprehensive_output("\n✅ Prompt Analysis Complete:\n", "success")
            self.append_comprehensive_output(f"   🎯 Goal: {understanding.get('primary_goal', 'N/A')}\n", "info")
            self.append_comprehensive_output(f"   📊 Complexity: {understanding.get('complexity_level', 'N/A')}\n",
                                             "info")
            self.append_comprehensive_output(
                f"   ⏱️  Estimated Time: {understanding.get('estimated_duration', 'N/A')}s\n", "info")
            apps = understanding.get('required_applications', [])
            if apps:
                self.append_comprehensive_output(f"   🔧 Required Apps: {', '.join(apps)}\n", "info")

            self.update_comprehensive_phase("UNDERSTAND", "complete")

            # Phase 2: Break Down
            self.append_comprehensive_output("\n" + "━" * 60 + "\n", "info")
            self.append_comprehensive_output("📋 PHASE 2: BREAKING INTO STEPS\n", "phase2")
            self.append_comprehensive_output("━" * 60 + "\n", "info")
            self.update_comprehensive_phase("PLAN", "active")

            execution_plan = self.comprehensive_controller.break_into_steps(understanding)
            steps = execution_plan.get("execution_plan", {}).get("steps", [])

            self.append_comprehensive_output("\n✅ Execution Plan Created:\n", "success")
            self.append_comprehensive_output(f"   Total Steps: {len(steps)}\n", "info")
            self.append_comprehensive_output(
                f"   Estimated Time: {execution_plan.get('execution_plan', {}).get('estimated_time', 'N/A')}s\n\n",
                "info")

            self.append_comprehensive_output("📝 Step Breakdown:\n", "highlight")
            for step in steps:
                self.append_comprehensive_output(f"   {step['step_number']}. {step.get('description', 'N/A')}\n",
                                                 "info")
                self.append_comprehensive_output(f"      → Expected: {step.get('expected_outcome', 'N/A')}\n", "info")

            self.update_comprehensive_phase("PLAN", "complete")

            # Phase 3: Monitor & Execute
            self.append_comprehensive_output("\n" + "━" * 60 + "\n", "info")
            self.append_comprehensive_output("👁️  PHASE 3: EXECUTING WITH MONITORING\n", "phase3")
            self.append_comprehensive_output("━" * 60 + "\n", "info")
            self.update_comprehensive_phase("MONITOR", "active")

            if self.comprehensive_controller.gui.demo_mode:
                self.append_comprehensive_output("\n⚠️  DEMO MODE: Commands will be simulated\n", "error")
                self.append_comprehensive_output("Download and run locally for actual execution\n\n", "info")

            # Execute each step
            for i, step in enumerate(steps, 1):
                self.append_comprehensive_output(f"\nStep {i}/{len(steps)}: {step.get('description', 'N/A')}\n",
                                                 "highlight")

                if self.comprehensive_controller.gui.demo_mode:
                    self.append_comprehensive_output(f"   [DEMO] Would execute: {step.get('action_type', 'N/A')}\n",
                                                     "info")
                    import time
                    time.sleep(0.5)
                    self.append_comprehensive_output("   ✅ Demo step completed\n", "success")
                else:
                    # Real execution with monitoring
                    result = self.comprehensive_controller.monitor_screen_during_execution(step, i)
                    if result.get("success"):
                        self.append_comprehensive_output("   ✅ Step completed successfully\n", "success")
                    else:
                        self.append_comprehensive_output("   ⚠️  Step failed\n", "error")

            self.update_comprehensive_phase("MONITOR", "complete")

            # Summary
            self.append_comprehensive_output("\n" + "━" * 60 + "\n", "info")
            self.append_comprehensive_output("📊 EXECUTION SUMMARY\n", "highlight")
            self.append_comprehensive_output("━" * 60 + "\n", "info")
            self.append_comprehensive_output(f"\n✅ All phases completed!\n", "success")
            self.append_comprehensive_output(f"   Total Steps: {len(steps)}\n", "info")

            if self.comprehensive_controller.gui.demo_mode:
                self.append_comprehensive_output("\n💡 TIP: Download and run locally for full automation\n", "info")

            self.append_comprehensive_output("\n", "info")

            # Update status
            self.comprehensive_status.config(text="✅ Completed", fg="#00ff88")

        except Exception as e:
            self.append_comprehensive_output(f"\n❌ Error: {str(e)}\n", "error")
            self.comprehensive_status.config(text="❌ Error", fg="#00d4aa")

    def show_comprehensive_guide(self):
        """Show comprehensive controller guide"""
        guide_text = """
🎯 COMPREHENSIVE DESKTOP CONTROLLER GUIDE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HOW IT WORKS:

🧠 Phase 1: UNDERSTAND
   • Analyzes your prompt deeply
   • Identifies intent, complexity, requirements
   • Predicts obstacles and plans mitigation

📋 Phase 2: BREAK DOWN
   • Creates detailed step-by-step execution plan
   • Defines validation checkpoints
   • Plans error recovery strategies

👁️  Phase 3: MONITOR & EXECUTE
   • Takes screenshots before each step
   • Executes the action
   • Takes screenshots after each step
   • AI verifies expected vs actual outcome

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXAMPLE COMMANDS:

Simple:
  • "Take a screenshot"
  • "Open Chrome"

For full functionality, download and run locally!
"""
        messagebox.showinfo("Comprehensive Controller Guide", guide_text)

    # ==================== Virtual Language Model Methods ====================

    def vlm_append_output(self, text, tag=None):
        """Append text to VLM output display"""
        self.vlm_output.config(state='normal')
        if tag:
            self.vlm_output.insert(tk.END, text, tag)
        else:
            self.vlm_output.insert(tk.END, text)
        self.vlm_output.see(tk.END)
        self.vlm_output.config(state='disabled')
        self.root.update_idletasks()

    def vlm_clear_output(self):
        """Clear VLM output"""
        self.vlm_output.config(state='normal')
        self.vlm_output.delete(1.0, tk.END)
        self.vlm_output.config(state='disabled')

        self.vlm_append_output("\n", "info")
        self.vlm_append_output("🧠 Output cleared. Ready for new learning!\n", "success")
        self.vlm_append_output("\n", "info")

    def vlm_refresh_stats(self):
        """Refresh and display VLM statistics"""
        if not self.vlm:
            return

        stats = self.vlm.get_stats()

        self.vlm_stats_display.config(state='normal')
        self.vlm_stats_display.delete(1.0, tk.END)

        stats_text = (
            f"📊 Observations: {stats['observations']}\n"
            f"🎨 UI Patterns: {stats['ui_patterns']}\n"
            f"💻 Known Apps: {stats['known_applications']}\n"
            f"📋 Workflows: {stats['learned_workflows']}\n"
            f"✅ Success Rate: {stats['success_rate']:.1f}%"
        )

        self.vlm_stats_display.insert(1.0, stats_text.strip())
        self.vlm_stats_display.config(state='disabled')

        # Update knowledge display
        self.vlm_knowledge_display.config(state='normal')
        self.vlm_knowledge_display.delete(1.0, tk.END)
        self.vlm_knowledge_display.insert(1.0, stats['knowledge_summary'])
        self.vlm_knowledge_display.config(state='disabled')

    def vlm_observe(self):
        """Let VLM observe the current screen"""
        if not self.vlm:
            messagebox.showwarning("VLM Not Available", "Virtual Language Model not initialized")
            return

        self.vlm_status.config(text="👁️ Observing...", fg="#00d4aa")
        self.vlm_append_output("\n" + "━" * 60 + "\n", "info")
        self.vlm_append_output("👁️ OBSERVING SCREEN\n", "highlight")
        self.vlm_append_output("━" * 60 + "\n", "info")

        # Run in thread
        thread = threading.Thread(target=self._vlm_observe_thread, daemon=True)
        thread.start()

    def _vlm_observe_thread(self):
        """Observe in background thread"""
        try:
            result = self.vlm.observe_screen("user requested observation")

            if result.get("demo"):
                self.vlm_append_output("\n⚠️ DEMO MODE\n", "error")
                self.vlm_append_output("Screen observation requires display access.\n", "info")
                self.vlm_append_output("Download and run locally for full functionality.\n\n", "info")
            elif result.get("success"):
                analysis = result.get("analysis", {})

                self.vlm_append_output("\n✅ Observation Complete!\n\n", "success")
                self.vlm_append_output(f"📝 Description: {analysis.get('description', 'N/A')}\n", "info")
                self.vlm_append_output(f"🎨 UI Elements Found: {len(analysis.get('ui_elements', []))}\n", "info")

                apps = analysis.get('visible_applications', [])
                if apps:
                    self.vlm_append_output(f"💻 Applications: {', '.join(apps)}\n", "info")

                self.vlm_append_output(f"\n💡 Learning Insights:\n", "highlight")
                self.vlm_append_output(f"{analysis.get('learning_insights', 'N/A')}\n", "info")
            else:
                self.vlm_append_output("\n❌ Observation failed\n", "error")
                self.vlm_append_output(f"Error: {result.get('message', 'Unknown error')}\n", "info")

            self.vlm_append_output("━" * 60 + "\n", "info")
            self.vlm_refresh_stats()
            self.vlm_status.config(text="✅ Ready to Learn", fg="#00ff88")

        except Exception as e:
            self.vlm_append_output(f"\n❌ Error: {str(e)}\n", "error")
            self.vlm_status.config(text="❌ Error", fg="#00d4aa")

    def vlm_decide(self):
        """Let VLM decide an action"""
        if not self.vlm:
            messagebox.showwarning("VLM Not Available", "Virtual Language Model not initialized")
            return

        goal = self.vlm_goal_input.get().strip()

        if not goal:
            messagebox.showwarning("No Goal", "Please enter a goal first!")
            return

        self.vlm_status.config(text="🤔 Deciding...", fg="#f9e2af")
        self.vlm_append_output("\n" + "━" * 60 + "\n", "info")
        self.vlm_append_output("🤔 MAKING DECISION\n", "decision")
        self.vlm_append_output("━" * 60 + "\n", "info")
        self.vlm_append_output(f"Goal: {goal}\n\n", "info")

        # Run in thread
        thread = threading.Thread(target=self._vlm_decide_thread, args=(goal,), daemon=True)
        thread.start()

    def _vlm_decide_thread(self, goal):
        """Decide in background thread"""
        try:
            decision = self.vlm.decide_action(goal)

            self.vlm_append_output("✅ Decision Made!\n\n", "success")
            self.vlm_append_output(f"🎯 Action: {decision.get('action', 'N/A')}\n", "decision")
            self.vlm_append_output(f"📍 Target: {decision.get('target', 'N/A')}\n", "info")
            self.vlm_append_output(f"💭 Reasoning: {decision.get('reasoning', 'N/A')}\n", "info")
            self.vlm_append_output(f"📊 Confidence: {decision.get('confidence', 0):.2%}\n", "info")

            alternatives = decision.get('alternative_actions', [])
            if alternatives:
                self.vlm_append_output(f"\n🔄 Alternatives: {', '.join(alternatives)}\n", "info")

            self.vlm_append_output("\n💡 Click 'Execute' to perform this action!\n", "highlight")
            self.vlm_append_output("━" * 60 + "\n", "info")

            # Store decision for execution
            self.vlm_last_decision = decision

            self.vlm_status.config(text="✅ Decision Ready", fg="#00ff88")

        except Exception as e:
            self.vlm_append_output(f"\n❌ Error: {str(e)}\n", "error")
            self.vlm_status.config(text="❌ Error", fg="#00d4aa")

    def vlm_execute(self):
        """Execute the last decided action"""
        if not self.vlm:
            messagebox.showwarning("VLM Not Available", "Virtual Language Model not initialized")
            return

        goal = self.vlm_goal_input.get().strip()

        if not goal:
            messagebox.showwarning("No Goal", "Please enter a goal first!")
            return

        self.vlm_status.config(text="▶️ Executing...", fg="#00ff88")

        # Run in thread
        thread = threading.Thread(target=self._vlm_execute_thread, args=(goal,), daemon=True)
        thread.start()

    def _vlm_execute_thread(self, goal):
        """Execute in background thread"""
        try:
            self.vlm_append_output("\n" + "━" * 60 + "\n", "info")
            self.vlm_append_output("▶️ EXECUTING LEARNED ACTION\n", "success")
            self.vlm_append_output("━" * 60 + "\n", "info")

            # First decide the action
            self.vlm_append_output("🤔 Analyzing goal and deciding action...\n", "info")
            decision = self.vlm.decide_action(goal)

            self.vlm_append_output(f"✅ Decision: {decision.get('action', 'N/A')}\n", "decision")
            self.vlm_append_output(f"   Confidence: {decision.get('confidence', 0):.2%}\n\n", "info")

            # Execute the action
            self.vlm_append_output("⚙️ Executing action...\n", "info")
            result = self.vlm.execute_learned_action(decision)

            if result.get("demo"):
                self.vlm_append_output("\n⚠️ DEMO MODE\n", "error")
                self.vlm_append_output("Desktop control requires local execution.\n", "info")
                self.vlm_append_output(f"Simulated: {result.get('message', 'N/A')}\n", "info")
            elif result.get("success"):
                self.vlm_append_output("\n✅ Action Executed Successfully!\n", "success")
                self.vlm_append_output(f"Result: {result.get('message', 'N/A')}\n", "info")
            else:
                self.vlm_append_output("\n⚠️ Action Failed\n", "error")
                self.vlm_append_output(f"Error: {result.get('message', 'Unknown error')}\n", "info")

            self.vlm_append_output("━" * 60 + "\n", "info")

            self.vlm_refresh_stats()
            self.vlm_status.config(text="✅ Ready to Learn", fg="#00ff88")

        except Exception as e:
            self.vlm_append_output(f"\n❌ Error: {str(e)}\n", "error")
            self.vlm_status.config(text="❌ Error", fg="#00d4aa")

    def vlm_learn_session(self):
        """Run an autonomous learning session"""
        if not self.vlm:
            messagebox.showwarning("VLM Not Available", "Virtual Language Model not initialized")
            return

        # Ask for duration
        duration = simpledialog.askinteger(
            "Learning Session",
            "How many minutes should the AI explore and learn?",
            initialvalue=3,
            minvalue=1,
            maxvalue=30
        )

        if not duration:
            return

        if messagebox.askyesno(
                "Start Learning Session",
                f"The AI will autonomously explore and learn for {duration} minute(s).\n\n"
                "It will:\n"
                "• Observe the screen\n"
                "• Identify UI patterns\n"
                "• Learn workflows\n"
                "• Make test actions\n\n"
                "Continue?"
        ):
            self.vlm_status.config(text="🧠 Learning...", fg="#cba6f7")
            thread = threading.Thread(target=self._vlm_learn_session_thread, args=(duration,), daemon=True)
            thread.start()

    def _vlm_learn_session_thread(self, duration):
        """Run learning session in background"""
        try:
            self.vlm_append_output("\n", "info")
            self.vlm_append_output("🧠 AUTONOMOUS LEARNING SESSION STARTING\n", "highlight")
            self.vlm_append_output("\n", "info")
            self.vlm_append_output(f"Duration: {duration} minute(s)\n\n", "info")

            self.vlm.autonomous_learning_session(duration)

            self.vlm_append_output("\n✅ Learning session complete!\n", "success")
            self.vlm_append_output("\n", "info")

            self.vlm_refresh_stats()
            self.vlm_status.config(text="✅ Learning Complete", fg="#00ff88")

        except Exception as e:
            self.vlm_append_output(f"\n❌ Error: {str(e)}\n", "error")
            self.vlm_status.config(text="❌ Error", fg="#00d4aa")

    def vlm_query(self):
        """Query the learned knowledge"""
        if not self.vlm:
            messagebox.showwarning("VLM Not Available", "Virtual Language Model not initialized")
            return

        question = simpledialog.askstring(
            "Query Knowledge",
            "Ask the AI about what it has learned:"
        )

        if not question:
            return

        self.vlm_status.config(text="💭 Thinking...", fg="#89dceb")

        thread = threading.Thread(target=self._vlm_query_thread, args=(question,), daemon=True)
        thread.start()

    def _vlm_query_thread(self, question):
        """Query in background thread"""
        try:
            self.vlm_append_output("\n" + "━" * 60 + "\n", "info")
            self.vlm_append_output("💬 KNOWLEDGE QUERY\n", "highlight")
            self.vlm_append_output("━" * 60 + "\n", "info")
            self.vlm_append_output(f"Question: {question}\n\n", "info")

            answer = self.vlm.query_knowledge(question)

            self.vlm_append_output("🤖 Answer:\n", "success")
            self.vlm_append_output(f"{answer}\n", "info")
            self.vlm_append_output("━" * 60 + "\n", "info")

            self.vlm_status.config(text="✅ Ready to Learn", fg="#00ff88")

        except Exception as e:
            self.vlm_append_output(f"\n❌ Error: {str(e)}\n", "error")
            self.vlm_status.config(text="❌ Error", fg="#00d4aa")

    def show_vlm_help(self):
        """Show VLM help dialog"""
        help_text = (
            "VIRTUAL LANGUAGE MODEL - HOW IT WORKS\n\n"
            "WHAT IS IT?\n\n"
            "A self-learning AI that:\n"
            "  - Observes your screen with AI vision\n"
            "  - Learns UI patterns and workflows\n"
            "  - Builds a knowledge base over time\n"
            "  - Makes intelligent decisions\n"
            "  - Controls your desktop based on learned knowledge\n\n"
            "HOW TO USE:\n\n"
            "1. OBSERVE: Click 'Observe Screen' to let AI see your desktop\n"
            "2. DECIDE: Enter a goal and click 'Decide Action'\n"
            "3. EXECUTE: Click 'Execute' to perform the action\n"
            "4. LEARN: Click 'Learn Session' for autonomous learning\n"
            "5. QUERY: Click 'Query Knowledge' to ask what it learned\n\n"
            "EXAMPLE WORKFLOW:\n\n"
            "1. Click 'Observe Screen' - AI sees your desktop\n"
            "2. Enter goal: 'Search for Python tutorials'\n"
            "3. Click 'Decide Action' - AI plans the steps\n"
            "4. Click 'Execute' - AI performs the search\n"
            "5. AI learns from this experience!\n\n"
            "MEMORY:\n\n"
            "All learned knowledge is saved to vlm_memory.json\n"
            "The AI remembers between sessions!\n\n"
            "For full functionality, download and run locally!"
        )
        messagebox.showinfo("Virtual Language Model Help", help_text)

    def view_comprehensive_screenshots(self):
        """View generated screenshots"""
        import os
        screenshot_files = [f for f in os.listdir('.') if f.startswith('step_') and f.endswith('.png')]

        if not screenshot_files:
            messagebox.showinfo("Screenshots",
                                "No screenshots found.\n\nScreenshots are generated during execution.\nDownload and run locally for full monitoring.")
        else:
            msg = f"Found {len(screenshot_files)} screenshots:\n\n"
            for f in sorted(screenshot_files[:10]):
                msg += f"• {f}\n"
            if len(screenshot_files) > 10:
                msg += f"\n... and {len(screenshot_files) - 10} more"
            messagebox.showinfo("Screenshots", msg)

    def show_comprehensive_stats(self):
        """Show comprehensive controller statistics"""
        if not self.comprehensive_controller:
            messagebox.showinfo("Stats", "Controller not available")
            return

        stats_text = f"""
COMPREHENSIVE CONTROLLER STATS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Status: {'✅ Ready' if self.comprehensive_controller else '❌ Not Available'}

Features:
  • Deep Prompt Understanding
  • Intelligent Task Breakdown  
  • Real-Time Screen Monitoring
  • AI Vision Verification
  • Adaptive Error Recovery

Executions: {len(self.comprehensive_controller.execution_log) if self.comprehensive_controller else 0}
Screen States: {len(self.comprehensive_controller.screen_states) if self.comprehensive_controller else 0}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 For full desktop control with actual mouse,
keyboard, and screen access:
  1. Download this project
  2. Install: pip install -r requirements.txt
  3. Set API key: GEMINI_API_KEY=your_key
  4. Run: python gui_app.py
"""
        messagebox.showinfo("Comprehensive Controller Stats", stats_text)

    def create_macro_recorder_tab(self, notebook):
        """Macro Recorder Tab - Record and playback automation macros"""
        tab = tk.Frame(notebook, bg="#1a1d2e")
        notebook.add(tab, text="🎬 Macro Recorder")

        # Header
        header_frame = tk.Frame(tab, bg="#252941")
        header_frame.pack(fill="x", pady=(10, 0), padx=10)

        header = tk.Label(header_frame,
                          text="🎬 Macro Recorder & Playback",
                          bg="#252941",
                          fg="#f5c2e7",
                          font=("Segoe UI", 14, "bold"))
        header.pack(pady=12)

        info = tk.Label(header_frame,
                        text="🎯 Record • 💾 Save • ▶️ Playback • 🔄 Loop • 📱 Remote Control",
                        bg="#252941",
                        fg="#b0b0b0",
                        font=("Segoe UI", 9, "italic"))
        info.pack(pady=(0, 12))

        # Main container
        main_container = tk.Frame(tab, bg="#1a1d2e")
        main_container.pack(fill="both", expand=True, padx=10, pady=5)

        # Left column - Controls
        left_column = tk.Frame(main_container, bg="#1a1d2e")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Recording controls
        record_frame = tk.Frame(left_column, bg="#2e3350", relief="flat")
        record_frame.pack(fill="x", pady=5)

        record_label = tk.Label(record_frame,
                                text="📹 Recording Controls",
                                bg="#2e3350",
                                fg="#f5c2e7",
                                font=("Segoe UI", 11, "bold"))
        record_label.pack(pady=10)

        # Record status
        self.macro_record_status = tk.Label(record_frame,
                                            text="⚫ Ready to Record",
                                            bg="#2e3350",
                                            fg="#b0b0b0",
                                            font=("Segoe UI", 10))
        self.macro_record_status.pack(pady=5)

        # Record buttons
        record_btn_frame = tk.Frame(record_frame, bg="#2e3350")
        record_btn_frame.pack(pady=10)

        self.macro_start_record_btn = tk.Button(record_btn_frame,
                                                text="🔴 Start Recording",
                                                bg="#00d4aa",
                                                fg="#0f0f1e",
                                                font=("Segoe UI", 10, "bold"),
                                                relief="flat",
                                                cursor="hand2",
                                                command=self.start_macro_recording,
                                                padx=20,
                                                pady=10)
        self.macro_start_record_btn.pack(side="left", padx=5)
        self.add_hover_effect(self.macro_start_record_btn, "#f38ba8", "#eba0ac")

        self.macro_stop_record_btn = tk.Button(record_btn_frame,
                                               text="⏹️ Stop & Save",
                                               bg="#00d4aa",
                                               fg="#0f0f1e",
                                               font=("Segoe UI", 10, "bold"),
                                               relief="flat",
                                               cursor="hand2",
                                               command=self.stop_macro_recording,
                                               padx=20,
                                               pady=10,
                                               state="disabled")
        self.macro_stop_record_btn.pack(side="left", padx=5)
        self.add_hover_effect(self.macro_stop_record_btn, "#89b4fa", "#74c7ec")

        # Macro list
        list_frame = tk.Frame(left_column, bg="#2e3350", relief="flat")
        list_frame.pack(fill="both", expand=True, pady=10)

        list_label = tk.Label(list_frame,
                              text="💾 Saved Macros",
                              bg="#2e3350",
                              fg="#00ff88",
                              font=("Segoe UI", 11, "bold"))
        list_label.pack(pady=10)

        # Macro listbox
        macro_list_container = tk.Frame(list_frame, bg="#2e3350")
        macro_list_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        macro_scrollbar = tk.Scrollbar(macro_list_container)
        macro_scrollbar.pack(side="right", fill="y")

        self.macro_listbox = tk.Listbox(macro_list_container,
                                        bg="#16182a",
                                        fg="#e0e0e0",
                                        font=("Consolas", 10),
                                        relief="flat",
                                        selectbackground="#45475a",
                                        selectforeground="#f5c2e7",
                                        yscrollcommand=macro_scrollbar.set)
        self.macro_listbox.pack(side="left", fill="both", expand=True)
        macro_scrollbar.config(command=self.macro_listbox.yview)

        # Refresh button
        refresh_btn = tk.Button(list_frame,
                                text="🔄 Refresh List",
                                bg="#3d4466",
                                fg="#e0e0e0",
                                font=("Segoe UI", 9),
                                relief="flat",
                                cursor="hand2",
                                command=self.refresh_macro_list,
                                padx=15,
                                pady=8)
        refresh_btn.pack(pady=5)
        self.add_hover_effect(refresh_btn, "#45475a", "#585b70")

        # Right column - Playback & Output
        right_column = tk.Frame(main_container, bg="#1a1d2e")
        right_column.pack(side="right", fill="both", expand=True, padx=(5, 0))

        # Playback controls
        playback_frame = tk.Frame(right_column, bg="#2e3350", relief="flat")
        playback_frame.pack(fill="x", pady=5)

        playback_label = tk.Label(playback_frame,
                                  text="▶️ Playback Controls",
                                  bg="#2e3350",
                                  fg="#89dceb",
                                  font=("Segoe UI", 11, "bold"))
        playback_label.pack(pady=10)

        # Repeat and speed controls
        controls_container = tk.Frame(playback_frame, bg="#2e3350")
        controls_container.pack(fill="x", padx=10, pady=10)

        # Repeat count
        repeat_frame = tk.Frame(controls_container, bg="#2e3350")
        repeat_frame.pack(fill="x", pady=5)

        tk.Label(repeat_frame,
                 text="🔄 Repeat:",
                 bg="#2e3350",
                 fg="#b0b0b0",
                 font=("Segoe UI", 9)).pack(side="left", padx=5)

        self.macro_repeat_var = tk.StringVar(value="1")
        repeat_spinbox = tk.Spinbox(repeat_frame,
                                    from_=1,
                                    to=100,
                                    textvariable=self.macro_repeat_var,
                                    bg="#16182a",
                                    fg="#e0e0e0",
                                    font=("Segoe UI", 10),
                                    relief="flat",
                                    width=10)
        repeat_spinbox.pack(side="left", padx=5)

        # Speed control
        speed_frame = tk.Frame(controls_container, bg="#2e3350")
        speed_frame.pack(fill="x", pady=5)

        tk.Label(speed_frame,
                 text="⚡ Speed:",
                 bg="#2e3350",
                 fg="#b0b0b0",
                 font=("Segoe UI", 9)).pack(side="left", padx=5)

        self.macro_speed_var = tk.StringVar(value="1.0")
        speed_options = ["0.5x", "1.0x", "1.5x", "2.0x", "3.0x"]
        speed_combo = ttk.Combobox(speed_frame,
                                   values=speed_options,
                                   textvariable=self.macro_speed_var,
                                   state="readonly",
                                   font=("Segoe UI", 9),
                                   width=10)
        speed_combo.current(1)
        speed_combo.pack(side="left", padx=5)

        # Playback buttons
        playback_btns = tk.Frame(playback_frame, bg="#2e3350")
        playback_btns.pack(pady=15)

        play_btn = tk.Button(playback_btns,
                             text="▶️ Play Selected",
                             bg="#00ff88",
                             fg="#0f0f1e",
                             font=("Segoe UI", 10, "bold"),
                             relief="flat",
                             cursor="hand2",
                             command=self.play_macro,
                             padx=20,
                             pady=10)
        play_btn.pack(side="left", padx=5)
        self.add_hover_effect(play_btn, "#a6e3a1", "#94e2d5")

        stop_btn = tk.Button(playback_btns,
                             text="⏹️ Stop",
                             bg="#00d4aa",
                             fg="#0f0f1e",
                             font=("Segoe UI", 10, "bold"),
                             relief="flat",
                             cursor="hand2",
                             command=self.stop_macro_playback,
                             padx=20,
                             pady=10)
        stop_btn.pack(side="left", padx=5)
        self.add_hover_effect(stop_btn, "#f38ba8", "#eba0ac")

        delete_btn = tk.Button(playback_btns,
                               text="🗑️ Delete",
                               bg="#3d4466",
                               fg="#e0e0e0",
                               font=("Segoe UI", 10, "bold"),
                               relief="flat",
                               cursor="hand2",
                               command=self.delete_macro,
                               padx=20,
                               pady=10)
        delete_btn.pack(side="left", padx=5)
        self.add_hover_effect(delete_btn, "#45475a", "#585b70")

        # Output console
        output_label = tk.Label(right_column,
                                text="📋 Macro Output",
                                bg="#1a1d2e",
                                fg="#b0b0b0",
                                font=("Segoe UI", 10, "bold"))
        output_label.pack(anchor="w", padx=5, pady=(10, 5))

        self.macro_output = scrolledtext.ScrolledText(right_column,
                                                      bg="#16182a",
                                                      fg="#e0e0e0",
                                                      font=("Consolas", 9),
                                                      wrap=tk.WORD,
                                                      state='disabled',
                                                      relief="flat",
                                                      padx=10,
                                                      pady=10)
        self.macro_output.pack(fill="both", expand=True, padx=5, pady=5)

        self.macro_output.tag_config("success", foreground="#a6e3a1")
        self.macro_output.tag_config("error", foreground="#f38ba8")
        self.macro_output.tag_config("info", foreground="#89dceb")
        self.macro_output.tag_config("event", foreground="#f9e2af")

        # Initialize macro list
        self.refresh_macro_list()

    def create_mobile_operations_tab(self, notebook):
        """Mobile Operations Tab - Remote control interface"""
        tab = tk.Frame(notebook, bg="#1a1d2e")
        notebook.add(tab, text="📱 Mobile Control")

        # Header
        header_frame = tk.Frame(tab, bg="#252941")
        header_frame.pack(fill="x", pady=(10, 0), padx=10)

        header = tk.Label(header_frame,
                          text="📱 Mobile Companion Control",
                          bg="#252941",
                          fg="#89dceb",
                          font=("Segoe UI", 14, "bold"))
        header.pack(pady=12)

        info = tk.Label(header_frame,
                        text="📡 Remote Access • 🎮 Mobile Commands • 🔔 Notifications • 🎬 Remote Macros",
                        bg="#252941",
                        fg="#b0b0b0",
                        font=("Segoe UI", 9, "italic"))
        info.pack(pady=(0, 12))

        # Main container
        main_container = tk.Frame(tab, bg="#1a1d2e")
        main_container.pack(fill="both", expand=True, padx=10, pady=5)

        # Left column - Server info and status
        left_column = tk.Frame(main_container, bg="#1a1d2e")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Server status
        status_frame = tk.Frame(left_column, bg="#2e3350", relief="flat")
        status_frame.pack(fill="x", pady=5)

        status_label = tk.Label(status_frame,
                                text="📡 Server Status",
                                bg="#2e3350",
                                fg="#89dceb",
                                font=("Segoe UI", 11, "bold"))
        status_label.pack(pady=10)

        self.mobile_status = tk.Label(status_frame,
                                      text="✅ Server Running",
                                      bg="#2e3350",
                                      fg="#00ff88",
                                      font=("Segoe UI", 10))
        self.mobile_status.pack(pady=5)

        # Server info
        info_text = tk.Text(status_frame,
                            bg="#16182a",
                            fg="#e0e0e0",
                            font=("Consolas", 9),
                            height=8,
                            relief="flat",
                            padx=10,
                            pady=10,
                            state='disabled',
                            wrap=tk.WORD)
        info_text.pack(fill="x", padx=10, pady=10)

        # Get domain info
        domain = os.environ.get('REPLIT_DEV_DOMAIN', 'localhost:5000')

        info_text.config(state='normal')
        info_text.insert("1.0",
                         f"📱 Mobile Interface:\n"
                         f"https://{domain}/mobile\n\n"
                         f"💻 Desktop Dashboard:\n"
                         f"https://{domain}/\n\n"
                         f"🔐 Default PIN: 1234\n"
                         f"📡 WebSocket: Connected\n"
                         f"🔔 Notifications: Enabled")
        info_text.config(state='disabled')

        # Quick actions
        actions_frame = tk.Frame(left_column, bg="#2e3350", relief="flat")
        actions_frame.pack(fill="both", expand=True, pady=10)

        actions_label = tk.Label(actions_frame,
                                 text="⚡ Quick Actions",
                                 bg="#2e3350",
                                 fg="#f9e2af",
                                 font=("Segoe UI", 11, "bold"))
        actions_label.pack(pady=10)

        actions = [
            ("📱 Open Mobile Interface", lambda: self.open_mobile_interface()),
            ("💻 Open Desktop Dashboard", lambda: self.open_desktop_dashboard()),
            ("🎬 Trigger Remote Macro", lambda: self.trigger_remote_macro()),
            ("📊 View Connected Clients", lambda: self.view_mobile_clients()),
            ("🔔 Send Test Notification", lambda: self.send_test_notification()),
        ]

        for text, command in actions:
            btn = tk.Button(actions_frame,
                            text=text,
                            bg="#3d4466",
                            fg="#e0e0e0",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10)
            btn.pack(fill="x", padx=10, pady=3)
            self.add_hover_effect(btn, "#45475a", "#585b70")

        # Right column - Mobile command history
        right_column = tk.Frame(main_container, bg="#1a1d2e")
        right_column.pack(side="right", fill="both", expand=True, padx=(5, 0))

        # Command history
        history_label = tk.Label(right_column,
                                 text="📜 Mobile Command History",
                                 bg="#1a1d2e",
                                 fg="#b0b0b0",
                                 font=("Segoe UI", 10, "bold"))
        history_label.pack(anchor="w", padx=5, pady=5)

        self.mobile_history = scrolledtext.ScrolledText(right_column,
                                                        bg="#16182a",
                                                        fg="#e0e0e0",
                                                        font=("Consolas", 9),
                                                        wrap=tk.WORD,
                                                        state='disabled',
                                                        relief="flat",
                                                        padx=10,
                                                        pady=10)
        self.mobile_history.pack(fill="both", expand=True, padx=5, pady=5)

        self.mobile_history.tag_config("timestamp", foreground="#6c7086")
        self.mobile_history.tag_config("command", foreground="#89dceb")
        self.mobile_history.tag_config("success", foreground="#a6e3a1")
        self.mobile_history.tag_config("error", foreground="#f38ba8")

        # Add initial message
        self.mobile_append_history("📱 Mobile Companion Server is running", "success")
        self.mobile_append_history(f"🌐 Access from your phone: https://{domain}/mobile", "info")

    # Macro Recorder Methods
    def start_macro_recording(self):
        """Start recording a macro"""
        if not self.macro_recorder:
            messagebox.showerror("Error", "Macro Recorder not initialized")
            return

        name = simpledialog.askstring("Macro Name", "Enter a name for this macro:")
        if not name:
            return

        self.current_macro_name = name
        self.macro_append_output(f"🔴 Starting macro recording: {name}\n", "info")

        def on_event(event):
            event_type = event.get('type', 'unknown')
            self.macro_append_output(f"  • {event_type}\n", "event")

        result = self.macro_recorder.start_recording(callback=on_event)
        self.macro_append_output(f"{result}\n", "success")

        self.macro_record_status.config(text="🔴 Recording...", fg="#00d4aa")
        self.macro_start_record_btn.config(state="disabled")
        self.macro_stop_record_btn.config(state="normal")
        self.recording_active = True

    def stop_macro_recording(self):
        """Stop recording and save macro"""
        if not self.macro_recorder or not self.recording_active:
            return

        result = self.macro_recorder.stop_recording(name=self.current_macro_name)
        self.macro_append_output(f"{result}\n", "success")

        self.macro_record_status.config(text="⚫ Ready to Record", fg="#b0b0b0")
        self.macro_start_record_btn.config(state="normal")
        self.macro_stop_record_btn.config(state="disabled")
        self.recording_active = False

        self.refresh_macro_list()

    def refresh_macro_list(self):
        """Refresh the list of saved macros"""
        if not self.macro_recorder:
            return

        self.macro_listbox.delete(0, tk.END)
        macros = self.macro_recorder.list_macros()

        for macro in macros:
            display_text = f"{macro['name']} ({macro['event_count']} events, {macro['duration']:.1f}s)"
            self.macro_listbox.insert(tk.END, display_text)

        if macros:
            self.macro_append_output(f"📋 Loaded {len(macros)} macro(s)\n", "info")

    def play_macro(self):
        """Play the selected macro"""
        if not self.macro_recorder:
            messagebox.showerror("Error", "Macro Recorder not initialized")
            return

        selection = self.macro_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a macro to play")
            return

        index = selection[0]
        macros = self.macro_recorder.list_macros()
        macro = macros[index]

        repeat = int(self.macro_repeat_var.get())
        speed_str = self.macro_speed_var.get().replace('x', '')
        speed = float(speed_str)

        self.macro_append_output(f"▶️ Playing macro: {macro['name']}\n", "info")
        self.macro_append_output(f"   Repeat: {repeat}x, Speed: {speed}x\n", "info")

        def on_complete(message):
            self.macro_append_output(f"{message}\n", "success")

        result = self.macro_recorder.play_macro(macro_name=macro['name'],
                                                repeat=repeat,
                                                speed=speed,
                                                callback=on_complete)
        self.macro_append_output(f"{result}\n", "success")

    def stop_macro_playback(self):
        """Stop macro playback"""
        if not self.macro_recorder:
            return

        result = self.macro_recorder.stop_playback()
        self.macro_append_output(f"{result}\n", "info")

    def delete_macro(self):
        """Delete the selected macro"""
        if not self.macro_recorder:
            return

        selection = self.macro_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a macro to delete")
            return

        index = selection[0]
        macros = self.macro_recorder.list_macros()
        macro = macros[index]

        if messagebox.askyesno("Confirm Delete", f"Delete macro '{macro['name']}'?"):
            result = self.macro_recorder.delete_macro(macro['name'])
            self.macro_append_output(f"{result}\n", "info")
            self.refresh_macro_list()

    def macro_append_output(self, text, tag=None):
        """Append text to macro output console"""
        if hasattr(self, 'macro_output'):
            self.macro_output.config(state='normal')
            self.macro_output.insert(tk.END, text, tag)
            self.macro_output.see(tk.END)
            self.macro_output.config(state='disabled')

    # Mobile Operations Methods
    def open_mobile_interface(self):
        """Open mobile interface in browser"""
        domain = os.environ.get('REPLIT_DEV_DOMAIN', 'localhost:5000')
        url = f"https://{domain}/mobile"
        self.mobile_append_history(f"🌐 Opening: {url}", "info")
        messagebox.showinfo("Mobile Interface",
                            f"Mobile interface URL:\n\n{url}\n\nOpen this URL on your mobile device.")

    def open_desktop_dashboard(self):
        """Open desktop dashboard"""
        domain = os.environ.get('REPLIT_DEV_DOMAIN', 'localhost:5000')
        url = f"https://{domain}/"
        self.mobile_append_history(f"💻 Opening: {url}", "info")
        messagebox.showinfo("Desktop Dashboard", f"Desktop dashboard URL:\n\n{url}")

    def trigger_remote_macro(self):
        """Trigger a macro from mobile interface"""
        if not self.macro_recorder:
            messagebox.showerror("Error", "Macro Recorder not initialized")
            return

        macros = self.macro_recorder.list_macros()
        if not macros:
            messagebox.showinfo("No Macros",
                                "No saved macros available.\n\nRecord a macro first in the Macro Recorder tab.")
            return

        macro_names = [m['name'] for m in macros]

        # Simple selection dialog
        selection = simpledialog.askstring("Remote Macro",
                                           f"Available macros:\n{', '.join(macro_names)}\n\nEnter macro name:")

        if selection and selection in macro_names:
            self.mobile_append_history(f"🎬 Triggered remote macro: {selection}", "command")
            self.mobile_append_history("   (Mobile trigger simulation)", "info")
            messagebox.showinfo("Success",
                                f"Macro '{selection}' triggered!\n\nIn the full version, this would execute from your mobile device.")
        elif selection:
            self.mobile_append_history(f"❌ Macro not found: {selection}", "error")

    def view_mobile_clients(self):
        """View connected mobile clients"""
        self.mobile_append_history("📊 Viewing connected clients...", "info")
        messagebox.showinfo("Connected Clients",
                            "Mobile Companion Server Status:\n\n"
                            "✅ Server Running\n"
                            "📡 WebSocket Enabled\n"
                            "🔔 Notifications Active\n\n"
                            "Connect your mobile device to:\n"
                            f"https://{os.environ.get('REPLIT_DEV_DOMAIN', 'localhost:5000')}/mobile")

    def send_test_notification(self):
        """Send a test notification"""
        self.mobile_append_history("🔔 Sending test notification...", "command")
        messagebox.showinfo("Test Notification", "Test notification sent!\n\nCheck your mobile device if connected.")
        self.mobile_append_history("✅ Test notification sent", "success")

    def mobile_append_history(self, text, tag=None):
        """Append text to mobile history console"""
        if hasattr(self, 'mobile_history'):
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.mobile_history.config(state='normal')
            self.mobile_history.insert(tk.END, f"[{timestamp}] ", "timestamp")
            self.mobile_history.insert(tk.END, f"{text}\n", tag)
            self.mobile_history.see(tk.END)
            self.mobile_history.config(state='disabled')

    def workflow_log(self, message, level="INFO"):
        """Log callback for workflow builder"""
        level_colors = {
            "INFO": "#89b4fa",
            "SUCCESS": "#a6e3a1",
            "ERROR": "#f38ba8",
            "WARNING": "#f9e2af"
        }
        if hasattr(self, 'workflow_output_text'):
            self.workflow_output_text.config(state='normal')
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.workflow_output_text.insert(tk.END, f"[{timestamp}] ", ("timestamp",))
            self.workflow_output_text.insert(tk.END, f"{message}\n", (level.lower(),))
            self.workflow_output_text.see(tk.END)
            self.workflow_output_text.config(state='disabled')

    def show_workflow_builder(self):
        """Open Natural Language Workflow Builder window"""
        if not self.nl_workflow_builder:
            messagebox.showerror("Error", "Workflow Builder not initialized")
            return

        builder_window = tk.Toplevel(self.root)
        builder_window.title("💬 Natural Language Workflow Builder")
        builder_window.geometry("1000x700")
        builder_window.configure(bg="#16182a")

        header_frame = tk.Frame(builder_window, bg="#252941")
        header_frame.pack(fill="x", padx=20, pady=15)

        header = tk.Label(header_frame,
                          text="💬 Natural Language Workflow Builder",
                          bg="#252941",
                          fg="#00d4aa",
                          font=("Segoe UI", 16, "bold"))
        header.pack(pady=10)

        info = tk.Label(header_frame,
                        text="🎯 Describe workflows in plain English • 🤖 AI converts to automation • 💬 Test & refine • 💾 Save as templates",
                        bg="#252941",
                        fg="#b0b0b0",
                        font=("Segoe UI", 9, "italic"))
        info.pack(pady=(0, 10))

        main_container = tk.Frame(builder_window, bg="#16182a")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)

        left_column = tk.Frame(main_container, bg="#16182a")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))

        examples_frame = tk.Frame(left_column, bg="#2e3350")
        examples_frame.pack(fill="x", pady=(0, 10))

        examples_label = tk.Label(examples_frame,
                                  text="💡 Example Workflows",
                                  bg="#2e3350",
                                  fg="#f9e2af",
                                  font=("Segoe UI", 10, "bold"))
        examples_label.pack(pady=10)

        examples_list = tk.Listbox(examples_frame,
                                   bg="#16182a",
                                   fg="#e0e0e0",
                                   font=("Segoe UI", 9),
                                   height=6,
                                   selectmode=tk.SINGLE,
                                   relief="flat")
        examples_list.pack(fill="x", padx=10, pady=(0, 10))

        examples = self.nl_workflow_builder.get_examples()
        for example in examples:
            examples_list.insert(tk.END, example['name'])

        def use_example():
            selection = examples_list.curselection()
            if selection:
                example = examples[selection[0]]
                input_text.delete("1.0", tk.END)
                input_text.insert("1.0", example['description'])

        use_example_btn = tk.Button(examples_frame,
                                    text="📋 Use Selected Example",
                                    bg="#00d4aa",
                                    fg="#0f0f1e",
                                    font=("Segoe UI", 9, "bold"),
                                    relief="flat",
                                    cursor="hand2",
                                    command=use_example,
                                    pady=8)
        use_example_btn.pack(fill="x", padx=10, pady=(0, 10))

        input_label = tk.Label(left_column,
                               text="💬 Describe Your Workflow:",
                               bg="#16182a",
                               fg="#00ff88",
                               font=("Segoe UI", 11, "bold"))
        input_label.pack(anchor="w", pady=(10, 5))

        input_text = tk.Text(left_column,
                             bg="#2e3350",
                             fg="#e0e0e0",
                             font=("Segoe UI", 11),
                             height=8,
                             wrap=tk.WORD,
                             relief="flat",
                             padx=10,
                             pady=10)
        input_text.pack(fill="both", expand=True, pady=(0, 10))

        button_frame = tk.Frame(left_column, bg="#16182a")
        button_frame.pack(fill="x", pady=10)

        def process_workflow():
            description = input_text.get("1.0", tk.END).strip()
            if not description:
                messagebox.showwarning("Empty Input", "Please describe your workflow")
                return

            self.workflow_log(f"Processing: {description}", "INFO")
            result = self.nl_workflow_builder.describe_workflow(description)

            if result.get("success"):
                if result.get("type") == "workflow":
                    workflow = result["workflow"]
                    output_text.delete("1.0", tk.END)
                    output_text.insert("1.0", f"Workflow: {workflow.get('workflow_name', 'Unnamed')}\n\n")
                    output_text.insert(tk.END, f"Description: {workflow.get('description', '')}\n\n")
                    output_text.insert(tk.END, "Steps:\n")
                    for i, step in enumerate(workflow.get("steps", []), 1):
                        output_text.insert(tk.END, f"{i}. {step.get('action')} - {step.get('parameters')}\n")

                    if workflow.get("suggestions"):
                        output_text.insert(tk.END, f"\n💡 Suggestions: {workflow['suggestions']}\n")

                    self.workflow_log(f"Generated workflow: {workflow.get('workflow_name')}", "SUCCESS")
                else:
                    self.workflow_log(result.get("message", "AI response received"), "INFO")
                    messagebox.showinfo("AI Response", result.get("message", ""))
            else:
                error = result.get("error", "Unknown error")
                self.workflow_log(f"Error: {error}", "ERROR")
                messagebox.showerror("Error", error)

        def save_current_workflow():
            current_draft = self.nl_workflow_builder.get_current_draft()
            if not current_draft:
                messagebox.showwarning("No Workflow", "Create a workflow first")
                return

            result = self.nl_workflow_builder.save_workflow()
            if result.get("success"):
                self.workflow_log(f"Saved workflow: {result.get('name')}", "SUCCESS")
                messagebox.showinfo("Success", result.get("message"))
                refresh_saved_list()
            else:
                self.workflow_log(f"Save failed: {result.get('error')}", "ERROR")
                messagebox.showerror("Error", result.get("error"))

        def clear_conversation():
            self.nl_workflow_builder.clear_conversation()
            self.nl_workflow_builder.clear_draft()
            input_text.delete("1.0", tk.END)
            output_text.delete("1.0", tk.END)
            self.workflow_log("Conversation cleared", "INFO")

        process_btn = tk.Button(button_frame,
                                text="🤖 Build Workflow",
                                bg="#00ff88",
                                fg="#0f0f1e",
                                font=("Segoe UI", 10, "bold"),
                                relief="flat",
                                cursor="hand2",
                                command=process_workflow,
                                padx=20,
                                pady=10)
        process_btn.pack(side="left", padx=5)

        save_btn = tk.Button(button_frame,
                             text="💾 Save Workflow",
                             bg="#00d4aa",
                             fg="#0f0f1e",
                             font=("Segoe UI", 10, "bold"),
                             relief="flat",
                             cursor="hand2",
                             command=save_current_workflow,
                             padx=20,
                             pady=10)
        save_btn.pack(side="left", padx=5)

        clear_btn = tk.Button(button_frame,
                              text="🗑️ Clear",
                              bg="#00d4aa",
                              fg="#0f0f1e",
                              font=("Segoe UI", 10, "bold"),
                              relief="flat",
                              cursor="hand2",
                              command=clear_conversation,
                              padx=20,
                              pady=10)
        clear_btn.pack(side="left", padx=5)

        right_column = tk.Frame(main_container, bg="#16182a")
        right_column.pack(side="right", fill="both", expand=True)

        output_label = tk.Label(right_column,
                                text="📋 Generated Workflow:",
                                bg="#16182a",
                                fg="#cba6f7",
                                font=("Segoe UI", 11, "bold"))
        output_label.pack(anchor="w", pady=(0, 5))

        output_text = tk.Text(right_column,
                              bg="#2e3350",
                              fg="#e0e0e0",
                              font=("Consolas", 10),
                              wrap=tk.WORD,
                              relief="flat",
                              padx=10,
                              pady=10)
        output_text.pack(fill="both", expand=True, pady=(0, 10))

        saved_frame = tk.Frame(right_column, bg="#2e3350")
        saved_frame.pack(fill="x", pady=(10, 0))

        saved_label = tk.Label(saved_frame,
                               text="💾 Saved Workflows",
                               bg="#2e3350",
                               fg="#f9e2af",
                               font=("Segoe UI", 10, "bold"))
        saved_label.pack(pady=10)

        saved_list = tk.Listbox(saved_frame,
                                bg="#16182a",
                                fg="#e0e0e0",
                                font=("Segoe UI", 9),
                                height=8,
                                selectmode=tk.SINGLE,
                                relief="flat")
        saved_list.pack(fill="x", padx=10, pady=(0, 10))

        def refresh_saved_list():
            saved_list.delete(0, tk.END)
            workflows = self.nl_workflow_builder.list_templates()
            for wf in workflows:
                saved_list.insert(tk.END, f"{wf['name']} ({wf['steps_count']} steps)")

        def run_saved_workflow():
            selection = saved_list.curselection()
            if not selection:
                return

            workflows = self.nl_workflow_builder.list_templates()
            workflow = workflows[selection[0]]
            command = f"run workflow: {workflow['name']}"
            self.workflow_log(f"Executing workflow: {workflow['name']}", "INFO")
            self.command_input.delete(0, tk.END)
            self.command_input.insert(0, command)
            self.execute_command()

        refresh_btn = tk.Button(saved_frame,
                                text="🔄 Refresh List",
                                bg="#3d4466",
                                fg="#e0e0e0",
                                font=("Segoe UI", 9),
                                relief="flat",
                                cursor="hand2",
                                command=refresh_saved_list,
                                pady=6)
        refresh_btn.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=(0, 10))

        run_btn = tk.Button(saved_frame,
                            text="▶️ Run Selected",
                            bg="#00ff88",
                            fg="#0f0f1e",
                            font=("Segoe UI", 9, "bold"),
                            relief="flat",
                            cursor="hand2",
                            command=run_saved_workflow,
                            pady=6)
        run_btn.pack(side="right", fill="x", expand=True, padx=(5, 10), pady=(0, 10))

        log_frame = tk.Frame(builder_window, bg="#252941")
        log_frame.pack(fill="x", padx=20, pady=(0, 15))

        log_label = tk.Label(log_frame,
                             text="📊 Activity Log",
                             bg="#252941",
                             fg="#f9e2af",
                             font=("Segoe UI", 9, "bold"))
        log_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.workflow_output_text = tk.Text(log_frame,
                                            bg="#16182a",
                                            fg="#e0e0e0",
                                            font=("Consolas", 9),
                                            height=6,
                                            state='disabled',
                                            relief="flat",
                                            padx=10,
                                            pady=10)
        self.workflow_output_text.pack(fill="x", padx=10, pady=(0, 10))

        self.workflow_output_text.tag_config("timestamp", foreground="#6c7086")
        self.workflow_output_text.tag_config("info", foreground="#89b4fa")
        self.workflow_output_text.tag_config("success", foreground="#a6e3a1")
        self.workflow_output_text.tag_config("error", foreground="#f38ba8")
        self.workflow_output_text.tag_config("warning", foreground="#f9e2af")

        refresh_saved_list()
        self.workflow_log("Workflow Builder ready!", "SUCCESS")

    # Phone Link & Contact Management Methods

    def make_phone_call(self):
        """Make a phone call using Phone Link"""
        name = self.phone_name_input.get().strip()
        number = self.phone_number_input.get().strip()

        if not name and not number:
            messagebox.showwarning("Input Required", "Please enter a contact name or phone number")
            return

        try:
            if name:
                # Call by name
                result = self.phone_dialer.call_contact(name)
            else:
                # Call by number
                result = self.phone_dialer.dial_with_phone_link(number)

            # Show result
            if result['success']:
                message = result['message']
                self.phone_history_text.insert("1.0", f"✅ {message}\n")
                self.phone_name_input.delete(0, tk.END)
                self.phone_number_input.delete(0, tk.END)
                messagebox.showinfo("Call Initiated", message)
            else:
                message = result['message']
                self.phone_history_text.insert("1.0", f"❌ {message}\n")
                messagebox.showerror("Call Failed", message)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to make call: {str(e)}")

    def refresh_contacts(self):
        """Refresh the contacts list"""
        self.contacts_listbox.delete(0, tk.END)

        try:
            contacts = self.contact_manager.list_contacts()
            for contact in sorted(contacts, key=lambda x: x['name']):
                display = f"{contact['name']}: {contact.get('phone', 'No phone')}"
                self.contacts_listbox.insert(tk.END, display)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load contacts: {str(e)}")

    def search_contacts(self):
        """Search and filter contacts"""
        query = self.contact_search_input.get().strip()
        self.contacts_listbox.delete(0, tk.END)

        try:
            if query:
                contacts = self.contact_manager.search_contacts(query)
            else:
                contacts = self.contact_manager.list_contacts()

            for contact in sorted(contacts, key=lambda x: x['name']):
                display = f"{contact['name']}: {contact.get('phone', 'No phone')}"
                self.contacts_listbox.insert(tk.END, display)
        except Exception as e:
            pass

    def call_selected_contact(self, event):
        """Call the selected contact (double-click handler)"""
        selection = self.contacts_listbox.curselection()
        if not selection:
            return

        selected_text = self.contacts_listbox.get(selection[0])
        contact_name = selected_text.split(':')[0].strip()

        try:
            result = self.phone_dialer.call_contact(contact_name)

            if result['success']:
                message = result['message']
                self.phone_history_text.insert("1.0", f"✅ {message}\n")
                messagebox.showinfo("Call Initiated", message)
            else:
                message = result['message']
                self.phone_history_text.insert("1.0", f"❌ {message}\n")
                messagebox.showerror("Call Failed", message)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to call contact: {str(e)}")

    def add_contact(self):
        """Add a new contact"""
        from tkinter import simpledialog

        name = simpledialog.askstring("Add Contact", "Enter contact name:")
        if not name:
            return

        phone = simpledialog.askstring("Add Contact", "Enter phone number\n(with country code, e.g., +1234567890):")
        if not phone:
            return

        email = simpledialog.askstring("Add Contact", "Enter email (optional):", initialvalue="")

        try:
            if self.contact_manager.add_contact(name, phone, email or None):
                messagebox.showinfo("Success", f"Contact '{name}' added successfully!")
                self.refresh_contacts()
            else:
                messagebox.showerror("Error", "Failed to add contact")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add contact: {str(e)}")

    def edit_contact(self):
        """Edit the selected contact"""
        from tkinter import simpledialog

        selection = self.contacts_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a contact to edit")
            return

        selected_text = self.contacts_listbox.get(selection[0])
        contact_name = selected_text.split(':')[0].strip()

        contact = self.contact_manager.get_contact(contact_name)
        if not contact:
            messagebox.showerror("Error", "Contact not found")
            return

        phone = simpledialog.askstring("Edit Contact",
                                       f"Enter new phone number for '{contact['name']}':",
                                       initialvalue=contact.get('phone', ''))
        if phone is None:
            return

        email = simpledialog.askstring("Edit Contact",
                                       f"Enter new email for '{contact['name']}':",
                                       initialvalue=contact.get('email', ''))

        try:
            if self.contact_manager.update_contact(contact_name, phone=phone or None, email=email or None):
                messagebox.showinfo("Success", f"Contact '{contact['name']}' updated!")
                self.refresh_contacts()
            else:
                messagebox.showerror("Error", "Failed to update contact")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update contact: {str(e)}")

    def delete_contact(self):
        """Delete the selected contact"""
        selection = self.contacts_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a contact to delete")
            return

        selected_text = self.contacts_listbox.get(selection[0])
        contact_name = selected_text.split(':')[0].strip()

        if not messagebox.askyesno("Confirm Delete", f"Delete contact '{contact_name}'?"):
            return

        try:
            if self.contact_manager.delete_contact(contact_name):
                messagebox.showinfo("Success", f"Contact '{contact_name}' deleted!")
                self.refresh_contacts()
            else:
                messagebox.showerror("Error", "Failed to delete contact")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete contact: {str(e)}")

    def run(self):
        """Start the GUI"""
        self.root.mainloop()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ModernBOIGUI(root)
    app.run()


if __name__ == "__main__":
    main()
