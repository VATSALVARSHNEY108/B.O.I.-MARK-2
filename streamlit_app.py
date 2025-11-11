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
    executor = None

load_dotenv()

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
    st.markdown("""
    ### How to use:
    1. **Click 'Record Audio'** button below
    2. **Speak your command** (in browser)
    3. **Click 'Stop Recording'** when done
    4. **Process** to execute
    
    ### Example Commands:
    - "Open Chrome"
    - "Search for Python tutorials"
    - "What's the weather?"
    - "Set a reminder for 5pm"
    - "Tell me a joke"
    """)
    
    st.divider()
    st.markdown("### ⚙️ Settings")
    st.markdown(f"**API Key:** {'✅ Configured' if api_key else '❌ Missing'}")
    st.markdown(f"**Command Executor:** {'✅ Ready' if executor else '❌ Error'}")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## 🎙️ Voice Input")
    st.markdown("**Record your command using your browser's microphone:**")
    
    # Audio input using Streamlit's audio_input
    audio_data = st.audio_input("🎤 Record your voice command")
    
    if audio_data:
        st.success("✅ Audio recorded! Processing...")
        
        # Save audio to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_data.read())
            tmp_file_path = tmp_file.name
        
        try:
            # Use speech recognition on the audio file
            recognizer = sr.Recognizer()
            with sr.AudioFile(tmp_file_path) as source:
                audio = recognizer.record(source)
                try:
                    command = recognizer.recognize_google(audio)
                    st.markdown(f'<div class="command-box"><strong>🎤 You said:</strong> "{command}"</div>', unsafe_allow_html=True)
                    
                    # Process command
                    if executor and api_key:
                        with st.spinner("🤖 Processing command..."):
                            try:
                                result = parse_command(command)
                                response = executor.execute(result)
                                
                                # Display result
                                st.markdown('<div class="success-box"><strong>✅ Response:</strong><br>' + str(response) + '</div>', unsafe_allow_html=True)
                                
                                # Add to history
                                st.session_state.history.insert(0, {
                                    'command': command,
                                    'response': str(response),
                                    'timestamp': str(Path.ctime(Path(__file__)))
                                })
                            except Exception as e:
                                st.markdown(f'<div class="error-box"><strong>❌ Error:</strong><br>{str(e)}</div>', unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ Command executor not available or API key missing")
                        
                except sr.UnknownValueError:
                    st.error("❌ Could not understand audio. Please speak clearly.")
                except sr.RequestError as e:
                    st.error(f"❌ Speech recognition service error: {e}")
        except Exception as e:
            st.error(f"❌ Error processing audio: {e}")
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
                        result = parse_command(text_command)
                        response = executor.execute(result)
                        st.markdown('<div class="success-box"><strong>✅ Response:</strong><br>' + str(response) + '</div>', unsafe_allow_html=True)
                        
                        # Add to history
                        st.session_state.history.insert(0, {
                            'command': text_command,
                            'response': str(response),
                            'timestamp': str(Path.ctime(Path(__file__)))
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
    else:
        st.info("No commands executed yet")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p><strong>✨ VATSAL AI Desktop Automation ✨</strong></p>
    <p>Voice-Powered AI Assistant | Powered by Google Gemini</p>
</div>
""", unsafe_allow_html=True)
