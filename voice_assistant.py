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
    
    def listen_continuous(self):
        """Listen continuously for voice commands"""
        self.listening = True
        
        def listen_thread():
            with sr.Microphone() as source:
                print("🎤 Voice assistant started (say 'stop listening' to quit)")
                self.recognizer.adjust_for_ambient_noise(source)
                
                while self.listening:
                    try:
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                        command = self.recognizer.recognize_google(audio)
                        print(f"✅ Command: {command}")
                        
                        if "stop listening" in command.lower():
                            self.listening = False
                            self.speak("Stopping voice assistant")
                            break
                        
                        if self.command_callback:
                            response = self.command_callback(command)
                            if response:
                                self.speak(response)
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        continue
                    except Exception as e:
                        print(f"❌ Error: {str(e)}")
                        continue
        
        thread = threading.Thread(target=listen_thread, daemon=True)
        thread.start()
        return "✅ Voice assistant started"
    
    def stop_listening(self):
        """Stop continuous listening"""
        self.listening = False
        return "✅ Voice assistant stopped"
    
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
🎤 Voice Commands:

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
"""

if __name__ == "__main__":
    assistant = VoiceAssistant()
    print("Voice Assistant Module - Testing")
    print(create_voice_commands_list())
    
    print("\nSay something:")
    command = assistant.listen_once()
    print(f"Result: {command}")
