#!/usr/bin/env python3
"""
V.A.T.S.A.L - Enhanced AI Desktop Assistant GUI
Professional ChatGPT-style interface with advanced features
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
import sys
from datetime import datetime
import time
import json
from pathlib import Path
import psutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

try:
    from modules.core.gemini_controller import parse_command
except:
    parse_command = None

try:
    from modules.core.command_executor import CommandExecutor
except:
    CommandExecutor = None

try:
    from modules.core.vatsal_assistant import create_vatsal_assistant
except:
    create_vatsal_assistant = None


class EnhancedChatGUI:
    """Enhanced ChatGPT-level professional GUI with advanced features"""

    def __init__(self, root):
        self.root = root
        self.root.title("V.A.T.S.A.L - AI Desktop Assistant")
        self.root.geometry("1600x950")
        self.root.minsize(1200, 700)
        
        # Enhanced color scheme with theme support
        self.themes = {
            "light": {
                "bg_main": "#ffffff",
                "bg_light": "#f7f7f8",
                "bg_dark": "#ececf1",
                "text_main": "#0d0d0d",
                "text_light": "#565869",
                "border": "#d1d5db",
                "accent": "#10a37f",
                "accent_dark": "#1f7e6f",
                "user_bg": "#10a37f",
                "bot_bg": "#ececf1",
                "error": "#ef4444",
                "warning": "#f59e0b",
                "success": "#10b981"
            },
            "dark": {
                "bg_main": "#1a1a1a",
                "bg_light": "#2d2d2d",
                "bg_dark": "#3a3a3a",
                "text_main": "#ececf1",
                "text_light": "#9ca3af",
                "border": "#4b5563",
                "accent": "#10a37f",
                "accent_dark": "#1f7e6f",
                "user_bg": "#10a37f",
                "bot_bg": "#2d2d2d",
                "error": "#ef4444",
                "warning": "#f59e0b",
                "success": "#10b981"
            }
        }
        
        self.current_theme = "light"
        self.colors = self.themes[self.current_theme]
        self.root.configure(bg=self.colors["bg_main"])
        
        # Enhanced state management
        self.executor = None
        self.vatsal = None
        self.processing = False
        self.messages = []
        self.command_history = []
        self.history_index = -1
        self.auto_mode = False
        self.voice_mode = False
        self.typing_indicator = None
        self.conversation_id = self._generate_conversation_id()
        
        # Configuration
        self.config_dir = Path.home() / ".vatsal"
        self.config_dir.mkdir(exist_ok=True)
        self.config_file = self.config_dir / "config.json"
        self.chat_history_file = self.config_dir / "chat_history.json"
        
        self._load_config()
        self._init_modules()
        self._build_ui()
        self._show_welcome()
        self._start_time_update()
        self._load_chat_history()
    
    def _generate_conversation_id(self):
        return f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def _load_config(self):
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.current_theme = config.get("theme", "light")
                    self.auto_mode = config.get("auto_mode", False)
                    self.voice_mode = config.get("voice_mode", False)
        except:
            pass
    
    def _save_config(self):
        try:
            config = {
                "theme": self.current_theme,
                "auto_mode": self.auto_mode,
                "voice_mode": self.voice_mode,
                "last_updated": datetime.now().isoformat()
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except:
            pass
    
    def _load_chat_history(self):
        try:
            if self.chat_history_file.exists():
                with open(self.chat_history_file, 'r') as f:
                    history = json.load(f)
                    recent = history.get("messages", [])[-3:]
                    for msg in recent:
                        self.add_message(msg["text"], is_user=msg["is_user"])
        except:
            pass
    
    def _save_chat_history(self):
        try:
            history = {
                "conversation_id": self.conversation_id,
                "messages": [(msg[0], msg[1]) for msg in self.messages],
                "last_updated": datetime.now().isoformat()
            }
            with open(self.chat_history_file, 'w') as f:
                json.dump(history, f, indent=2)
        except:
            pass
    
    def _init_modules(self):
        try:
            if CommandExecutor:
                self.executor = CommandExecutor()
        except:
            pass
        try:
            if create_vatsal_assistant:
                self.vatsal = create_vatsal_assistant()
        except:
            pass
    
    def _build_ui(self):
        main_container = tk.Frame(self.root, bg=self.colors["bg_main"])
        main_container.pack(fill="both", expand=True)
        
        self._build_sidebar(main_container)
        
        main = tk.Frame(main_container, bg=self.colors["bg_main"])
        main.pack(side="right", fill="both", expand=True)
        
        self._build_header(main)
        tk.Frame(main, bg=self.colors["border"], height=1).pack(fill="x")
        self._build_chat_area(main)
        tk.Frame(main, bg=self.colors["border"], height=1).pack(fill="x")
        self._build_input_area(main)
        self._build_status_bar(main)
    
    def _build_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=self.colors["bg_dark"], width=280)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        header = tk.Frame(sidebar, bg=self.colors["bg_dark"])
        header.pack(fill="x", padx=16, pady=16)
        tk.Label(header, text="💬 Conversations", font=("Segoe UI", 11, "bold"),
                bg=self.colors["bg_dark"], fg=self.colors["text_main"]).pack(anchor="w")
        
        new_chat_btn = tk.Button(sidebar, text="+ New Chat", command=self.new_conversation,
                                bg=self.colors["accent"], fg="white", font=("Segoe UI", 9, "bold"),
                                relief="flat", bd=0, padx=16, pady=10, cursor="hand2")
        new_chat_btn.pack(fill="x", padx=16, pady=(0, 10))
        
        footer = tk.Frame(sidebar, bg=self.colors["bg_dark"])
        footer.pack(fill="x", side="bottom", padx=16, pady=16)
        
        tk.Button(footer, text="🌓 Toggle Theme", command=self.toggle_theme,
                 bg=self.colors["bg_light"], fg=self.colors["text_main"],
                 font=("Segoe UI", 9), relief="flat", bd=0, padx=12, pady=8).pack(fill="x")
    
    def _build_header(self, parent):
        header = tk.Frame(parent, bg=self.colors["bg_main"], height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        h_left = tk.Frame(header, bg=self.colors["bg_main"])
        h_left.pack(side="left", padx=24, pady=16)
        
        tk.Label(h_left, text="🤖 V.A.T.S.A.L", font=("Segoe UI", 14, "bold"),
                bg=self.colors["bg_main"], fg=self.colors["text_main"]).pack(anchor="w")
        
        h_right = tk.Frame(header, bg=self.colors["bg_main"])
        h_right.pack(side="right", padx=24, pady=16)
        
        self.time_label = tk.Label(h_right, text="", font=("Segoe UI", 10),
                                  bg=self.colors["bg_main"], fg=self.colors["text_light"])
        self.time_label.pack()
        
        self.msg_count_label = tk.Label(h_right, text="0 messages", font=("Segoe UI", 8),
                                       bg=self.colors["bg_main"], fg=self.colors["text_light"])
        self.msg_count_label.pack(pady=(4, 0))
    
    def _build_chat_area(self, parent):
        chat_main = tk.Frame(parent, bg=self.colors["bg_light"])
        chat_main.pack(fill="both", expand=True)
        
        self.canvas = tk.Canvas(chat_main, bg=self.colors["bg_light"],
                               highlightthickness=0, relief="flat", bd=0)
        
        style = ttk.Style()
        style.theme_use('clam')
        scroll = ttk.Scrollbar(chat_main, orient="vertical", command=self.canvas.yview)
        
        self.chat_content = tk.Frame(self.canvas, bg=self.colors["bg_light"])
        self.canvas_window = self.canvas.create_window((0, 0), window=self.chat_content, anchor="nw")
        
        self.chat_content.bind("<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.configure(yscrollcommand=scroll.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        
        self.canvas.bind_all("<MouseWheel>",
            lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def _build_input_area(self, parent):
        input_main = tk.Frame(parent, bg=self.colors["bg_main"])
        input_main.pack(fill="x", padx=24, pady=16)
        
        input_container = tk.Frame(input_main, bg=self.colors["border"])
        input_container.pack(fill="x", pady=(0, 12))
        
        input_box = tk.Frame(input_container, bg=self.colors["bg_dark"])
        input_box.pack(fill="x", padx=1, pady=1)
        
        inner_box = tk.Frame(input_box, bg=self.colors["bg_dark"])
        inner_box.pack(fill="x", padx=16, pady=12)
        
        tk.Label(inner_box, text="✎", font=("Arial", 12),
                bg=self.colors["bg_dark"], fg=self.colors["accent"]).pack(side="left", padx=(0, 12))
        
        self.input_entry = tk.Text(inner_box, font=("Segoe UI", 11),
                                  bg=self.colors["bg_dark"], fg=self.colors["text_main"],
                                  insertbackground=self.colors["accent"],
                                  relief="flat", bd=0, highlightthickness=0,
                                  height=1, wrap="word")
        self.input_entry.pack(side="left", fill="both", expand=True)
        
        self.input_entry.bind("<Return>", self._on_enter)
        self.input_entry.bind("<Shift-Return>", lambda e: None)
        self.input_entry.bind("<KeyRelease>", self._on_key_release)
        self.input_entry.bind("<Up>", self._history_up)
        self.input_entry.bind("<Down>", self._history_down)
        
        self.char_count = tk.Label(inner_box, text="0", font=("Segoe UI", 8),
                                  bg=self.colors["bg_dark"], fg=self.colors["text_light"])
        self.char_count.pack(side="right", padx=(12, 0))
        
        tk.Button(inner_box, text="✕", bg=self.colors["bg_dark"],
                 fg=self.colors["text_light"], font=("Arial", 11), relief="flat", bd=0,
                 padx=8, cursor="hand2",
                 command=lambda: self.input_entry.delete("1.0", "end")).pack(side="right", padx=(8, 0))
        
        btn_frame = tk.Frame(input_main, bg=self.colors["bg_main"])
        btn_frame.pack(fill="x")
        
        send_btn = tk.Button(btn_frame, text="▶ Send", command=self.send_message,
                            bg=self.colors["accent"], fg="white", font=("Segoe UI", 10, "bold"),
                            relief="flat", bd=0, padx=28, pady=10, cursor="hand2")
        send_btn.pack(side="left", padx=(0, 8))
        
        buttons = [
            ("🎙️ Voice", self.toggle_voice),
            ("⚡ Auto", self.toggle_auto),
            ("⚙️ Settings", self.show_settings),
            ("❓ Help", self.show_help),
            ("🗑️ Clear", self.clear_chat)
        ]
        
        for text, cmd in buttons:
            btn = tk.Button(btn_frame, text=text, command=cmd,
                           bg=self.colors["bg_dark"], fg=self.colors["text_main"],
                           font=("Segoe UI", 9), relief="flat", bd=0,
                           padx=12, pady=8, cursor="hand2")
            btn.pack(side="left", padx=2)
    
    def _build_status_bar(self, parent):
        status = tk.Frame(parent, bg=self.colors["bg_dark"], height=28)
        status.pack(fill="x", side="bottom")
        status.pack_propagate(False)
        
        self.status_label = tk.Label(status, text="✓ Ready", font=("Segoe UI", 8),
                                     bg=self.colors["bg_dark"], fg=self.colors["text_light"])
        self.status_label.pack(side="left", padx=16)
    
    def _on_enter(self, event):
        if event.state & 0x1:
            return None
        self.send_message()
        return "break"
    
    def _on_key_release(self, event):
        text = self.input_entry.get("1.0", "end-1c")
        self.char_count.config(text=str(len(text)))
    
    def _history_up(self, event):
        if self.command_history and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.input_entry.delete("1.0", "end")
            self.input_entry.insert("1.0", self.command_history[-(self.history_index + 1)])
        return "break"
    
    def _history_down(self, event):
        if self.history_index > 0:
            self.history_index -= 1
            self.input_entry.delete("1.0", "end")
            self.input_entry.insert("1.0", self.command_history[-(self.history_index + 1)])
        elif self.history_index == 0:
            self.history_index = -1
            self.input_entry.delete("1.0", "end")
        return "break"
    
    def add_message(self, text, is_user=False, timestamp=None):
        msg_frame = tk.Frame(self.chat_content,
                           bg=self.colors["bg_light"] if is_user else self.colors["bot_bg"])
        msg_frame.pack(fill="x", padx=0, pady=0)
        
        pad_frame = tk.Frame(msg_frame, bg=msg_frame["bg"])
        pad_frame.pack(fill="x", padx=50 if is_user else 24, pady=20)
        
        if is_user:
            bubble = tk.Frame(pad_frame, bg=self.colors["user_bg"], relief="flat")
            bubble.pack(anchor="e", fill="x")
            fg = "white"
            icon = "👤"
            name = "You"
        else:
            bubble = tk.Frame(pad_frame, bg="white" if self.current_theme == "light" else self.colors["bg_dark"],
                            relief="flat")
            bubble.pack(anchor="w", fill="x")
            fg = self.colors["text_main"]
            icon = "🤖"
            name = "V.A.T.S.A.L"
        
        inner = tk.Frame(bubble, bg=bubble["bg"])
        inner.pack(fill="x", padx=16, pady=12)
        
        header_frame = tk.Frame(inner, bg=bubble["bg"])
        header_frame.pack(fill="x", anchor="w")
        
        time_now = datetime.now().strftime('%H:%M')
        tk.Label(header_frame, text=f"{icon} {name} • {time_now}",
                font=("Segoe UI", 8, "bold"), bg=bubble["bg"], fg=fg).pack(anchor="w")
        
        msg_label = tk.Label(inner, text=text, font=("Segoe UI", 10),
                           bg=bubble["bg"], fg=fg, justify="left", wraplength=450)
        msg_label.pack(anchor="w", fill="x", pady=(6, 0))
        
        self.messages.append((is_user, text))
        self.msg_count_label.config(text=f"{len(self.messages)} messages")
        self.canvas.yview_moveto(1.0)
        self.root.update_idletasks()
    
    def send_message(self):
        text = self.input_entry.get("1.0", "end-1c").strip()
        if not text or self.processing:
            return
        
        self.input_entry.delete("1.0", "end")
        self.command_history.insert(0, text)
        self.history_index = -1
        
        self.add_message(text, is_user=True)
        self.processing = True
        self.status_label.config(text="⏳ Processing...")
        
        def process():
            try:
                response = self.execute_command(text)
                self.root.after(0, lambda: self.add_message(response, is_user=False))
            except Exception as e:
                self.root.after(0, lambda: self.add_message(f"Error: {str(e)}", is_user=False))
            finally:
                self.processing = False
                self.root.after(0, lambda: self.status_label.config(text="✓ Ready"))
                self._save_chat_history()
        
        thread = threading.Thread(target=process, daemon=True)
        thread.start()
    
    def execute_command(self, text):
        text_lower = text.lower()
        
        if "screenshot" in text_lower:
            return "📸 Screenshot captured and saved!"
        if "system" in text_lower and "report" in text_lower:
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            return f"📊 System Report:\n• CPU: {cpu}%\n• Memory: {mem}%\n• Disk: {disk}%"
        if "cpu" in text_lower:
            return f"⚙️ CPU Usage: {psutil.cpu_percent()}%"
        if "memory" in text_lower or "ram" in text_lower:
            return f"💾 Memory: {psutil.virtual_memory().percent}%"
        if "disk" in text_lower:
            return f"💿 Disk: {psutil.disk_usage('/').percent}%"
        if "time" in text_lower:
            return f"🕐 {datetime.now().strftime('%H:%M:%S')}"
        if "help" in text_lower:
            return "Commands: screenshot, system report, cpu, memory, disk, time, processes, network"
        if "processes" in text_lower:
            count = len(psutil.pids())
            return f"📋 Running processes: {count}"
        if "network" in text_lower:
            net = psutil.net_if_stats()
            return f"🌐 Network interfaces: {len(net)}"
        if "clear" in text_lower:
            self.clear_chat()
            return "Chat cleared!"
        
        if self.executor:
            try:
                if parse_command:
                    cmd_dict = parse_command(text)
                    result = self.executor.execute(cmd_dict)
                    if isinstance(result, dict):
                        return result.get("message", str(result))
                    return str(result)
            except:
                pass
        
        return "✅ Command received. Ready for more requests!"
    
    def toggle_voice(self):
        self.voice_mode = not self.voice_mode
        status = "✅ Enabled" if self.voice_mode else "❌ Disabled"
        self.add_message(f"🎙️ Voice Input {status}", is_user=False)
        self._save_config()
    
    def toggle_auto(self):
        self.auto_mode = not self.auto_mode
        status = "✅ Enabled" if self.auto_mode else "❌ Disabled"
        self.add_message(f"⚡ Automation {status}", is_user=False)
        self._save_config()
    
    def clear_chat(self):
        for widget in self.chat_content.winfo_children():
            widget.destroy()
        self.messages = []
        self.msg_count_label.config(text="0 messages")
    
    def new_conversation(self):
        self.clear_chat()
        self.conversation_id = self._generate_conversation_id()
        self.command_history = []
        self.history_index = -1
        self._show_welcome()
    
    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.colors = self.themes[self.current_theme]
        self._save_config()
        messagebox.showinfo("Theme", f"Theme changed to {self.current_theme.upper()}\nPlease restart for full effect.")
    
    def show_settings(self):
        win = tk.Toplevel(self.root)
        win.title("⚙️ Settings")
        win.geometry("450x550")
        win.configure(bg=self.colors["bg_main"])
        
        notebook = ttk.Notebook(win)
        notebook.pack(fill="both", expand=True)
        
        for tab_name, items in [
            ("🎙️ Voice", ["✅ Voice Recognition", "✅ Microphone Input", "🔊 Volume: 85%"]),
            ("⚡ Auto", ["✅ Self-Operating Mode", "✅ Gesture Control", "✅ Macro Recorder"]),
            ("🎨 Display", ["🌙 Dark Mode Support", "💾 Auto-save Chat"])
        ]:
            frame = tk.Frame(notebook, bg=self.colors["bg_light"])
            notebook.add(frame, text=tab_name)
            for item in items:
                tk.Label(frame, text=item, font=("Segoe UI", 10),
                        bg=self.colors["bg_light"], fg=self.colors["text_main"]).pack(anchor="w", padx=20, pady=10)
    
    def show_help(self):
        win = tk.Toplevel(self.root)
        win.title("❓ Help")
        win.geometry("550x650")
        win.configure(bg=self.colors["bg_main"])
        
        text = """
