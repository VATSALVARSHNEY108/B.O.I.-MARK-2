import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
from datetime import datetime
from dotenv import load_dotenv

from modules.core.command_executor import CommandExecutor
from modules.core.gemini_controller import parse_command
from modules.voice.feature_speaker import create_feature_speaker

load_dotenv()


class ModernBOIGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("V.A.T.S.A.L - AI Desktop Assistant")
        self.root.geometry("630x900")
        self.root.configure(bg="#F5F1E8")

        # Colors
        self.BG_PRIMARY = "#F5F1E8"
        self.BG_SECONDARY = "#FAF8F3"
        self.TEXT_PRIMARY = "#1a1a1a"
        self.ACTIVE_GREEN = "#007B55"
        self.CHAT_BG = "#ffffff"

        # State
        self.processing = False
        self.chat_messages = []

        # Initialize modules
        self.executor = CommandExecutor()
        self.speaker = create_feature_speaker() if os.getenv("GEMINI_API_KEY") else None

        # Build GUI
        self._create_gui()
        self._show_welcome()

    def _create_gui(self):
        """Create main GUI"""
        main = tk.Frame(self.root, bg=self.BG_PRIMARY)
        main.pack(fill="both", expand=True, padx=8, pady=8)

        # Header
        header = tk.Frame(main, bg=self.BG_SECONDARY)
        header.pack(fill="x", padx=10, pady=(0, 10))
        tk.Label(header, text="💬 BOI Chat", font=("Segoe UI", 14, "bold"), bg=self.BG_SECONDARY, fg=self.TEXT_PRIMARY).pack(side="left", padx=10, pady=8)

        # Input section
        input_frame = tk.Frame(main, bg=self.BG_SECONDARY, relief="solid", bd=1)
        input_frame.pack(fill="x", padx=5, pady=(0, 8))

        input_row = tk.Frame(input_frame, bg=self.BG_SECONDARY)
        input_row.pack(fill="x", padx=10, pady=10)

        self.input_field = tk.Entry(input_row, font=("Segoe UI", 10), bg="white", fg=self.TEXT_PRIMARY, relief="solid", bd=1)
        self.input_field.pack(side="left", fill="both", expand=True)
        self.input_field.bind("<Return>", lambda e: self.execute_command())

        btn_frame = tk.Frame(input_frame, bg=self.BG_SECONDARY)
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))

        tk.Button(btn_frame, text="Send", command=self.execute_command, bg=self.ACTIVE_GREEN, fg="white", font=("Segoe UI", 10, "bold"), padx=15, pady=5).pack(side="left", padx=(0, 5))
        tk.Button(btn_frame, text="Clear Chat", command=self.clear_chat, bg="#E74C3C", fg="white", font=("Segoe UI", 10, "bold"), padx=15, pady=5).pack(side="left")

        # Chat area
        chat_frame = tk.Frame(main, bg=self.CHAT_BG, relief="solid", bd=1)
        chat_frame.pack(fill="both", expand=True, padx=5)

        self.chat_canvas = tk.Canvas(chat_frame, bg=self.CHAT_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(chat_frame, orient="vertical", command=self.chat_canvas.yview)
        self.chat_scrollable = tk.Frame(self.chat_canvas, bg=self.CHAT_BG)

        self.chat_scrollable.bind("<Configure>", lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")))
        self.chat_canvas.create_window((0, 0), window=self.chat_scrollable, anchor="nw")
        self.chat_canvas.configure(yscrollcommand=scrollbar.set)

        self.chat_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.chat_canvas.bind_all("<MouseWheel>", lambda e: self.chat_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    def add_message(self, text, sender="BOI"):
        """Add message to chat with clear distinction"""
        row = tk.Frame(self.chat_scrollable, bg=self.CHAT_BG)
        row.pack(fill="x", padx=5, pady=5)

        if sender == "USER":
            # User message - RIGHT side, BLUE
            spacer = tk.Frame(row, bg=self.CHAT_BG)
            spacer.pack(side="left", fill="x", expand=True)

            bubble = tk.Frame(row, bg="#2196F3", relief="flat", bd=0)
            bubble.pack(side="right", padx=(0, 5))

            label = tk.Label(bubble, text="👤 YOU", bg="#2196F3", fg="white", font=("Segoe UI", 8, "bold"), padx=8, pady=3)
            label.pack(anchor="w")

            msg = tk.Label(bubble, text=text, bg="#2196F3", fg="white", font=("Segoe UI", 10, "bold"), justify="left", wraplength=250, padx=8, pady=6)
            msg.pack(anchor="w", fill="x")
        else:
            # BOI message - LEFT side, GREEN
            bubble = tk.Frame(row, bg="#4CAF50", relief="flat", bd=0)
            bubble.pack(side="left", padx=(5, 0))

            label = tk.Label(bubble, text="🤖 BOI", bg="#4CAF50", fg="white", font=("Segoe UI", 8, "bold"), padx=8, pady=3)
            label.pack(anchor="w")

            msg = tk.Label(bubble, text=text, bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"), justify="left", wraplength=250, padx=8, pady=6)
            msg.pack(anchor="w", fill="x")

            spacer = tk.Frame(row, bg=self.CHAT_BG)
            spacer.pack(side="left", fill="x", expand=True)

        self.chat_messages.append(row)
        self.root.after(50, lambda: self.chat_canvas.yview_moveto(1.0))

    def clear_chat(self):
        """Clear all chat messages"""
        for msg in self.chat_messages:
            msg.destroy()
        self.chat_messages.clear()
        self.add_message("✨ Chat cleared", sender="BOI")

    def execute_command(self):
        """Execute user command"""
        cmd = self.input_field.get().strip()
        if not cmd:
            return

        if self.processing:
            messagebox.showwarning("Busy", "Processing current command...")
            return

        self.input_field.delete(0, "end")
        self.add_message(cmd, sender="USER")

        self.processing = True
        thread = threading.Thread(target=self._execute_thread, args=(cmd,))
        thread.daemon = True
        thread.start()

    def _execute_thread(self, cmd):
        """Execute in thread"""
        try:
            parsed = parse_command(cmd)
            result = self.executor.execute(parsed)
            response = result.get("message", "Command executed")
            self.add_message(response, sender="BOI")
        except Exception as e:
            self.add_message(f"Error: {str(e)}", sender="BOI")
        finally:
            self.processing = False

    def _show_welcome(self):
        """Show welcome message"""
        if os.getenv("GEMINI_API_KEY"):
            self.add_message("✅ BOI Ready! Type commands to get started.", sender="BOI")
        else:
            self.add_message("⚠️ GEMINI_API_KEY not set!", sender="BOI")


def main():
    root = tk.Tk()
    app = ModernBOIGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
