# 🤖 VATSAL AI Chatbot

An intelligent chatbot powered by Google Gemini AI that can answer any type of question!

## 🌟 Features

- **Intelligent Responses**: Uses Google Gemini AI to provide accurate, helpful answers
- **Learning Capability**: Remembers your preferences and conversation history
- **Persistent Memory**: Saves conversations between sessions
- **Comprehensive Knowledge**: Can help with:
  - General knowledge questions
  - Programming and coding help
  - Math and science problems
  - Creative writing and ideas
  - Explanations and tutorials
  - And much more!

## 🚀 How to Use

### Running the Chatbot

You can run the chatbot in two ways:

**Option 1: Run the main AI file directly (Recommended)**
```bash
python vatsal_ai.py
```

**Option 2: Run the standalone chatbot script**
```bash
python vatsal_chatbot.py
```

Both options provide the same intelligent chatbot experience!

### Interactive Commands

Once the chatbot is running, you can:

- **Ask any question**: Just type your question and press Enter
- **View statistics**: Type `stats` to see chatbot usage statistics
- **Reset conversation**: Type `reset` to start a new conversation
- **Exit**: Type `quit`, `exit`, or `bye` to end the session

### Example Conversation

```
👤 You: What is Python?
🤖 VATSAL: Python is a high-level programming language...

👤 You: How do I create a list in Python?
🤖 VATSAL: You can create a list in Python using square brackets...

👤 You: stats
📊 Chatbot Statistics:
  👤 User Name: User
  💬 Messages this session: 2
  ...

👤 You: quit
🤖 VATSAL: Goodbye! It was nice talking with you.
```

## 💾 Memory System

The chatbot uses a persistent memory system that:
- Saves all conversations to `vatsal_memory.json`
- Learns your preferences and interests over time
- Remembers your name and conversation style
- Tracks topics you discuss most frequently

## 🔑 Requirements

- Python 3.8+
- Google Gemini API key (set as `GEMINI_API_KEY` environment variable)
- Required packages (automatically installed):
  - google-genai
  - python-dotenv

## 📊 Statistics Tracking

The chatbot tracks:
- Total number of conversations
- Total messages exchanged
- Your learned preferences
- Most discussed topics
- First and last interaction times

## 🎯 Tips for Best Results

1. **Be specific**: The more specific your question, the better the answer
2. **Ask follow-ups**: The chatbot maintains conversation context
3. **Check stats**: Use `stats` to see what the chatbot has learned about you
4. **Start fresh**: Use `reset` if you want to change topics completely

## 🛠️ Technical Details

- Built on the existing VATSAL AI framework
- Uses async/await for efficient processing
- Integrates with Google Gemini for natural language understanding
- Stores data in JSON format for easy portability

## 📝 Example Questions to Try

- "Explain quantum computing in simple terms"
- "Write a Python function to reverse a string"
- "What are the capitals of European countries?"
- "Help me debug this code: [paste your code]"
- "Create a creative story about space exploration"
- "Explain the difference between machine learning and deep learning"

---

**Enjoy chatting with VATSAL AI!** 🎉
