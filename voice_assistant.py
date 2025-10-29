"""
Voice Assistant Module
Voice commands for hands-free automation control
"""

import speech_recognition as sr
import pyttsx3
import threading

class VoiceAssistant:
    def __init__(self, command_callback=None):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.command_callback = command_callback
        self.listening = False
        self.wake_word_enabled = True
        # Simple and easy wake words for quick activation
        self.wake_words = ["hello", "open", "search", "oye", "bhaiya", "bhaisahb"]
        # Action verbs that should be kept in the command
        self.action_wake_words = ["open", "search"]
        
        # Increase sensitivity settings
        self.recognizer.energy_threshold = 300  # Lower = more sensitive (default ~4000)
        self.recognizer.dynamic_energy_threshold = True  # Auto-adjust to ambient noise
        self.recognizer.dynamic_energy_adjustment_damping = 0.15  # Faster adaptation
        self.recognizer.dynamic_energy_ratio = 1.2  # Lower threshold for speech detection
        self.recognizer.pause_threshold = 0.5  # Shorter pause before phrase ends (default 0.8)
        
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        
        voices = self.engine.getProperty('voices')
        if len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)
    
    def speak(self, text):
        """Convert text to speech"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"❌ Speech failed: {str(e)}")
    
    def listen_once(self):
        """Listen for a single voice command"""
        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                # Quick ambient noise adjustment for faster response
                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                # Increased timeout and phrase limit for better detection
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=8)
                
                print("🔄 Processing...")
                command = self.recognizer.recognize_google(audio)
                print(f"✅ Heard: {command}")
                
                return command
        except sr.WaitTimeoutError:
            return "❌ No speech detected"
        except sr.UnknownValueError:
            return "❌ Could not understand audio"
        except sr.RequestError as e:
            return f"❌ Recognition service error: {str(e)}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def check_for_wake_word(self, text):
        """Check if the text starts with any wake word (as a standalone word)"""
        text_lower = text.lower().strip()
        words = text_lower.split()
        
        # Check if the first word matches any wake word
        if words and words[0] in self.wake_words:
            return True
        
        # Also check for wake word at the very beginning (for short phrases)
        for wake_word in self.wake_words:
            # Check if text starts with wake word followed by space or is exactly the wake word
            if text_lower == wake_word or text_lower.startswith(wake_word + " "):
                return True
        
        return False
    
    def listen_continuous(self):
        """Listen continuously for voice commands with wake word detection"""
        self.listening = True
        
        def listen_thread():
            with sr.Microphone() as source:
                if self.wake_word_enabled:
                    wake_words_str = ", ".join(self.wake_words)
                    print(f"🎤 Voice assistant started! Say wake word ({wake_words_str}) followed by your command")
                    print("   Or say 'stop listening' to quit")
                else:
                    print("🎤 Voice assistant started (say 'stop listening' to quit)")
                
                # Quick calibration for faster startup
                print("📊 Calibrating microphone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("✅ Ready! Listening...")
                waiting_for_wake_word = self.wake_word_enabled
                
                while self.listening:
                    try:
                        # Increased sensitivity: longer timeout, longer phrase limit
                        audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=8)
                        command = self.recognizer.recognize_google(audio)
                        command_lower = command.lower()
                        
                        if "stop listening" in command_lower:
                            self.listening = False
                            self.speak("Stopping voice assistant")
                            print("👋 Voice assistant stopped")
                            break
                        
                        if self.wake_word_enabled:
                            if waiting_for_wake_word:
                                if self.check_for_wake_word(command):
                                    # Extract command from the same phrase if present
                                    command_parts = command.lower().strip().split(None, 1)
                                    wake_word_used = command_parts[0] if command_parts else ""
                                    
                                    # Check if there's a command after the wake word
                                    if len(command_parts) > 1:
                                        # Wake word + command in same phrase
                                        # If wake word is an action verb, keep it in the command
                                        if wake_word_used in self.action_wake_words:
                                            # Keep the full phrase (e.g., "open chrome" stays as "open chrome")
                                            actual_command = command.lower().strip()
                                        else:
                                            # Remove non-action wake word (e.g., "hello open chrome" → "open chrome")
                                            actual_command = command_parts[1]
                                        
                                        print(f"👂 Wake word detected with command: {actual_command}")
                                        self.speak("Ji")
                                        
                                        # Process the command immediately
                                        if self.command_callback:
                                            response = self.command_callback(actual_command)
                                            if response:
                                                self.speak(response)
                                            else:
                                                self.speak("Samajh nahi aaya")
                                        waiting_for_wake_word = True  # Reset for next command
                                    else:
                                        # Wake word only, wait for command
                                        print(f"👂 Wake word detected! Listening for command...")
                                        self.speak("Ji, kaho")
                                        waiting_for_wake_word = False
                                else:
                                    continue
                            else:
                                # Already activated, process command
                                print(f"✅ Command: {command}")
                                waiting_for_wake_word = True
                                
                                if self.command_callback:
                                    response = self.command_callback(command)
                                    if response:
                                        self.speak(response)
                                    else:
                                        self.speak("Samajh nahi aaya. Phir se kaho")
                        else:
                            print(f"✅ Command: {command}")
                            if self.command_callback:
                                response = self.command_callback(command)
                                if response:
                                    self.speak(response)
                                    
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        if not waiting_for_wake_word:
                            waiting_for_wake_word = True
                        continue
                    except Exception as e:
                        print(f"❌ Error: {str(e)}")
                        if not waiting_for_wake_word:
                            waiting_for_wake_word = True
                        continue
        
        thread = threading.Thread(target=listen_thread, daemon=True)
        thread.start()
        return "✅ Voice assistant started"
    
    def stop_listening(self):
        """Stop continuous listening"""
        self.listening = False
        return "✅ Voice assistant stopped"
    
    def add_wake_word(self, wake_word):
        """Add a custom wake word"""
        if wake_word.lower() not in self.wake_words:
            self.wake_words.append(wake_word.lower())
            return f"✅ Wake word '{wake_word}' added"
        return f"⚠️ Wake word '{wake_word}' already exists"
    
    def remove_wake_word(self, wake_word):
        """Remove a wake word"""
        if wake_word.lower() in self.wake_words:
            self.wake_words.remove(wake_word.lower())
            return f"✅ Wake word '{wake_word}' removed"
        return f"⚠️ Wake word '{wake_word}' not found"
    
    def enable_wake_word(self):
        """Enable wake word detection"""
        self.wake_word_enabled = True
        return "✅ Wake word detection enabled"
    
    def disable_wake_word(self):
        """Disable wake word detection"""
        self.wake_word_enabled = False
        return "✅ Wake word detection disabled"
    
    def get_wake_words(self):
        """Get list of current wake words"""
        return self.wake_words
    
    def set_sensitivity(self, level="high"):
        """
        Set microphone sensitivity level
        
        Args:
            level: "low", "medium", "high", or "ultra"
        """
        if level == "low":
            self.recognizer.energy_threshold = 2000
            self.recognizer.pause_threshold = 1.0
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.dynamic_energy_ratio = 2.0  # Higher ratio = less sensitive
            self.recognizer.dynamic_energy_adjustment_damping = 0.25
            return "✅ Sensitivity set to LOW (fewer false triggers)"
        elif level == "medium":
            self.recognizer.energy_threshold = 1000
            self.recognizer.pause_threshold = 0.8
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.dynamic_energy_ratio = 1.5
            self.recognizer.dynamic_energy_adjustment_damping = 0.20
            return "✅ Sensitivity set to MEDIUM (balanced)"
        elif level == "high":
            self.recognizer.energy_threshold = 300
            self.recognizer.pause_threshold = 0.5
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.dynamic_energy_ratio = 1.2
            self.recognizer.dynamic_energy_adjustment_damping = 0.15
            return "✅ Sensitivity set to HIGH (very responsive)"
        elif level == "ultra":
            self.recognizer.energy_threshold = 100
            self.recognizer.pause_threshold = 0.3
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.dynamic_energy_ratio = 1.1
            self.recognizer.dynamic_energy_adjustment_damping = 0.10
            return "✅ Sensitivity set to ULTRA HIGH (maximum sensitivity)"
        else:
            return "❌ Invalid level. Use: low, medium, high, or ultra"
    
    def get_sensitivity_info(self):
        """Get current sensitivity settings"""
        return f"""
