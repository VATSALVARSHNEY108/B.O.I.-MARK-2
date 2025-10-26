"""
VATSAL AI - Simple Conversational Chatbot
A friendly AI chatbot for natural conversations
"""

import os
from datetime import datetime
from typing import List, Dict, Any, Optional

try:
    from gemini_controller import GeminiController
except ImportError:
    GeminiController = None


class VatsalAI:
    """Simple conversational AI chatbot"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.name = "VATSAL"
        
        # Initialize Gemini for conversations
        if GeminiController:
            self.gemini = GeminiController(api_key)
        else:
            self.gemini = None
            
        # Conversation history (keep last 20 messages)
        self.conversation_history: List[Dict[str, str]] = []
    
    def initiate_conversation(self) -> str:
        """Start a conversation with a greeting"""
        current_hour = datetime.now().hour
        
        if 5 <= current_hour < 12:
            greeting = "Good morning! How can I help you today?"
        elif 12 <= current_hour < 17:
            greeting = "Good afternoon! What can I do for you?"
        elif 17 <= current_hour < 21:
            greeting = "Good evening! How may I assist you?"
        else:
            greeting = "Hello! How can I help you?"
        
        return greeting
    
    async def process_message(self, user_message: str) -> str:
        """Process user message and return response"""
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "message": user_message
        })
        
        # Get AI response
        if self.gemini:
            response = await self._chat_with_gemini(user_message)
        else:
            response = self._simple_response(user_message)
        
        # Add response to history
        self.conversation_history.append({
            "role": "assistant",
            "message": response
        })
        
        # Keep only last 20 messages (10 exchanges)
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
        
        return response
    
    async def _chat_with_gemini(self, user_message: str) -> str:
        """Use Gemini AI for natural conversation"""
        
        # Build conversation context
        context = self._get_conversation_context()
        
        prompt = f"""You are VATSAL, a friendly and helpful AI assistant chatbot.

Be conversational, friendly, and helpful. Answer questions naturally and provide useful information.
Keep responses concise (2-3 sentences unless more detail is needed).

Previous conversation:
{context}

User: {user_message}

Respond naturally as VATSAL:"""
        
        try:
            response = await self.gemini.analyze_text_async(prompt)
            return response
        except Exception as e:
            return self._simple_response(user_message)
    
    def _simple_response(self, user_message: str) -> str:
        """Simple fallback response without AI"""
        msg_lower = user_message.lower()
        
        # Greetings
        if any(word in msg_lower for word in ["hello", "hi", "hey"]):
            return "Hello! How can I help you today?"
        
        # Thanks
        if any(word in msg_lower for word in ["thank", "thanks"]):
            return "You're welcome! Is there anything else I can help with?"
        
        # Goodbye
        if any(word in msg_lower for word in ["bye", "goodbye", "see you"]):
            return "Goodbye! Have a great day!"
        
        # Questions
        if '?' in user_message:
            return "That's an interesting question! I'd be happy to help answer that."
        
        # Default
        return "I understand. How can I assist you with that?"
    
    def _get_conversation_context(self, limit: int = 6) -> str:
        """Get recent conversation as text"""
        recent = self.conversation_history[-limit:] if len(self.conversation_history) > limit else self.conversation_history
        
        context_lines = []
        for item in recent:
            role = "User" if item["role"] == "user" else "VATSAL"
            context_lines.append(f"{role}: {item['message']}")
        
        return "\n".join(context_lines) if context_lines else "No previous conversation"
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get basic chatbot statistics"""
        return {
            "total_messages": len(self.conversation_history),
            "conversation_length": len(self.conversation_history) // 2,
            "ai_available": self.gemini is not None
        }


def create_vatsal_ai(api_key: Optional[str] = None) -> VatsalAI:
    """Factory function to create VATSAL AI chatbot"""
    return VatsalAI(api_key)


# For testing
if __name__ == "__main__":
    import asyncio
    
    async def test_vatsal():
        vatsal = create_vatsal_ai()
        
        print("\n" + "="*60)
        print("🤖 VATSAL AI - Simple Chatbot")
        print("="*60)
        
        # Initial greeting
        print(f"\n{vatsal.initiate_conversation()}")
        
        # Test conversation
        test_messages = [
            "Hello!",
            "What's the weather like?",
            "Thanks for your help!"
        ]
        
        for msg in test_messages:
            print(f"\nUSER: {msg}")
            response = await vatsal.process_message(msg)
            print(f"VATSAL: {response}")
        
        # Show stats
        print("\n" + "="*60)
        print("📊 Stats:")
        stats = vatsal.get_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    asyncio.run(test_vatsal())
