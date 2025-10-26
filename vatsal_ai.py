"""
VATSAL AI - Intelligent Chatbot with Gemini AI
A smart AI chatbot powered by Google Gemini that can answer any type of question
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from google import genai
from google.genai import types


class VatsalAI:
    """Intelligent conversational AI chatbot powered by Google Gemini"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.name = "VATSAL"
        self.memory_file = "vatsal_memory.json"
        
        # Initialize Gemini AI client
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.0-flash-exp"
        
        # Load persistent memory
        self.memory = self._load_memory()
        
        # Current session conversation
        self.current_conversation: List[Dict[str, str]] = []
        
        # User profile and learning data
        self.user_profile = self.memory.get("user_profile", {
            "name": "User",
            "preferences": {},
            "interests": [],
            "common_topics": [],
            "conversation_style": "friendly"
        })
        
        # All past conversations (loaded from memory)
        self.all_conversations = self.memory.get("conversations", [])
        
        # Statistics
        self.stats = self.memory.get("stats", {
            "total_conversations": 0,
            "total_messages": 0,
            "favorite_topics": {},
            "first_interaction": None,
            "last_interaction": None
        })
    
    def _load_memory(self) -> Dict[str, Any]:
        """Load persistent memory from file"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_memory(self):
        """Save memory to persistent storage"""
        try:
            self.memory = {
                "user_profile": self.user_profile,
                "conversations": self.all_conversations[-50:],
                "stats": self.stats,
                "last_saved": datetime.now().isoformat()
            }
            with open(self.memory_file, 'w') as f:
                json.dump(self.memory, f, indent=2)
        except Exception as e:
            print(f"Failed to save memory: {e}")
    
    def initiate_conversation(self) -> str:
        """Start a conversation with a personalized greeting"""
        current_hour = datetime.now().hour
        
        if 5 <= current_hour < 12:
            time_greeting = "Good morning"
        elif 12 <= current_hour < 17:
            time_greeting = "Good afternoon"
        elif 17 <= current_hour < 21:
            time_greeting = "Good evening"
        else:
            time_greeting = "Hello"
        
        user_name = self.user_profile.get("name", "")
        if user_name and user_name != "User":
            greeting = f"{time_greeting}, {user_name}!"
        else:
            greeting = f"{time_greeting}!"
        
        if self.stats.get("total_conversations", 0) > 0:
            greeting += " Welcome back! How can I help you today?"
        else:
            greeting += " I'm VATSAL, your AI assistant. I learn from our conversations to help you better. What can I help you with?"
        
        return greeting
    
    async def process_message(self, user_message: str) -> str:
        """Process user message with Gemini AI"""
        
        message_data = {
            "role": "user",
            "message": user_message,
            "timestamp": datetime.now().isoformat()
        }
        self.current_conversation.append(message_data)
        
        self._learn_from_message(user_message)
        
        try:
            response = await self._get_gemini_response(user_message)
        except Exception as e:
            response = f"I apologize, but I encountered an error: {str(e)}. Please try again."
        
        response_data = {
            "role": "assistant",
            "message": response,
            "timestamp": datetime.now().isoformat()
        }
        self.current_conversation.append(response_data)
        
        self._update_stats()
        
        return response
    
    async def _get_gemini_response(self, user_message: str) -> str:
        """Get response from Gemini AI with context"""
        
        context = self._build_context()
        
        system_instruction = f"""You are VATSAL, an intelligent and helpful AI assistant. 
Your personality: Friendly, knowledgeable, and concise.

Guidelines:
- Provide clear, simple, and direct answers
- Be helpful and informative
- Keep responses concise but complete
- Use examples when helpful
- Be encouraging and positive
- For technical topics, explain in simple terms first, then add details if needed

