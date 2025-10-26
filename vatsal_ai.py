"""
VATSAL AI - Powerful Learning Chatbot
A smart AI chatbot that learns from all past conversations and remembers context
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from collections import Counter

try:
    from gemini_controller import GeminiController
except ImportError:
    GeminiController = None


class VatsalAI:
    """Powerful learning conversational AI chatbot with persistent memory"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.name = "VATSAL"
        self.memory_file = "vatsal_memory.json"
        
        # Initialize Gemini for conversations
        if GeminiController:
            self.gemini = GeminiController(api_key)
        else:
            self.gemini = None
        
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
                "conversations": self.all_conversations[-50:],  # Keep last 50 conversations
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
        
        # Time-based greeting
        if 5 <= current_hour < 12:
            time_greeting = "Good morning"
        elif 12 <= current_hour < 17:
            time_greeting = "Good afternoon"
        elif 17 <= current_hour < 21:
            time_greeting = "Good evening"
        else:
            time_greeting = "Hello"
        
        # Personalize based on history
        user_name = self.user_profile.get("name", "")
        if user_name and user_name != "User":
            greeting = f"{time_greeting}, {user_name}!"
        else:
            greeting = f"{time_greeting}!"
        
        # Add context if returning user
        if self.stats.get("total_conversations", 0) > 0:
            greeting += " Welcome back! How can I help you today?"
        else:
            greeting += " I'm VATSAL, your AI assistant. I learn from our conversations to help you better. What can I help you with?"
        
        return greeting
    
    async def process_message(self, user_message: str) -> str:
        """Process user message with learning and context awareness"""
        
        # Add user message to current conversation
        message_data = {
            "role": "user",
            "message": user_message,
            "timestamp": datetime.now().isoformat()
        }
        self.current_conversation.append(message_data)
        
        # Learn from the message
        self._learn_from_message(user_message)
        
        # Get AI response
        if self.gemini:
            response = await self._chat_with_gemini(user_message)
        else:
            response = self._simple_response(user_message)
        
        # Add response to current conversation
        response_data = {
            "role": "assistant",
            "message": response,
            "timestamp": datetime.now().isoformat()
        }
        self.current_conversation.append(response_data)
        
        # Update statistics
        self._update_stats()
        
        # Save every 5 messages to preserve memory
        if len(self.current_conversation) % 5 == 0:
            self._save_conversation_to_memory()
            self._save_memory()
        
        return response
    
    async def _chat_with_gemini(self, user_message: str) -> str:
        """Use Gemini AI with full context and learning"""
        
        # Build comprehensive context
        recent_context = self._get_recent_context(limit=10)
        learned_info = self._get_learned_info()
        past_topics = self._get_relevant_past_topics(user_message)
        
        prompt = f"""You are VATSAL, an intelligent AI assistant that learns from every conversation.

LEARNED INFORMATION ABOUT USER:
{learned_info}

RELEVANT PAST TOPICS:
{past_topics}

RECENT CONVERSATION:
{recent_context}

CURRENT MESSAGE: {user_message}

Instructions:
1. Use what you've learned about the user to personalize your response
2. Reference past conversations when relevant
3. Be conversational, friendly, and helpful
4. Show that you remember previous discussions
5. Provide insightful, context-aware responses
6. Answer questions clearly and directly
7. Keep responses concise (2-4 sentences) unless detail is needed

Respond as VATSAL:"""
        
        try:
            response = await self.gemini.analyze_text_async(prompt)
            if response and len(response.strip()) > 5:
                return response
            else:
                print("Empty Gemini response, using fallback")
                return self._simple_response(user_message)
        except Exception as e:
            print(f"Gemini error: {e}")
            return self._simple_response(user_message)
    
    def _learn_from_message(self, message: str):
        """Learn patterns, preferences, and topics from user messages"""
        msg_lower = message.lower()
        
        # Detect user name if mentioned
        if "my name is" in msg_lower or "i'm" in msg_lower or "i am" in msg_lower:
            words = message.split()
            for i, word in enumerate(words):
                if word.lower() in ["is", "i'm", "am"] and i + 1 < len(words):
                    potential_name = words[i + 1].strip('.,!?')
                    if potential_name and potential_name[0].isupper() and len(potential_name) > 1:
                        self.user_profile["name"] = potential_name
        
        # Detect preferences (I like, I love, I prefer, I enjoy)
        preference_indicators = ["i like", "i love", "i prefer", "i enjoy", "i'm interested in", "i want"]
        for indicator in preference_indicators:
            if indicator in msg_lower:
                preference = msg_lower.split(indicator)[1].split('.')[0].split(',')[0].strip()
                if preference and len(preference) > 2:
                    if "preferences" not in self.user_profile:
                        self.user_profile["preferences"] = []
                    if preference not in self.user_profile["preferences"]:
                        self.user_profile["preferences"].append(preference)
        
        # Track topics (extract keywords)
        keywords = self._extract_keywords(message)
        if keywords:
            for keyword in keywords:
                topic = keyword.lower()
                if topic not in self.stats["favorite_topics"]:
                    self.stats["favorite_topics"][topic] = 0
                self.stats["favorite_topics"][topic] += 1
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        # Simple keyword extraction (words longer than 4 characters)
        words = text.lower().split()
        stop_words = {"what", "when", "where", "which", "who", "whom", "this", "that", "these", 
                      "those", "with", "from", "about", "could", "would", "should", "have", "been"}
        keywords = [w.strip('.,!?') for w in words if len(w) > 4 and w not in stop_words]
        return keywords[:5]  # Top 5 keywords
    
    def _get_recent_context(self, limit: int = 10) -> str:
        """Get recent conversation context"""
        recent = self.current_conversation[-limit:] if len(self.current_conversation) > limit else self.current_conversation
        
        context_lines = []
        for item in recent:
            role = "User" if item["role"] == "user" else "VATSAL"
            context_lines.append(f"{role}: {item['message']}")
        
        return "\n".join(context_lines) if context_lines else "No recent conversation"
    
    def _get_learned_info(self) -> str:
        """Get summary of learned information about user"""
        info_lines = []
        
        if self.user_profile.get("name") and self.user_profile["name"] != "User":
            info_lines.append(f"- User's name: {self.user_profile['name']}")
        
        if self.user_profile.get("preferences"):
            prefs = ", ".join(self.user_profile["preferences"][-5:])  # Last 5 preferences
            info_lines.append(f"- User's preferences: {prefs}")
        
        if self.stats.get("favorite_topics"):
            top_topics = sorted(self.stats["favorite_topics"].items(), key=lambda x: x[1], reverse=True)[:3]
            topics = ", ".join([t[0] for t in top_topics])
            info_lines.append(f"- Common topics: {topics}")
        
        total_convos = self.stats.get("total_conversations", 0)
        if total_convos > 0:
            info_lines.append(f"- We've had {total_convos} conversations before")
        
        return "\n".join(info_lines) if info_lines else "New user - no previous learning data"
    
    def _get_relevant_past_topics(self, current_message: str) -> str:
        """Find relevant topics from past conversations"""
        if not self.all_conversations:
            return "No past conversations"
        
        # Simple relevance check - look for keyword matches in past conversations
        keywords = set(self._extract_keywords(current_message))
        relevant = []
        
        for convo in self.all_conversations[-10:]:  # Check last 10 conversations
            for msg in convo:
                if msg["role"] == "user":
                    msg_keywords = set(self._extract_keywords(msg["message"]))
                    if keywords & msg_keywords:  # If there's overlap
                        relevant.append(f"Past: {msg['message'][:100]}")
                        if len(relevant) >= 3:
                            break
            if len(relevant) >= 3:
                break
        
        return "\n".join(relevant) if relevant else "No directly relevant past topics"
    
    def _simple_response(self, user_message: str) -> str:
        """Enhanced fallback response with built-in knowledge"""
        msg_lower = user_message.lower()
        
        # Greetings
        if any(word in msg_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon"]):
            return "Hello! How can I help you today?"
        
        # Thanks
        if any(word in msg_lower for word in ["thank", "thanks"]):
            return "You're welcome! I'm always learning from our conversations to help you better."
        
        # Goodbye
        if any(word in msg_lower for word in ["bye", "goodbye", "see you"]):
            self._save_conversation_to_memory()
            self._save_memory()
            return "Goodbye! I'll remember our conversation for next time. Have a great day!"
        
        # Technical questions - Built-in knowledge
        if any(term in msg_lower for term in ["deep learning", "deeplearning", "machine learning", "ml", "ai", "neural network"]):
            if "deep learning" in msg_lower or "deeplearning" in msg_lower:
                return """Deep learning is a subset of machine learning that uses multi-layered neural networks to learn from data. 
                
Think of it like this: Traditional programming uses rules to process data. Deep learning learns the rules from the data itself by using layers of artificial neurons. Each layer learns increasingly complex patterns - from simple edges in images to recognizing faces.

Popular applications: Image recognition, speech recognition, natural language processing, self-driving cars.

Common frameworks: TensorFlow, PyTorch, Keras.

Would you like to know more about a specific aspect?"""
            
            if "machine learning" in msg_lower or "ml" in msg_lower:
                return "Machine learning is AI that learns from data without being explicitly programmed. It includes supervised learning (labeled data), unsupervised learning (finding patterns), and reinforcement learning (learning from rewards)."
            
            if "neural network" in msg_lower:
                return "Neural networks are computing systems inspired by biological brains. They consist of layers of interconnected nodes (neurons) that process and transform data to learn patterns and make predictions."
        
        # Programming questions
        if any(term in msg_lower for term in ["python", "javascript", "programming", "coding", "code"]):
            return "I'd be happy to help with programming! Could you be more specific about what you'd like to know? For example, ask about a specific language, concept, or problem you're facing."
        
        # General questions (with or without ?)
        if any(word in msg_lower for word in ["what", "how", "why", "when", "where", "who", "explain", "tell me"]):
            return "That's a great question! I'd love to help you with that. Could you provide a bit more detail so I can give you the best answer?"
        
        # Technical request
        if "technical" in msg_lower or "explain" in msg_lower:
            context = self._get_recent_context(limit=2)
            if context and "deep learning" in context.lower():
                return """Deep Learning (Technical):

Architecture: Multi-layer neural networks (typically 3+ hidden layers) with non-linear activation functions.

Key Components:
- Input Layer: Receives raw data
- Hidden Layers: Extract hierarchical features through transformations
- Output Layer: Produces predictions

Training: Uses backpropagation algorithm with gradient descent optimization to minimize loss functions.

Types: CNNs (images), RNNs/LSTMs (sequences), Transformers (NLP), GANs (generation).

Requires: Large datasets, GPUs/TPUs for computation, frameworks like PyTorch/TensorFlow."""
            return "I can provide technical details! What specific topic would you like me to explain technically?"
        
        # Default - more engaging
        return "I'm here to help! Could you tell me more about what you'd like to know or do? Feel free to ask me anything - I'm always learning!"
    
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
            "preferences": [],
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
            "ai_available": self.gemini is not None,
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
        print("🤖 VATSAL AI - Intelligent Chatbot")
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
        # Check for API key
        if not os.getenv("GEMINI_API_KEY"):
            print("❌ Error: GEMINI_API_KEY not found!")
            print("Please set your Gemini API key in the .env file or environment variables.")
            sys.exit(1)
        
        # Create chatbot instance
        print("🔧 Initializing VATSAL AI chatbot...")
        try:
            vatsal = create_vatsal_ai()
            print("✅ Chatbot ready!\n")
        except Exception as e:
            print(f"❌ Error initializing chatbot: {e}")
            sys.exit(1)
        
        # Display header
        print_header()
        
        # Initial greeting
        greeting = vatsal.initiate_conversation()
        print(f"🤖 VATSAL: {greeting}\n")
        
        # Conversation loop
        conversation_active = True
        
        while conversation_active:
            try:
                # Get user input
                user_input = input("👤 You: ").strip()
                
                # Handle empty input
                if not user_input:
                    continue
                
                # Handle special commands
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
                
                # Process the message with AI
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
    
    # Run the chatbot
    try:
        asyncio.run(run_chatbot())
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
