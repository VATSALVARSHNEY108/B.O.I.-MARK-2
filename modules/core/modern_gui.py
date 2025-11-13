#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import os
from dotenv import load_dotenv
from modules.core.gemini_controller import parse_command, get_ai_suggestion
from modules.core.command_executor import CommandExecutor
from modules.core.vatsal_assistant import create_vatsal_assistant
from modules.ai_features.chatbots import SimpleChatbot
from datetime import datetime
from pathlib import Path

load_dotenv()


class ModernBlock(tk.Frame):
    """A 3D-like block widget with shadows and hover effects"""
    
    def __init__(self, parent, title="", **kwargs):
        super().__init__(parent, **kwargs)
        
        # 3D shadow effect - multiple layers
        self.shadow_frame = tk.Frame(
            parent, 
            bg="#c8c8c8",  # Darker shadow
            highlightthickness=0
        )
        self.shadow_frame.place(x=5, y=5, relwidth=1, relheight=1)
        
        # Light shadow
        self.light_shadow = tk.Frame(
            parent,
            bg="#d8d8d8",  # Light shadow
            highlightthickness=0
        )
        self.light_shadow.place(x=3, y=3, relwidth=1, relheight=1)
        
        # Main block
        self.configure(
            bg="#f5f5f0",  # Off-white cream
            relief="flat",
            highlightthickness=1,
            highlightbackground="#e0e0d8",
            highlightcolor="#d0d0c8"
        )
        self.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Title if provided
        if title:
            title_frame = tk.Frame(self, bg="#e8e8dc", height=40)
            title_frame.pack(fill="x", padx=2, pady=2)
            title_frame.pack_propagate(False)
            
            tk.Label(
                title_frame,
                text=title,
                font=("Segoe UI", 12, "bold"),
                bg="#e8e8dc",
                fg="#4a4a3d"
            ).pack(pady=10)
        
        # Content frame
        self.content = tk.Frame(self, bg="#f5f5f0")
        self.content.pack(fill="both", expand=True, padx=8, pady=8)
    
    def bind_hover(self, enter_func=None, leave_func=None):
        """Add hover effect"""
        def on_enter(e):
            self.configure(highlightbackground="#c8c8b8", highlightthickness=2)
            if enter_func:
                enter_func(e)
        
        def on_leave(e):
            self.configure(highlightbackground="#e0e0d8", highlightthickness=1)
            if leave_func:
                leave_func(e)
        
        self.bind("<Enter>", on_enter)
        self.bind("<Leave>", on_leave)


class Modern3DButton(tk.Button):
    """A 3D-style button with depth"""
    
    def __init__(self, parent, text="", command=None, **kwargs):
        # Default styling
        default_style = {
            "bg": "#d8d8ca",
            "fg": "#3a3a2d",
            "font": ("Segoe UI", 10, "bold"),
            "relief": "raised",
            "borderwidth": 3,
            "activebackground": "#c8c8ba",
            "activeforeground": "#2a2a1d",
            "cursor": "hand2",
            "padx": 20,
            "pady": 10
        }
        default_style.update(kwargs)
        
        super().__init__(parent, text=text, command=command, **default_style)
        
        # Hover effects
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        
        self.default_bg = default_style.get("bg", "#d8d8ca")
    
    def _on_enter(self, e):
        self.configure(bg="#c8c8ba")
    
    def _on_leave(self, e):
        self.configure(bg=self.default_bg)
    
    def _on_press(self, e):
        self.configure(relief="sunken", borderwidth=2)
    
    def _on_release(self, e):
        self.configure(relief="raised", borderwidth=3)