{context}"""
        
        conversation_history = self._get_recent_context(limit=10)
        
        full_prompt = f"{conversation_history}\n\nUser: {user_message}\n\nVATSAL:"
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=full_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
                max_output_tokens=1000,
            )
        )
        
        return response.text.strip()
    
    def _build_context(self) -> str:
        """Build context from user profile and conversation history"""
        context_parts = []
        
        if self.user_profile.get("name") and self.user_profile["name"] != "User":
            context_parts.append(f"User's name: {self.user_profile['name']}")
        
        if self.user_profile.get("interests"):
            context_parts.append(f"User's interests: {', '.join(self.user_profile['interests'][:5])}")
        
        if self.user_profile.get("common_topics"):
            context_parts.append(f"Common topics: {', '.join(self.user_profile['common_topics'][:5])}")
        
        if context_parts:
            return "Context:\n" + "\n".join(context_parts)
        return ""
    
    def _get_recent_context(self, limit: int = 5) -> str:
        """Get recent conversation context"""
        if not self.current_conversation:
            return ""
        
        recent = self.current_conversation[-limit*2:]
        context_lines = []
        
        for msg in recent:
            role = "User" if msg["role"] == "user" else "VATSAL"
            context_lines.append(f"{role}: {msg['message']}")
        
        return "\n".join(context_lines) if context_lines else ""
    
    def _learn_from_message(self, message: str):
        """Learn from user messages"""
        msg_lower = message.lower()
        
        if "my name is" in msg_lower or "i'm " in msg_lower or "i am " in msg_lower:
            words = message.split()
            for i, word in enumerate(words):
                if word.lower() in ["name", "i'm", "i am"] and i < len(words) - 1:
                    potential_name = words[i + 1].strip(",.!?")
                    if potential_name and len(potential_name) > 1:
                        self.user_profile["name"] = potential_name.capitalize()
        
        keywords = ["python", "javascript", "ai", "programming", "music", "sports", "science", "math"]
        for keyword in keywords:
            if keyword in msg_lower:
                if keyword not in self.user_profile.get("interests", []):
                    if "interests" not in self.user_profile:
                        self.user_profile["interests"] = []
                    self.user_profile["interests"].append(keyword)
                
                if keyword not in self.stats.get("favorite_topics", {}):
                    if "favorite_topics" not in self.stats:
                        self.stats["favorite_topics"] = {}
                    self.stats["favorite_topics"][keyword] = 0
                self.stats["favorite_topics"][keyword] += 1
    
    def _update_stats(self):
        """Update conversation statistics"""
        self.stats["total_messages"] = self.stats.get("total_messages", 0) + 1
        self.stats["last_interaction"] = datetime.now().isoformat()
        
        if not self.stats.get("first_interaction"):
            self.stats["first_interaction"] = datetime.now().isoformat()
    
    def _save_conversation_to_memory(self):
        """Save current conversation to long-term memory"""
        if self.current_conversation:
            self.all_conversations.append(self.current_conversation.copy())
            self.stats["total_conversations"] = len(self.all_conversations)
    
    def end_conversation(self):
        """Properly end conversation and save everything"""
        self._save_conversation_to_memory()
        self._save_memory()
        self.current_conversation = []
    
    def reset_conversation(self):
        """Clear current conversation but keep long-term memory"""
        self._save_conversation_to_memory()
        self._save_memory()
        self.current_conversation = []
    
    def reset_all_memory(self):
        """Completely reset all memory (use with caution)"""
        self.current_conversation = []
        self.all_conversations = []
        self.user_profile = {
            "name": "User",
            "preferences": {},
            "interests": [],
            "common_topics": [],
            "conversation_style": "friendly"
        }
        self.stats = {
            "total_conversations": 0,
            "total_messages": 0,
            "favorite_topics": {},
            "first_interaction": None,
            "last_interaction": None
        }
        self._save_memory()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive chatbot statistics"""
        return {
            "current_messages": len(self.current_conversation),
            "total_conversations": self.stats.get("total_conversations", 0),
            "total_messages": self.stats.get("total_messages", 0),
            "learned_preferences": len(self.user_profile.get("preferences", [])),
            "top_topics": self._get_top_topics(5),
            "user_name": self.user_profile.get("name", "Unknown"),
            "ai_available": True,
            "first_interaction": self.stats.get("first_interaction", "Never"),
            "last_interaction": self.stats.get("last_interaction", "Never")
        }
    
    def _get_top_topics(self, limit: int = 5) -> List[str]:
        """Get most discussed topics"""
        if not self.stats.get("favorite_topics"):
            return []
        sorted_topics = sorted(self.stats["favorite_topics"].items(), key=lambda x: x[1], reverse=True)
        return [topic[0] for topic in sorted_topics[:limit]]


