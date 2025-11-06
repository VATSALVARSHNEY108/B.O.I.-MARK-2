#!/usr/bin/env python3

import streamlit as st

st.set_page_config(page_title="Minimal Chat", page_icon="💬")

st.title("💬 Minimal Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def get_minimal_response(user_input):
    user_lower = user_input.lower().strip()
    
    if any(word in user_lower for word in ["hello", "hi", "hey", "hola"]):
        return "Hi!"
    
    elif any(word in user_lower for word in ["how are you", "how r u", "wassup", "sup"]):
        return "Good!"
    
    elif any(word in user_lower for word in ["bye", "goodbye", "see you"]):
        return "Bye!"
    
    elif any(word in user_lower for word in ["thanks", "thank you", "thx"]):
        return "Welcome!"
    
    elif any(word in user_lower for word in ["yes", "yeah", "yep", "yup"]):
        return "OK!"
    
    elif any(word in user_lower for word in ["no", "nope", "nah"]):
        return "OK!"
    
    elif any(word in user_lower for word in ["help", "what can you do"]):
        return "I chat!"
    
    elif "?" in user_input:
        return "Hmm..."
    
    else:
        return "OK!"

if prompt := st.chat_input("Say something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    response = get_minimal_response(prompt)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
