#!/usr/bin/env python3
"""
VATSAL AI Web Interface
Streamlit-based web interface with browser audio input
"""

import streamlit as st

# Page configuration MUST be first Streamlit command
st.set_page_config(
    page_title="✨ VATSAL AI Desktop Automation",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

import speech_recognition as sr
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import tempfile
from datetime import datetime
import time

# Load environment variables FIRST
load_dotenv()

# Add modules to path
workspace_dir = Path(__file__).parent
modules_dir = workspace_dir / 'modules'
sys.path.insert(0, str(workspace_dir))
sys.path.insert(0, str(modules_dir))
sys.path.insert(0, str(modules_dir / 'core'))

# Import command executor
try:
    from modules.core.command_executor import CommandExecutor
    from modules.core.gemini_controller import parse_command
    executor = CommandExecutor()
except Exception as e:
    st.error(f"Failed to load command executor: {e}")
    import traceback
    st.code(traceback.format_exc())
    executor = None

# Initialize TTS engine for voice responses
@st.cache_resource
def get_tts_engine():
    """Initialize and cache the TTS engine"""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        voices = engine.getProperty('voices')
        if len(voices) > 0:
            engine.setProperty('voice', voices[0].id)
        return engine
    except ImportError:
        return None
    except Exception as e:
        return None

def text_to_speech_file(text):
    """Convert text to speech and return audio file path"""
    try:
        engine = get_tts_engine()
        if not engine:
            return None
        
        # Create temporary file for audio
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_path = temp_file.name
        temp_file.close()
        
        # Save speech to file
        engine.save_to_file(text, temp_path)
        engine.runAndWait()
        
        # Wait a moment for file to be written
        time.sleep(0.5)
        
        if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
            return temp_path
        return None
    except Exception as e:
        st.warning(f"⚠️ Failed to generate speech: {e}")
        return None

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #0a0a0a;
        color: #ffffff;
    }
    .stTextInput > div > div > input {
        background-color: #1a1a1a;
        color: #00d4ff;
        border: 2px solid #00d4ff;
    }
    .stButton > button {
        background-color: #00d4ff;
        color: #000000;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        border: none;
        font-size: 1.1rem;
    }
    .stButton > button:hover {
        background-color: #00ff88;
        box-shadow: 0 0 20px #00ff88;
    }
    h1 {
        color: #00d4ff;
        text-align: center;
        font-family: 'Copperplate Gothic Bold', sans-serif;
    }
    h2, h3 {
        color: #00ff88;
    }
    .success-box {
        background-color: #1a3a1a;
        border-left: 5px solid #00ff88;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #3a1a1a;
        border-left: 5px solid #ff0080;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .command-box {
        background-color: #1a1a2a;
        border: 2px solid #b19cd9;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'voice_response_enabled' not in st.session_state:
    st.session_state.voice_response_enabled = True

# Header
st.markdown("# ✨ V.A.T.S.A.L. ✨")
st.markdown("### ⚡ Vastly Advanced Technological System Above Limitations ⚡")
st.divider()

# Check API key
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ GEMINI_API_KEY not found in environment variables. Please add it to .env file")

# Sidebar
with st.sidebar:
    st.markdown("## 🎤 Voice Commands")
    
    st.warning("⚠️ **IMPORTANT:** When you click Record, your browser will ask for microphone permission. Click **ALLOW**!")
    
    st.markdown("""
    ### Step-by-Step:
    1. **Click the microphone button** 🎤 below
    2. **Allow microphone access** when browser asks
    3. **Speak clearly** into your microphone
    4. **Wait** - it will auto-process
    
    ### ❌ If Not Working:
    - Check browser microphone permissions in settings
    - Ensure microphone is not muted
    - Try refreshing the page
    - Use **Text Input** as alternative
    
    ### Example Commands:
    - "Open Chrome"
    - "Search for Python tutorials"
    - "What's the weather?"
    - "Set a reminder for 5pm"
    - "Tell me a joke"
    """)
    
    st.divider()
    st.markdown("### ⚙️ Settings")
    
    # Voice response toggle
    st.session_state.voice_response_enabled = st.checkbox(
        "🔊 Enable Voice Responses", 
        value=st.session_state.voice_response_enabled,
        help="When enabled, the AI will speak responses out loud"
    )
    
    st.divider()
    st.markdown("### ⚙️ Status")
    st.markdown(f"**API Key:** {'✅ Configured' if api_key else '❌ Missing'}")
    st.markdown(f"**Command Executor:** {'✅ Ready' if executor else '❌ Error'}")
    tts_engine = get_tts_engine()
    st.markdown(f"**Voice Output:** {'✅ Available' if tts_engine else '❌ Not Available'}")
    
    st.divider()
    st.info("💡 **Tip:** If voice doesn't work, use the **Text Input** option below - it works the same way!")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## 🎙️ Voice Input")
    
    # Voice response status indicator
    if st.session_state.voice_response_enabled:
        st.success("🔊 Voice Responses: **ENABLED** - AI will speak responses")
    else:
        st.info("🔇 Voice Responses: **DISABLED** - Text only")
    
    # Important notice
    st.info("🔔 **First Time?** Your browser will ask for microphone permission. Click **ALLOW** when prompted!")
    
    st.markdown("**Click the microphone icon below, speak clearly, then click stop:**")
    
    # Audio input using Streamlit's audio_input
    audio_data = st.audio_input("🎤 Click here → Speak your command → Click stop")
    
    if audio_data:
        st.success("✅ Audio recorded! Processing...")
        
        # Get audio bytes
        audio_bytes = audio_data.getvalue()
        
        # Check if audio is not empty
        if len(audio_bytes) < 100:
            st.error("❌ Audio recording too short or empty. Try recording again and speak louder.")
        else:
            st.info(f"📊 Audio size: {len(audio_bytes)} bytes")
            
            # Save audio to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(audio_bytes)
                tmp_file_path = tmp_file.name
            
            try:
                # Configure speech recognizer with better settings
                recognizer = sr.Recognizer()
                recognizer.energy_threshold = 300  # Lower = more sensitive
                recognizer.dynamic_energy_threshold = False  # Prevent timeout issues
                recognizer.pause_threshold = 0.8
                
                # Process audio file
                with sr.AudioFile(tmp_file_path) as source:
                    st.info("🔄 Processing audio...")
                    # Adjust for ambient noise
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    # Record the audio
                    audio = recognizer.record(source)
                    
                    try:
                        st.info("🌐 Sending to Google Speech Recognition...")
                        command = recognizer.recognize_google(audio, language="en-US")  # type: ignore
                        
                        if command:
                            st.markdown(f'<div class="command-box"><strong>🎤 You said:</strong> "{command}"</div>', unsafe_allow_html=True)
                            
                            # Process command
                            if executor and api_key:
                                with st.spinner("🤖 Processing command..."):
                                    try:
                                        result = parse_command(command)  # type: ignore
                                        response = executor.execute(result)
                                        response_text = str(response)
                                        
                                        # Display result
                                        st.markdown('<div class="success-box"><strong>✅ Response:</strong><br>' + response_text + '</div>', unsafe_allow_html=True)
                                        
                                        # Voice response playback
                                        if st.session_state.voice_response_enabled:
                                            with st.spinner("🔊 Generating voice response..."):
                                                audio_file = text_to_speech_file(response_text)
                                                if audio_file and os.path.exists(audio_file):
                                                    # Read audio file as bytes for st.audio
                                                    try:
                                                        with open(audio_file, 'rb') as f:
                                                            audio_bytes = f.read()
                                                        st.audio(audio_bytes, format="audio/wav")
                                                        # Clean up temp file
                                                        os.unlink(audio_file)
                                                    except Exception as e:
                                                        st.warning(f"⚠️ Could not play audio: {e}")
                                        
                                        # Add to history
                                        st.session_state.history.insert(0, {
                                            'command': command,
                                            'response': response_text,
                                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                        })
                                    except Exception as e:
                                        st.markdown(f'<div class="error-box"><strong>❌ Command Error:</strong><br>{str(e)}</div>', unsafe_allow_html=True)
                            else:
                                st.warning("⚠️ Command executor not available or API key missing")
                        else:
                            st.warning("⚠️ No speech detected in audio")
                            
                    except sr.UnknownValueError:
                        st.error("❌ **Could not understand audio**\n\n**Tips:**\n- Speak clearly and loudly\n- Reduce background noise\n- Try recording again\n- Use Text Input as alternative")
                    except sr.RequestError as e:
                        st.error(f"❌ **Speech recognition service error:** {e}\n\nPlease check your internet connection and try again.")
            except Exception as e:
                st.error(f"❌ **Error processing audio file:** {str(e)}\n\nTry using **Text Input** instead.")
                import traceback
                st.code(traceback.format_exc())
            finally:
                # Clean up temporary file
                try:
                    os.unlink(tmp_file_path)
                except:
                    pass
    
    st.divider()
    
    # Text input alternative
    st.markdown("## ⌨️ Text Input (Alternative)")
    text_command = st.text_input("Type your command:", placeholder="e.g., Open Chrome, Search for Python...")
    
    if st.button("▶️ Execute Command", type="primary"):
        if text_command:
            with st.spinner("🤖 Processing..."):
                if executor and api_key:
                    try:
                        result = parse_command(text_command)  # type: ignore
                        response = executor.execute(result)
                        response_text = str(response)
                        
                        st.markdown('<div class="success-box"><strong>✅ Response:</strong><br>' + response_text + '</div>', unsafe_allow_html=True)
                        
                        # Voice response playback
                        if st.session_state.voice_response_enabled:
                            with st.spinner("🔊 Generating voice response..."):
                                audio_file = text_to_speech_file(response_text)
                                if audio_file and os.path.exists(audio_file):
                                    # Read audio file as bytes for st.audio
                                    try:
                                        with open(audio_file, 'rb') as f:
                                            audio_bytes = f.read()
                                        st.audio(audio_bytes, format="audio/wav")
                                        # Clean up temp file
                                        os.unlink(audio_file)
                                    except Exception as e:
                                        st.warning(f"⚠️ Could not play audio: {e}")
                        
                        # Add to history
                        st.session_state.history.insert(0, {
                            'command': text_command,
                            'response': response_text,
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                    except Exception as e:
                        st.markdown(f'<div class="error-box"><strong>❌ Error:</strong><br>{str(e)}</div>', unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Command executor not available or API key missing")
        else:
            st.warning("⚠️ Please enter a command")

with col2:
    st.markdown("## 📜 Command History")
    if st.session_state.history:
        for idx, item in enumerate(st.session_state.history[:10]):  # Show last 10
            with st.expander(f"🔹 {item['command'][:30]}..."):
                st.markdown(f"**Command:** {item['command']}")
                st.markdown(f"**Response:** {item['response']}")
                st.markdown(f"**Time:** {item['timestamp']}")
    else:
        st.info("No commands executed yet")
    
    # Quick reference for common commands
    st.divider()
    st.markdown("## 💡 Quick Reference")
    with st.expander("📖 Common Commands"):
        st.markdown("""
        **⏰ Time & Date:**
        - "What time is it?"
        - "What's the date?"
        
        **🔍 Search:**
        - "Search for [query]"
        - "Google [something]"
        
        **🌤️ Weather:**
        - "What's the weather?"
        - "Weather in [city]"
        
        **🔢 Calculator:**
        - "Calculate 25 plus 37"
        - "What is 100 divided by 4?"
        
        **🎵 Music:**
        - "Play [song name]"
        - "Play lofi beats"
        
        **💻 System:**
        - "Screenshot"
        - "Volume up/down"
        - "Shutdown/Restart"
        
        **🎲 Fun:**
        - "Tell me a joke"
        - "Flip a coin"
        - "Roll dice"
        """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p><strong>✨ VATSAL AI Desktop Automation ✨</strong></p>
    <p>Voice-Powered AI Assistant | Powered by Google Gemini</p>
</div>
""", unsafe_allow_html=True)
