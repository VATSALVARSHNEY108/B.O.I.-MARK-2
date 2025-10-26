#!/usr/bin/env python3
"""
Simple VATSAL Chatbot - Powered by Google Gemini AI
A clean, easy-to-use chatbot with conversation memory
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


class SimpleChatbot:
    """Simple chatbot using Gemini AI"""
    
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"
        self.conversation_history = []
        
        self.system_prompt = """You are VATSAL, a friendly and helpful AI assistant.

Your personality:
- Friendly, approachable, and knowledgeable
- Clear and concise in your explanations
- Patient and understanding
- Professional yet warm

Guidelines:
- Keep responses concise but complete
- Be helpful and encouraging
- Remember the conversation context"""
    
    def chat(self, user_message):
        """Send a message and get AI response"""
        try:
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            
            conversation_text = ""
            for msg in self.conversation_history[-10:]:
                role = "User" if msg["role"] == "user" else "VATSAL"
                conversation_text += f"{role}: {msg['content']}\n"
            
            conversation_text += "VATSAL:"
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=conversation_text,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    temperature=0.8,
                    max_output_tokens=1500,
                )
            )
            
            ai_response = response.text.strip()
            
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_response
            })
            
            return ai_response
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"
    
    def reset(self):
        """Clear conversation history"""
        self.conversation_history = []
        return "Conversation reset! Let's start fresh."
    
    def greeting(self):
        """Get a greeting message"""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            time_greeting = "Good morning"
        elif 12 <= hour < 17:
            time_greeting = "Good afternoon"
        elif 17 <= hour < 22:
            time_greeting = "Good evening"
        else:
            time_greeting = "Hello"
        
        return f"{time_greeting}! I'm VATSAL, your AI assistant. How can I help you today?"


def main():
    """Run the chatbot"""
    
    print("\n" + "="*60)
    print("🤖 VATSAL - Simple AI Chatbot")
    print("="*60)
    print("\n💬 Commands:")
    print("   • Type your message to chat")
    print("   • 'reset' - Start a new conversation")
    print("   • 'quit' or 'exit' - End chat")
    print("="*60 + "\n")
    
    try:
        chatbot = SimpleChatbot()
        print(f"🤖 VATSAL: {chatbot.greeting()}\n")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n📝 Make sure GEMINI_API_KEY is set in your Replit Secrets")
        return
    
    while True:
        try:
            user_input = input("👤 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n🤖 VATSAL: Goodbye! Have a great day! 👋\n")
                break
            
            if user_input.lower() == 'reset':
                message = chatbot.reset()
                print(f"\n🔄 {message}\n")
                continue
            
            response = chatbot.chat(user_input)
            print(f"\n🤖 VATSAL: {response}\n")
        
        except KeyboardInterrupt:
            print("\n\n🤖 VATSAL: Goodbye! 👋\n")
            break
        
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
