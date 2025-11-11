#!/usr/bin/env python3
"""
GUI Voice Diagnostic Tool
Tests microphone and voice recognition in Tkinter GUI
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import os
import sys

class VoiceDiagnosticGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎤 Voice & Microphone Diagnostic")
        self.root.geometry("900x700")
        self.root.configure(bg="#0a0a0a")
        
        # Check if running on Replit
        self.is_replit = os.environ.get('REPL_ID') is not None
        self.is_testing = False
        
        self.setup_ui()
        self.run_initial_checks()
    
    def setup_ui(self):
        """Setup the diagnostic interface"""
        
        # Header
        header = tk.Label(
            self.root,
            text="🎤 VOICE & MICROPHONE DIAGNOSTIC",
            font=("Arial", 20, "bold"),
            bg="#0a0a0a",
            fg="#00d4ff"
        )
        header.pack(pady=10)
        
        # Environment warning
        if self.is_replit:
            warning_frame = tk.Frame(self.root, bg="#3a1a1a", relief="solid", borderwidth=2)
            warning_frame.pack(fill="x", padx=20, pady=10)
            
            warning_label = tk.Label(
                warning_frame,
                text="⚠️ RUNNING ON CLOUD SERVER (Replit)\nServer cannot access your laptop's microphone!",
                font=("Arial", 12, "bold"),
                bg="#3a1a1a",
                fg="#ff6b6b",
                justify="left"
            )
            warning_label.pack(pady=10, padx=10)
            
            solution_label = tk.Label(
                warning_frame,
                text="💡 SOLUTION: Run this app on your LOCAL laptop to use microphone!",
                font=("Arial", 11),
                bg="#3a1a1a",
                fg="#00ff88"
            )
            solution_label.pack(pady=5, padx=10)
        
        # Status display
        status_frame = tk.LabelFrame(
            self.root,
            text="📊 Diagnostic Results",
            font=("Arial", 12, "bold"),
            bg="#1a1a1a",
            fg="#00d4ff",
            relief="groove",
            borderwidth=2
        )
        status_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Scrolled text for results
        self.result_text = scrolledtext.ScrolledText(
            status_frame,
            font=("Courier", 10),
            bg="#000000",
            fg="#00ff88",
            insertbackground="#00d4ff",
            height=20
        )
        self.result_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Button frame
        button_frame = tk.Frame(self.root, bg="#0a0a0a")
        button_frame.pack(pady=10)
        
        # Test microphone button
        self.test_btn = tk.Button(
            button_frame,
            text="🎤 TEST MICROPHONE",
            font=("Arial", 12, "bold"),
            bg="#00d4ff",
            fg="#000000",
            activebackground="#00ff88",
            command=self.test_microphone,
            width=20,
            height=2
        )
        self.test_btn.grid(row=0, column=0, padx=10)
        
        # List devices button
        list_btn = tk.Button(
            button_frame,
            text="📋 LIST DEVICES",
            font=("Arial", 12, "bold"),
            bg="#b19cd9",
            fg="#000000",
            activebackground="#00ff88",
            command=self.list_devices,
            width=20,
            height=2
        )
        list_btn.grid(row=0, column=1, padx=10)
        
        # Clear button
        clear_btn = tk.Button(
            button_frame,
            text="🗑️ CLEAR LOG",
            font=("Arial", 12, "bold"),
            bg="#ff6b6b",
            fg="#000000",
            activebackground="#ff9999",
            command=self.clear_log,
            width=20,
            height=2
        )
        clear_btn.grid(row=0, column=2, padx=10)
        
        # Instructions
        instructions = tk.Label(
            self.root,
            text="Click 'TEST MICROPHONE' to check if your voice input is working",
            font=("Arial", 10),
            bg="#0a0a0a",
            fg="#888888"
        )
        instructions.pack(pady=5)
    
    def log(self, message, color=None):
        """Add message to log"""
        self.result_text.insert(tk.END, message + "\n")
        self.result_text.see(tk.END)
        self.root.update()
    
    def clear_log(self):
        """Clear the log"""
        self.result_text.delete(1.0, tk.END)
    
    def run_initial_checks(self):
        """Run initial diagnostic checks"""
        self.log("=" * 70)
        self.log("🔍 INITIAL ENVIRONMENT CHECKS", "#00d4ff")
        self.log("=" * 70)
        
        # Check Python version
        python_version = sys.version.split()[0]
        self.log(f"\n✅ Python Version: {python_version}")
        
        # Check environment
        if self.is_replit:
            self.log("⚠️  Environment: REPLIT (Cloud Server)")
            self.log("   → Your laptop's microphone is NOT accessible here!")
            self.log("   → You need to run this app on your LOCAL machine")
        else:
            self.log("✅ Environment: Local Machine")
            self.log("   → Microphone should be accessible")
        
        # Check display
        display = os.environ.get('DISPLAY', 'Not set')
        self.log(f"\n📺 DISPLAY: {display}")
        
        # Check X authority
        xauth = os.path.exists(os.path.expanduser('~/.Xauthority'))
        if xauth:
            self.log("✅ X Server: Available")
        else:
            self.log("⚠️  X Server: Not available (expected on Replit)")
        
        # Check for PyAudio
        self.log("\n" + "=" * 70)
        self.log("🔍 CHECKING REQUIRED LIBRARIES")
        self.log("=" * 70)
        
        try:
            import pyaudio
            self.log("\n✅ PyAudio: INSTALLED")
            self.log(f"   Version: {pyaudio.__version__ if hasattr(pyaudio, '__version__') else 'Unknown'}")
        except ImportError:
            self.log("\n❌ PyAudio: NOT INSTALLED")
            self.log("   → Install with: pip install pyaudio")
            self.log("   → This is REQUIRED for microphone access")
        
        # Check SpeechRecognition
        try:
            import speech_recognition as sr
            self.log(f"\n✅ SpeechRecognition: INSTALLED")
            self.log(f"   Version: {sr.__version__}")
        except ImportError:
            self.log("\n❌ SpeechRecognition: NOT INSTALLED")
            self.log("   → Install with: pip install SpeechRecognition")
        
        self.log("\n" + "=" * 70)
        self.log("💡 Click 'TEST MICROPHONE' to test voice input")
        self.log("=" * 70 + "\n")
    
    def list_devices(self):
        """List all available audio devices"""
        self.log("\n" + "=" * 70)
        self.log("📋 LISTING AUDIO DEVICES")
        self.log("=" * 70)
        
        try:
            import speech_recognition as sr
            
            self.log("\nAvailable Microphones:")
            mic_list = sr.Microphone.list_microphone_names()
            
            if not mic_list:
                self.log("\n❌ NO MICROPHONES FOUND!")
                if self.is_replit:
                    self.log("\n💡 This is expected on Replit (cloud server)")
                    self.log("   Replit servers don't have physical microphones")
                    self.log("   You need to run this app LOCALLY on your laptop")
                else:
                    self.log("\n💡 Possible reasons:")
                    self.log("   1. No microphone connected")
                    self.log("   2. PyAudio not properly installed")
                    self.log("   3. Audio drivers missing")
            else:
                for idx, name in enumerate(mic_list):
                    self.log(f"   [{idx}] {name}")
                self.log(f"\n✅ Found {len(mic_list)} microphone(s)")
                
        except Exception as e:
            self.log(f"\n❌ ERROR: {e}")
            if "PyAudio" in str(e):
                self.log("\n💡 PyAudio is not installed!")
                self.log("   Install with: pip install pyaudio")
        
        self.log("=" * 70 + "\n")
    
    def test_microphone(self):
        """Test microphone in separate thread"""
        if self.is_testing:
            messagebox.showwarning("Test in Progress", "A test is already running!")
            return
        
        # Run test in thread to prevent GUI freeze
        thread = threading.Thread(target=self._test_microphone_thread, daemon=True)
        thread.start()
    
    def _test_microphone_thread(self):
        """Actual microphone test (runs in thread)"""
        self.is_testing = True
        self.test_btn.config(state="disabled", text="🔄 TESTING...")
        
        self.log("\n" + "=" * 70)
        self.log("🎤 TESTING MICROPHONE")
        self.log("=" * 70)
        
        try:
            import speech_recognition as sr
            
            self.log("\n✅ SpeechRecognition library loaded")
            
            # Try to access microphone
            self.log("\n🔌 Attempting to access microphone...")
            
            try:
                recognizer = sr.Recognizer()
                
                # Configure for better sensitivity
                recognizer.energy_threshold = 300
                recognizer.pause_threshold = 0.8
                
                self.log(f"📊 Energy Threshold: {recognizer.energy_threshold}")
                self.log(f"📊 Pause Threshold: {recognizer.pause_threshold}")
                
                with sr.Microphone() as source:
                    self.log("\n✅ Microphone accessed successfully!")
                    
                    self.log("\n🔊 Adjusting for ambient noise (2 seconds)...")
                    self.log("   Please wait quietly...")
                    recognizer.adjust_for_ambient_noise(source, duration=2)
                    
                    self.log(f"\n✅ Adjusted! New energy threshold: {recognizer.energy_threshold}")
                    
                    self.log("\n🎤 LISTENING NOW!")
                    self.log("=" * 70)
                    self.log(">>> SPEAK CLEARLY INTO YOUR MICROPHONE <<<")
                    self.log(">>> Say something like: 'Hello' or 'Testing' <<<")
                    self.log(">>> You have 10 seconds <<<")
                    self.log("=" * 70)
                    
                    # Show messagebox to alert user
                    self.root.after(0, lambda: messagebox.showinfo(
                        "🎤 Listening!", 
                        "SPEAK NOW!\n\nSay something clearly into your microphone.\n\nYou have 10 seconds.",
                        parent=self.root
                    ))
                    
                    # Listen
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=8)
                    
                    self.log("\n✅ Audio captured!")
                    self.log(f"📊 Audio data size: {len(audio.get_raw_data())} bytes")
                    
                    if len(audio.get_raw_data()) == 0:
                        self.log("\n⚠️  WARNING: Audio data is empty!")
                        self.log("   No sound was captured from microphone")
                    else:
                        self.log("\n🌐 Sending to Google Speech Recognition...")
                        
                        try:
                            text = recognizer.recognize_google(audio)
                            self.log("\n" + "🎉" * 35)
                            self.log(f"✅ SUCCESS! You said: '{text}'")
                            self.log("🎉" * 35)
                            self.log("\n✅ YOUR MICROPHONE IS WORKING PERFECTLY!")
                            
                            # Show success messagebox
                            self.root.after(0, lambda: messagebox.showinfo(
                                "🎉 Success!",
                                f"Your microphone works!\n\nYou said: '{text}'",
                                parent=self.root
                            ))
                            
                        except sr.UnknownValueError:
                            self.log("\n⚠️  Audio captured but couldn't understand speech")
                            self.log("\n💡 Try again and:")
                            self.log("   1. Speak LOUDER")
                            self.log("   2. Speak more CLEARLY")
                            self.log("   3. Reduce background noise")
                            self.log("   4. Get closer to microphone")
                            
                        except sr.RequestError as e:
                            self.log(f"\n❌ Google Speech Recognition error: {e}")
                            self.log("\n💡 Check your internet connection")
                
            except sr.WaitTimeoutError:
                self.log("\n❌ TIMEOUT - No speech detected!")
                self.log("\n💡 Possible issues:")
                self.log("   1. Microphone is MUTED")
                self.log("   2. Wrong microphone selected in system settings")
                self.log("   3. Microphone volume too LOW")
                self.log("   4. No microphone connected")
                if self.is_replit:
                    self.log("   5. Running on CLOUD SERVER (Replit) - can't access your mic!")
                
            except OSError as e:
                self.log(f"\n❌ OS ERROR: {e}")
                self.log("\n💡 This usually means:")
                self.log("   1. No audio input device available")
                if self.is_replit:
                    self.log("   2. You're on a CLOUD SERVER - microphone not accessible!")
                    self.log("\n🔧 SOLUTION:")
                    self.log("   → Download this app to your LAPTOP")
                    self.log("   → Run it LOCALLY (not on Replit)")
                    self.log("   → Then your laptop's microphone will work!")
                else:
                    self.log("   2. Audio drivers not installed")
                    self.log("   3. Microphone not connected")
                
        except ImportError as e:
            self.log(f"\n❌ IMPORT ERROR: {e}")
            if "speech_recognition" in str(e).lower():
                self.log("\n💡 Install SpeechRecognition:")
                self.log("   pip install SpeechRecognition")
            elif "pyaudio" in str(e).lower():
                self.log("\n💡 Install PyAudio:")
                self.log("   pip install pyaudio")
        
        except Exception as e:
            self.log(f"\n❌ UNEXPECTED ERROR: {e}")
            import traceback
            self.log("\nFull error:")
            self.log(traceback.format_exc())
        
        finally:
            self.log("\n" + "=" * 70)
            self.log("🏁 TEST COMPLETE")
            self.log("=" * 70 + "\n")
            
            self.is_testing = False
            self.test_btn.config(state="normal", text="🎤 TEST MICROPHONE")


def main():
    root = tk.Tk()
    app = VoiceDiagnosticGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
