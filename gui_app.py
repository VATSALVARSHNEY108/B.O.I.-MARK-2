#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
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
        self.root.geometry("900x700")
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
        style.configure("Action.TButton",
                       background="#89b4fa",
                       foreground="#1e1e2e",
                       font=("Arial", 10, "bold"),
                       borderwidth=0,
                       padding=10)
        
        header_frame = tk.Frame(self.root, bg="#1e1e2e", pady=20)
        header_frame.pack(fill="x")
        
        title = ttk.Label(header_frame, 
                         text="🤖 AI Desktop Automation Controller",
                         style="Header.TLabel")
        title.pack()
        
        subtitle = ttk.Label(header_frame,
                            text="Powered by Gemini AI • Code Generation & Desktop Automation",
                            style="Info.TLabel")
        subtitle.pack()
        
        main_frame = tk.Frame(self.root, bg="#1e1e2e", padx=20)
        main_frame.pack(fill="both", expand=True)
        
        examples_frame = tk.LabelFrame(main_frame, 
                                      text="  💡 Quick Examples  ",
                                      bg="#313244",
                                      fg="#cdd6f4",
                                      font=("Arial", 10, "bold"),
                                      padx=10,
                                      pady=10)
        examples_frame.pack(fill="x", pady=(0, 15))
        
        examples = [
            ("🤖 Write code for checking palindrome", self.example1),
            ("📝 Open notepad and type Hello World", self.example2),
            ("📸 Take a screenshot", self.example3),
            ("🔍 Search Google for Python tutorials", self.example4),
        ]
        
        for text, command in examples:
            btn = tk.Button(examples_frame,
                          text=text,
                          bg="#45475a",
                          fg="#cdd6f4",
                          font=("Arial", 9),
                          relief="flat",
                          cursor="hand2",
                          command=command,
                          padx=10,
                          pady=5)
            btn.pack(side="left", padx=5, expand=True, fill="x")
        
        input_frame = tk.Frame(main_frame, bg="#1e1e2e")
        input_frame.pack(fill="x", pady=(0, 15))
        
        input_label = tk.Label(input_frame,
                              text="🎯 What would you like to do?",
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
        
        output_label = tk.Label(main_frame,
                               text="📋 Output",
                               bg="#1e1e2e",
                               fg="#cdd6f4",
                               font=("Arial", 11, "bold"))
        output_label.pack(anchor="w", pady=(0, 5))
        
        self.output_area = scrolledtext.ScrolledText(main_frame,
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
        
        help_btn = tk.Button(bottom_frame, text="❓ Help", command=self.show_help, **button_config)
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
    
    def check_api_key(self):
        if not os.environ.get("GEMINI_API_KEY"):
            self.log_output("❌ ERROR: GEMINI_API_KEY not found in environment variables", "error")
            self.log_output("Please add your Gemini API key to continue.", "error")
            self.set_status("❌ API Key Missing", "#f38ba8")
        else:
            self.log_output("✅ Connected to Gemini AI", "success")
            self.log_output("💡 Ready to execute commands! Try the examples above or type your own.", "info")
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
📚 Available Features:

🤖 AI Code Generation:
   • Write code for checking palindrome
   • Generate Python code for bubble sort
   • Create JavaScript code for calculator

🖥️ Desktop Automation:
   • Open notepad
   • Type Hello World
   • Take a screenshot
   • Press enter
   • Search Google for Python tutorials

📱 Messaging (Advanced):
   • Text Sarah that I'm running late
   • Email my boss about the meeting
   • Add contact Mom with phone 555-1234

💡 Multi-Step Workflows:
   • Open notepad and type Hello World
   • Create file test.txt with content Hello
"""
        self.log_output(help_text, "info")
    
    def show_contacts(self):
        result = self.executor.execute_single_action("list_contacts", {})
        self.log_output(result["message"], "info")
    
    def example1(self):
        self.command_input.delete(0, "end")
        self.command_input.insert(0, "Write code for checking palindrome")
    
    def example2(self):
        self.command_input.delete(0, "end")
        self.command_input.insert(0, "Open notepad and type Hello World")
    
    def example3(self):
        self.command_input.delete(0, "end")
        self.command_input.insert(0, "Take a screenshot")
    
    def example4(self):
        self.command_input.delete(0, "end")
        self.command_input.insert(0, "Search Google for Python tutorials")

def main():
    root = tk.Tk()
    app = AutomationControllerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