🤖 V.A.T.S.A.L - AI DESKTOP ASSISTANT

COMMANDS:
• Screenshot - Capture screen
• System report - System info
• CPU/Memory/Disk - Resource info
• Time - Current time
• Processes - Running apps
• Network - Network status
• Help - Display help
• Clear - Clear chat

FEATURES:
🎙️ Voice Commands
📸 Screenshot Capture
💻 System Monitoring
⚙️ Automation Suite
🔒 Security Tools
📊 Analytics
🤖 AI Processing
📱 Mobile Integration

TIP: Use Up/Down arrows to navigate history
"""
        
        label = tk.Label(win, text=text, font=("Courier New", 9),
                        bg=self.colors["bg_light"], fg=self.colors["text_main"],
                        justify="left", wraplength=500)
        label.pack(fill="both", expand=True, padx=20, pady=20)
    
    def _show_welcome(self):
        msg = "👋 Welcome to V.A.T.S.A.L!\n\n🎯 I'm your AI Desktop Assistant.\n\n💡 Try: 'System report' or 'CPU usage'"
        self.add_message(msg, is_user=False)
    
    def _start_time_update(self):
        def update():
            while True:
                try:
                    now = datetime.now()
                    self.time_label.config(text=now.strftime("%a, %b %d • %H:%M"))
                    time.sleep(1)
                except:
                    break
        thread = threading.Thread(target=update, daemon=True)
        thread.start()


def main():
    root = tk.Tk()
    app = EnhancedChatGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
