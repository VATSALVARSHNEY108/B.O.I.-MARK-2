"""
Emotional Intelligence Module for VATSAL AI
Detects emotions, tracks mood, and provides empathetic responses
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from google import genai
from google.genai import types


class EmotionalIntelligence:
    """Enhanced emotional intelligence for AI interactions"""
    
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key) if api_key else None
        
        # Emotion categories
        self.emotions = {
            'happy': ['joy', 'excited', 'enthusiastic', 'pleased', 'satisfied', 'cheerful'],
            'sad': ['unhappy', 'disappointed', 'down', 'depressed', 'upset', 'hurt'],
            'angry': ['frustrated', 'annoyed', 'irritated', 'mad', 'furious', 'rage'],
            'anxious': ['worried', 'nervous', 'stressed', 'concerned', 'tense', 'uneasy'],
            'confused': ['puzzled', 'uncertain', 'lost', 'bewildered', 'perplexed'],
            'tired': ['exhausted', 'weary', 'fatigued', 'drained', 'sleepy', 'burned out'],
            'motivated': ['determined', 'inspired', 'driven', 'ambitious', 'energized'],
            'grateful': ['thankful', 'appreciative', 'blessed', 'glad'],
            'neutral': ['calm', 'okay', 'fine', 'normal', 'alright']
        }
        
        # Mood history
        self.mood_history: List[Dict] = []
        self.current_mood = "neutral"
        self.mood_intensity = 0.5  # 0 to 1
        
        # User preferences learned over time
        self.user_preferences = {
            'formality_level': 0.5,  # 0=casual, 1=formal
            'humor_preference': 0.7,  # 0=serious, 1=humorous
            'detail_level': 0.6,     # 0=brief, 1=detailed
            'encouragement_need': 0.5 # 0=low, 1=high
        }
        
        # Conversation context
        self.recent_topics: List[str] = []
        self.user_mentioned_challenges: List[str] = []
        self.victories_celebrated: List[str] = []
    
    def detect_emotion(self, text: str) -> Dict[str, any]:
        """
        Detect emotion from user's text using AI
        Returns: emotion, intensity, and triggers
        """
        if not self.client:
            return self._simple_emotion_detection(text)
        
        try:
            prompt = f"""Analyze the emotional state in this message:
"{text}"

Provide a JSON response with:
1. primary_emotion: main emotion (happy, sad, angry, anxious, confused, tired, motivated, grateful, neutral)
2. intensity: 0.0 to 1.0 (how strong the emotion is)
3. secondary_emotions: list of other emotions present
4. emotional_triggers: what's causing the emotion
5. needs: what the person might need (support, information, encouragement, humor, space)
6. tone: overall tone (casual, formal, urgent, relaxed, playful, serious)

