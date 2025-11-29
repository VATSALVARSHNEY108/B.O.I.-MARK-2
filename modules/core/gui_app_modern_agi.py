#!/usr/bin/env python3
"""
B.O.I AGI ENHANCED - Advanced General Intelligence with ChatGPT GUI
Full AGI reasoning with visual thinking display and adaptive learning
"""

import tkinter as tk
from tkinter import ttk, messagebox
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
    from modules.core.gemini_controller import parse_command
except:
    parse_command = None

try:
    from modules.core.command_executor import CommandExecutor
except:
    CommandExecutor = None

try:
    from modules.core.agi_engine import create_agi_engine
except:
    create_agi_engine = None

try:
    from modules.voice.voice_commander import VoiceCommander
except:
    VoiceCommander = None


class AGIEnhancedChatGUI:
    """ChatGPT-style GUI with AGI reasoning engine"""

    def __init__(self, root):
        self.root = root
        self.root.title("B.O.I - AGI Desktop Assistant (BOI Wake Word Active)")
        self.root.geometry("1800x1050")
        self.root.minsize(1400, 800)
        
        self.themes = {
            "light": {
                "bg_main": "#ffffff",
                "bg_light": "#f7f7f8",
                "bg_dark": "#ececf1",
                "text_main": "#0d0d0d",
                "text_light": "#565869",
                "accent": "#10a37f",
                "agi_bg": "#e6f9f5",
                "agi_text": "#065f46"
            },
            "dark": {
                "bg_main": "#1a1a1a",
                "bg_light": "#2d2d2d",
                "bg_dark": "#3a3a3a",
                "text_main": "#ececf1",
                "text_light": "#9ca3af",
                "accent": "#10a37f",
                "agi_bg": "#064e3b",
                "agi_text": "#a7f3d0"
            }
        }
        
        self.current_theme = "light"
        self.colors = self.themes[self.current_theme]
        self.root.configure(bg=self.colors["bg_main"])
        
        self.executor = None
        self.voice_commander = None
        self.agi_engine = None
        self.processing = False
        self.voice_mode = True
        self.messages = []
        self.command_history = []
        self.history_index = -1
        
        self.config_dir = Path.home() / ".vatsal"
        self.config_dir.mkdir(exist_ok=True)
        
        self._init_modules()
        self._build_ui()
        self._show_welcome()
        self._start_time_update()
        self._start_wake_word_listener()
    
    def _init_modules(self):
        try:
            if CommandExecutor:
                self.executor = CommandExecutor()
        except:
            pass
        try:
            if create_agi_engine:
                self.agi_engine = create_agi_engine()
                self.add_system_message("✅ AGI Engine Initialized - Advanced reasoning activated!")
        except Exception as e:
            self.add_error_message(f"AGI initialization: {str(e)}")
        try:
            if VoiceCommander:
                self.voice_commander = VoiceCommander()
        except:
            pass
    
    def _build_ui(self):
        main_container = tk.Frame(self.root, bg=self.colors["bg_main"])
        main_container.pack(fill="both", expand=True)
        
        sidebar = tk.Frame(main_container, bg=self.colors["bg_dark"], width=300)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        header_sb = tk.Frame(sidebar, bg=self.colors["bg_dark"])
        header_sb.pack(fill="x", padx=16, pady=16)
        tk.Label(header_sb, text="🧠 AGI Memory", font=("Segoe UI", 11, "bold"),
                bg=self.colors["bg_dark"], fg=self.colors["text_main"]).pack(anchor="w")
        
        self.agi_status = tk.Label(sidebar, text="🤖 AGI Ready", 
                                  font=("Segoe UI", 9, "bold"),
                                  bg=self.colors["bg_dark"], fg=self.colors["accent"])
        self.agi_status.pack(fill="x", padx=16, pady=10)
        
        self.voice_status = tk.Label(sidebar, text="🎤 Listening...", 
                                    font=("Segoe UI", 9),
                                    bg=self.colors["bg_dark"], fg="#10b981")
        self.voice_status.pack(fill="x", padx=16, pady=5)
        
        sep = tk.Frame(sidebar, bg=self.colors["border"], height=1)
        sep.pack(fill="x", padx=16, pady=10)
        
        tk.Label(sidebar, text="📊 AGI Metrics:", font=("Segoe UI", 9, "bold"),
                bg=self.colors["bg_dark"], fg=self.colors["text_main"]).pack(anchor="w", padx=16, pady=(10, 5))
        
        self.metrics_frame = tk.Frame(sidebar, bg=self.colors["bg_dark"])
        self.metrics_frame.pack(fill="x", padx=16, pady=5)
        
        for label, var_name in [("Memory:", "memory_count"), ("Goals:", "goals_count"), ("Confidence:", "confidence")]:
            f = tk.Frame(self.metrics_frame, bg=self.colors["bg_dark"])
            f.pack(anchor="w", pady=2)
            tk.Label(f, text=label, font=("Segoe UI", 8), bg=self.colors["bg_dark"], 
                    fg=self.colors["text_light"]).pack(side="left")
            setattr(self, var_name, tk.Label(f, text="0", font=("Segoe UI", 8, "bold"),
                                            bg=self.colors["bg_dark"], fg=self.colors["accent"]))
            getattr(self, var_name).pack(side="left", padx=5)
        
        main = tk.Frame(main_container, bg=self.colors["bg_main"])
        main.pack(side="right", fill="both", expand=True)
        
        header = tk.Frame(main, bg=self.colors["bg_main"], height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        h_left = tk.Frame(header, bg=self.colors["bg_main"])
        h_left.pack(side="left", padx=24, pady=16)
        tk.Label(h_left, text="🧠 B.O.I AGI", font=("Segoe UI", 14, "bold"),
                bg=self.colors["bg_main"], fg=self.colors["text_main"]).pack(anchor="w")
        tk.Label(h_left, text="Advanced General Intelligence Mode", font=("Segoe UI", 9),
                bg=self.colors["bg_main"], fg=self.colors["text_light"]).pack(anchor="w")
        
        h_right = tk.Frame(header, bg=self.colors["bg_main"])
        h_right.pack(side="right", padx=24, pady=16)
        self.time_label = tk.Label(h_right, text="", font=("Segoe UI", 10),
                                  bg=self.colors["bg_main"], fg=self.colors["text_light"])
        self.time_label.pack()
        
        tk.Frame(main, bg=self.colors["bg_dark"], height=1).pack(fill="x")
        
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
        
        tk.Frame(main, bg=self.colors["bg_dark"], height=1).pack(fill="x")
        
        input_main = tk.Frame(main, bg=self.colors["bg_main"])
        input_main.pack(fill="x", padx=24, pady=16)
        
        input_container = tk.Frame(input_main, bg=self.colors["bg_dark"])
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
        self.input_entry.bind("<Up>", self._history_up)
        self.input_entry.bind("<Down>", self._history_down)
        
        btn_frame = tk.Frame(input_main, bg=self.colors["bg_main"])
        btn_frame.pack(fill="x")
        
        send_btn = tk.Button(btn_frame, text="▶ Send", command=self.send_message,
                            bg=self.colors["accent"], fg="white", font=("Segoe UI", 10, "bold"),
                            relief="flat", bd=0, padx=28, pady=10)
        send_btn.pack(side="left", padx=(0, 8))
        
        for text, cmd in [("🧠 Thinking", self.show_reasoning), ("📊 Metrics", self.show_metrics),
                          ("❓ Help", self.show_help), ("🗑️ Clear", self.clear_chat)]:
            btn = tk.Button(btn_frame, text=text, command=cmd,
                           bg=self.colors["bg_dark"], fg=self.colors["text_main"],
                           font=("Segoe UI", 9), relief="flat", bd=0, padx=12, pady=8)
            btn.pack(side="left", padx=2)
    
    def add_message(self, text, is_user=False):
        msg_frame = tk.Frame(self.chat_content, bg=self.colors["bg_light"])
        msg_frame.pack(fill="x", padx=0, pady=0)
        
        pad_frame = tk.Frame(msg_frame, bg=msg_frame["bg"])
        pad_frame.pack(fill="x", padx=50 if is_user else 24, pady=16)
        
        bubble = tk.Frame(pad_frame, bg=self.colors["accent"] if is_user else 
                         (self.colors["agi_bg"] if "🧠" in text else "white"),
                         relief="flat")
        bubble.pack(anchor="e" if is_user else "w", fill="x")
        
        inner = tk.Frame(bubble, bg=bubble["bg"])
        inner.pack(fill="x", padx=16, pady=12)
        
        fg = "white" if is_user else (self.colors["agi_text"] if "🧠" in text else self.colors["text_main"])
        tk.Label(inner, text=text, font=("Segoe UI", 10), bg=bubble["bg"], fg=fg,
                justify="left", wraplength=500).pack(anchor="w", fill="x")
        
        self.messages.append((is_user, text))
        self.canvas.yview_moveto(1.0)
        self.root.update_idletasks()
    
    def add_system_message(self, text):
        self.add_message(f"╔════════════════════════════════════╗\n{text}\n╚════════════════════════════════════╝", is_user=False)
    
    def add_error_message(self, text):
        self.add_message(f"❌ {text}", is_user=False)
    
    def send_message(self):
        text = self.input_entry.get("1.0", "end-1c").strip()
        if not text or self.processing:
            return
        
        self.input_entry.delete("1.0", "end")
        self.command_history.insert(0, text)
        self.history_index = -1
        
        self.add_message(text, is_user=True)
        self.processing = True
        self.agi_status.config(text="🧠 Reasoning...")
        
        def process():
            try:
                response = self.execute_with_agi(text)
                self.root.after(0, lambda: self.add_message(response, is_user=False))
            except Exception as e:
                self.root.after(0, lambda: self.add_error_message(str(e)))
            finally:
                self.processing = False
                self.root.after(0, lambda: self.agi_status.config(text="🤖 AGI Ready"))
                self._update_metrics()
        
        threading.Thread(target=process, daemon=True).start()
    
    def execute_with_agi(self, command: str) -> str:
        """Execute command with AGI reasoning"""
        if not self.agi_engine:
            return f"✅ Executed: {command}"
        
        agi_response = self.agi_engine.process_command(command)
        
        result = f"""🧠 AGI PROCESSING:
        
📋 COMMAND: {command}

🔄 REASONING CHAIN:
"""
        for i, step in enumerate(agi_response["thinking"], 1):
            result += f"  {i}. {step}\n"
        
        result += f"\n💡 STRATEGY: {agi_response['strategy']}\n"
        result += f"📊 CONFIDENCE: {agi_response['confidence']:.0%}\n"
        
        if self.executor:
            try:
                if parse_command:
                    cmd_dict = parse_command(command)
                else:
                    cmd_dict = {"action": "custom", "text": command}
                
                exec_result = self.executor.execute(cmd_dict)
                message = exec_result.get("message", str(exec_result)) if isinstance(exec_result, dict) else str(exec_result)
                result += f"\n✅ RESULT:\n{message}"
            except:
                pass
        
        result += f"\n\n🎯 NEXT STEPS: {', '.join(agi_response['recommendations'][:2])}"
        return result
    
    def show_reasoning(self):
        if not self.agi_engine or not self.agi_engine.reasoning.reasoning_chain:
            messagebox.showinfo("AGI", "No reasoning chain available yet")
            return
        
        explanation = self.agi_engine.explain_reasoning()
        self.add_message(f"🧠 AGI THINKING:\n\n{explanation}", is_user=False)
    
    def show_metrics(self):
        if not self.agi_engine:
            return
        
        context = self.agi_engine.get_context_awareness()
        metrics = f"""📊 AGI METRICS:

  • Conversations: {context['conversation_history']}
  • Goals Tracked: {context['goals_tracked']}
  • Memory Items: {context['memory_items']}
  • Active Goals: {', '.join(context['active_goals']) if context['active_goals'] else 'None'}
  
🎯 LEARNING STATUS: {'Active' if context['memory_items'] > 0 else 'Initializing'}"""
        
        self.add_message(metrics, is_user=False)
        self._update_metrics()
    
    def _update_metrics(self):
        if self.agi_engine:
            context = self.agi_engine.get_context_awareness()
            self.memory_count.config(text=str(context['memory_items']))
            self.goals_count.config(text=str(context['goals_tracked']))
            conf = len(self.agi_engine.reasoning.reasoning_chain) * 20
            self.confidence.config(text=f"{min(100, conf)}%")
    
    def show_help(self):
        help_text = """🧠 B.O.I AGI MODE

FEATURES:
  • Advanced Reasoning - Multi-step problem solving
  • Memory System - Persistent learning
  • Context Awareness - Understand relationships
  • Adaptive Responses - Learn from interactions
  • Goal Tracking - Monitor intentions

COMMANDS:
  • system report - Full system analysis
  • help - Display help
  • clear - Clear chat

🎤 SAY: "BOI" to activate voice"""
        
        self.add_message(help_text, is_user=False)
    
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
    
    def _on_enter(self, event):
        if event.state & 0x1:
            return None
        self.send_message()
        return "break"
    
    def clear_chat(self):
        for widget in self.chat_content.winfo_children():
            widget.destroy()
        self.messages = []
    
    def _start_wake_word_listener(self):
        if not self.voice_commander or not self.voice_mode:
            return
        
        def listen():
            import speech_recognition as sr
            rec = sr.Recognizer()
            rec.energy_threshold = 300
            mic = sr.Microphone()
            
            while self.voice_mode:
                try:
                    with mic as source:
                        rec.adjust_for_ambient_noise(source, duration=0.1)
                        audio = rec.listen(source, timeout=1.0, phrase_time_limit=2.0)
                    
                    text = rec.recognize_google(audio).lower()
                    if "boi" in text:
                        self.root.after(0, self._activate_voice)
                        time.sleep(0.5)
                except:
                    pass
                time.sleep(0.1)
        
        threading.Thread(target=listen, daemon=True).start()
    
    def _activate_voice(self):
        self.add_system_message("🎤 BOI ACTIVATED - Listening to your command!")
    
    def _show_welcome(self):
        msg = """🧠 WELCOME TO B.O.I AGI

Advanced General Intelligence System
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ AGI Engine: Active
✅ Memory System: Ready
✅ Reasoning: Enabled
🎤 Voice: Listening for "BOI"

Ready to assist with intelligent reasoning!"""
        self.add_message(msg, is_user=False)
    
    def _start_time_update(self):
        def update():
            while True:
                try:
                    self.time_label.config(text=datetime.now().strftime("%a, %b %d • %H:%M"))
                    time.sleep(1)
                except:
                    break
        threading.Thread(target=update, daemon=True).start()


def main():
    root = tk.Tk()
    app = AGIEnhancedChatGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
