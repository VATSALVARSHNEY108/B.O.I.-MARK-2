#!/usr/bin/env python3
"""
V.A.T.S.A.L - Modern ChatGPT GUI with BOI Wake Word + Voice Integration
Professional interface with wake word listening and voice command execution
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

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

try:
    from modules.core.gemini_controller import parse_command, get_ai_suggestion
except:
    parse_command = None
    get_ai_suggestion = None

try:
    from modules.core.command_executor import CommandExecutor
except:
    CommandExecutor = None

try:
    from modules.core.vatsal_assistant import create_vatsal_assistant
except:
    create_vatsal_assistant = None

try:
    from modules.voice.voice_commander import VoiceCommander
except:
    VoiceCommander = None


class EnhancedChatGUI:
    """ChatGPT-style GUI with BOI wake word + voice command integration"""

    def __init__(self, root):
        self.root = root
        self.root.title("V.A.T.S.A.L - AI Desktop Assistant (BOI Wake Word Active)")
        self.root.geometry("1600x950")
        self.root.minsize(1200, 700)
        
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
        
        self.executor = None
        self.vatsal = None
        self.voice_commander = None
        self.processing = False
        self.voice_active = False
        self.messages = []
        self.command_history = []
        self.history_index = -1
        self.auto_mode = False
        self.voice_mode = True  # Voice listening enabled by default
        self.conversation_id = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.config_dir = Path.home() / ".vatsal"
        self.config_dir.mkdir(exist_ok=True)
        
        self._load_config()
        self._init_modules()
        self._build_ui()
        self._show_welcome()
        self._start_time_update()
        self._start_wake_word_listener()
    
    def _load_config(self):
        try:
            config_file = self.config_dir / "config.json"
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    self.current_theme = config.get("theme", "light")
                    self.auto_mode = config.get("auto_mode", False)
                    self.voice_mode = config.get("voice_mode", True)
        except:
            pass
    
    def _save_config(self):
        try:
            config_file = self.config_dir / "config.json"
            config = {
                "theme": self.current_theme,
                "auto_mode": self.auto_mode,
                "voice_mode": self.voice_mode,
                "last_updated": datetime.now().isoformat()
            }
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
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
        try:
            if VoiceCommander:
                self.voice_commander = VoiceCommander()
                self.add_message("🎤 Voice system initialized. Say 'BOI' to wake me up!", is_user=False)
        except Exception as e:
            self.add_message(f"⚠️ Voice not available: {str(e)}", is_user=False)
    
    def _build_ui(self):
        main_container = tk.Frame(self.root, bg=self.colors["bg_main"])
        main_container.pack(fill="both", expand=True)
        
        sidebar = tk.Frame(main_container, bg=self.colors["bg_dark"], width=280)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        header_sb = tk.Frame(sidebar, bg=self.colors["bg_dark"])
        header_sb.pack(fill="x", padx=16, pady=16)
        tk.Label(header_sb, text="💬 Conversations", font=("Segoe UI", 11, "bold"),
                bg=self.colors["bg_dark"], fg=self.colors["text_main"]).pack(anchor="w")
        
        new_chat_btn = tk.Button(sidebar, text="+ New Chat", command=self.new_conversation,
                                bg=self.colors["accent"], fg="white", font=("Segoe UI", 9, "bold"),
                                relief="flat", bd=0, padx=16, pady=10)
        new_chat_btn.pack(fill="x", padx=16, pady=(0, 10))
        
        self.voice_status = tk.Label(sidebar, text="🎤 Listening for BOI...", 
                                    font=("Segoe UI", 9, "bold"),
                                    bg=self.colors["bg_dark"], fg=self.colors["success"])
        self.voice_status.pack(fill="x", padx=16, pady=10)
        
        main = tk.Frame(main_container, bg=self.colors["bg_main"])
        main.pack(side="right", fill="both", expand=True)
        
        header = tk.Frame(main, bg=self.colors["bg_main"], height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        h_left = tk.Frame(header, bg=self.colors["bg_main"])
        h_left.pack(side="left", padx=24, pady=16)
        tk.Label(h_left, text="🤖 V.A.T.S.A.L (BOI Wake Word Active)", font=("Segoe UI", 14, "bold"),
                bg=self.colors["bg_main"], fg=self.colors["text_main"]).pack(anchor="w")
        
        h_right = tk.Frame(header, bg=self.colors["bg_main"])
        h_right.pack(side="right", padx=24, pady=16)
        self.time_label = tk.Label(h_right, text="", font=("Segoe UI", 10),
                                  bg=self.colors["bg_main"], fg=self.colors["text_light"])
        self.time_label.pack()
        self.msg_count_label = tk.Label(h_right, text="0 messages", font=("Segoe UI", 8),
                                       bg=self.colors["bg_main"], fg=self.colors["text_light"])
        self.msg_count_label.pack(pady=(4, 0))
        
        tk.Frame(main, bg=self.colors["border"], height=1).pack(fill="x")
        
        chat_main = tk.Frame(main, bg=self.colors["bg_light"])
        chat_main.pack(fill="both", expand=True)
        
        self.canvas = tk.Canvas(chat_main, bg=self.colors["bg_light"],
                               highlightthickness=0, relief="flat", bd=0)
        scroll = ttk.Scrollbar(chat_main, orient="vertical", command=self.canvas.yview)
        
        self.chat_content = tk.Frame(self.canvas, bg=self.colors["bg_light"])
        self.canvas_window = self.canvas.create_window((0, 0), window=self.chat_content, anchor="nw")
        
        self.chat_content.bind("<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        self.canvas.configure(yscrollcommand=scroll.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        tk.Frame(main, bg=self.colors["border"], height=1).pack(fill="x")
        
        input_main = tk.Frame(main, bg=self.colors["bg_main"])
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
        self.input_entry.bind("<Up>", self._history_up)
        self.input_entry.bind("<Down>", self._history_down)
        
        self.char_count = tk.Label(inner_box, text="0", font=("Segoe UI", 8),
                                  bg=self.colors["bg_dark"], fg=self.colors["text_light"])
        self.char_count.pack(side="right", padx=(12, 0))
        self.input_entry.bind("<KeyRelease>", lambda e: self.char_count.config(text=str(len(self.input_entry.get("1.0", "end-1c")))))
        
        tk.Button(inner_box, text="✕", bg=self.colors["bg_dark"], fg=self.colors["text_light"],
                 font=("Arial", 11), relief="flat", bd=0, padx=8,
                 command=lambda: self.input_entry.delete("1.0", "end")).pack(side="right", padx=(8, 0))
        
        btn_frame = tk.Frame(input_main, bg=self.colors["bg_main"])
        btn_frame.pack(fill="x")
        
        send_btn = tk.Button(btn_frame, text="▶ Send Message", command=self.send_message,
                            bg=self.colors["accent"], fg="white", font=("Segoe UI", 10, "bold"),
                            relief="flat", bd=0, padx=28, pady=10)
        send_btn.pack(side="left", padx=(0, 8))
        
        self.voice_btn = tk.Button(btn_frame, text="🎤 Voice Record", command=self.manual_voice_record,
                                  bg=self.colors["bg_dark"], fg=self.colors["text_main"],
                                  font=("Segoe UI", 9), relief="flat", bd=0, padx=12, pady=8)
        self.voice_btn.pack(side="left", padx=2)
        
        for text, cmd in [("⚡ Auto", self.toggle_auto), ("⚙️ Settings", self.show_settings),
                          ("❓ Help", self.show_help), ("🗑️ Clear", self.clear_chat)]:
            btn = tk.Button(btn_frame, text=text, command=cmd,
                           bg=self.colors["bg_dark"], fg=self.colors["text_main"],
                           font=("Segoe UI", 9), relief="flat", bd=0, padx=12, pady=8)
            btn.pack(side="left", padx=2)
        
        status = tk.Frame(main, bg=self.colors["bg_dark"], height=28)
        status.pack(fill="x", side="bottom")
        status.pack_propagate(False)
        
        self.status_label = tk.Label(status, text="✓ Ready | 🎤 Wake word listening...", font=("Segoe UI", 8),
                                     bg=self.colors["bg_dark"], fg=self.colors["text_light"])
        self.status_label.pack(side="left", padx=16)
    
    def _start_wake_word_listener(self):
        """Start continuous BOI wake word listening in background"""
        if not self.voice_commander or not self.voice_mode:
            return
        
        def listen_for_wake_word():
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            recognizer.energy_threshold = 300
            mic = sr.Microphone()
            
            while self.voice_mode:
                try:
                    with mic as source:
                        recognizer.adjust_for_ambient_noise(source, duration=0.1)
                        audio = recognizer.listen(source, timeout=1.0, phrase_time_limit=2.0)
                    
                    text = recognizer.recognize_google(audio).lower()
                    
                    if "boi" in text or text == "boi":
                        self.root.after(0, lambda: self._on_wake_word_detected(text))
                        time.sleep(0.5)
                
                except sr.UnknownValueError:
                    pass
                except sr.RequestError:
                    pass
                except:
                    pass
                
                time.sleep(0.1)
        
        if VoiceCommander:
            threading.Thread(target=listen_for_wake_word, daemon=True).start()
    
    def _on_wake_word_detected(self, detected_text):
        """Called when BOI wake word is detected"""
        self.voice_active = True
        self.voice_status.config(text="🎤 BOI ACTIVATED!", fg=self.colors["warning"])
        self.status_label.config(text="🎤 Listening to command...")
        self.add_message("👂 BOI is listening... Please say your command!", is_user=False)
        
        def listen_for_command():
            try:
                import speech_recognition as sr
                recognizer = sr.Recognizer()
                recognizer.energy_threshold = 300
                mic = sr.Microphone()
                
                with mic as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    audio = recognizer.listen(source, timeout=10.0, phrase_time_limit=8.0)
                
                command = recognizer.recognize_google(audio)
                self.root.after(0, lambda: self._process_voice_command(command))
            
            except Exception as e:
                self.root.after(0, lambda: self.add_message(f"❌ Voice recognition failed: {str(e)}", is_user=False))
            finally:
                self.voice_active = False
                self.root.after(0, lambda: self._reset_voice_status())
        
        threading.Thread(target=listen_for_command, daemon=True).start()
    
    def _process_voice_command(self, command):
        """Process voice command through backend"""
        self.add_message(f"🎤 You said: {command}", is_user=True)
        
        self.processing = True
        self.status_label.config(text="⏳ Processing voice command...")
        
        def process():
            try:
                response = self.execute_backend(command)
                self.root.after(0, lambda: self.add_message(response, is_user=False))
            except Exception as e:
                self.root.after(0, lambda: self.add_message(f"❌ Error: {str(e)}", is_user=False))
            finally:
                self.processing = False
                self.root.after(0, lambda: self._reset_voice_status())
        
        threading.Thread(target=process, daemon=True).start()
    
    def _reset_voice_status(self):
        """Reset voice status after command"""
        self.voice_active = False
        self.voice_status.config(text="🎤 Listening for BOI...", fg=self.colors["success"])
        self.status_label.config(text="✓ Ready | 🎤 Wake word listening...")
    
    def manual_voice_record(self):
        """Manually record voice command"""
        if self.voice_active or self.processing:
            messagebox.showwarning("Busy", "Please wait for current operation")
            return
        
        self.add_message("🎤 Recording... (Speak now!)", is_user=False)
        self._on_wake_word_detected("manual")
    
    def _on_enter(self, event):
        if event.state & 0x1:
            return None
        self.send_message()
        return "break"
    
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
    
    def add_message(self, text, is_user=False):
        msg_frame = tk.Frame(self.chat_content,
                           bg=self.colors["bg_light"] if is_user else self.colors["bot_bg"])
        msg_frame.pack(fill="x", padx=0, pady=0)
        
        pad_frame = tk.Frame(msg_frame, bg=msg_frame["bg"])
        pad_frame.pack(fill="x", padx=50 if is_user else 24, pady=20)
        
        bubble = tk.Frame(pad_frame, bg=self.colors["user_bg"] if is_user else 
                         ("white" if self.current_theme == "light" else self.colors["bg_dark"]),
                         relief="flat")
        bubble.pack(anchor="e" if is_user else "w", fill="x")
        
        inner = tk.Frame(bubble, bg=bubble["bg"])
        inner.pack(fill="x", padx=16, pady=12)
        
        fg = "white" if is_user else self.colors["text_main"]
        icon = "👤" if is_user else "🤖"
        name = "You" if is_user else "V.A.T.S.A.L"
        
        time_str = datetime.now().strftime('%H:%M')
        tk.Label(inner, text=f"{icon} {name} • {time_str}", font=("Segoe UI", 8, "bold"),
                bg=bubble["bg"], fg=fg).pack(anchor="w")
        
        tk.Label(inner, text=text, font=("Segoe UI", 10), bg=bubble["bg"], fg=fg,
                justify="left", wraplength=450).pack(anchor="w", fill="x", pady=(6, 0))
        
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
                response = self.execute_backend(text)
                self.root.after(0, lambda: self.add_message(response, is_user=False))
            except Exception as e:
                self.root.after(0, lambda: self.add_message(f"❌ Error: {str(e)}", is_user=False))
            finally:
                self.processing = False
                self.root.after(0, lambda: self.status_label.config(text="✓ Ready"))
        
        threading.Thread(target=process, daemon=True).start()
    
    def execute_backend(self, text):
        """Execute command via gui_app.py backend"""
        text_lower = text.lower()
        
        if text_lower in ["clear", "cls"]:
            self.clear_chat()
            return "✓ Chat cleared!"
        
        if "help" in text_lower:
            return """Available Commands:
