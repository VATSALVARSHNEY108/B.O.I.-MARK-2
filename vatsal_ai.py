arns from data without being explicitly programmed. It includes supervised learning (labeled data), unsupervised learning (finding patterns), and reinforcement learning (learning from rewards)."
            
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