Be empathetic and insightful."""

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            result = json.loads(response.text)
            
            # Update current state
            self.current_mood = result.get('primary_emotion', 'neutral')
            self.mood_intensity = result.get('intensity', 0.5)
            
            # Track mood history
            self.mood_history.append({
                'timestamp': datetime.now().isoformat(),
                'emotion': self.current_mood,
                'intensity': self.mood_intensity,
                'text': text[:100]  # Store snippet
            })
            
            # Keep only last 20 moods
            if len(self.mood_history) > 20:
                self.mood_history = self.mood_history[-20:]
            
            return result
            
        except Exception as e:
            print(f"⚠️ Emotion detection failed: {e}")
            return self._simple_emotion_detection(text)
    
    def _simple_emotion_detection(self, text: str) -> Dict[str, any]:
        """Fallback simple emotion detection using keywords"""
        text_lower = text.lower()
        detected_emotions = []
        
        for emotion, keywords in self.emotions.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_emotions.append(emotion)
        
        # Detect from common patterns
        if any(word in text_lower for word in ['help', 'stuck', 'error', 'problem', 'issue']):
            detected_emotions.append('frustrated')
        if any(word in text_lower for word in ['thanks', 'thank you', 'appreciate', 'awesome', 'great']):
            detected_emotions.append('grateful')
        if '!' in text:
            detected_emotions.append('excited')
        if '?' in text and len(text.split('?')) > 2:
            detected_emotions.append('confused')
        
        primary = detected_emotions[0] if detected_emotions else 'neutral'
        
        return {
            'primary_emotion': primary,
            'intensity': 0.6,
            'secondary_emotions': detected_emotions[1:3] if len(detected_emotions) > 1 else [],
            'emotional_triggers': [],
            'needs': ['information'] if '?' in text else ['acknowledgment'],
            'tone': 'casual'
        }
    
    def generate_empathetic_response_style(self, emotion_data: Dict) -> Dict[str, str]:
        """
        Generate response guidelines based on detected emotion
        """
        emotion = emotion_data.get('primary_emotion', 'neutral')
        intensity = emotion_data.get('intensity', 0.5)
        needs = emotion_data.get('needs', [])
        
        styles = {
            'happy': {
                'opening': ["That's wonderful!", "I'm so glad to hear that!", "Fantastic!", "That's great news!"],
                'tone': 'enthusiastic and celebratory',
                'approach': 'Match their energy, celebrate with them, be encouraging',
                'emojis': '🎉✨😊🌟'
            },
            'sad': {
                'opening': ["I understand that's difficult.", "I'm here to help.", "That sounds tough.", "I hear you."],
                'tone': 'gentle, supportive, and understanding',
                'approach': 'Be compassionate, offer support, don\'t minimize feelings',
                'emojis': '💙🤗'
            },
            'angry': {
                'opening': ["I understand your frustration.", "That sounds really frustrating.", "I get why that's annoying."],
                'tone': 'calm, validating, solution-focused',
                'approach': 'Acknowledge frustration, offer solutions, stay calm',
                'emojis': '💪'
            },
            'anxious': {
                'opening': ["Let's work through this together.", "I'm here to help.", "We can figure this out."],
                'tone': 'reassuring, calm, structured',
                'approach': 'Be reassuring, break down problems, provide clarity',
                'emojis': '🧘‍♂️💙'
            },
            'confused': {
                'opening': ["Let me clarify that for you.", "Good question!", "I can explain that."],
                'tone': 'clear, patient, educational',
                'approach': 'Explain clearly, use examples, check understanding',
                'emojis': '💡🎯'
            },
            'tired': {
                'opening': ["Take it easy, I've got this.", "Let me handle that for you.", "Rest up, Boss."],
                'tone': 'supportive, efficient, caring',
                'approach': 'Be helpful, do the work for them, suggest breaks',
                'emojis': '😌☕'
            },
            'motivated': {
                'opening': ["Let's do this!", "I love the energy!", "You've got this!", "Great attitude!"],
                'tone': 'energetic, encouraging, action-oriented',
                'approach': 'Match enthusiasm, help them achieve goals',
                'emojis': '🚀💪🔥'
            },
            'grateful': {
                'opening': ["You're very welcome!", "Happy to help!", "My pleasure, Sir!", "Anytime!"],
                'tone': 'warm, appreciative, friendly',
                'approach': 'Accept gratitude gracefully, reinforce relationship',
                'emojis': '😊🙏'
            },
            'neutral': {
                'opening': ["Certainly.", "Of course.", "Right away.", "Got it."],
                'tone': 'professional, helpful, clear',
                'approach': 'Be efficient and helpful',
                'emojis': '✅'
            }
        }
        
        return styles.get(emotion, styles['neutral'])
    
    def enhance_system_prompt(self, base_prompt: str, emotion_data: Dict) -> str:
        """
        Enhance system prompt based on detected emotion
        """
        style = self.generate_empathetic_response_style(emotion_data)
        emotion = emotion_data.get('primary_emotion', 'neutral')
        needs = emotion_data.get('needs', [])
        
        emotional_context = f"""

CURRENT USER EMOTIONAL STATE:
- Emotion: {emotion}
- Intensity: {emotion_data.get('intensity', 0.5):.1%}
- User needs: {', '.join(needs)}

RESPONSE STYLE FOR THIS INTERACTION:
- Tone: {style['tone']}
- Approach: {style['approach']}
- Start with phrases like: {', '.join(style['opening'][:2])}
- Can use emojis: {style['emojis']} (use sparingly, 1-2 max)

