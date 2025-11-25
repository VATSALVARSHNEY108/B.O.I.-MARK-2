"""
🎤 Feature Speaker Module
Speaks the main key features and capabilities of BOI when speaking mode is activated
"""

import pyttsx3
import threading
from modules.core.gemini_controller import get_ai_response


class FeatureSpeaker:
    """Speaks BOI features and capabilities with optimized text"""
    
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        self.is_speaking = False
        self.speaking_lock = threading.Lock()
    
    def extract_main_points(self, text):
        """Extract main points from text using AI"""
        try:
            prompt = f"""Analyze this text and extract ONLY the main key points (3-5 bullet points max). 
Make it concise and speaking-friendly (short sentences, no technical jargon).
Don't include verbose explanations.

Text to analyze:
{text}

Return ONLY the main points, one per line, prefixed with a bullet point or number.
Make it sound natural for speaking aloud."""
            
            response = get_ai_response(prompt)
            return response.strip() if response else text[:200]
        except Exception as e:
            print(f"⚠️ AI extraction failed: {e}")
            return text[:300]  # Fallback to first 300 chars
    
    def speak_text(self, text):
        """Speak text in non-blocking mode - extracts main points if text is long"""
        # If text is short, speak it directly. If long, extract main points
        if len(text) > 200:
            text = self.extract_main_points(text)
        
        def speak_thread():
            with self.speaking_lock:
                self.is_speaking = True
                try:
                    self.engine.say(text)
                    self.engine.runAndWait()
                finally:
                    self.is_speaking = False
        
        thread = threading.Thread(target=speak_thread, daemon=True)
        thread.start()
    
    def get_main_features_text(self):
        """Get optimized text for speaking main features"""
        return """
        Welcome to BOI, your AI Desktop Automation Controller powered by Google Gemini!
        
        Here are my main capabilities:
        
        I can control your Desktop with over 410 features including:
        
        Communication - Send emails, WhatsApp messages, and phone calls. Generate smart email replies and translate messages.
        
        System Control - Manage Windows 11 settings, brightness, volume, power options, and monitor system performance.
        
        Media Control - Play YouTube videos, control Spotify music, manage audio, and organize media files.
        
        AI Intelligence - Generate and debug code, analyze screenshots, extract text using OCR, understand context, and make predictions.
        
        File Management - Search files, organize folders, find duplicates, and manage your entire desktop.
        
        Security - Facial recognition authentication, threat detection, encrypted storage, and device management.
        
        Voice Commands - I understand natural language and respond with personality and empathy.
        
        Automation - Record macros, create workflows, schedule tasks, and chain multiple actions together.
        
        Data Analysis - Visualize data, generate reports, track productivity, and provide insights.
        
        Creative Tools - Generate stories, create content, write code, make designs automatically.
        
        Future-Tech Features - Including holographic memory recall, quantum-fast search, emotion detection, real-time translation, and autonomous task execution.
        
        I can also remember everything, predict your next actions, detect your emotional state, and suggest what you should do next.
        
        How can I help you today? You can ask me to do almost anything on your computer!
        """
    
    def get_brief_features_text(self):
        """Get brief version for quick introduction"""
        return """
        Hi! I'm BOI, your AI Desktop Automation Controller.
        
        I can help with:
        
        Communication - Emails, WhatsApp, phone calls, and smart replies.
        System Control - Windows settings, brightness, volume, power management.
        Media - YouTube, Spotify, audio control.
        AI Features - Code generation, screenshot analysis, OCR, predictions.
        File Management - Search, organize, find duplicates.
        Security - Facial recognition, threat detection.
        Voice Commands - Natural language understanding with personality.
        Automation - Macros, workflows, task scheduling.
        Data Analysis - Reports, productivity tracking, insights.
        Creative Tools - Stories, content, code, designs.
        
        Plus Future-Tech: Memory recall, fast search, emotion detection, translation, and autonomous tasks.
        
        What would you like me to do?
        """
    
    def get_quick_start_text(self):
        """Get quick action suggestions"""
        return """
        Here are some things you can ask me to do:
        
        Send an email to someone
        Play a song on Spotify
        Take a screenshot and analyze it
        Find files on your computer
        Check system status and performance
        Control brightness or volume
        Generate Python code for a task
        Create a workflow for your daily routine
        Translate text to another language
        Read your emotions and suggest a break
        Search through all your desktop files
        Control YouTube and play videos
        Monitor your productivity
        Lock or shutdown your computer
        Anything else on your desktop!
        
        Just ask me naturally, and I'll do it!
        """
    
    def speak_main_features(self):
        """Speak the main features when speaking mode opens"""
        text = self.get_main_features_text()
        self.speak_text(text)
        return {"success": True, "message": "Speaking main features..."}
    
    def speak_brief_features(self):
        """Speak brief feature overview"""
        text = self.get_brief_features_text()
        self.speak_text(text)
        return {"success": True, "message": "Speaking brief features overview..."}
    
    def speak_quick_start(self):
        """Speak quick action suggestions"""
        text = self.get_quick_start_text()
        self.speak_text(text)
        return {"success": True, "message": "Speaking quick start suggestions..."}
    
    def speak_custom(self, text):
        """Speak custom text - intelligently extracts main points"""
        # Extract main points if text is long
        if len(text) > 200:
            main_points = self.extract_main_points(text)
            self.speak_text(main_points)
            return {"success": True, "message": "Speaking main points...", "points": main_points}
        else:
            self.speak_text(text)
            return {"success": True, "message": "Speaking text..."}


def create_feature_speaker():
    """Factory function to create FeatureSpeaker instance"""
    return FeatureSpeaker()