🎚️ Current Sensitivity Settings:
  • Energy Threshold: {self.recognizer.energy_threshold}
  • Pause Threshold: {self.recognizer.pause_threshold}
  • Dynamic Adjustment: {self.recognizer.dynamic_energy_threshold}
  • Dynamic Damping: {self.recognizer.dynamic_energy_adjustment_damping}
  • Dynamic Ratio: {self.recognizer.dynamic_energy_ratio}
"""
    
    def process_voice_command(self, command):
        """Process and execute voice commands"""
        command = command.lower()
        
        # Check if command STARTS with "search" (not just contains it)
        if command.strip().startswith("search"):
            # Extract search query (remove "search" from beginning and optional "for" after it)
            query = command.strip()
            if query.startswith("search "):
                query = query[7:]  # Remove "search "
            elif query.startswith("search"):
                query = query[6:]  # Remove "search"
            
            # Remove optional "for " at the beginning of query
            query = query.strip()
            if query.startswith("for "):
                query = query[4:]  # Remove "for "
            
            query = query.strip()
            if query:
                return f"web_search|{query}"
            else:
                return "web_search"
        
        elif "open" in command:
            if "project folder" in command:
                return "open_folder|."
            elif "chrome" in command or "browser" in command:
                return "open_app|chrome"
            elif "notepad" in command:
                return "open_app|notepad"
        
        elif "play" in command:
            if "lofi" in command or "beats" in command:
                return "play_music|lofi beats"
            else:
                song = command.replace("play", "").strip()
                return f"play_music|{song}"
        
        elif "send email" in command:
            return "send_email|" + command
        
        elif "screenshot" in command or "take a picture" in command:
            return "screenshot"
        
        elif "brightness" in command:
            if "increase" in command or "up" in command:
                return "brightness|80"
            elif "decrease" in command or "down" in command:
                return "brightness|30"
        
        elif "volume" in command:
            if "mute" in command:
                return "mute"
            elif "unmute" in command:
                return "unmute"
        
        elif "system" in command and "report" in command:
            return "system_report"
        
        elif "organize" in command and "downloads" in command:
            return "organize_downloads"
        
        return None

def create_voice_commands_list():
    """Return list of supported voice commands"""
    return """