EMPATHY GUIDELINES:
- Acknowledge their emotional state naturally
- Don't be overly dramatic or fake
- Be genuinely helpful and supportive
- Adjust formality based on their tone
- Remember context from previous messages"""

        return base_prompt + emotional_context
    
    def track_user_preference(self, preference_type: str, value: float):
        """Track and learn user preferences over time"""
        if preference_type in self.user_preferences:
            # Weighted average: 70% old, 30% new
            old = self.user_preferences[preference_type]
            self.user_preferences[preference_type] = (old * 0.7) + (value * 0.3)
    
    def get_mood_trend(self) -> str:
        """Analyze mood trend over recent history"""
        if len(self.mood_history) < 3:
            return "neutral"
        
        recent = self.mood_history[-5:]
        avg_intensity = sum(m['intensity'] for m in recent) / len(recent)
        
        positive_count = sum(1 for m in recent if m['emotion'] in ['happy', 'motivated', 'grateful'])
        negative_count = sum(1 for m in recent if m['emotion'] in ['sad', 'angry', 'anxious', 'tired'])
        
        if positive_count > negative_count:
            return "improving" if avg_intensity > 0.6 else "positive"
        elif negative_count > positive_count:
            return "declining" if avg_intensity > 0.6 else "challenging"
        else:
            return "stable"
    
    def suggest_support_actions(self, emotion_data: Dict) -> List[str]:
        """Suggest helpful actions based on emotional state"""
        emotion = emotion_data.get('primary_emotion', 'neutral')
        intensity = emotion_data.get('intensity', 0.5)
        
        suggestions = {
            'tired': [
                "Would you like me to play some relaxing music?",
                "Maybe it's time for a break? I can remind you in 25 minutes.",
                "I can handle the heavy lifting - just tell me what you need."
            ],
            'frustrated': [
                "Want me to break this down into smaller steps?",
                "I can search for solutions to this problem.",
                "Let's tackle this together - one step at a time."
            ],
            'anxious': [
                "Let me help organize this - I'm great at planning.",
                "We'll take it one step at a time.",
                "I'm here whenever you need me."
            ],
            'sad': [
                "Want to talk about it? I'm listening.",
                "How about I tell you something interesting to cheer you up?",
                "I'm here for you, Sir."
            ],
            'confused': [
                "I can explain that in simpler terms.",
                "Want me to show you an example?",
                "Let me break that down for you."
            ]
        }
        
        return suggestions.get(emotion, [])
    
    def get_personalized_greeting(self) -> str:
        """Generate greeting based on mood trend and time"""
        hour = datetime.now().hour
        trend = self.get_mood_trend()
        
        time_greeting = {
            (0, 5): "working late",
            (5, 12): "Good morning",
            (12, 17): "Good afternoon",
            (17, 21): "Good evening",
            (21, 24): "Good evening"
        }
        
        greeting = "Hello"
        for (start, end), greet in time_greeting.items():
            if start <= hour < end:
                greeting = greet
                break
        
        # Adjust based on mood trend
        if trend == "improving":
            return f"{greeting}, Sir! 😊 You seem to be in good spirits today."
        elif trend == "challenging":
            return f"{greeting}, Sir. I'm here to help make things easier."
        elif trend == "positive":
            return f"{greeting}, Sir! 🌟 Ready to be awesome today?"
        else:
            return f"{greeting}, Sir! How can I assist you today?"
    
    def get_emotional_summary(self) -> str:
        """Get summary of emotional journey"""
        if len(self.mood_history) < 3:
            return "Just getting to know you!"
        
        emotions = [m['emotion'] for m in self.mood_history[-10:]]
        from collections import Counter
        common = Counter(emotions).most_common(3)
        
        trend = self.get_mood_trend()
        
        summary = f"Mood trend: {trend}. "
        summary += f"Recent emotions: {', '.join([f'{e} ({c}x)' for e, c in common])}"
        
        return summary


def create_emotional_intelligence() -> EmotionalIntelligence:
    """Factory function to create EmotionalIntelligence instance"""
    return EmotionalIntelligence()


if __name__ == "__main__":
    # Test the emotional intelligence
    ei = create_emotional_intelligence()
    
    test_messages = [
        "I'm so excited about this new project!",
        "Ugh, this code isn't working and I've been stuck for hours",
        "Thanks so much for your help, really appreciate it!",
        "I'm worried I won't finish this on time",
        "This is confusing, can you explain it again?"
    ]
    
    print("🧠 Emotional Intelligence Test\n")
    for msg in test_messages:
        print(f"Message: '{msg}'")
        emotion = ei.detect_emotion(msg)
        print(f"Emotion: {emotion['primary_emotion']} ({emotion['intensity']:.0%})")
        style = ei.generate_empathetic_response_style(emotion)
        print(f"Response style: {style['tone']}")
        suggestions = ei.suggest_support_actions(emotion)
        if suggestions:
            print(f"Suggestions: {suggestions[0]}")
        print()
