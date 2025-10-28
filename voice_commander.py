"""
Enhanced Voice Commander for VATSAL
Provides voice input and speech output for all VATSAL commands
"""

import speech_recognition as sr
import pyttsx3
import threading
import queue
import time
from typing import Callable, Optional

class VoiceCommander:
    """Enhanced voice commanding with speech recognition and text-to-speech"""
    
    def __init__(self, command_callback: Optional[Callable] = None):
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        self.command_callback = command_callback
        
        # Speech settings
        self.tts_engine.setProperty('rate', 165)
        self.tts_engine.setProperty('volume', 0.95)
        
        # Set voice (try to use a better voice if available)
        voices = self.tts_engine.getProperty('voices')
        if len(voices) > 1:
            self.tts_engine.setProperty('voice', voices[1].id)
        
        # Recognition settings
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        # State management
        self.continuous_listening = False
        self.listen_thread = None
        self.tts_queue = queue.Queue()
        self.tts_thread = None
        self.is_speaking = False
        
        # Wake word detection
        self.wake_word = "vatsal"
        self.wake_word_enabled = False
        
        # Start TTS worker thread
        self._start_tts_worker()
    
    def _start_tts_worker(self):
        """Start background thread for text-to-speech"""
        def tts_worker():
            while True:
                try:
                    text = self.tts_queue.get()
                    if text is None:
                        break
                    
                    self.is_speaking = True
                    try:
                        self.tts_engine.say(text)
                        self.tts_engine.runAndWait()
                    except Exception as e:
                        print(f"❌ TTS Error: {str(e)}")
                    finally:
                        self.is_speaking = False
                        
                except Exception as e:
                    print(f"❌ TTS Worker Error: {str(e)}")
        
        self.tts_thread = threading.Thread(target=tts_worker, daemon=True)
        self.tts_thread.start()
    
    def speak(self, text: str, interrupt: bool = False):
        """Queue text for speech output"""
        if interrupt:
            # Clear the queue and speak immediately
            while not self.tts_queue.empty():
                try:
                    self.tts_queue.get_nowait()
                except queue.Empty:
                    break
        
        self.tts_queue.put(text)
    
    def listen_once(self, timeout: int = 5) -> dict:
        """
        Listen for a single voice command
        Returns: dict with 'success', 'command', and 'message'
        """
        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                
                print("🔄 Processing speech...")
                command = self.recognizer.recognize_google(audio)
                
                print(f"✅ Heard: {command}")
                return {
                    "success": True,
                    "command": command,
                    "message": f"Heard: {command}"
                }
                
        except sr.WaitTimeoutError:
            return {
                "success": False,
                "command": None,
                "message": "No speech detected (timeout)"
            }
        except sr.UnknownValueError:
            return {
                "success": False,
                "command": None,
                "message": "Could not understand audio"
            }
        except sr.RequestError as e:
            return {
                "success": False,
                "command": None,
                "message": f"Recognition service error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "command": None,
                "message": f"Error: {str(e)}"
            }
    
    def start_continuous_listening(self, callback: Optional[Callable] = None):
        """Start continuous voice command listening"""
        if self.continuous_listening:
            return {"success": False, "message": "Already listening"}
        
        if callback:
            self.command_callback = callback
        
        if not self.command_callback:
            return {"success": False, "message": "No command callback provided"}
        
        self.continuous_listening = True
        
        def listen_loop():
            """Continuous listening loop"""
            try:
                with sr.Microphone() as source:
                    print("🎤 Continuous listening started")
                    self.speak("Voice commanding activated", interrupt=True)
                    
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    
                    while self.continuous_listening:
                        try:
                            # Don't listen while speaking
                            if self.is_speaking:
                                time.sleep(0.1)
                                continue
                            
                            audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)
                            
                            try:
                                command = self.recognizer.recognize_google(audio)
                                print(f"🎤 Heard: {command}")
                                
                                # Check for stop command
                                if any(phrase in command.lower() for phrase in ["stop listening", "stop voice", "disable voice"]):
                                    self.stop_continuous_listening()
                                    break
                                
                                # Check for wake word if enabled
                                if self.wake_word_enabled:
                                    if self.wake_word.lower() not in command.lower():
                                        continue
                                    # Remove wake word from command
                                    command = command.lower().replace(self.wake_word.lower(), "").strip()
                                
                                # Execute command
                                if command:
                                    self.command_callback(command)
                                
                            except sr.UnknownValueError:
                                continue
                            except sr.RequestError as e:
                                print(f"❌ Recognition error: {str(e)}")
                                time.sleep(1)
                                continue
                                
                        except sr.WaitTimeoutError:
                            continue
                        except Exception as e:
                            print(f"❌ Listen error: {str(e)}")
                            continue
                            
            except Exception as e:
                print(f"❌ Microphone error: {str(e)}")
                self.continuous_listening = False
        
        self.listen_thread = threading.Thread(target=listen_loop, daemon=True)
        self.listen_thread.start()
        
        return {"success": True, "message": "Continuous listening started"}
    
    def stop_continuous_listening(self):
        """Stop continuous listening"""
        if not self.continuous_listening:
            return {"success": False, "message": "Not currently listening"}
        
        self.continuous_listening = False
        self.speak("Voice commanding deactivated", interrupt=True)
        
        return {"success": True, "message": "Continuous listening stopped"}
    
    def toggle_wake_word(self, enabled: bool = None) -> dict:
        """Toggle wake word detection"""
        if enabled is None:
            self.wake_word_enabled = not self.wake_word_enabled
        else:
            self.wake_word_enabled = enabled
        
        status = "enabled" if self.wake_word_enabled else "disabled"
        return {
            "success": True,
            "message": f"Wake word '{self.wake_word}' {status}",
            "enabled": self.wake_word_enabled
        }
    
    def set_wake_word(self, wake_word: str) -> dict:
        """Set custom wake word"""
        self.wake_word = wake_word.lower().strip()
        return {
            "success": True,
            "message": f"Wake word set to '{self.wake_word}'"
        }
    
    def get_status(self) -> dict:
        """Get current voice commander status"""
        return {
            "listening": self.continuous_listening,
            "speaking": self.is_speaking,
            "wake_word_enabled": self.wake_word_enabled,
            "wake_word": self.wake_word
        }
    
    def cleanup(self):
        """Clean up resources"""
        self.stop_continuous_listening()
        self.tts_queue.put(None)
        if self.tts_thread:
            self.tts_thread.join(timeout=2)


def create_voice_commander(command_callback: Optional[Callable] = None) -> VoiceCommander:
    """Factory function to create a VoiceCommander instance"""
    return VoiceCommander(command_callback)


if __name__ == "__main__":
    # Test the voice commander
    print("Testing Voice Commander")
    
    def test_callback(command):
        print(f"Executing command: {command}")
    
    commander = create_voice_commander(test_callback)
    
    print("\n1. Testing single listen:")
    result = commander.listen_once()
    print(f"Result: {result}")
    
    if result['success']:
        commander.speak(f"You said: {result['command']}")
    
    print("\n2. Testing text-to-speech:")
    commander.speak("Hello, I am VATSAL, your AI desktop automation assistant")
    
    time.sleep(3)
    
    print("\nVoice Commander test complete")