• system report / cpu / memory / disk
• take screenshot
• processes / network
• weather / news / search
• settings / stats / help
• clear / time"""
        
        try:
            if parse_command:
                cmd_dict = parse_command(text)
            else:
                cmd_dict = {"action": "custom", "text": text}
            
            if self.executor:
                result = self.executor.execute(cmd_dict)
                if isinstance(result, dict):
                    return result.get("message", str(result))
                return str(result)
            
            if self.vatsal:
                return self.vatsal.acknowledge_command(text)
            
            return f"✅ Command processed: {text}"
        
        except Exception as e:
            return f"⚠️ Error: {str(e)}\n\nTry: 'help' for commands"
    
    def toggle_auto(self):
        self.auto_mode = not self.auto_mode
        self.add_message(f"⚡ Automation {'✓ Enabled' if self.auto_mode else '✗ Disabled'}", is_user=False)
        self._save_config()
    
    def clear_chat(self):
        for widget in self.chat_content.winfo_children():
            widget.destroy()
        self.messages = []
        self.msg_count_label.config(text="0 messages")
    
    def new_conversation(self):
        self.clear_chat()
        self.conversation_id = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self._show_welcome()
    
    def show_settings(self):
        win = tk.Toplevel(self.root)
        win.title("⚙️ Settings")
        win.geometry("450x400")
        win.configure(bg=self.colors["bg_main"])
        
        notebook = ttk.Notebook(win)
        notebook.pack(fill="both", expand=True)
        
        for tab_name, items in [("🎤 Voice", ["✓ Wake word: BOI", "✓ Microphone Active", "✓ Google Speech API"]),
                                ("⚡ Auto", ["✓ Self-Operating", "✓ Gesture Control"]),
                                ("🎨 Display", ["✓ Dark Mode", "✓ Auto-save"])]:
            frame = tk.Frame(notebook, bg=self.colors["bg_light"])
            notebook.add(frame, text=tab_name)
            for item in items:
                tk.Label(frame, text=item, font=("Segoe UI", 10),
                        bg=self.colors["bg_light"], fg=self.colors["text_main"]).pack(anchor="w", padx=20, pady=10)
    
    def show_help(self):
        win = tk.Toplevel(self.root)
        win.title("❓ Help - BOI Wake Word")
        win.geometry("500x600")
        win.configure(bg=self.colors["bg_main"])
        
        text = """V.A.T.S.A.L - BOI Wake Word System

🎤 VOICE ACTIVATION:
• Say "BOI" to wake me up
• I'll start listening for your command
• Speak your command naturally
• Results appear instantly

SYSTEM COMMANDS:
• system report - Full system info
• cpu usage - CPU statistics
• memory - RAM usage
• disk - Disk usage
• processes - Running apps
• network - Network status

ACTION COMMANDS:
• take screenshot - Capture screen
• weather - Weather report
• news - Latest news
• search - Web search
• time - Current time

UI COMMANDS:
• help - Display help
• settings - Open settings
• clear - Clear chat

Use arrow keys to navigate history."""
        
        label = tk.Label(win, text=text, font=("Courier New", 9),
                        bg=self.colors["bg_light"], fg=self.colors["text_main"],
                        justify="left", wraplength=450)
        label.pack(fill="both", expand=True, padx=20, pady=20)
    
    def _show_welcome(self):
        msg = "👋 Welcome to V.A.T.S.A.L with BOI Wake Word!\n\n🎤 Say 'BOI' to activate voice commands\n💡 Or type manually below\n⚠️ Make sure microphone is enabled"
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
        threading.Thread(target=update, daemon=True).start()


def main():
    root = tk.Tk()
    app = EnhancedChatGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
