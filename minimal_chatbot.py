#!/usr/bin/env python3

import streamlit as st
import streamlit.components.v1 as components
import random
from datetime import datetime
import math
import platform
import psutil

st.set_page_config(page_title="Minimal Chat", page_icon="💬")

st.title("💬 Minimal Chatbot")

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

def get_minimal_response(user_input):
    user_lower = user_input.lower().strip()
    
    if any(word in user_lower for word in ["time", "what time"]):
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
        return "Time, date, math, system info, chat."
    
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

if prompt := st.chat_input("Say something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    response = get_minimal_response(prompt)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
    
    speak_text(response)
