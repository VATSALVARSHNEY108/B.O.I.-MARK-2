#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import os
from dotenv import load_dotenv
from gemini_controller import parse_command, get_ai_suggestion
from command_executor import CommandExecutor
from vatsal_assistant import create_vatsal_assistant
from advanced_smart_screen_monitor import create_advanced_smart_screen_monitor
from ai_screen_monitoring_system import create_ai_screen_monitoring_system
from simple_chatbot import SimpleChatbot
from datetime import datetime

load_dotenv()

class AutomationControllerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 VATSAL - AI Desktop Automation Controller")
        self.root.geometry("1400x900")
        self.root.configure(bg="#0f0f1e")
        
        self.executor = CommandExecutor()
        self.vatsal = create_vatsal_assistant()
        self.advanced_monitor = create_advanced_smart_screen_monitor()
        self.ai_monitor = create_ai_screen_monitoring_system()
        
        try:
            self.simple_chatbot = SimpleChatbot()
        except Exception as e:
            self.simple_chatbot = None
            print(f"Simple chatbot initialization failed: {e}")
        
        self.vatsal_mode = True
        self.processing = False
        self.hover_colors = {}
        self.vatsal_conversation_active = False
        self.active_chatbot = "simple"
        
        self.setup_ui()
        self.check_api_key()
        self.start_time_update()
        self.show_vatsal_greeting()
    
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
                         text="🤖 VATSAL - AI Desktop Automation Controller",
                         bg="#1a1a2e",
                         fg="#ffffff",
                         font=("Segoe UI", 26, "bold"))
        title.pack()
        
        subtitle = tk.Label(title_frame,
                            text="⚡ Virtual Assistant To Serve And Learn • Powered by Gemini AI",
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
        
        self.vatsal_toggle_btn = tk.Button(stats_frame,
                                                  text="🤖 VATSAL Mode: ON",
                                                  bg="#89b4fa",
                                                  fg="#0f0f1e",
                                                  font=("Segoe UI", 9, "bold"),
                                                  relief="flat",
                                                  cursor="hand2",
                                                  command=self.toggle_vatsal_mode,
                                                  padx=15,
                                                  pady=5)
        self.vatsal_toggle_btn.pack(side="left", padx=15)
        self.add_hover_effect(self.vatsal_toggle_btn, "#89b4fa", "#74c7ec")
        
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
        
        self.create_vatsal_ai_tab(notebook)
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
        
        suggest_btn = tk.Button(bottom_frame, text="💡 Suggestion", command=self.show_suggestion, **button_config)
        suggest_btn.pack(side="left", padx=5)
        self.add_hover_effect(suggest_btn, "#313244", "#45475a")
        
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
    
    def create_vatsal_ai_tab(self, notebook):
        """VATSAL AI - Advanced Conversational Assistant with Multiple Chatbot Options"""
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="💬 VATSAL Chat")
        
        header_frame = tk.Frame(tab, bg="#1a1a2e")
        header_frame.pack(fill="x", pady=(10, 0), padx=10)
        
        header = tk.Label(header_frame,
                         text="💬 VATSAL - AI Chatbot Suite",
                         bg="#1a1a2e",
                         fg="#89b4fa",
                         font=("Segoe UI", 14, "bold"))
        header.pack(pady=12)
        
        selector_frame = tk.Frame(header_frame, bg="#1a1a2e")
        selector_frame.pack(pady=(0, 12))
        
        tk.Label(selector_frame,
                text="Choose Chatbot:",
                bg="#1a1a2e",
                fg="#a6adc8",
                font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 10))
        
        chatbot_options = [
            ("🚀 Simple Chat", "simple", "Easy & straightforward"),
            ("🤖 VATSAL Assistant", "assistant", "Sophisticated personality")
        ]
        
        for label, mode, desc in chatbot_options:
            btn = tk.Button(selector_frame,
                          text=f"{label}\n{desc}",
                          bg="#313244" if self.active_chatbot != mode else "#89b4fa",
                          fg="#ffffff" if self.active_chatbot != mode else "#0f0f1e",
                          font=("Segoe UI", 8, "bold"),
                          relief="flat",
                          cursor="hand2",
                          command=lambda m=mode: self.switch_chatbot(m),
                          padx=12,
                          pady=6)
            btn.pack(side="left", padx=3)
            setattr(self, f"chatbot_btn_{mode}", btn)
        
        self.chatbot_info_label = tk.Label(header_frame,
                       text=self.get_chatbot_description("simple"),
                       bg="#1a1a2e",
                       fg="#a6adc8",
                       font=("Segoe UI", 9, "italic"))
        self.chatbot_info_label.pack(pady=(0, 12))
        
        self.vatsal_conversation_display = scrolledtext.ScrolledText(
            tab,
            bg="#0f0f1e",
            fg="#cdd6f4",
            font=("Consolas", 10),
            wrap=tk.WORD,
            height=15,
            state='disabled',
            relief="flat",
            padx=10,
            pady=10
        )
        self.vatsal_conversation_display.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.vatsal_conversation_display.tag_config("vatsal", foreground="#89b4fa", font=("Consolas", 10, "bold"))
        self.vatsal_conversation_display.tag_config("user", foreground="#a6e3a1", font=("Consolas", 10, "bold"))
        self.vatsal_conversation_display.tag_config("timestamp", foreground="#6c7086", font=("Consolas", 8))
        
        input_frame = tk.Frame(tab, bg="#1a1a2e")
        input_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.vatsal_input = tk.Entry(input_frame,
                                     bg="#313244",
                                     fg="#ffffff",
                                     font=("Segoe UI", 11),
                                     relief="flat",
                                     insertbackground="#89b4fa")
        self.vatsal_input.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10, ipady=8)
        self.vatsal_input.bind("<Return>", lambda e: self.send_to_vatsal_ai())
        
        send_btn = tk.Button(input_frame,
                            text="Send",
                            bg="#89b4fa",
                            fg="#0f0f1e",
                            font=("Segoe UI", 10, "bold"),
                            relief="flat",
                            cursor="hand2",
                            command=self.send_to_vatsal_ai,
                            padx=20,
                            pady=8)
        send_btn.pack(side="right", padx=(5, 10))
        self.add_hover_effect(send_btn, "#89b4fa", "#74c7ec")
        
        button_frame = tk.Frame(tab, bg="#1e1e2e")
        button_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        start_btn = tk.Button(button_frame,
                             text="▶️ Start Conversation",
                             bg="#313244",
                             fg="#ffffff",
                             font=("Segoe UI", 9, "bold"),
                             relief="flat",
                             cursor="hand2",
                             command=self.start_vatsal_ai_conversation,
                             padx=15,
                             pady=8)
        start_btn.pack(side="left", padx=5)
        self.add_hover_effect(start_btn, "#313244", "#45475a")
        
        suggest_btn = tk.Button(button_frame,
                               text="💡 Help Me Start",
                               bg="#313244",
                               fg="#ffffff",
                               font=("Segoe UI", 9, "bold"),
                               relief="flat",
                               cursor="hand2",
                               command=self.vatsal_ai_get_suggestion,
                               padx=15,
                               pady=8)
        suggest_btn.pack(side="left", padx=5)
        self.add_hover_effect(suggest_btn, "#313244", "#45475a")
        
        clear_btn = tk.Button(button_frame,
                             text="🗑️ Clear Chat",
                             bg="#313244",
                             fg="#ffffff",
                             font=("Segoe UI", 9, "bold"),
                             relief="flat",
                             cursor="hand2",
                             command=self.clear_vatsal_ai_conversation,
                             padx=15,
                             pady=8)
        clear_btn.pack(side="left", padx=5)
        self.add_hover_effect(clear_btn, "#313244", "#45475a")
        
        stats_btn = tk.Button(button_frame,
                             text="📊 View Stats",
                             bg="#313244",
                             fg="#ffffff",
                             font=("Segoe UI", 9, "bold"),
                             relief="flat",
                             cursor="hand2",
                             command=self.show_vatsal_ai_stats,
                             padx=15,
                             pady=8)
        stats_btn.pack(side="left", padx=5)
        self.add_hover_effect(stats_btn, "#313244", "#45475a")
    
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
        
        screen_monitor_section = tk.Label(scrollable_frame,
                                          text="👁️ AI SCREEN MONITORING SYSTEM (Next-Gen)",
                                          bg="#1e1e2e",
                                          fg="#f9e2af",
                                          font=("Segoe UI", 11, "bold"))
        screen_monitor_section.pack(pady=(10, 8), anchor="w", padx=8)
        
        info_label = tk.Label(scrollable_frame,
                             text="Real-time AI monitoring with intelligent triggers, analytics, and automated actions",
                             bg="#1e1e2e",
                             fg="#a6adc8",
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
            ("",  None),
            ("🔄 Start Continuous Monitoring", self.ai_monitor_start_continuous),
            ("⏸️ Pause/Resume Monitoring", self.ai_monitor_pause_resume),
            ("🛑 Stop Monitoring", self.ai_monitor_stop),
            ("",  None),
            ("📈 View Analytics Dashboard", self.ai_monitor_view_analytics),
            ("📊 Productivity Trends", self.ai_monitor_productivity_trends),
            ("🚨 Recent Alerts", self.ai_monitor_view_alerts),
            ("⚙️ Configure Settings", self.ai_monitor_configure),
            ("🧹 Clear Analytics Data", self.ai_monitor_clear_analytics),
        ]
        
        for text, command in screen_monitor_actions:
            btn = tk.Button(scrollable_frame,
                          text=text,
                          bg="#313244",
                          fg="#ffffff",
                          font=("Segoe UI", 10),
                          relief="flat",
                          cursor="hand2",
                          command=command,
                          anchor="w",
                          padx=15,
                          pady=10,
                          activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")
        
        rag_section = tk.Label(scrollable_frame,
                              text="🧠 DESKTOP RAG - SMART FILE INTELLIGENCE",
                              bg="#1e1e2e",
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
        
        ai_section = tk.Label(scrollable_frame,
                             text="💬 AI ASSISTANTS & TEXT GENERATION",
                             bg="#1e1e2e",
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
    
    def toggle_vatsal_mode(self):
        """Toggle VATSAL personality mode"""
        self.vatsal_mode = not self.vatsal_mode
        if self.vatsal_mode:
            self.vatsal_toggle_btn.config(text="🤖 VATSAL Mode: ON", bg="#89b4fa")
            self.update_output("\n" + "="*60 + "\n", "info")
            self.update_output("🤖 VATSAL Mode Activated\n", "success")
            self.update_output(self.vatsal.get_status_update('ready') + "\n", "info")
            self.update_output("="*60 + "\n\n", "info")
        else:
            self.vatsal_toggle_btn.config(text="🤖 VATSAL Mode: OFF", bg="#45475a")
            self.update_output("\n" + "="*60 + "\n", "info")
            self.update_output("Standard Mode Activated\n", "warning")
            self.update_output("="*60 + "\n\n", "info")
    
    def show_vatsal_greeting(self):
        """Show VATSAL greeting message"""
        greeting = self.vatsal.get_greeting()
        self.update_output("\n" + "="*60 + "\n", "info")
        self.update_output("🤖 VATSAL AI Assistant\n", "success")
        self.update_output("="*60 + "\n", "info")
        self.update_output(f"{greeting}\n\n", "info")
        
        # Show proactive suggestion
        suggestion = self.vatsal.get_proactive_suggestion()
        self.update_output(f"{suggestion}\n\n", "command")
    
    def get_vatsal_response(self, user_input, command_result=None):
        """Get VATSAL personality response"""
        if self.vatsal_mode and self.vatsal.ai_available:
            return self.vatsal.process_with_personality(user_input, command_result)
        return command_result
    
    def switch_chatbot(self, mode):
        """Switch between different chatbot modes"""
        self.active_chatbot = mode
        
        for m in ["simple", "assistant"]:
            btn = getattr(self, f"chatbot_btn_{m}", None)
            if btn:
                if m == mode:
                    btn.config(bg="#89b4fa", fg="#0f0f1e")
                else:
                    btn.config(bg="#313244", fg="#ffffff")
        
        self.chatbot_info_label.config(text=self.get_chatbot_description(mode))
        
        self.vatsal_conversation_display.config(state='normal')
        self.vatsal_conversation_display.delete(1.0, tk.END)
        self.vatsal_conversation_display.config(state='disabled')
        
        mode_names = {
            "simple": "Simple Chat",
            "assistant": "VATSAL Assistant"
        }
        self._add_vatsal_ai_message("SYSTEM", f"Switched to {mode_names[mode]} mode. Say hello to start chatting!")
    
    def get_chatbot_description(self, mode):
        """Get description for each chatbot mode"""
        descriptions = {
            "simple": "🚀 Simple & clean chatbot - Perfect for quick questions and friendly conversations",
            "assistant": "🤖 Sophisticated VATSAL - Professional personality with proactive suggestions"
        }
        return descriptions.get(mode, "")
    
    def start_vatsal_ai_conversation(self):
        """Start conversation with the active chatbot"""
        if self.active_chatbot == "simple" and self.simple_chatbot:
            greeting = self.simple_chatbot.greeting()
        elif self.active_chatbot == "assistant":
            greeting = self.vatsal.get_greeting()
        else:
            greeting = "Hello! I'm VATSAL, ready to chat!"
        
        self._add_vatsal_ai_message("VATSAL", greeting)
        self.vatsal_conversation_active = True
    
    def send_to_vatsal_ai(self):
        """Send message to VATSAL"""
        user_message = self.vatsal_input.get().strip()
        if not user_message:
            return
        
        self.vatsal_input.delete(0, tk.END)
        self._add_vatsal_ai_message("YOU", user_message)
        
        thread = threading.Thread(target=self._process_vatsal_ai_message, args=(user_message,))
        thread.start()
    
    def _process_vatsal_ai_message(self, user_message):
        """Process message with the active chatbot in background"""
        try:
            if self.active_chatbot == "simple" and self.simple_chatbot:
                response = self.simple_chatbot.chat(user_message)
            elif self.active_chatbot == "assistant":
                response = self.vatsal.process_with_personality(user_message)
            else:
                response = "Chatbot not available. Please check configuration."
            
            self._add_vatsal_ai_message("VATSAL", response)
        except Exception as e:
            self._add_vatsal_ai_message("VATSAL", f"My apologies, I encountered an error: {str(e)}")
    
    def _add_vatsal_ai_message(self, sender, message):
        """Add message to VATSAL conversation display"""
        self.vatsal_conversation_display.config(state='normal')
        
        timestamp = datetime.now().strftime("%I:%M:%S %p")
        
        if sender == "VATSAL":
            self.vatsal_conversation_display.insert(tk.END, f"\n🤖 VATSAL", "vatsal")
            self.vatsal_conversation_display.insert(tk.END, f" ({timestamp})\n", "timestamp")
            self.vatsal_conversation_display.insert(tk.END, f"{message}\n", "")
        else:
            self.vatsal_conversation_display.insert(tk.END, f"\n👤 {sender}", "user")
            self.vatsal_conversation_display.insert(tk.END, f" ({timestamp})\n", "timestamp")
            self.vatsal_conversation_display.insert(tk.END, f"{message}\n", "")
        
        self.vatsal_conversation_display.config(state='disabled')
        self.vatsal_conversation_display.see(tk.END)
    
    def vatsal_ai_get_suggestion(self):
        """Get a friendly prompt from VATSAL"""
        stats = self.vatsal_ai.get_stats()
        if stats.get('total_conversations', 0) > 0:
            self._add_vatsal_ai_message("VATSAL", "Hello! I remember our past conversations. What would you like to chat about today? I'm always learning and improving!")
        else:
            self._add_vatsal_ai_message("VATSAL", "Hello! I'm VATSAL, and I learn from every conversation with you. The more we chat, the better I understand you. What would you like to talk about?")
    
    def clear_vatsal_ai_conversation(self):
        """Clear conversation history for the active chatbot"""
        if self.active_chatbot == "simple" and self.simple_chatbot:
            self.simple_chatbot.reset()
            msg = "Chat cleared! Ready for a fresh conversation."
        elif self.active_chatbot == "assistant":
            self.vatsal.conversation_history = []
            msg = "Chat cleared! VATSAL Assistant is ready for new commands."
        else:
            msg = "Chat cleared."
        
        self.vatsal_conversation_display.config(state='normal')
        self.vatsal_conversation_display.delete(1.0, tk.END)
        self.vatsal_conversation_display.config(state='disabled')
        self.vatsal_conversation_active = False
        messagebox.showinfo("Cleared", msg)
    
    def show_vatsal_ai_stats(self):
        """Show statistics for the active chatbot"""
        if self.active_chatbot == "simple" and self.simple_chatbot:
            conv_count = len(self.simple_chatbot.conversation_history)
            stats_message = f"""
📊 Simple Chatbot Statistics

💬 Current Conversation: {conv_count // 2} exchanges
🤖 Model: Gemini 2.5 Flash
🧠 Memory: Last 10 exchanges
✅ Status: Active and ready!
"""
            title = "Simple Chatbot Stats"
        elif self.active_chatbot == "assistant":
            conv_count = len(self.vatsal.conversation_history)
            stats_message = f"""
📊 VATSAL Assistant Statistics

💬 Conversation History: {conv_count} exchanges
🎭 Personality: Sophisticated & Proactive
🧠 Context Memory: {len(self.vatsal.context_memory)} items
🤖 AI Available: {'Yes' if self.vatsal.ai_available else 'No'}
✨ Features: Time-aware greetings, Proactive suggestions
"""
            title = "VATSAL Assistant Stats"
        else:
            stats_message = "No statistics available."
            title = "Stats"
        
        messagebox.showinfo(title, stats_message)
    
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
            self.update_output(f"\n{'='*60}\n", "info")
            self.update_output(f"📝 You: {command}\n", "command")
            self.update_output(f"{'='*60}\n\n", "info")
            
            # VATSAL acknowledgment
            if self.vatsal_mode:
                ack = self.vatsal.acknowledge_command(command)
                self.update_output(f"🤖 VATSAL: {ack}\n\n", "info")
            
            command_dict = parse_command(command)
            
            if command_dict.get("action") == "error":
                error_msg = command_dict.get('description', 'Error processing command')
                
                if self.vatsal_mode:
                    vatsal_response = self.vatsal.process_with_personality(
                        command, 
                        f"Error: {error_msg}"
                    )
                    self.update_output(f"🤖 VATSAL: {vatsal_response}\n", "error")
                else:
                    self.update_output(f"❌ {error_msg}\n", "error")
                    suggestion = get_ai_suggestion(f"User tried: {command}, but got error. Suggest alternatives.")
                    self.update_output(f"\n💡 Suggestion: {suggestion}\n", "info")
                
                self.update_status("❌ Error", "#f38ba8")
                return
            
            result = self.executor.execute(command_dict)
            
            if result["success"]:
                # Get VATSAL response if mode is enabled
                if self.vatsal_mode:
                    vatsal_response = self.get_vatsal_response(command, result['message'])
                    self.update_output(f"🤖 VATSAL:\n{vatsal_response}\n\n", "success")
                    
                    # Show technical result in smaller text
                    self.update_output(f"📊 Technical Details:\n{result['message']}\n", "info")
                else:
                    self.update_output(f"✅ Result:\n{result['message']}\n", "success")
                
                self.update_status("✅ Ready", "#a6e3a1")
                
                # Occasionally show proactive suggestions
                import random
                if random.random() < 0.3 and self.vatsal_mode:  # 30% chance
                    suggestion = self.vatsal.get_proactive_suggestion()
                    self.update_output(f"\n{suggestion}\n", "command")
                
            else:
                if self.vatsal_mode:
                    vatsal_response = self.vatsal.process_with_personality(
                        command, 
                        f"Error: {result['message']}"
                    )
                    self.update_output(f"🤖 VATSAL: {vatsal_response}\n", "error")
                else:
                    self.update_output(f"❌ Error:\n{result['message']}\n", "error")
                
                self.update_status("❌ Error", "#f38ba8")
            
        except Exception as e:
            if self.vatsal_mode:
                self.update_output(f"🤖 VATSAL: Apologies, Sir. Encountered an unexpected error: {str(e)}\n", "error")
            else:
                self.update_output(f"❌ Error: {str(e)}\n", "error")
            self.update_status("❌ Error", "#f38ba8")
        
        finally:
            self.processing = False
            self.root.after(0, lambda: self.execute_btn.config(state="normal", text="▶ Execute"))
    
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
    
    def show_suggestion(self):
        """Show VATSAL proactive suggestion"""
        suggestion = self.vatsal.get_proactive_suggestion()
        self.update_output(f"\n{suggestion}\n\n", "command")
    
    def show_about(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("ℹ️ About VATSAL")
        about_window.geometry("700x600")
        about_window.configure(bg="#1a1a2e")
        
        header = tk.Label(about_window,
                         text="🤖 VATSAL AI Assistant",
                         bg="#1a1a2e",
                         fg="#ffffff",
                         font=("Segoe UI", 18, "bold"),
                         pady=20)
        header.pack()
        
        version = tk.Label(about_window,
                          text="Version 2.0.0 - VATSAL Edition",
                          bg="#1a1a2e",
                          fg="#89b4fa",
                          font=("Segoe UI", 11))
        version.pack()
        
        description_frame = tk.Frame(about_window, bg="#2a2a3e")
        description_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        description = tk.Label(description_frame,
                              text="""
⚡ Virtual Assistant To Serve And Learn

Powered by Google Gemini AI

VATSAL is your intelligent AI assistant with sophisticated 
personality and advanced capabilities.

✓ 80+ AI-powered features
✓ Sophisticated personality & conversational AI
✓ Context-aware responses with memory
✓ Proactive suggestions & assistance
✓ Natural language command processing
✓ Desktop automation & control
✓ Code generation assistance
✓ Email & messaging automation
✓ System management tools
✓ Productivity tracking
✓ Smart scheduling & workflows

VATSAL Mode Features:
• Personalized responses with wit and charm
• Contextual understanding of your commands
• Proactive suggestions based on time and usage
• Conversational memory across sessions
• Professional yet friendly communication

Toggle VATSAL Mode ON/OFF anytime from the header.

© 2025 AI Automation Suite
                              """,
                              bg="#2a2a3e",
                              fg="#ffffff",
                              font=("Segoe UI", 10),
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
        dialog.configure(bg="#1a1a2e")
        
        tk.Label(dialog, text="⚙️ Configure Continuous Monitoring",
                bg="#1a1a2e", fg="#ffffff",
                font=("Segoe UI", 14, "bold")).pack(pady=15)
        
        tk.Label(dialog, text="Duration (minutes):",
                bg="#1a1a2e", fg="#a6adc8",
                font=("Segoe UI", 10)).pack(pady=(10, 5))
        duration_entry = tk.Entry(dialog, font=("Segoe UI", 11), width=20)
        duration_entry.insert(0, "60")
        duration_entry.pack()
        
        tk.Label(dialog, text="Check Interval (seconds):",
                bg="#1a1a2e", fg="#a6adc8",
                font=("Segoe UI", 10)).pack(pady=(10, 5))
        interval_entry = tk.Entry(dialog, font=("Segoe UI", 11), width=20)
        interval_entry.insert(0, "30")
        interval_entry.pack()
        
        triggers_frame = tk.Frame(dialog, bg="#1a1a2e")
        triggers_frame.pack(pady=15)
        
        tk.Label(triggers_frame, text="Triggers:",
                bg="#1a1a2e", fg="#a6adc8",
                font=("Segoe UI", 10, "bold")).pack()
        
        error_var = tk.BooleanVar(value=True)
        security_var = tk.BooleanVar(value=True)
        perf_var = tk.BooleanVar(value=True)
        
        tk.Checkbutton(triggers_frame, text="Error Detection",
                      variable=error_var, bg="#1a1a2e", fg="#ffffff",
                      selectcolor="#313244", font=("Segoe UI", 9)).pack(anchor="w")
        tk.Checkbutton(triggers_frame, text="Security Monitoring",
                      variable=security_var, bg="#1a1a2e", fg="#ffffff",
                      selectcolor="#313244", font=("Segoe UI", 9)).pack(anchor="w")
        tk.Checkbutton(triggers_frame, text="Performance Issues",
                      variable=perf_var, bg="#1a1a2e", fg="#ffffff",
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
                    self.update_output(f"✅ Monitoring completed! {result['total_checks']} checks performed, {result['alerts_triggered']} alerts triggered.", "success")
                else:
                    self.update_output(f"Error: {result.get('error', 'Unknown error')}", "error")
            
            threading.Thread(target=execute, daemon=True).start()
        
        tk.Button(dialog, text="▶️ Start Monitoring",
                 bg="#89b4fa", fg="#0f0f1e",
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
        dialog.configure(bg="#1a1a2e")
        
        tk.Label(dialog, text="🔄 Continuous AI Monitoring",
                bg="#1a1a2e", fg="#ffffff",
                font=("Segoe UI", 14, "bold")).pack(pady=15)
        
        tk.Label(dialog, text="Select monitoring modes:",
                bg="#1a1a2e", fg="#a6adc8",
                font=("Segoe UI", 10, "bold")).pack(pady=(10, 5))
        
        modes_frame = tk.Frame(dialog, bg="#1a1a2e")
        modes_frame.pack(pady=10)
        
        mode_vars = {}
        for mode_id, mode_info in self.ai_monitor.ANALYSIS_MODES.items():
            var = tk.BooleanVar(value=mode_id in ["productivity", "errors", "security"])
            tk.Checkbutton(modes_frame, text=f"{mode_info['icon']} {mode_info['name']}",
                          variable=var, bg="#1a1a2e", fg="#ffffff",
                          selectcolor="#313244", font=("Segoe UI", 9)).pack(anchor="w")
            mode_vars[mode_id] = var
        
        tk.Label(dialog, text="Check interval (seconds):",
                bg="#1a1a2e", fg="#a6adc8",
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
                    self.update_output(f"   ℹ️ Monitoring is running in background. Use 'Stop Monitoring' to end.\n", "info")
                else:
                    self.update_output(f"❌ {result.get('message')}", "error")
            
            threading.Thread(target=execute, daemon=True).start()
        
        tk.Button(dialog, text="▶️ Start Monitoring",
                 bg="#89b4fa", fg="#0f0f1e",
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
            self.update_output("=" * 60 + "\n", "info")
            
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
            
            self.update_output("\n" + "=" * 60 + "\n", "info")
        
        threading.Thread(target=execute, daemon=True).start()
    
    def ai_monitor_productivity_trends(self):
        """View productivity trends"""
        def execute():
            self.update_output("\n📊 Productivity Trends Analysis\n", "command")
            self.update_output("=" * 60 + "\n", "info")
            
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
            
            self.update_output("\n" + "=" * 60 + "\n", "info")
        
        threading.Thread(target=execute, daemon=True).start()
    
    def ai_monitor_view_alerts(self):
        """View recent alerts"""
        def execute():
            self.update_output("\n🚨 Recent Alerts\n", "command")
            self.update_output("=" * 60 + "\n", "info")
            
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
            
            self.update_output("\n" + "=" * 60 + "\n", "info")
        
        threading.Thread(target=execute, daemon=True).start()
    
    def ai_monitor_configure(self):
        """Configure monitoring settings"""
        dialog = tk.Toplevel(self.root)
        dialog.title("⚙️ Monitoring Configuration")
        dialog.geometry("500x550")
        dialog.configure(bg="#1a1a2e")
        
        tk.Label(dialog, text="⚙️ Monitoring Settings",
                bg="#1a1a2e", fg="#ffffff",
                font=("Segoe UI", 14, "bold")).pack(pady=15)
        
        config = self.ai_monitor.get_config()
        
        tk.Label(dialog, text="Default check interval (seconds):",
                bg="#1a1a2e", fg="#a6adc8",
                font=("Segoe UI", 10)).pack(pady=(10, 5))
        interval_entry = tk.Entry(dialog, font=("Segoe UI", 11), width=20)
        interval_entry.insert(0, str(config.get("default_interval", 30)))
        interval_entry.pack()
        
        change_detection_var = tk.BooleanVar(value=config.get("change_detection", True))
        tk.Checkbutton(dialog, text="Enable change detection (skip identical screens)",
                      variable=change_detection_var, bg="#1a1a2e", fg="#ffffff",
                      selectcolor="#313244", font=("Segoe UI", 9)).pack(pady=5)
        
        smart_scheduling_var = tk.BooleanVar(value=config.get("smart_scheduling", True))
        tk.Checkbutton(dialog, text="Enable smart scheduling",
                      variable=smart_scheduling_var, bg="#1a1a2e", fg="#ffffff",
                      selectcolor="#313244", font=("Segoe UI", 9)).pack(pady=5)
        
        privacy_mode_var = tk.BooleanVar(value=config.get("privacy_mode", False))
        tk.Checkbutton(dialog, text="Privacy mode (no screenshots saved)",
                      variable=privacy_mode_var, bg="#1a1a2e", fg="#ffffff",
                      selectcolor="#313244", font=("Segoe UI", 9)).pack(pady=5)
        
        tk.Label(dialog, text="Auto Actions:",
                bg="#1a1a2e", fg="#a6adc8",
                font=("Segoe UI", 10, "bold")).pack(pady=(15, 5))
        
        auto_actions = config.get("auto_actions", {})
        
        screenshot_on_error_var = tk.BooleanVar(value=auto_actions.get("screenshot_on_error", True))
        tk.Checkbutton(dialog, text="Auto-screenshot on errors",
                      variable=screenshot_on_error_var, bg="#1a1a2e", fg="#ffffff",
                      selectcolor="#313244", font=("Segoe UI", 9)).pack(pady=2)
        
        alert_on_security_var = tk.BooleanVar(value=auto_actions.get("alert_on_security", True))
        tk.Checkbutton(dialog, text="Alert on security issues",
                      variable=alert_on_security_var, bg="#1a1a2e", fg="#ffffff",
                      selectcolor="#313244", font=("Segoe UI", 9)).pack(pady=2)
        
        log_productivity_var = tk.BooleanVar(value=auto_actions.get("log_productivity", True))
        tk.Checkbutton(dialog, text="Log productivity metrics",
                      variable=log_productivity_var, bg="#1a1a2e", fg="#ffffff",
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
                 bg="#89b4fa", fg="#0f0f1e",
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

def main():
    root = tk.Tk()
    app = AutomationControllerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
