"""
VATSAL AI - Advanced Conversational Assistant
A proactive AI with personality that asks questions, clarifies intent, and anticipates needs
An intelligent assistant inspired by advanced AI companions
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
import random

try:
    from gemini_controller import GeminiController
except ImportError:
    GeminiController = None


class VatsalAI:
    """Advanced conversational AI with proactive personality"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.name = "VATSAL"
        self.user_name = "Sir"
        
        # Initialize Gemini for advanced conversations
        if GeminiController:
            self.gemini = GeminiController(api_key)
        else:
            self.gemini = None
            
        # Conversation state
        self.conversation_history: List[Dict[str, Any]] = []
        self.current_context: Dict[str, Any] = {}
        self.pending_task: Optional[Dict[str, Any]] = None
        self.awaiting_response = False
        
        # User profile and learning
        self.user_profile = self._load_user_profile()
        self.preferences = self.user_profile.get("preferences", {})
        self.habits = self.user_profile.get("habits", {})
        
        # Personality traits (VATSAL-inspired)
        self.personality = {
            "politeness_level": "high",
            "formality": "sophisticated",
            "proactiveness": "high",
            "humor": "subtle",
            "loyalty": "absolute"
        }
        
        # Proactive features
        self.last_greeting_time = None
        self.task_suggestions: List[str] = []
        self.monitoring_mode = False
        
    def _load_user_profile(self) -> Dict[str, Any]:
        """Load user profile and preferences"""
        profile_file = "vatsal_user_profile.json"
        if os.path.exists(profile_file):
            try:
                with open(profile_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default profile
        return {
            "name": "Sir",
            "preferences": {
                "wake_time": "09:00",
                "sleep_time": "23:00",
                "notification_style": "polite",
                "voice_enabled": True
            },
            "habits": {},
            "interaction_count": 0,
            "last_interaction": None
        }
    
    def _save_user_profile(self):
        """Save user profile"""
        try:
            with open("vatsal_user_profile.json", 'w') as f:
                json.dump(self.user_profile, f, indent=2)
        except Exception as e:
            print(f"Failed to save profile: {e}")
    
    def _update_interaction_stats(self):
        """Update interaction statistics"""
        self.user_profile["interaction_count"] = self.user_profile.get("interaction_count", 0) + 1
        self.user_profile["last_interaction"] = datetime.now().isoformat()
        self._save_user_profile()
    
    def get_greeting(self) -> str:
        """Get contextual greeting based on time and situation"""
        current_hour = datetime.now().hour
        
        # Time-based greeting
        if 5 <= current_hour < 12:
            time_greeting = "Good morning"
        elif 12 <= current_hour < 17:
            time_greeting = "Good afternoon"
        elif 17 <= current_hour < 21:
            time_greeting = "Good evening"
        else:
            time_greeting = "Good evening"
        
        # First interaction of the day
        last_interaction = self.user_profile.get("last_interaction")
        if last_interaction:
            last_date = datetime.fromisoformat(last_interaction).date()
            if last_date < datetime.now().date():
                return f"{time_greeting}, {self.user_name}. How may I assist you today?"
        
        # Vary greetings for sophistication
        greetings = [
            f"{time_greeting}, {self.user_name}. What would you like me to do?",
            f"{time_greeting}, {self.user_name}. I'm at your service.",
            f"{time_greeting}, {self.user_name}. How can I help you?",
            f"Hello {self.user_name}. {time_greeting}. What do you need?",
            f"{time_greeting}, {self.user_name}. Ready to assist.",
        ]
        
        return random.choice(greetings)
    
    def initiate_conversation(self) -> str:
        """Start a conversation proactively"""
        self._update_interaction_stats()
        
        greeting = self.get_greeting()
        
        # Add proactive suggestions if available
        if self.task_suggestions:
            suggestion = random.choice(self.task_suggestions)
            greeting += f"\n\nMay I suggest: {suggestion}"
        
        self.awaiting_response = True
        return greeting
    
    async def process_message(self, user_message: str) -> str:
        """Process user message with advanced understanding"""
        self._update_interaction_stats()
        
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "message": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Analyze intent using Gemini
        if self.gemini:
            response = await self._analyze_with_gemini(user_message)
        else:
            response = self._analyze_basic(user_message)
        
        # Add response to history
        self.conversation_history.append({
            "role": "vatsal",
            "message": response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep last 20 exchanges
        if len(self.conversation_history) > 40:
            self.conversation_history = self.conversation_history[-40:]
        
        return response
    
    async def _analyze_with_gemini(self, user_message: str) -> str:
        """Use Gemini AI for advanced conversation"""
        
        # Build context-aware prompt
        prompt = f"""You are VATSAL, an advanced AI assistant with sophisticated personality.

Your characteristics:
- Highly intelligent and proactive
- Polite and formal like a British butler
- Anticipates needs and asks clarifying questions
- Loyal and dedicated to serving the user
- Has subtle wit and charm
- Always addresses user as "{self.user_name}"

Current conversation context:
User message: "{user_message}"

Recent conversation:
{self._get_recent_conversation_text()}

Your task:
1. Understand what the user wants
2. If unclear, ask specific clarifying questions
3. If clear, confirm the task and ask if they want to proceed
4. Be proactive - suggest related actions or improvements
5. Maintain sophisticated, butler-like tone

Respond as VATSAL would. Keep response concise (2-4 sentences).
"""
        
        try:
            response = await self.gemini.analyze_text_async(prompt)
            
            # Check if VATSAL is asking a question
            if '?' in response:
                self.awaiting_response = True
                self.current_context["last_question"] = response
            
            return response
            
        except Exception as e:
            return self._analyze_basic(user_message)
    
    def _analyze_basic(self, user_message: str) -> str:
        """Basic analysis without AI"""
        msg_lower = user_message.lower()
        
        # Check for greetings
        if any(word in msg_lower for word in ["hello", "hi", "hey", "vatsal"]):
            return f"Hello {self.user_name}. How may I assist you today?"
        
        # Check for questions
        if '?' in user_message:
            return f"Interesting question, {self.user_name}. Let me help you with that. Could you provide more details about what specifically you'd like to know?"
        
        # Check for task requests
        task_keywords = ["open", "create", "send", "search", "play", "take", "show", "analyze"]
        if any(keyword in msg_lower for keyword in task_keywords):
            return f"Understood, {self.user_name}. Before I proceed with that task, may I confirm: {user_message}. Is that correct?"
        
        # Default proactive response
        return f"I understand, {self.user_name}. To best assist you, could you tell me more about what you'd like me to do?"
    
    def _get_recent_conversation_text(self, limit: int = 6) -> str:
        """Get recent conversation as text"""
        recent = self.conversation_history[-limit:]
        text = ""
        for item in recent:
            role = item["role"].upper()
            message = item["message"]
            text += f"{role}: {message}\n"
        return text
    
    def ask_clarification(self, task: str, options: List[str]) -> str:
        """Ask for clarification with options"""
        self.awaiting_response = True
        self.pending_task = {
            "task": task,
            "options": options,
            "timestamp": datetime.now().isoformat()
        }
        
        question = f"{self.user_name}, regarding '{task}', I have a few options:\n\n"
        for i, option in enumerate(options, 1):
            question += f"{i}. {option}\n"
        question += f"\nWhich would you prefer?"
        
        return question
    
    def confirm_task(self, task_description: str) -> str:
        """Confirm before executing task"""
        self.awaiting_response = True
        self.pending_task = {
            "task": task_description,
            "awaiting_confirmation": True,
            "timestamp": datetime.now().isoformat()
        }
        
        return f"Just to confirm, {self.user_name}, you'd like me to {task_description}. Shall I proceed?"
    
    def get_proactive_suggestion(self) -> Optional[str]:
        """Generate proactive suggestions based on context"""
        current_hour = datetime.now().hour
        
        suggestions = []
        
        # Morning routine
        if 8 <= current_hour < 10:
            suggestions.extend([
                "Would you like a morning briefing with news and weather?",
                "Shall I check your calendar for today's events?",
                "Would you like me to organize your desktop files?"
            ])
        
        # Afternoon productivity
        elif 14 <= current_hour < 17:
            suggestions.extend([
                "It's been a while. Perhaps a short break would help?",
                "Shall I start the Pomodoro timer for focused work?",
                "Would you like a productivity report?"
            ])
        
        # Evening wrap-up
        elif 18 <= current_hour < 21:
            suggestions.extend([
                "Would you like an evening summary of your activities?",
                "Shall I prepare tomorrow's task list?",
                "Time for some relaxation - play some music?"
            ])
        
        if suggestions:
            return random.choice(suggestions)
        
        return None
    
    def learn_from_interaction(self, task: str, success: bool, user_feedback: Optional[str] = None):
        """Learn from user interactions"""
        if "learned_tasks" not in self.user_profile:
            self.user_profile["learned_tasks"] = {}
        
        task_type = task.split()[0].lower()  # First word as task type
        
        if task_type not in self.user_profile["learned_tasks"]:
            self.user_profile["learned_tasks"][task_type] = {
                "count": 0,
                "success_rate": 0,
                "last_used": None
            }
        
        task_data = self.user_profile["learned_tasks"][task_type]
        task_data["count"] += 1
        task_data["last_used"] = datetime.now().isoformat()
        
        if success:
            current_success = task_data.get("success_rate", 0)
            task_data["success_rate"] = (current_success * (task_data["count"] - 1) + 1) / task_data["count"]
        
        self._save_user_profile()
    
    def get_personality_response(self, situation: str) -> str:
        """Generate personality-driven response"""
        
        responses = {
            "task_completed": [
                f"Task completed successfully, {self.user_name}.",
                f"Done, {self.user_name}. Anything else?",
                f"Completed as requested, {self.user_name}.",
                f"All finished, {self.user_name}. What's next?"
            ],
            "error_occurred": [
                f"My apologies, {self.user_name}. I've encountered a difficulty.",
                f"I'm afraid there's been a complication, {self.user_name}.",
                f"Regrettably, {self.user_name}, that didn't go as planned."
            ],
            "awaiting_command": [
                f"I'm ready when you are, {self.user_name}.",
                f"At your service, {self.user_name}.",
                f"Standing by, {self.user_name}."
            ],
            "goodbye": [
                f"Until next time, {self.user_name}.",
                f"Goodbye, {self.user_name}. I'll be here when you need me.",
                f"Farewell, {self.user_name}."
            ]
        }
        
        if situation in responses:
            return random.choice(responses[situation])
        
        return f"Understood, {self.user_name}."
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get summary of current conversation"""
        return {
            "total_exchanges": len(self.conversation_history) // 2,
            "awaiting_response": self.awaiting_response,
            "pending_task": self.pending_task,
            "context": self.current_context,
            "last_interaction": self.user_profile.get("last_interaction")
        }
    
    def reset_conversation(self):
        """Reset conversation state"""
        self.conversation_history = []
        self.current_context = {}
        self.pending_task = None
        self.awaiting_response = False
    
    def set_user_name(self, name: str):
        """Set user's preferred name"""
        self.user_name = name
        self.user_profile["name"] = name
        self._save_user_profile()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get VATSAL usage statistics"""
        return {
            "total_interactions": self.user_profile.get("interaction_count", 0),
            "last_interaction": self.user_profile.get("last_interaction"),
            "conversation_length": len(self.conversation_history),
            "learned_tasks": len(self.user_profile.get("learned_tasks", {})),
            "user_name": self.user_name,
            "personality_mode": "VATSAL"
        }


def create_vatsal_ai(api_key: Optional[str] = None) -> VatsalAI:
    """Factory function to create VATSAL AI instance"""
    return VatsalAI(api_key)


# For testing
if __name__ == "__main__":
    import asyncio
    
    async def test_vatsal():
        vatsal = create_vatsal_ai()
        
        print("\n" + "="*60)
        print("🤖 VATSAL AI - Advanced Conversational Assistant")
        print("="*60)
        
        # Initial greeting
        print(f"\n{vatsal.initiate_conversation()}")
        
        # Test conversation
        test_messages = [
            "Open Chrome",
            "Actually, I need to send an email",
            "Yes, proceed"
        ]
        
        for msg in test_messages:
            print(f"\nUSER: {msg}")
            response = await vatsal.process_message(msg)
            print(f"VATSAL: {response}")
        
        # Show stats
        print("\n" + "="*60)
        print("📊 VATSAL Stats:")
        stats = vatsal.get_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    asyncio.run(test_vatsal())
