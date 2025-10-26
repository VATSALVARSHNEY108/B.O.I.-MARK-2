#!/usr/bin/env python3
"""
Simple Intelligent Chatbot powered by Google Gemini AI
Ask any question and get intelligent answers!
"""

import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()


class SimpleChatbot:
    """Simple intelligent chatbot using Gemini AI"""
    
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.0-flash-exp"
        self.conversation_history = []
    
    def chat(self, user_message: str) -> str:
        """Send a message and get AI response"""
        
        # Add user message to history
        self.conversation_history.append(f"User: {user_message}")
        
        # Build conversation context (last 10 messages)
        context = "\n".join(self.conversation_history[-10:])
        prompt = f"{context}\n\nAssistant:"
        
        # System instruction for the AI
        system_instruction = """You are a helpful, friendly, and knowledgeable AI assistant.
Provide clear, simple, and accurate answers to questions.
Be concise but complete in your explanations.
Use examples when helpful.
For technical topics, explain in simple terms first."""
        
        # Get response from Gemini
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
                max_output_tokens=1000,
            )
        )
        
        ai_response = response.text.strip()
        
        # Add AI response to history
        self.conversation_history.append(f"Assistant: {ai_response}")
        
        return ai_response
    
    def reset(self):
        """Clear conversation history"""
        self.conversation_history = []
        return "Conversation reset! Starting fresh."


def create_vatsal_ai(api_key=None):
    """Create chatbot instance (for compatibility with GUI app)"""
    return SimpleChatbot(api_key)


def print_header():
    """Display chatbot header"""
    print("\n" + "="*70)
    print("🤖 Intelligent AI Chatbot (Powered by Google Gemini)")
    print("="*70)
    print("💡 Ask me anything! I can help with:")
    print("   • General knowledge & facts")
    print("   • Programming & coding")
    print("   • Math & science")
    print("   • Writing & creativity")
    print("   • Explanations & how-to guides")
    print("   • And much more!")
    print("\n💬 Commands:")
    print("   • Type your question to get an answer")
    print("   • Type 'reset' to start a new conversation")
    print("   • Type 'quit' or 'exit' to end")
    print("="*70 + "\n")


def main():
    """Run the chatbot"""
    
    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY not found!")
        print("Please set your Gemini API key in environment variables.")
        sys.exit(1)
    
    # Initialize chatbot
    print("🔧 Initializing AI chatbot...")
    try:
        chatbot = SimpleChatbot()
        print("✅ Chatbot ready!\n")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    
    # Display header
    print_header()
    
    # Initial greeting
    print("🤖 AI: Hello! I'm your intelligent AI assistant. Ask me anything!\n")
    
    # Main conversation loop
    while True:
        try:
            # Get user input
            user_input = input("👤 You: ").strip()
            
            # Skip empty input
            if not user_input:
                continue
            
            # Handle exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("\n🤖 AI: Goodbye! Have a great day! 👋\n")
                break
            
            # Handle reset command
            if user_input.lower() == 'reset':
                message = chatbot.reset()
                print(f"\n🔄 {message}\n")
                continue
            
            # Get AI response
            print("\n🤖 AI: ", end="", flush=True)
            response = chatbot.chat(user_input)
            print(f"{response}\n")
        
        except KeyboardInterrupt:
            print("\n\n🤖 AI: Goodbye! 👋\n")
            break
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()
