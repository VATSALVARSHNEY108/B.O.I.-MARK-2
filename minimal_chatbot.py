#!/usr/bin/env python3

import streamlit as st
import streamlit.components.v1 as components
import random
from datetime import datetime
import math
import platform
import psutil
import os

st.set_page_config(page_title="Minimal Chat", page_icon="💬")

st.title("💬 Minimal Chatbot")

st.markdown("""
<style>
    .stButton button {
        width: 100%;
        padding: 15px;
        font-size: 18px;
        margin: 5px 0;
    }
    @media (max-width: 768px) {
        .stChatInput input {
            font-size: 16px;
        }
    }
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("⏰ Time"):
        st.session_state.quick_cmd = "time"
with col2:
    if st.button("📅 Date"):
        st.session_state.quick_cmd = "date"
with col3:
    if st.button("💻 System"):
        st.session_state.quick_cmd = "system status"
with col4:
    if st.button("❓ Help"):
        st.session_state.quick_cmd = "help"

def speak_text(text):
    components.html(
        f"""
        <script>
            const utterance = new SpeechSynthesisUtterance("{text}");
            utterance.rate = 1.0;
            utterance.pitch = 1.0;
            utterance.volume = 1.0;
            window.speechSynthesis.speak(utterance);
        </script>
        """,
        height=0,
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

if "quick_cmd" not in st.session_state:
    st.session_state.quick_cmd = None

if "reminders" not in st.session_state:
    st.session_state.reminders = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def calculate(expression):
    try:
        allowed = set("0123456789+-*/()%. ")
        if all(c in allowed for c in expression):
            result = eval(expression)
            return str(result)
    except:
        pass
    return None

def get_system_info():
    try:
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        return f"CPU: {cpu}%, Memory: {memory}%"
    except:
        return "System running smoothly."

def send_sms(phone_number, message):
    try:
        from twilio.rest import Client
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        twilio_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        if not all([account_sid, auth_token, twilio_number]):
            return "Twilio not configured. Set up required."
        
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message,
            from_=twilio_number,
            to=phone_number
        )
        return f"SMS sent to {phone_number}!"
    except ImportError:
        return "Twilio not installed."
    except Exception as e:
        return f"SMS failed: {str(e)}"

def make_call(phone_number):
    try:
        from twilio.rest import Client
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        twilio_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        if not all([account_sid, auth_token, twilio_number]):
            return "Twilio not configured."
        
        client = Client(account_sid, auth_token)
        call = client.calls.create(
            url='http://demo.twilio.com/docs/voice.xml',
            to=phone_number,
            from_=twilio_number
        )
        return f"Calling {phone_number}..."
    except ImportError:
        return "Twilio not installed."
    except Exception as e:
        return f"Call failed: {str(e)}"

def get_minimal_response(user_input):
    user_lower = user_input.lower().strip()
    
    if ("text" in user_lower or "sms" in user_lower or "message" in user_lower) and any(word in user_lower for word in ["send", "to"]):
        parts = user_input.split()
        phone_idx = -1
        for i, part in enumerate(parts):
            if part.replace("+", "").replace("-", "").replace(" ", "").isdigit():
                phone_idx = i
                break
        
        if phone_idx >= 0:
            phone = parts[phone_idx]
            message_parts = parts[phone_idx+1:] if phone_idx+1 < len(parts) else ["Hello"]
            msg_text = " ".join(message_parts) if message_parts else "Hello"
            return send_sms(phone, msg_text)
        return "Need phone number. Try: 'text +1234567890 hello'"
    
    elif ("call" in user_lower or "phone" in user_lower) and any(word in user_lower for word in ["make", "dial"]):
        parts = user_input.split()
        for part in parts:
            if part.replace("+", "").replace("-", "").replace(" ", "").isdigit() and len(part) >= 10:
                return make_call(part)
        return "Need phone number. Try: 'call +1234567890'"
    
    elif "find" in user_lower and "phone" in user_lower:
        return "Phone locator activated. (simulated) 📍"
    
    elif "lock" in user_lower and "phone" in user_lower:
        return "Phone locked remotely. 🔒"
    
    elif "unlock" in user_lower and "phone" in user_lower:
        return "Phone unlocked. 🔓"
    
    elif "ring" in user_lower and "phone" in user_lower:
        return "Ringing your phone... 📱🔔"
    
    elif "silent" in user_lower or "dnd" in user_lower or "do not disturb" in user_lower:
        if "on" in user_lower or "enable" in user_lower:
            return "Silent mode on. 🔕"
        elif "off" in user_lower or "disable" in user_lower:
            return "Silent mode off. 🔔"
        return "Silent mode active."
    
    elif "remind" in user_lower and ("me" in user_lower or "set" in user_lower):
        reminder_text = user_input.replace("remind me", "").replace("set reminder", "").strip()
        st.session_state.reminders.append({
            "text": reminder_text,
            "time": datetime.now().strftime("%I:%M %p")
        })
        return f"Reminder set: {reminder_text}"
    
    elif "show" in user_lower and "reminder" in user_lower:
        if st.session_state.reminders:
            reminders = "\n".join([f"- {r['text']} ({r['time']})" for r in st.session_state.reminders])
            return f"Reminders:\n{reminders}"
        return "No reminders set."
    
    elif "clear" in user_lower and "reminder" in user_lower:
        count = len(st.session_state.reminders)
        st.session_state.reminders = []
        return f"Cleared {count} reminders."
    
    elif any(word in user_lower for word in ["open", "launch", "start"]) and any(app in user_lower for app in ["chrome", "browser", "calculator", "music", "spotify", "youtube", "gmail", "maps"]):
        apps = ["chrome", "browser", "calculator", "music", "spotify", "youtube", "gmail", "maps"]
        app_found = next((app for app in apps if app in user_lower), None)
        if app_found:
            return f"Opening {app_found}... (simulated)"
        return "Can't find that app."
    
    elif "volume" in user_lower:
        if "up" in user_lower or "increase" in user_lower or "+" in user_lower:
            return "Volume up. 🔊"
        elif "down" in user_lower or "decrease" in user_lower or "-" in user_lower:
            return "Volume down. 🔉"
        elif "mute" in user_lower:
            return "Muted. 🔇"
        return "Volume at 50%."
    
    elif "brightness" in user_lower:
        if "up" in user_lower or "increase" in user_lower:
            return "Brightness up. ☀️"
        elif "down" in user_lower or "decrease" in user_lower:
            return "Brightness down. 🌙"
        return "Brightness at 50%."
    
    elif any(word in user_lower for word in ["wifi", "wi-fi"]):
        if "on" in user_lower or "enable" in user_lower:
            return "WiFi enabled. 📶"
        elif "off" in user_lower or "disable" in user_lower:
            return "WiFi disabled."
        return "WiFi connected."
    
    elif "bluetooth" in user_lower:
        if "on" in user_lower or "enable" in user_lower:
            return "Bluetooth on. 🔵"
        elif "off" in user_lower or "disable" in user_lower:
            return "Bluetooth off."
        return "Bluetooth ready."
    
    elif "battery" in user_lower or "charge" in user_lower:
        return random.choice(["Battery at 85%.", "75% charged.", "Nearly full.", "Battery good.", "92% remaining."])
    
    elif any(word in user_lower for word in ["time", "what time"]):
        current_time = datetime.now().strftime("%I:%M %p")
        return f"It's {current_time}."
    
    elif any(word in user_lower for word in ["date", "what day", "today"]) and "update" not in user_lower:
        current_date = datetime.now().strftime("%B %d, %Y")
        day = datetime.now().strftime("%A")
        return f"{day}, {current_date}."
    
    elif "calculate" in user_lower or "+" in user_input or "-" in user_input or "*" in user_input or "/" in user_input:
        parts = user_input.split()
        for part in parts:
            result = calculate(part)
            if result:
                return f"Result: {result}"
        nums = [word for word in parts if word.replace(".", "").replace("-", "").isdigit()]
        if len(nums) >= 2:
            expr = " ".join(parts[-5:])
            result = calculate(expr)
            if result:
                return f"Result: {result}"
        return "Can't calculate that."
    
    elif "system" in user_lower and any(word in user_lower for word in ["status", "info", "check"]):
        return get_system_info()
    
    elif "weather" in user_lower:
        return random.choice(["Check outside.", "No idea, mate.", "Sunny, probably.", "Ask Google.", "It's fine."])
    
    elif any(word in user_lower for word in ["hello", "hi", "hey", "hola", "greetings"]):
        return random.choice(["Oh, you again.", "Yeah, hi.", "Sup.", "Hey there.", "What now?", "Greetings."])
    
    elif any(word in user_lower for word in ["how are you", "how r u", "wassup"]):
        return random.choice(["Peachy.", "Living the dream.", "Stellar, obviously.", "Better than you.", "Still here."])
    
    elif any(word in user_lower for word in ["bye", "goodbye", "see you", "later"]):
        return random.choice(["Finally.", "Bye.", "See ya.", "Later, I guess.", "Off you go."])
    
    elif any(word in user_lower for word in ["thanks", "thank you", "thx"]):
        return random.choice(["Sure.", "Uh-huh.", "No worries.", "Don't mention it.", "Yeah, yeah."])
    
    elif any(word in user_lower for word in ["sorry", "my bad", "apologies"]):
        return random.choice(["Whatever.", "Sure you are.", "Noted.", "Happens.", "Mmhmm."])
    
    elif any(word in user_lower for word in ["love you", "i love", "ily"]):
        return random.choice(["Sure you do.", "Aww, how sweet.", "That's nice.", "Cool story.", "OK then."])
    
    elif any(word in user_lower for word in ["help", "what can you do", "features"]):
        return """📱 Mobile Phone Control:
• Send SMS: "text +123 hello"
• Make Call: "call +123"
• Find Phone: "find phone"
• Lock/Unlock Phone
• Ring Phone
• Silent Mode On/Off
• Reminders
• Volume/Brightness
• WiFi/Bluetooth
• Battery Status
• Time, Date, Calculator
• System Status"""
    
    elif any(word in user_lower for word in ["stupid", "dumb", "idiot", "useless"]):
        return random.choice(["Right back at ya.", "Original.", "Harsh.", "Ouch.", "Love you too."])
    
    elif any(word in user_lower for word in ["smart", "clever", "genius", "brilliant"]):
        return random.choice(["I know.", "Obviously.", "Tell me more.", "Yep.", "Thanks, I try."])
    
    elif any(word in user_lower for word in ["funny", "lol", "haha", "😂"]):
        return random.choice(["I try.", "Glad you think so.", "Yeah, hilarious.", "My pleasure.", "😏"])
    
    elif any(word in user_lower for word in ["boring", "bored"]):
        return random.choice(["Same.", "Story of my life.", "Tell me about it.", "Join the club.", "Yawn."])
    
    elif "what" in user_lower and "name" in user_lower:
        return random.choice(["Does it matter?", "Call me Bot.", "Just Bot.", "Nobody important.", "Not telling."])
    
    elif "why" in user_lower:
        return random.choice(["Because.", "Why not?", "Good question.", "Dunno.", "Life's mysteries."])
    
    elif "how" in user_lower and "?" in user_input:
        return random.choice(["Magic.", "Very carefully.", "It's complicated.", "Wouldn't you like to know.", "Figure it out."])
    
    elif "?" in user_input:
        return random.choice(["Maybe.", "Probably not.", "Who knows?", "Ask again later.", "Doubtful."])
    
    elif user_lower in ["ok", "okay", "k"]:
        return random.choice(["K.", "Yep.", "Cool.", "Uh-huh.", "Right."])
    
    elif len(user_input) > 100:
        return random.choice(["Too long, didn't read.", "Wow, that's a lot.", "Summarize?", "Short version?", "Cool essay."])
    
    else:
        return random.choice(["OK.", "Sure.", "Whatever.", "Noted.", "Interesting.", "Cool.", "If you say so.", "Mmhmm."])

if st.session_state.quick_cmd:
    prompt = st.session_state.quick_cmd
    st.session_state.quick_cmd = None
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    response = get_minimal_response(prompt)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
    
    speak_text(response)
    st.rerun()

if prompt := st.chat_input("Say something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    response = get_minimal_response(prompt)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
    
    speak_text(response)