class ModernGUI:
    """Modern GUI with off-white colors and 3D blocks"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("✨ VATSAL - Modern AI Assistant")
        self.root.geometry("1200x800")
        
        # Off-white background
        self.root.configure(bg="#fafaf5")
        
        # Initialize components
        try:
            self.executor = CommandExecutor()
            self.vatsal = create_vatsal_assistant()
            self.simple_chatbot = SimpleChatbot() if os.getenv("GEMINI_API_KEY") else None
        except Exception as e:
            print(f"⚠️ Initialization warning: {e}")
            self.executor = None
            self.vatsal = None
            self.simple_chatbot = None
        
        self.command_history = []
        
        # Build UI
        self._create_header()
        self._create_main_content()
        self._create_footer()
        
        # Update clock
        self._update_clock()
    
    def _create_header(self):
        """Create header with title and status"""
        header = tk.Frame(self.root, bg="#e8e8dc", height=80)
        header.pack(fill="x", pady=(0, 10))
        header.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header,
            text="✨ VATSAL AI Assistant",
            font=("Segoe UI", 24, "bold"),
            bg="#e8e8dc",
            fg="#3a3a2d"
        )
        title_label.pack(side="left", padx=30, pady=20)
        
        # Clock
        self.clock_label = tk.Label(
            header,
            text="",
            font=("Segoe UI", 14),
            bg="#e8e8dc",
            fg="#5a5a4d"
        )
        self.clock_label.pack(side="right", padx=30)
        
        # Status indicator
        status_frame = tk.Frame(header, bg="#e8e8dc")
        status_frame.pack(side="right", padx=20)
        
        self.status_dot = tk.Canvas(status_frame, width=12, height=12, bg="#e8e8dc", highlightthickness=0)
        self.status_dot.pack(side="left", padx=(0, 5))
        self.status_dot.create_oval(2, 2, 10, 10, fill="#7cb342", outline="")
        
        tk.Label(
            status_frame,
            text="Online",
            font=("Segoe UI", 10),
            bg="#e8e8dc",
            fg="#5a5a4d"
        ).pack(side="left")
    
    def _create_main_content(self):
        """Create main content area with 3D blocks"""
        main_container = tk.Frame(self.root, bg="#fafaf5")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left panel - Command input
        left_panel = tk.Frame(main_container, bg="#fafaf5")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Command block
        cmd_container = tk.Frame(left_panel, bg="#fafaf5", height=200)
        cmd_container.pack(fill="x", pady=(0, 15))
        cmd_container.pack_propagate(False)
        
        cmd_block = ModernBlock(cmd_container, title="🎤 Voice Command")
        
        # Command input
        input_frame = tk.Frame(cmd_block.content, bg="#f5f5f0")
        input_frame.pack(fill="x", pady=10)
        
        self.command_entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 12),
            bg="#ffffff",
            fg="#3a3a2d",
            relief="solid",
            borderwidth=1,
            insertbackground="#3a3a2d"
        )
        self.command_entry.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=8)
        self.command_entry.bind("<Return>", lambda e: self._execute_command())
        
        Modern3DButton(
            input_frame,
            text="Execute",
            command=self._execute_command,
            bg="#8cb369",
            activebackground="#7ca359"
        ).pack(side="left")
        
        # Quick actions
        actions_frame = tk.Frame(cmd_block.content, bg="#f5f5f0")
        actions_frame.pack(fill="x", pady=10)
        
        tk.Label(
            actions_frame,
            text="Quick Actions:",
            font=("Segoe UI", 9, "bold"),
            bg="#f5f5f0",
            fg="#5a5a4d"
        ).pack(anchor="w", pady=(0, 5))
        
        quick_btns = tk.Frame(actions_frame, bg="#f5f5f0")
        quick_btns.pack(fill="x")
        
        quick_actions = [
            ("📁 Open File", lambda: self.command_entry.insert(0, "open file ")),
            ("💬 Chat", lambda: self._switch_to_chat()),
            ("📊 System Info", lambda: self.command_entry.insert(0, "system info"))
        ]
        
        for text, cmd in quick_actions:
            Modern3DButton(
                quick_btns,
                text=text,
                command=cmd,
                bg="#d8d8ca",
                font=("Segoe UI", 9)
            ).pack(side="left", padx=5)
        
        # Output block
        output_container = tk.Frame(left_panel, bg="#fafaf5")
        output_container.pack(fill="both", expand=True)
        
        output_block = ModernBlock(output_container, title="📋 Output Console")
        
        self.output_console = scrolledtext.ScrolledText(
            output_block.content,
            font=("Consolas", 10),
            bg="#ffffff",
            fg="#2a2a2a",
            relief="flat",
            wrap="word",
            highlightthickness=0,
            insertbackground="#3a3a2d"
        )
        self.output_console.pack(fill="both", expand=True)
        self._log_output("Welcome to VATSAL AI Assistant! 👋\n")
        self._log_output("Type a command or use voice input to get started.\n")
        
        # Right panel - Stats and info
        right_panel = tk.Frame(main_container, bg="#fafaf5", width=300)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)
        
        # Stats block
        stats_container = tk.Frame(right_panel, bg="#fafaf5", height=200)
        stats_container.pack(fill="x", pady=(0, 15))
        stats_container.pack_propagate(False)
        
        stats_block = ModernBlock(stats_container, title="📊 Statistics")
        
        self.stats_labels = {}
        stats_data = [
            ("Commands Run", "0"),
            ("Success Rate", "100%"),
            ("Active Time", "0m")
        ]
        
        for label, value in stats_data:
            stat_row = tk.Frame(stats_block.content, bg="#f5f5f0")
            stat_row.pack(fill="x", pady=8)
            
            tk.Label(
                stat_row,
                text=label,
                font=("Segoe UI", 9),
                bg="#f5f5f0",
                fg="#6a6a5d"
            ).pack(anchor="w")
            
            value_label = tk.Label(
                stat_row,
                text=value,
                font=("Segoe UI", 14, "bold"),
                bg="#f5f5f0",
                fg="#3a3a2d"
            )
            value_label.pack(anchor="w")
            self.stats_labels[label] = value_label
        
        # History block
        history_container = tk.Frame(right_panel, bg="#fafaf5")
        history_container.pack(fill="both", expand=True)
        
        history_block = ModernBlock(history_container, title="🕐 Recent Commands")
        
        self.history_listbox = tk.Listbox(
            history_block.content,
            font=("Segoe UI", 9),
            bg="#ffffff",
            fg="#3a3a2d",
            relief="flat",
            highlightthickness=0,
            selectbackground="#c8c8ba",
            activestyle="none"
        )
        self.history_listbox.pack(fill="both", expand=True)
    
    def _create_footer(self):
        """Create footer with info"""
        footer = tk.Frame(self.root, bg="#e8e8dc", height=40)
        footer.pack(fill="x", pady=(10, 0))
        footer.pack_propagate(False)
        
        tk.Label(
            footer,
            text="Powered by Google Gemini AI ✨",
            font=("Segoe UI", 9),
            bg="#e8e8dc",
            fg="#6a6a5d"
        ).pack(side="left", padx=20)
        
        tk.Label(
            footer,
            text="Ready to assist",
            font=("Segoe UI", 9, "italic"),
            bg="#e8e8dc",
            fg="#6a6a5d"
        ).pack(side="right", padx=20)
    
    def _update_clock(self):
        """Update clock display"""
        now = datetime.now().strftime("%I:%M:%S %p")
        self.clock_label.config(text=now)
        self.root.after(1000, self._update_clock)
    
    def _execute_command(self):
        """Execute user command"""
        command = self.command_entry.get().strip()
        
        if not command:
            return
        
        self.command_entry.delete(0, tk.END)
        self._log_output(f"\n> {command}\n", tag="command")
        
        # Add to history
        self.command_history.append(command)
        self.history_listbox.insert(0, f"{datetime.now().strftime('%H:%M')} - {command[:40]}")
        
        # Update stats
        current_count = int(self.stats_labels["Commands Run"].cget("text"))
        self.stats_labels["Commands Run"].config(text=str(current_count + 1))
        
        # Execute in thread
        thread = threading.Thread(target=self._run_command, args=(command,))
        thread.daemon = True
        thread.start()
    
    def _run_command(self, command):
        """Run command in background"""
        try:
            if self.executor:
                result = self.executor.execute(command)
                self._log_output(f"✓ {result}\n", tag="success")
            else:
                self._log_output("⚠️ Executor not initialized. Please set GEMINI_API_KEY.\n", tag="error")
        except Exception as e:
            self._log_output(f"❌ Error: {str(e)}\n", tag="error")
    
    def _log_output(self, message, tag="normal"):
        """Log message to output console"""
        self.output_console.insert(tk.END, message)
        
        # Configure tags for colors
        if tag == "command":
            self.output_console.tag_config("command", foreground="#5a7db8", font=("Consolas", 10, "bold"))
            self.output_console.tag_add("command", "end-2c linestart", "end-1c")
        elif tag == "success":
            self.output_console.tag_config("success", foreground="#7cb342")
            self.output_console.tag_add("success", "end-2c linestart", "end-1c")
        elif tag == "error":
            self.output_console.tag_config("error", foreground="#d32f2f")
            self.output_console.tag_add("error", "end-2c linestart", "end-1c")
        
        self.output_console.see(tk.END)
    
    def _switch_to_chat(self):
        """Open chat mode"""
        self._log_output("\n💬 Chat mode activated! Start chatting below.\n", tag="success")
        self.command_entry.focus()
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()


def main():
    """Launch the modern GUI"""
    root = tk.Tk()
    app = ModernGUI(root)
    app.run()


if __name__ == "__main__":
    main()
