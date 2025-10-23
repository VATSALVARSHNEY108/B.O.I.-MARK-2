#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import os
from dotenv import load_dotenv
from gemini_controller import parse_command, get_ai_suggestion
from command_executor import CommandExecutor

load_dotenv()

class AutomationControllerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 AI Desktop Automation Controller")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1e1e2e")
        
        self.executor = CommandExecutor()
        self.processing = False
        
        self.setup_ui()
        self.check_api_key()
    
    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("Header.TLabel", 
                       background="#1e1e2e", 
                       foreground="#cdd6f4",
                       font=("Arial", 20, "bold"))
        style.configure("Info.TLabel", 
                       background="#1e1e2e", 
                       foreground="#89b4fa",
                       font=("Arial", 10))
        style.configure("Category.TLabel",
                       background="#313244",
                       foreground="#f9e2af",
                       font=("Arial", 11, "bold"))
        
        header_frame = tk.Frame(self.root, bg="#1e1e2e", pady=15)
        header_frame.pack(fill="x")
        
        title = ttk.Label(header_frame, 
                         text="🤖 AI Desktop Automation Controller",
                         style="Header.TLabel")
        title.pack()
        
        subtitle = ttk.Label(header_frame,
                            text="Powered by Gemini AI • Complete Desktop Automation Suite",
                            style="Info.TLabel")
        subtitle.pack()
        
        main_container = tk.Frame(self.root, bg="#1e1e2e")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        left_panel = tk.Frame(main_container, bg="#1e1e2e", width=400)
        left_panel.pack(side="left", fill="both", expand=False, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        categories_label = tk.Label(left_panel,
                                   text="🎯 Quick Actions",
                                   bg="#1e1e2e",
                                   fg="#cdd6f4",
                                   font=("Arial", 13, "bold"))
        categories_label.pack(pady=(0, 10))
        
        notebook = ttk.Notebook(left_panel)
        notebook.pack(fill="both", expand=True)
        
        self.create_code_tab(notebook)
        self.create_desktop_tab(notebook)
        self.create_messaging_tab(notebook)
        self.create_system_tab(notebook)
        self.create_productivity_tab(notebook)
        self.create_fun_tab(notebook)
        
        right_panel = tk.Frame(main_container, bg="#1e1e2e")
        right_panel.pack(side="right", fill="both", expand=True)
        
        input_frame = tk.Frame(right_panel, bg="#1e1e2e")
        input_frame.pack(fill="x", pady=(0, 15))
        
        input_label = tk.Label(input_frame,
                              text="💬 Enter Command or Use Quick Actions",
                              bg="#1e1e2e",
                              fg="#cdd6f4",
                              font=("Arial", 11, "bold"))
        input_label.pack(anchor="w", pady=(0, 5))
        
        input_container = tk.Frame(input_frame, bg="#1e1e2e")
        input_container.pack(fill="x")
        
        self.command_input = tk.Entry(input_container,
                                     bg="#313244",
                                     fg="#cdd6f4",
                                     font=("Arial", 12),
                                     insertbackground="#cdd6f4",
                                     relief="flat",
                                     bd=0)
        self.command_input.pack(side="left", fill="both", expand=True, ipady=10, padx=(0, 10))
        self.command_input.bind("<Return>", lambda e: self.execute_command())
        
        self.execute_btn = tk.Button(input_container,
                                    text="▶ Execute",
                                    bg="#89b4fa",
                                    fg="#1e1e2e",
                                    font=("Arial", 11, "bold"),
                                    relief="flat",
                                    cursor="hand2",
                                    command=self.execute_command,
                                    padx=20,
                                    pady=10)
        self.execute_btn.pack(side="right")
        
        output_label = tk.Label(right_panel,
                               text="📋 Output Console",
                               bg="#1e1e2e",
                               fg="#cdd6f4",
                               font=("Arial", 11, "bold"))
        output_label.pack(anchor="w", pady=(0, 5))
        
        self.output_area = scrolledtext.ScrolledText(right_panel,
                                                     bg="#313244",
                                                     fg="#cdd6f4",
                                                     font=("Consolas", 10),
                                                     relief="flat",
                                                     bd=0,
                                                     padx=10,
                                                     pady=10,
                                                     wrap="word")
        self.output_area.pack(fill="both", expand=True)
        self.output_area.config(state="disabled")
        
        bottom_frame = tk.Frame(self.root, bg="#1e1e2e", pady=15, padx=20)
        bottom_frame.pack(fill="x", side="bottom")
        
        button_config = {
            "bg": "#45475a",
            "fg": "#cdd6f4",
            "font": ("Arial", 9),
            "relief": "flat",
            "cursor": "hand2",
            "padx": 15,
            "pady": 8
        }
        
        help_btn = tk.Button(bottom_frame, text="❓ Full Help", command=self.show_help, **button_config)
        help_btn.pack(side="left", padx=5)
        
        contacts_btn = tk.Button(bottom_frame, text="👥 Contacts", command=self.show_contacts, **button_config)
        contacts_btn.pack(side="left", padx=5)
        
        clear_btn = tk.Button(bottom_frame, text="🗑️ Clear", command=self.clear_output, **button_config)
        clear_btn.pack(side="left", padx=5)
        
        self.status_label = tk.Label(bottom_frame,
                                    text="✅ Ready",
                                    bg="#1e1e2e",
                                    fg="#a6e3a1",
                                    font=("Arial", 9))
        self.status_label.pack(side="right")
    
    def create_code_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#313244")
        notebook.add(tab, text="💻 Code")
        
        canvas = tk.Canvas(tab, bg="#313244", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#313244")
        
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
                          bg="#45475a",
                          fg="#cdd6f4",
                          font=("Arial", 9),
                          relief="flat",
                          cursor="hand2",
                          command=lambda c=command: self.quick_command(c),
                          anchor="w",
                          padx=10,
                          pady=8)
            btn.pack(fill="x", padx=5, pady=2)
    
    def create_desktop_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#313244")
        notebook.add(tab, text="🖥️ Desktop")
        
        canvas = tk.Canvas(tab, bg="#313244", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#313244")
        
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
                          bg="#45475a",
                          fg="#cdd6f4",
                          font=("Arial", 9),
                          relief="flat",
                          cursor="hand2",
                          command=lambda c=command: self.quick_command(c),
                          anchor="w",
                          padx=10,
                          pady=8)
            btn.pack(fill="x", padx=5, pady=2)
    
    def create_messaging_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#313244")
        notebook.add(tab, text="📱 Messaging")
        
        canvas = tk.Canvas(tab, bg="#313244", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#313244")
        
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
                          bg="#45475a",
                          fg="#cdd6f4",
                          font=("Arial", 9),
                          relief="flat",
                          cursor="hand2",
                          command=lambda c=command: self.quick_command(c),
                          anchor="w",
                          padx=10,
                          pady=8)
            btn.pack(fill="x", padx=5, pady=2)
    
    def create_system_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#313244")
        notebook.add(tab, text="⚙️ System")
        
        canvas = tk.Canvas(tab, bg="#313244", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#313244")
        
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
                          bg="#45475a",
                          fg="#cdd6f4",
                          font=("Arial", 9),
                          relief="flat",
                          cursor="hand2",
                          command=lambda c=command: self.quick_command(c),
                          anchor="w",
                          padx=10,
                          pady=8)
            btn.pack(fill="x", padx=5, pady=2)
    
    def create_productivity_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#313244")
        notebook.add(tab, text="📈 Productivity")
        
        canvas = tk.Canvas(tab, bg="#313244", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#313244")
        
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
                          bg="#45475a",
                          fg="#cdd6f4",
                          font=("Arial", 9),
                          relief="flat",
                          cursor="hand2",
                          command=lambda c=command: self.quick_command(c),
                          anchor="w",
                          padx=10,
                          pady=8)
            btn.pack(fill="x", padx=5, pady=2)
    
    def create_fun_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#313244")
        notebook.add(tab, text="🎉 Fun")
        
        canvas = tk.Canvas(tab, bg="#313244", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#313244")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        actions = [
            ("😊 Get Compliment", "Give me a compliment"),
            ("🎊 Celebrate Task", "Celebrate task completion"),
            ("🎨 Set Mood: Happy", "Set mood to happy"),
            ("🌙 Set Mood: Calm", "Set mood to calm"),
            ("⚡ Set Mood: Energetic", "Set mood to energetic"),
            ("💬 Chat with Bot", "Talk to chatbot"),
            ("🎲 Random Fact", "Tell me a random fact"),
            ("🌟 Motivate Me", "Give me motivation"),
        ]
        
        for text, command in actions:
            btn = tk.Button(scrollable_frame,
                          text=text,
                          bg="#45475a",
                          fg="#cdd6f4",
                          font=("Arial", 9),
                          relief="flat",
                          cursor="hand2",
                          command=lambda c=command: self.quick_command(c),
                          anchor="w",
                          padx=10,
                          pady=8)
            btn.pack(fill="x", padx=5, pady=2)
    
    def quick_command(self, command):
        self.command_input.delete(0, "end")
        self.command_input.insert(0, command)
        self.execute_command()
    
    def check_api_key(self):
        if not os.environ.get("GEMINI_API_KEY"):
            self.log_output("❌ ERROR: GEMINI_API_KEY not found in environment variables", "error")
            self.log_output("Please add your Gemini API key to continue.", "error")
            self.set_status("❌ API Key Missing", "#f38ba8")
        else:
            self.log_output("✅ Connected to Gemini AI", "success")
            self.log_output("💡 Ready to execute commands! Try the quick actions or type your own command.", "info")
            self.set_status("✅ Ready", "#a6e3a1")
    
    def set_status(self, text, color="#a6e3a1"):
        self.status_label.config(text=text, fg=color)
    
    def log_output(self, message, msg_type="normal"):
        self.output_area.config(state="normal")
        
        if msg_type == "success":
            self.output_area.insert("end", f"✅ {message}\n", "success")
            self.output_area.tag_config("success", foreground="#a6e3a1")
        elif msg_type == "error":
            self.output_area.insert("end", f"❌ {message}\n", "error")
            self.output_area.tag_config("error", foreground="#f38ba8")
        elif msg_type == "info":
            self.output_area.insert("end", f"💡 {message}\n", "info")
            self.output_area.tag_config("info", foreground="#89b4fa")
        elif msg_type == "task":
            self.output_area.insert("end", f"📋 {message}\n", "task")
            self.output_area.tag_config("task", foreground="#f9e2af")
        else:
            self.output_area.insert("end", f"{message}\n")
        
        self.output_area.see("end")
        self.output_area.config(state="disabled")
    
    def clear_output(self):
        self.output_area.config(state="normal")
        self.output_area.delete(1.0, "end")
        self.output_area.config(state="disabled")
        self.log_output("🗑️ Output cleared", "info")
    
    def execute_command(self):
        if self.processing:
            return
        
        command_text = self.command_input.get().strip()
        if not command_text:
            return
        
        self.command_input.delete(0, "end")
        self.log_output(f"\n🎯 Command: {command_text}\n", "task")
        
        def run_command():
            self.processing = True
            self.set_status("⏳ Processing...", "#f9e2af")
            self.execute_btn.config(state="disabled")
            
            try:
                if command_text.lower() in ['help', 'h']:
                    self.show_help()
                elif command_text.lower() == 'contacts':
                    self.show_contacts()
                else:
                    self.log_output("🤔 Processing with AI...", "info")
                    command_dict = parse_command(command_text)
                    
                    if command_dict.get("action") == "error":
                        self.log_output(f"{command_dict.get('description', 'Error processing command')}", "error")
                        suggestion = get_ai_suggestion(f"User tried: {command_text}, but got error. Suggest alternatives.")
                        self.log_output(f"💡 Suggestion: {suggestion}", "info")
                    else:
                        result = self.executor.execute(command_dict)
                        
                        if result["success"]:
                            self.log_output(result["message"], "success")
                        else:
                            self.log_output(result["message"], "error")
            
            except Exception as e:
                self.log_output(f"Unexpected error: {str(e)}", "error")
            
            finally:
                self.processing = False
                self.set_status("✅ Ready", "#a6e3a1")
                self.execute_btn.config(state="normal")
        
        thread = threading.Thread(target=run_command, daemon=True)
        thread.start()
    
    def show_help(self):
        help_text = """
╔══════════════════════════════════════════════════════════════╗
║          🤖 AI DESKTOP AUTOMATION CONTROLLER HELP            ║
╚══════════════════════════════════════════════════════════════╝

📚 AVAILABLE FEATURES:

┌─ 💻 CODE GENERATION ─────────────────────────────────────────┐
│ • Generate code in any language (Python, JavaScript, etc.)   │
│ • Explain existing code                                      │
│ • Improve and optimize code                                  │
│ • Debug code and find errors                                 │
│ • Write code directly to editor                              │
│                                                               │
│ Examples:                                                     │
│   - "Write code for checking palindrome"                     │
│   - "Generate Python code for bubble sort"                   │
│   - "Create JavaScript calculator"                           │
└───────────────────────────────────────────────────────────────┘

┌─ 🖥️ DESKTOP AUTOMATION ──────────────────────────────────────┐
│ • Open applications                                           │
│ • Type text and press keys                                   │
│ • Take screenshots                                            │
│ • Click and move mouse                                        │
│ • Search the web                                              │
│ • Analyze screen content                                      │
│                                                               │
│ Examples:                                                     │
│   - "Open notepad and type Hello World"                      │
│   - "Take a screenshot"                                       │
│   - "Search Google for Python tutorials"                     │
└───────────────────────────────────────────────────────────────┘

┌─ 📱 MESSAGING & COMMUNICATION ───────────────────────────────┐
│ • Send emails (plain, HTML, with attachments)                │
│ • Send WhatsApp messages                                      │
│ • Manage contacts                                             │
│ • YouTube automation                                          │
│ • Email templates                                             │
│                                                               │
│ Examples:                                                     │
│   - "Add contact Mom with phone 555-1234"                    │
│   - "Send email to boss about meeting"                       │
│   - "Send WhatsApp message to John"                          │
│   - "Play YouTube video about Python"                        │
└───────────────────────────────────────────────────────────────┘

┌─ ⚙️ SYSTEM & FILE MANAGEMENT ────────────────────────────────┐
│ • System monitoring (CPU, memory, disk)                       │
│ • File organization and cleanup                              │
│ • Find large/duplicate files                                 │
│ • Compress and backup files                                  │
│ • System control (sleep, lock, volume)                       │
│ • Process management                                          │
│                                                               │
│ Examples:                                                     │
│   - "Show system information"                                │
│   - "Find large files"                                        │
│   - "Organize downloads folder"                              │
│   - "Set volume to 50"                                        │
└───────────────────────────────────────────────────────────────┘

┌─ 📈 PRODUCTIVITY FEATURES ───────────────────────────────────┐
│ • Screen time tracking                                        │
│ • Focus mode and distraction blocking                        │
│ • Productivity scoring                                        │
│ • Smart reminders                                             │
│ • Daily summaries                                             │
│ • Smart typing and replies                                    │
│                                                               │
│ Examples:                                                     │
│   - "Enable focus mode for 2 hours"                          │
│   - "Show screen time dashboard"                             │
│   - "Send water reminder"                                     │
│   - "Generate daily summary"                                  │
└───────────────────────────────────────────────────────────────┘

┌─ 🎉 FUN FEATURES ────────────────────────────────────────────┐
│ • Get random compliments                                      │
│ • Celebrate task completion                                   │
│ • Set mood themes                                             │
│ • Chatbot conversations                                       │
│ • Motivation and inspiration                                  │
│                                                               │
│ Examples:                                                     │
│   - "Give me a compliment"                                   │
│   - "Celebrate task completion"                              │
│   - "Set mood to energetic"                                   │
└───────────────────────────────────────────────────────────────┘

💡 TIP: Use the tabbed quick actions panel on the left to quickly
        access common commands, or type natural language commands!

🎯 MULTI-STEP WORKFLOWS:
   You can combine multiple actions in one command:
   • "Open notepad and type my todo list"
   • "Take screenshot and analyze it"
   • "Search YouTube and play first result"

❓ For more help, type 'help' or visit the quick actions tabs!
"""
        self.log_output(help_text, "info")
    
    def show_contacts(self):
        result = self.executor.execute_single_action("list_contacts", {})
        self.log_output(result["message"], "info")

def main():
    root = tk.Tk()
    app = AutomationControllerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
