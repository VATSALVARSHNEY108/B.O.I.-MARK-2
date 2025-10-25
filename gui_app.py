#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import os
from dotenv import load_dotenv
from gemini_controller import parse_command, get_ai_suggestion
from command_executor import CommandExecutor
from datetime import datetime

load_dotenv()

class AutomationControllerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 AI Desktop Automation Controller")
        self.root.geometry("1400x900")
        self.root.configure(bg="#0f0f1e")
        
        self.executor = CommandExecutor()
        self.processing = False
        self.hover_colors = {}
        
        self.setup_ui()
        self.check_api_key()
        self.start_time_update()
    
    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("Header.TLabel", 
                       background="#0f0f1e", 
                       foreground="#ffffff",
                       font=("Segoe UI", 24, "bold"))
        style.configure("Info.TLabel", 
                       background="#0f0f1e", 
                       foreground="#a6adc8",
                       font=("Segoe UI", 11))
        style.configure("Category.TLabel",
                       background="#1e1e2e",
                       foreground="#f9e2af",
                       font=("Segoe UI", 11, "bold"))
        style.configure("TNotebook", background="#1e1e2e", borderwidth=0)
        style.configure("TNotebook.Tab", 
                       background="#313244",
                       foreground="#cdd6f4",
                       padding=[15, 8],
                       font=("Segoe UI", 9, "bold"))
        style.map("TNotebook.Tab",
                 background=[("selected", "#45475a")],
                 foreground=[("selected", "#ffffff")])
        
        header_frame = tk.Frame(self.root, bg="#0f0f1e", pady=20)
        header_frame.pack(fill="x")
        
        header_container = tk.Frame(header_frame, bg="#1a1a2e", relief="flat")
        header_container.pack(fill="x", padx=30)
        
        self.add_gradient_effect(header_container)
        
        title_frame = tk.Frame(header_container, bg="#1a1a2e")
        title_frame.pack(pady=15)
        
        title = tk.Label(title_frame, 
                         text="🤖 AI Desktop Automation Controller",
                         bg="#1a1a2e",
                         fg="#ffffff",
                         font=("Segoe UI", 26, "bold"))
        title.pack()
        
        subtitle = tk.Label(title_frame,
                            text="⚡ Powered by Gemini AI • Complete Desktop Automation Suite",
                            bg="#1a1a2e",
                            fg="#89b4fa",
                            font=("Segoe UI", 11))
        subtitle.pack(pady=(5, 0))
        
        stats_frame = tk.Frame(header_container, bg="#1a1a2e")
        stats_frame.pack(pady=(10, 15))
        
        self.time_label = tk.Label(stats_frame,
                                   text="",
                                   bg="#1a1a2e",
                                   fg="#a6e3a1",
                                   font=("Segoe UI", 10))
        self.time_label.pack(side="left", padx=15)
        
        separator1 = tk.Label(stats_frame, text="•", bg="#1a1a2e", fg="#45475a", font=("Segoe UI", 10))
        separator1.pack(side="left", padx=5)
        
        features_label = tk.Label(stats_frame,
                                 text="80+ AI Features Available",
                                 bg="#1a1a2e",
                                 fg="#f9e2af",
                                 font=("Segoe UI", 10))
        features_label.pack(side="left", padx=15)
        
        separator2 = tk.Label(stats_frame, text="•", bg="#1a1a2e", fg="#45475a", font=("Segoe UI", 10))
        separator2.pack(side="left", padx=5)
        
        ready_label = tk.Label(stats_frame,
                              text="✓ System Ready",
                              bg="#1a1a2e",
                              fg="#a6e3a1",
                              font=("Segoe UI", 10))
        ready_label.pack(side="left", padx=15)
        
        main_container = tk.Frame(self.root, bg="#0f0f1e")
        main_container.pack(fill="both", expand=True, padx=30, pady=10)
        
        left_panel = tk.Frame(main_container, bg="#0f0f1e", width=450)
        left_panel.pack(side="left", fill="both", expand=False, padx=(0, 15))
        left_panel.pack_propagate(False)
        
        left_header = tk.Frame(left_panel, bg="#1a1a2e", relief="flat")
        left_header.pack(fill="x", pady=(0, 10))
        
        categories_label = tk.Label(left_header,
                                   text="🎯 Quick Actions Center",
                                   bg="#1a1a2e",
                                   fg="#ffffff",
                                   font=("Segoe UI", 14, "bold"),
                                   pady=12)
        categories_label.pack()
        
        notebook_container = tk.Frame(left_panel, bg="#1a1a2e", relief="flat")
        notebook_container.pack(fill="both", expand=True)
        
        notebook = ttk.Notebook(notebook_container)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.create_code_tab(notebook)
        self.create_desktop_tab(notebook)
        self.create_messaging_tab(notebook)
        self.create_system_tab(notebook)
        self.create_productivity_tab(notebook)
        self.create_utilities_tab(notebook)
        self.create_ecosystem_tab(notebook)
        self.create_ai_features_tab(notebook)
        self.create_fun_tab(notebook)
        self.create_web_tools_tab(notebook)
        
        right_panel = tk.Frame(main_container, bg="#0f0f1e")
        right_panel.pack(side="right", fill="both", expand=True)
        
        command_card = tk.Frame(right_panel, bg="#1a1a2e", relief="flat")
        command_card.pack(fill="x", pady=(0, 15))
        
        input_frame = tk.Frame(command_card, bg="#1a1a2e")
        input_frame.pack(fill="x", padx=20, pady=15)
        
        input_label = tk.Label(input_frame,
                              text="💬 Command Input",
                              bg="#1a1a2e",
                              fg="#ffffff",
                              font=("Segoe UI", 12, "bold"))
        input_label.pack(anchor="w", pady=(0, 10))
        
        input_container = tk.Frame(input_frame, bg="#1a1a2e")
        input_container.pack(fill="x")
        
        self.command_input = tk.Entry(input_container,
                                     bg="#2a2a3e",
                                     fg="#ffffff",
                                     font=("Segoe UI", 13),
                                     insertbackground="#89b4fa",
                                     relief="flat",
                                     bd=0)
        self.command_input.pack(side="left", fill="both", expand=True, ipady=12, padx=(0, 10))
        self.command_input.bind("<Return>", lambda e: self.execute_command())
        
        self.execute_btn = tk.Button(input_container,
                                    text="▶ Execute",
                                    bg="#89b4fa",
                                    fg="#0f0f1e",
                                    font=("Segoe UI", 12, "bold"),
                                    relief="flat",
                                    cursor="hand2",
                                    command=self.execute_command,
                                    padx=25,
                                    pady=12,
                                    activebackground="#74c7ec")
        self.execute_btn.pack(side="right")
        self.add_hover_effect(self.execute_btn, "#89b4fa", "#74c7ec")
        
        output_card = tk.Frame(right_panel, bg="#1a1a2e", relief="flat")
        output_card.pack(fill="both", expand=True)
        
        output_header = tk.Frame(output_card, bg="#1a1a2e")
        output_header.pack(fill="x", padx=20, pady=(15, 10))
        
        output_label = tk.Label(output_header,
                               text="📋 Output Console",
                               bg="#1a1a2e",
                               fg="#ffffff",
                               font=("Segoe UI", 12, "bold"))
        output_label.pack(side="left")
        
        clear_console_btn = tk.Button(output_header,
                                     text="🗑️ Clear",
                                     bg="#45475a",
                                     fg="#ffffff",
                                     font=("Segoe UI", 9),
                                     relief="flat",
                                     cursor="hand2",
                                     command=self.clear_output,
                                     padx=15,
                                     pady=5,
                                     activebackground="#585b70")
        clear_console_btn.pack(side="right")
        self.add_hover_effect(clear_console_btn, "#45475a", "#585b70")
        
        self.output_area = scrolledtext.ScrolledText(output_card,
                                                     bg="#2a2a3e",
                                                     fg="#ffffff",
                                                     font=("Consolas", 11),
                                                     relief="flat",
                                                     bd=0,
                                                     padx=15,
                                                     pady=15,
                                                     wrap="word",
                                                     insertbackground="#89b4fa")
        self.output_area.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        self.output_area.config(state="disabled")
        
        bottom_frame = tk.Frame(self.root, bg="#1a1a2e", pady=15, padx=30)
        bottom_frame.pack(fill="x", side="bottom")
        
        button_config = {
            "bg": "#313244",
            "fg": "#ffffff",
            "font": ("Segoe UI", 10),
            "relief": "flat",
            "cursor": "hand2",
            "padx": 20,
            "pady": 10,
            "activebackground": "#45475a"
        }
        
        help_btn = tk.Button(bottom_frame, text="❓ Full Help", command=self.show_help, **button_config)
        help_btn.pack(side="left", padx=5)
        self.add_hover_effect(help_btn, "#313244", "#45475a")
        
        contacts_btn = tk.Button(bottom_frame, text="👥 Contacts", command=self.show_contacts, **button_config)
        contacts_btn.pack(side="left", padx=5)
        self.add_hover_effect(contacts_btn, "#313244", "#45475a")
        
        about_btn = tk.Button(bottom_frame, text="ℹ️ About", command=self.show_about, **button_config)
        about_btn.pack(side="left", padx=5)
        self.add_hover_effect(about_btn, "#313244", "#45475a")
        
        status_container = tk.Frame(bottom_frame, bg="#313244", relief="flat")
        status_container.pack(side="right", padx=10, pady=0)
        
        self.status_label = tk.Label(status_container,
                                    text="✅ Ready",
                                    bg="#313244",
                                    fg="#a6e3a1",
                                    font=("Segoe UI", 10, "bold"),
                                    padx=20,
                                    pady=10)
        self.status_label.pack()
    
    def add_gradient_effect(self, widget):
        widget.configure(highlightbackground="#45475a", highlightthickness=1)
    
    def add_hover_effect(self, button, normal_color, hover_color):
        def on_enter(e):
            button['background'] = hover_color
        
        def on_leave(e):
            button['background'] = normal_color
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def start_time_update(self):
        def update_time():
            current_time = datetime.now().strftime("%A, %B %d, %Y • %I:%M:%S %p")
            self.time_label.config(text=current_time)
            self.root.after(1000, update_time)
        
        update_time()
    
    def create_code_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="💻 Code")
        
        canvas = tk.Canvas(tab, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")
        
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
                          bg="#313244",
                          fg="#ffffff",
                          font=("Segoe UI", 10),
                          relief="flat",
                          cursor="hand2",
                          command=lambda c=command: self.quick_command(c),
                          anchor="w",
                          padx=15,
                          pady=10,
                          activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")
    
    def create_desktop_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="🖥️ Desktop")
        
        canvas = tk.Canvas(tab, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
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
                          bg="#313244",
                          fg="#ffffff",
                          font=("Segoe UI", 10),
                          relief="flat",
                          cursor="hand2",
                          command=lambda c=command: self.quick_command(c),
                          anchor="w",
                          padx=15,
                          pady=10,
                          activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")
    
    def create_messaging_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="📱 Messaging")
        
        canvas = tk.Canvas(tab, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")
        
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
                          bg="#313244",
                          fg="#ffffff",
                          font=("Segoe UI", 10),
                          relief="flat",
                          cursor="hand2",
                          command=lambda c=command: self.quick_command(c),
                          anchor="w",
                          padx=15,
                          pady=10,
                          activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")
    
    def create_system_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="⚙️ System")
        
        canvas = tk.Canvas(tab, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
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
            ("🔒 Lock Computer", "Lock the computer"),
            ("🔊 Volume Control", "Set volume to 50"),
        ]
        
        for text, command in actions:
            btn = tk.Button(scrollable_frame,
                          text=text,
                          bg="#313244",
                          fg="#ffffff",
                          font=("Segoe UI", 10),
                          relief="flat",
                          cursor="hand2",
                          command=lambda c=command: self.quick_command(c),
                          anchor="w",
                          padx=15,
                          pady=10,
                          activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")
    
    def create_productivity_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="📈 Productivity")
        
        canvas = tk.Canvas(tab, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")
        
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
                          bg="#313244",
                          fg="#ffffff",
                          font=("Segoe UI", 10),
                          relief="flat",
                          cursor="hand2",
                          command=lambda c=command: self.quick_command(c),
                          anchor="w",
                          padx=15,
                          pady=10,
                          activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")
    
    def create_utilities_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="🔧 Utilities")
        
        canvas = tk.Canvas(tab, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")
        
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
                          bg="#313244",
                          fg="#ffffff",
                          font=("Segoe UI", 10),
                          relief="flat",
                          cursor="hand2",
                          command=lambda c=command: self.quick_command(c),
                          anchor="w",
                          padx=15,
                          pady=10,
                          activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")
    
    def create_ecosystem_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="🌐 Ecosystem")
        
        canvas = tk.Canvas(tab, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")
        
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
                          bg="#313244",
                          fg="#ffffff",
                          font=("Segoe UI", 10),
                          relief="flat",
                          cursor="hand2",
                          command=lambda c=command: self.quick_command(c),
                          anchor="w",
                          padx=15,
                          pady=10,
                          activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")
    
    def create_ai_features_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="🤖 AI Features")
        
        canvas = tk.Canvas(tab, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")
        
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
                         bg="#1e1e2e",
                         fg="#89b4fa",
                         font=("Segoe UI", 12, "bold"))
        header.pack(pady=12)
        
        info = tk.Label(scrollable_frame,
                       text="80+ AI-powered features available",
                       bg="#1e1e2e",
                       fg="#a6adc8",
                       font=("Segoe UI", 9))
        info.pack(pady=(0, 15))
        
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
                              bg="#313244",
                              fg="#ffffff",
                              font=("Segoe UI", 10),
                              relief="flat",
                              cursor="hand2",
                              command=lambda c=command: self.quick_command(c),
                              anchor="w",
                              padx=15,
                              pady=10,
                              activebackground="#45475a")
                btn.pack(fill="x", padx=8, pady=3)
                self.add_hover_effect(btn, "#313244", "#45475a")
    
    def create_fun_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="🎉 Fun")
        
        canvas = tk.Canvas(tab, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")
        
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
                          bg="#313244",
                          fg="#ffffff",
                          font=("Segoe UI", 10),
                          relief="flat",
                          cursor="hand2",
                          command=lambda c=command: self.quick_command(c),
                          anchor="w",
                          padx=15,
                          pady=10,
                          activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")
    
    def create_web_tools_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="🌐 Web")
        
        canvas = tk.Canvas(tab, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")
        
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
                          bg="#313244",
                          fg="#ffffff",
                          font=("Segoe UI", 10),
                          relief="flat",
                          cursor="hand2",
                          command=lambda c=command: self.quick_command(c),
                          anchor="w",
                          padx=15,
                          pady=10,
                          activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")
    
    def select_command_text(self):
        """Select all text in command input for easy editing"""
        self.command_input.select_range(0, tk.END)
        self.command_input.icursor(tk.END)
    
    def check_api_key(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            self.update_output("⚠️ WARNING: GOOGLE_API_KEY not found in environment variables.\n", "warning")
            self.update_output("Please set your Gemini API key to use AI features.\n\n", "info")
            self.update_status("⚠️ API Key Missing", "#f9e2af")
        else:
            self.update_output("✅ Gemini AI is ready!\n", "success")
            self.update_output("Type a command or click a Quick Action button to get started.\n\n", "info")
    
    def quick_command(self, command):
        self.command_input.delete(0, tk.END)
        self.command_input.insert(0, command)
        self.execute_command()
    
    def execute_command(self):
        if self.processing:
            messagebox.showwarning("Busy", "Please wait for the current command to finish.")
            return
        
        command = self.command_input.get().strip()
        if not command:
            messagebox.showwarning("Empty Command", "Please enter a command.")
            return
        
        self.processing = True
        self.update_status("⚙️ Processing...", "#f9e2af")
        self.execute_btn.config(state="disabled")
        
        thread = threading.Thread(target=self._execute_in_thread, args=(command,))
        thread.start()
    
    def _execute_in_thread(self, command):
        try:
            self.update_output(f"\n{'='*60}\n", "info")
            self.update_output(f"📝 Command: {command}\n", "command")
            self.update_output(f"{'='*60}\n\n", "info")
            
            command_dict = parse_command(command)
            
            if command_dict.get("action") == "error":
                error_msg = command_dict.get('description', 'Error processing command')
                self.update_output(f"❌ {error_msg}\n", "error")
                suggestion = get_ai_suggestion(f"User tried: {command}, but got error. Suggest alternatives.")
                self.update_output(f"\n💡 Suggestion: {suggestion}\n", "info")
                self.update_status("❌ Error", "#f38ba8")
                return
            
            result = self.executor.execute(command_dict)
            
            if result["success"]:
                self.update_output(f"✅ Result:\n{result['message']}\n", "success")
                self.update_status("✅ Ready", "#a6e3a1")
            else:
                self.update_output(f"❌ Error:\n{result['message']}\n", "error")
                self.update_status("❌ Error", "#f38ba8")
            
        except Exception as e:
            self.update_output(f"❌ Error: {str(e)}\n", "error")
            self.update_status("❌ Error", "#f38ba8")
        
        finally:
            self.processing = False
            self.root.after(0, lambda: self.execute_btn.config(state="normal"))
            self.root.after(0, self.select_command_text)
    
    def update_output(self, message, msg_type="info"):
        def _update():
            self.output_area.config(state="normal")
            
            colors = {
                "info": "#a6adc8",
                "success": "#a6e3a1",
                "error": "#f38ba8",
                "warning": "#f9e2af",
                "command": "#89b4fa"
            }
            
            tag_name = msg_type
            if tag_name not in self.output_area.tag_names():
                self.output_area.tag_configure(tag_name, foreground=colors.get(msg_type, "#ffffff"))
            
            self.output_area.insert(tk.END, message, tag_name)
            self.output_area.see(tk.END)
            self.output_area.config(state="disabled")
        
        self.root.after(0, _update)
    
    def update_status(self, text, color):
        def _update():
            self.status_label.config(text=text, fg=color)
        
        self.root.after(0, _update)
    
    def clear_output(self):
        self.output_area.config(state="normal")
        self.output_area.delete(1.0, tk.END)
        self.output_area.config(state="disabled")
        self.update_output("✨ Console cleared!\n\n", "success")
    
    def show_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("❓ Help Guide")
        help_window.geometry("900x700")
        help_window.configure(bg="#1a1a2e")
        
        header = tk.Label(help_window,
                         text="🤖 AI Desktop Automation Controller - Help Guide",
                         bg="#1a1a2e",
                         fg="#ffffff",
                         font=("Segoe UI", 16, "bold"),
                         pady=20)
        header.pack()
        
        text_area = scrolledtext.ScrolledText(help_window,
                                             bg="#2a2a3e",
                                             fg="#ffffff",
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

• Gemini API key (set GOOGLE_API_KEY environment variable)
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
                             bg="#89b4fa",
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
        contacts_window.configure(bg="#1a1a2e")
        
        header = tk.Label(contacts_window,
                         text="👥 Contact Manager",
                         bg="#1a1a2e",
                         fg="#ffffff",
                         font=("Segoe UI", 16, "bold"),
                         pady=20)
        header.pack()
        
        info = tk.Label(contacts_window,
                       text="Manage your contacts for email and messaging automation",
                       bg="#1a1a2e",
                       fg="#a6adc8",
                       font=("Segoe UI", 10))
        info.pack()
        
        text_area = scrolledtext.ScrolledText(contacts_window,
                                             bg="#2a2a3e",
                                             fg="#ffffff",
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
            text_area.insert(1.0, f"No contacts found or error loading contacts.\n\nUse the command:\n'Add contact NAME with phone NUMBER and email EMAIL'\n\nError details: {str(e)}")
        
        text_area.config(state="disabled")
        
        close_btn = tk.Button(contacts_window,
                             text="Close",
                             bg="#89b4fa",
                             fg="#0f0f1e",
                             font=("Segoe UI", 11, "bold"),
                             relief="flat",
                             cursor="hand2",
                             command=contacts_window.destroy,
                             padx=30,
                             pady=10)
        close_btn.pack(pady=(0, 20))
    
    def show_about(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("ℹ️ About")
        about_window.geometry("700x500")
        about_window.configure(bg="#1a1a2e")
        
        header = tk.Label(about_window,
                         text="🤖 AI Desktop Automation Controller",
                         bg="#1a1a2e",
                         fg="#ffffff",
                         font=("Segoe UI", 18, "bold"),
                         pady=20)
        header.pack()
        
        version = tk.Label(about_window,
                          text="Version 2.0.0 - Enhanced Edition",
                          bg="#1a1a2e",
                          fg="#89b4fa",
                          font=("Segoe UI", 11))
        version.pack()
        
        description_frame = tk.Frame(about_window, bg="#2a2a3e")
        description_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        description = tk.Label(description_frame,
                              text="""
⚡ Powered by Google Gemini AI

A comprehensive desktop automation suite featuring:

✓ 80+ AI-powered features
✓ Natural language command processing
✓ Desktop automation & control
✓ Code generation assistance
✓ Email & messaging automation
✓ System management tools
✓ Productivity tracking
✓ Smart scheduling & workflows
✓ And much more!

Created with modern design principles
and user experience in mind.

© 2025 AI Automation Suite
                              """,
                              bg="#2a2a3e",
                              fg="#ffffff",
                              font=("Segoe UI", 11),
                              justify="center")
        description.pack(expand=True)
        
        close_btn = tk.Button(about_window,
                             text="Close",
                             bg="#89b4fa",
                             fg="#0f0f1e",
                             font=("Segoe UI", 11, "bold"),
                             relief="flat",
                             cursor="hand2",
                             command=about_window.destroy,
                             padx=30,
                             pady=10)
        close_btn.pack(pady=(0, 20))

def main():
    root = tk.Tk()
    app = AutomationControllerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
