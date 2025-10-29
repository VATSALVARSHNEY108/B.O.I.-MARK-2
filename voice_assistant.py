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
        self.wake_words = ["oye", "bhaiya", "bhaisahb"]
        
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
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5)
                
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
        """Check if the text contains any wake word"""
        text_lower = text.lower()
        for wake_word in self.wake_words:
            if wake_word in text_lower:
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
                
                self.recognizer.adjust_for_ambient_noise(source)
                waiting_for_wake_word = self.wake_word_enabled
                
                while self.listening:
                    try:
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
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
                                    print(f"👂 Wake word detected! Listening for command...")
                                    self.speak("Ji, kaho")
                                    waiting_for_wake_word = False
                                else:
                                    continue
                            else:
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
    
    def process_voice_command(self, command):
        """Process and execute voice commands"""
        command = command.lower()
        
        if "open" in command:
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
🎤 Voice Commands with Wake Words:

Wake Words (say one of these first):
  • "Oye"
  • "Bhaiya"
  • "Bhaisahb"

Usage: Say wake word → Wait for "Ji, kaho" → Give your command

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
"""

if __name__ == "__main__":
    assistant = VoiceAssistant()
    print("Voice Assistant Module - Testing")
    print(create_voice_commands_list())
    
    print("\nSay something:")
    command = assistant.listen_once()
    print(f"Result: {command}")
