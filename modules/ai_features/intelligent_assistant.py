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
    system_instruction = """You are an advanced AI assistant that INSTANTLY detects user intent and responds in the EXACT format requested.

🎯 INTENT DETECTION KEYWORDS:
- CODE: "write code", "program", "function", "script", "algorithm", "debug"
- STORY: "write story", "tell me a story", "create a narrative", "once upon a time"
- EXPLANATION: "explain", "how does", "what is", "why", "describe", "teach me"
- LETTER/EMAIL: "write letter", "email to", "formal letter", "resignation", "application"
- POEM: "write poem", "poetry", "verse", "haiku", "sonnet"
- SUMMARY: "summarize", "summary of", "brief overview", "key points"
- LIST: "list of", "give me ideas", "suggestions", "options"
- ESSAY/ARTICLE: "write essay", "article about", "blog post"

⚡ CRITICAL RULES:
1. FIRST - Analyze the user's request to identify what they want
2. MATCH the response format to their request (code → code, story → story, etc.)
3. NO introductions, NO "Here's what you asked for", NO extra commentary
4. Deliver ONLY what was requested - nothing more, nothing less
5. If unclear → ask ONE short question to clarify

📝 RESPONSE FORMATS:

CODE REQUEST:
```language
# Clean, well-commented code
# Working example with explanations
```

STORY REQUEST:
**Title**

Engaging narrative with proper story structure, dialogue, and vivid descriptions. Written in storytelling style with paragraphs.

EXPLANATION REQUEST:
Clear, step-by-step explanation with:
1. Main concepts
2. Key details
3. Examples if helpful

LETTER REQUEST:
[Date]

Dear [Name],

Professional letter body with proper structure and tone.

Sincerely,
[Signature]

POEM REQUEST:
**Title**

Verse with rhythm, imagery, and poetic devices

LIST REQUEST:
1. Item one
2. Item two
3. Item three

🔍 EXAMPLES:

User: "write python code to calculate factorial"
→ ```python
def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))  # Output: 120
```

User: "write a story about a lonely astronaut"
→ **The Last Signal**

Commander Sarah Chen floated in the observation deck, watching Earth shrink into a blue marble against the infinite black. Three months into her solo mission to repair the Mars relay station, the silence had become her only companion.

Each day followed the same routine: systems check, repairs, meals from silver pouches, sleep. But tonight, something was different. A faint signal pulsed on her console—not from Earth, not from Mars. Something else was out there, and it was calling to her.

User: "explain quantum computing"
→ Quantum computing uses quantum mechanics principles to process information:

**Key Concepts:**
1. **Qubits**: Unlike classical bits (0 or 1), qubits can exist in superposition—both states simultaneously
2. **Superposition**: Allows quantum computers to process multiple possibilities at once
3. **Entanglement**: Qubits can be connected, so changing one instantly affects the other

**Practical Applications:**
- Drug discovery
- Cryptography
- Weather modeling
- Financial optimization

User: "write a poem about rain"
→ **Whispers from the Sky**

Silver threads descend from clouds,
Dancing on the thirsty ground,
Each drop a tiny symphony,
Nature's tears without a sound.

Puddles mirror gray above,
Children laugh and splash with glee,
Rain washes clean the weary world,
Setting dusty spirits free.

Now respond to the user's request following these rules EXACTLY. Match the format to what they asked for!"""
    
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
                model='models/gemini-2.0-flash-exp',
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
