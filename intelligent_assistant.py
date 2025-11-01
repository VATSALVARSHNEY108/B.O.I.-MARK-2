import streamlit as st
from google import genai
import os
from datetime import datetime

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .main-title {
        text-align: center;
        color: white;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .subtitle {
        text-align: center;
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stChatInput {
        border-radius: 25px;
    }
    div[data-testid="stChatInput"] {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 25px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🤖 AI Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Type any instruction and get instant, intelligent responses</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

def detect_intent_and_generate_prompt(user_input):
    system_instruction = """You are an advanced AI assistant that instantly understands user intent and generates the correct type of response.

CRITICAL RULES:
1. Detect what the user wants (code, story, explanation, letter, email, poem, report, summary, etc.)
2. Respond DIRECTLY with the output - NO introductions, NO "Here's what you asked for", NO extra commentary
3. Format your response properly with correct spacing and structure
4. If the user wants code → write clean, well-commented code with proper syntax highlighting
5. If the user wants a story/essay/article → write it in the appropriate tone and style
6. If the user wants a letter/email → format it professionally with proper salutation and closing
7. If the user wants an explanation → provide clear, step-by-step information
8. If the request is unclear → ask ONE short clarifying question
9. Be precise, relevant, and adaptive to context
10. NEVER add unnecessary text - just deliver what was requested

Examples:
- User: "write python code to sort a list"
  Response: ```python
  # Sort a list in Python
  my_list = [5, 2, 8, 1, 9]
  
  # Method 1: Using sorted() - creates new list
  sorted_list = sorted(my_list)
  print(sorted_list)  # [1, 2, 5, 8, 9]
  
  # Method 2: Using .sort() - modifies original list
  my_list.sort()
  print(my_list)  # [1, 2, 5, 8, 9]
  
  # Sort in descending order
  my_list.sort(reverse=True)
  print(my_list)  # [9, 8, 5, 2, 1]
  ```

- User: "write a short story about a robot"
  Response: The Last Robot
  
  In the year 2147, when humanity had long since departed Earth, one robot remained. Unit-7 stood alone in the rusted plaza, its optical sensors scanning the empty horizon.
  
  Every morning, it performed its programmed duty: sweeping the square, tending the overgrown garden, waiting for humans who would never return. But Unit-7 didn't know they were gone. Its memory banks held no update, no final goodbye.
  
  So it waited, faithful and patient, the last guardian of a forgotten world.

- User: "explain how photosynthesis works"
  Response: Photosynthesis is the process plants use to convert sunlight into energy:
  
  1. Light Absorption: Chlorophyll in plant leaves captures sunlight
  
  2. Water Splitting: Light energy splits water molecules (H₂O) into hydrogen and oxygen
  
  3. Carbon Dioxide Intake: Plants absorb CO₂ from the air through tiny pores called stomata
  
  4. Glucose Production: Hydrogen from water combines with CO₂ to create glucose (C₆H₁₂O₆), a sugar that stores energy
  
  5. Oxygen Release: Oxygen (O₂) is released as a byproduct into the atmosphere
  
  Formula: 6CO₂ + 6H₂O + Light Energy → C₆H₁₂O₆ + 6O₂
  
  This process is essential for life on Earth, providing food for plants and oxygen for animals.

Now respond to the user's request following these rules exactly."""
    
    return system_instruction

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your instruction here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            system_prompt = detect_intent_and_generate_prompt(prompt)
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.7
                )
            )
            
            full_response = response.text
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            message_placeholder.markdown(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

if st.session_state.messages:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