def create_vatsal_ai(api_key: Optional[str] = None) -> VatsalAI:
    """Factory function to create VATSAL AI chatbot"""
    return VatsalAI(api_key)


# Interactive Chatbot - Run this file directly to start chatting!
if __name__ == "__main__":
    import asyncio
    import sys
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    def print_header():
        """Display chatbot header"""
        print("\n" + "="*70)
        print("🤖 VATSAL AI - Intelligent Chatbot (Powered by Google Gemini)")
        print("="*70)
        print("💡 Ask me anything! I can help with:")
        print("   • General knowledge questions")
        print("   • Coding and programming help")
        print("   • Math and science problems")
        print("   • Creative writing and ideas")
        print("   • Explanations and tutorials")
        print("   • And much more!")
        print("\n📝 Type 'quit', 'exit', or 'bye' to end the conversation")
        print("📊 Type 'stats' to see chatbot statistics")
        print("🔄 Type 'reset' to start a new conversation")
        print("="*70 + "\n")
    
    async def run_chatbot():
        """Main chatbot conversation loop"""
        if not os.getenv("GEMINI_API_KEY"):
            print("❌ Error: GEMINI_API_KEY not found!")
            print("Please set your Gemini API key in the .env file or environment variables.")
            sys.exit(1)
        
        print("🔧 Initializing VATSAL AI chatbot...")
        try:
            vatsal = create_vatsal_ai()
            print("✅ Chatbot ready!\n")
        except Exception as e:
            print(f"❌ Error initializing chatbot: {e}")
            sys.exit(1)
        
        print_header()
        
        greeting = vatsal.initiate_conversation()
        print(f"🤖 VATSAL: {greeting}\n")
        
        conversation_active = True
        
        while conversation_active:
            try:
                user_input = input("👤 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    print("\n🤖 VATSAL: Goodbye! It was nice talking with you. Your conversation has been saved!")
                    vatsal.end_conversation()
                    conversation_active = False
                    break
                
                elif user_input.lower() == 'stats':
                    stats = vatsal.get_stats()
                    print("\n📊 Chatbot Statistics:")
                    print("="*50)
                    print(f"  👤 User Name: {stats.get('user_name', 'Unknown')}")
                    print(f"  💬 Messages this session: {stats.get('current_messages', 0)}")
                    print(f"  📝 Total conversations: {stats.get('total_conversations', 0)}")
                    print(f"  📨 Total messages: {stats.get('total_messages', 0)}")
                    print(f"  🎯 Learned preferences: {stats.get('learned_preferences', 0)}")
                    print(f"  🔥 Top topics: {', '.join(stats.get('top_topics', []))}")
                    print(f"  🤖 AI available: {stats.get('ai_available', False)}")
                    print(f"  📅 First interaction: {stats.get('first_interaction', 'Never')}")
                    print(f"  🕐 Last interaction: {stats.get('last_interaction', 'Never')}")
                    print("="*50 + "\n")
                    continue
                
                elif user_input.lower() == 'reset':
                    print("\n🔄 Starting a new conversation...")
                    vatsal.reset_conversation()
                    greeting = vatsal.initiate_conversation()
                    print(f"🤖 VATSAL: {greeting}\n")
                    continue
                
                print("🤖 VATSAL: ", end="", flush=True)
                response = await vatsal.process_message(user_input)
                print(f"{response}\n")
            
            except KeyboardInterrupt:
                print("\n\n🤖 VATSAL: Conversation interrupted. Saving your chat...")
                vatsal.end_conversation()
                conversation_active = False
                break
            
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again or type 'quit' to exit.\n")
        
        print("\n" + "="*70)
        print("Thank you for using VATSAL AI! 👋")
        print("="*70 + "\n")
    
    try:
        asyncio.run(run_chatbot())
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