🎤 Voice Commands with Wake Words (HIGH SENSITIVITY):

Wake Words (say one of these first):
  Simple & Quick:
  • "Hello"
  • "Open"
  • "Search"
  
  Hindi:
  • "Oye"
  • "Bhaiya"
  • "Bhaisahb"

Usage: Say wake word → Wait for "Ji, kaho" → Give your command

🎚️ Sensitivity Levels:
  • LOW    - Fewer false triggers, louder voice needed
  • MEDIUM - Balanced detection
  • HIGH   - Very responsive (DEFAULT) ⭐
  • ULTRA  - Maximum sensitivity, detects quiet speech

System Control:
  • "Increase brightness"
  • "Decrease brightness"
  • "Mute microphone"
  • "Unmute microphone"
  • "Show system report"

File Management:
  • "Open project folder"
  • "Organize downloads"
  • "Take a screenshot"

Apps & Web:
  • "Open Chrome"
  • "Open Notepad"
  • "Play lofi beats"
  • "Play [song name]"

Communication:
  • "Send email to [name]"
  • "Text [name] that [message]"

Stop Listening:
  • "Stop listening"

Example:
  1. Say "Oye" or "Bhaiya" or "Bhaisahb"
  2. Wait for assistant to say "Ji, kaho"
  3. Give your command like "Open Chrome"
  
To change sensitivity:
  assistant.set_sensitivity('ultra')  # ultra, high, medium, or low
"""

if __name__ == "__main__":
    assistant = VoiceAssistant()
    print("Voice Assistant Module - Testing")
    print(create_voice_commands_list())
    
    print("\nSay something:")
    command = assistant.listen_once()
    print(f"Result: {command}")
