#!/usr/bin/env python3
"""
Voice Input Test Page for Streamlit
Tests browser-based audio input and speech recognition
"""

import streamlit as st
import speech_recognition as sr
import tempfile
import os

st.set_page_config(
    page_title="🎤 Voice Input Test",
    page_icon="🎤",
    layout="wide"
)

st.markdown("# 🎤 Voice Input Diagnostic Test")
st.markdown("### Test if your microphone and voice recognition are working")

st.divider()

# Explanation
st.info("""
**How this works on Replit:**
1. ✅ Your browser captures audio from YOUR laptop's microphone
2. ✅ Audio is sent to this Replit server
3. ✅ Server processes the audio with Google Speech Recognition
4. ✅ Result is displayed back to you

**This is DIFFERENT from desktop apps** - we're using browser-based audio capture!
""")

st.divider()

# Step-by-step test
st.markdown("## 📋 Follow These Steps:")

st.markdown("### Step 1: Check Browser Permissions")
st.warning("""
🔒 **CRITICAL:** Your browser MUST have microphone permission!

**How to check:**
- Chrome: Click the 🔒 or 🎥 icon in address bar → Site settings → Microphone: Allow
- Firefox: Click the 🔒 icon in address bar → Permissions → Microphone: Allow
- Safari: Safari → Settings → Websites → Microphone: Allow
""")

st.markdown("### Step 2: Record Audio")

# Audio input
audio_data = st.audio_input("🎤 Click to record → Speak clearly → Click again to stop")

if audio_data:
    st.success("✅ Audio recorded!")
    
    # Get audio bytes
    audio_bytes = audio_data.getvalue()
    
    # Show audio details
    st.markdown("### Step 3: Audio Analysis")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Audio Size", f"{len(audio_bytes)} bytes")
    with col2:
        st.metric("Status", "✅ Valid" if len(audio_bytes) > 100 else "❌ Too Short")
    with col3:
        audio_kb = len(audio_bytes) / 1024
        st.metric("Size (KB)", f"{audio_kb:.2f} KB")
    
    # Check if audio is valid
    if len(audio_bytes) < 100:
        st.error("""
        ❌ **Audio is too short!**
        
        **This means:**
        - Microphone didn't capture any sound
        - Recording was stopped immediately
        - Browser didn't get microphone permission
        
        **Try this:**
        1. Check browser microphone permission (see Step 1)
        2. Record for at least 2-3 seconds
        3. Speak loudly and clearly
        4. Check your microphone isn't muted
        """)
    else:
        st.markdown("### Step 4: Speech Recognition")
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_file_path = tmp_file.name
        
        try:
            # Show audio player
            st.audio(audio_bytes, format="audio/wav")
            st.caption("👆 Play this to hear what was recorded")
            
            # Process with speech recognition
            with st.spinner("🔄 Processing with Google Speech Recognition..."):
                recognizer = sr.Recognizer()
                
                # Show recognizer settings
                with st.expander("🔧 Recognizer Settings"):
                    st.code(f"""
Energy Threshold: {recognizer.energy_threshold}
Pause Threshold: {recognizer.pause_threshold}
Dynamic Energy: {recognizer.dynamic_energy_threshold}
                    """)
                
                try:
                    with sr.AudioFile(tmp_file_path) as source:
                        # Adjust for noise
                        st.info("🔊 Adjusting for ambient noise...")
                        recognizer.adjust_for_ambient_noise(source, duration=0.2)
                        
                        # Record audio
                        st.info("📝 Reading audio data...")
                        audio = recognizer.record(source)
                        
                        # Try recognition
                        st.info("🌐 Sending to Google Speech Recognition API...")
                        
                        try:
                            text = recognizer.recognize_google(audio, language="en-US")
                            
                            st.success("### ✅ SUCCESS!")
                            st.markdown(f"### You said: **\"{text}\"**")
                            
                            st.balloons()
                            
                            st.info("""
                            🎉 **Your microphone is working perfectly!**
                            
                            If the main app still doesn't work, try:
                            1. Refreshing the main app page
                            2. Checking you allowed microphone permission there too
                            3. Clearing browser cache
                            """)
                            
                        except sr.UnknownValueError:
                            st.error("""
                            ❌ **Audio captured but couldn't understand speech**
                            
                            **Why this happens:**
                            - Audio is too quiet (speak louder)
                            - Too much background noise
                            - Unclear pronunciation
                            - Audio quality too low
                            
                            **Try again:**
                            1. Move closer to microphone
                            2. Speak clearly and loudly
                            3. Reduce background noise
                            4. Record for 3-5 seconds
                            """)
                            
                        except sr.RequestError as e:
                            st.error(f"""
                            ❌ **Google Speech Recognition API Error**
                            
                            Error: {e}
                            
                            **Possible causes:**
                            - No internet connection
                            - Google API temporarily unavailable
                            - Network firewall blocking request
                            
                            **Solution:**
                            - Check your internet connection
                            - Try again in a few moments
                            """)
                            
                except Exception as e:
                    st.error(f"""
                    ❌ **Error processing audio file**
                    
                    Error: {e}
                    
                    This is a technical error. Try recording again.
                    """)
                    
        finally:
            # Clean up
            try:
                os.unlink(tmp_file_path)
            except:
                pass

else:
    st.info("👆 Click the microphone button above to start the test")

st.divider()

# Troubleshooting guide
with st.expander("🆘 Still Not Working? Common Issues & Solutions"):
    st.markdown("""
    ### ❌ Problem 1: No audio recorded (0 bytes)
    **Solution:**
    - Browser didn't get microphone permission
    - Click 🔒 icon in browser address bar
    - Go to Site Settings → Microphone → Allow
    - Refresh this page and try again
    
    ### ❌ Problem 2: Audio too short
    **Solution:**
    - You need to record for at least 2-3 seconds
    - Click microphone → WAIT → Speak → WAIT → Click again
    - Don't stop recording immediately
    
    ### ❌ Problem 3: Can't understand audio
    **Solution:**
    - Speak louder and more clearly
    - Get closer to your microphone
    - Reduce background noise
    - Check microphone volume in system settings
    - Make sure microphone isn't muted
    
    ### ❌ Problem 4: Wrong microphone selected
    **Solution:**
    - Check system sound settings
    - Select correct microphone as default input device
    - Windows: Settings → Sound → Input
    - Mac: System Preferences → Sound → Input
    
    ### ❌ Problem 5: Browser compatibility
    **Solution:**
    - Use Chrome or Firefox (recommended)
    - Update browser to latest version
    - Try in incognito/private mode
    """)

# System info
with st.expander("🔍 System Information"):
    st.code(f"""
Environment: Replit Cloud Server
Display: {os.environ.get('DISPLAY', 'Not set')}
Replit ID: {os.environ.get('REPL_ID', 'Not set')}
Audio Devices on Server: Not available (normal for cloud)
Your Microphone: Connected to YOUR browser, not the server

This is why we use browser-based audio input!
    """)
