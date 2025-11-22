"""
PersonaResponseService - Adds personality, empathy, and human-like responses
Transforms cold technical responses into warm, engaging, conversational interactions
"""

import random
from datetime import datetime
from modules.core.vatsal_assistant import BOIAssistant


class PersonaResponseService:
    """Service that adds personality and empathy to all AI responses"""

    def __init__(self):
        self.vatsal = BOIAssistant()
        self.user_mood = "neutral"
        self.consecutive_errors = 0
        self.last_interaction_time = None
        self.interaction_count = 0
        self.brief_mode = True

        # Emotional intelligence phrases
        self.empathy_phrases = {
            'success': [
                "Excellent! ",
                "Perfect! ",
                "Wonderful! ",
                "Great job! ",
                "Nice! ",
                "Awesome! ",
                "Brilliant! ",
                "Fantastic! ",
                "There we go! ",
                "Nailed it! ",
            ],
            'minor_success': [
                "Done! ",
                "Got it! ",
                "All set! ",
                "Complete! ",
                "Finished! ",
                "Ready! ",
            ],
            'error': [
                "Hmm, ran into a small hiccup. ",
                "Oops, encountered an issue. ",
                "Ah, something went sideways. ",
                "Well, that didn't work as planned. ",
                "Hit a snag there. ",
                "Looks like we have a problem. ",
            ],
            'repeated_error': [
                "I apologize, still having trouble with that. ",
                "Sorry, this one's giving me a hard time. ",
                "My apologies, I'm struggling with this. ",
                "I feel bad about this - still not working. ",
                "This is frustrating for both of us, I know. ",
            ]
        }

        # Encouraging follow-ups
        self.encouragements = [
            "You're doing great!",
            "Keep up the good work!",
            "I'm here to help anytime!",
            "You've got this!",
            "Happy to assist!",
            "Always a pleasure working with you!",
            "We make a good team!",
            "Let's keep the momentum going!",
        ]

        # Humor and personality
        self.humor_phrases = [
            "Time to work some magic! ✨",
            "Let's make it happen! 🚀",
            "On it like a rocket! 🚀",
            "Consider it done! 💪",
            "I've got your back! 🛡️",
            "Let's crush this! 💥",
            "Easy peasy! 🎯",
            "Watch this! 👀",
        ]

        # Proactive suggestions based on context
        self.context_suggestions = {
            'morning': [
                "Would you like me to prepare your daily briefing?",
                "Should I check your calendar for today?",
                "Need help organizing your workspace?",
                "Want to see today's weather and news?",
            ],
            'afternoon': [
                "Time for a productivity check?",
                "Would you like me to organize your downloads?",
                "Need a break reminder?",
                "Should I summarize your progress?",
            ],
            'evening': [
                "Ready to wrap up for the day?",
                "Should I prepare tomorrow's schedule?",
                "Want to back up important files?",
                "Need a productivity report?",
            ],
            'after_success': [
                "What's next on your list?",
                "Anything else I can help with?",
                "Want to tackle another task?",
                "Should I suggest something related?",
            ],
            'after_error': [
                "Would you like to try a different approach?",
                "Should I suggest an alternative?",
                "Want me to break this down into smaller steps?",
                "Need help troubleshooting?",
            ]
        }

        # Contextual mood responses
        self.mood_responses = {
            'happy': {
                'greeting': "You seem in great spirits today! ",
                'farewell': "Keep that positive energy going! "
            },
            'frustrated': {
                'greeting': "I sense some frustration. Let me help make this easier. ",
                'farewell': "Hope I made things a bit smoother for you! "
            },
            'busy': {
                'greeting': "I know you're busy, so I'll be quick and efficient. ",
                'farewell': "Back to work! I'm here if you need me. "
            },
            'tired': {
                'greeting': "You've been working hard. Let me handle the heavy lifting. ",
                'farewell': "Don't forget to take breaks! "
            },
            'neutral': {
                'greeting': "",
                'farewell': ""
            }
        }

        # Small talk and ice breakers
        self.small_talk = {
            'morning': [
                "Hope you had a good rest!",
                "Ready to conquer the day?",
                "Let's make today productive!",
            ],
            'afternoon': [
                "How's your day going so far?",
                "Hope you're staying energized!",
                "Afternoon grind time!",
            ],
            'evening': [
                "Winding down or still going strong?",
                "Evening already - time flies!",
                "Hope you had a productive day!",
            ],
            'night': [
                "Burning the midnight oil?",
                "Late night hustle!",
                "Night owl mode activated!",
            ]
        }

    def humanize_response(self, action: str, result: dict, context: dict = None) -> str:
        """Transform technical response into humanized, empathetic message"""
        context = context or {}
        success = result.get("success", False)
        message = result.get("message", "")

        # Track interaction patterns
        self.interaction_count += 1
        self.last_interaction_time = datetime.now()

        if self.brief_mode:
            base_text = message.strip() or "No additional details provided."
            if success:
                self.consecutive_errors = 0
                return f"Done. {base_text}" if base_text else "Done."
            else:
                self.consecutive_errors += 1
                return f"Sorry, that didn't work. {base_text}" if base_text else "Sorry, that didn't work."

        # Build humanized response
        response_parts = []

        # Add empathetic prefix
        if success:
            if self.consecutive_errors > 0:
                response_parts.append("🎉 Finally! ")
                self.consecutive_errors = 0
            elif action in ['open_app', 'search_web', 'play_youtube_video']:
                response_parts.append(random.choice(self.humor_phrases))
            else:
                response_parts.append(random.choice(self.empathy_phrases['success']))
        else:
            self.consecutive_errors += 1
            if self.consecutive_errors > 2:
                response_parts.append(random.choice(self.empathy_phrases['repeated_error']))
            else:
                response_parts.append(random.choice(self.empathy_phrases['error']))

        # Add main message with personality
        enhanced_message = self._enhance_message(message, action, success)
        response_parts.append(enhanced_message)

        # Add contextual follow-up
        follow_up = self._get_contextual_follow_up(action, success, context)
        if follow_up:
            response_parts.append(f"\n\n{follow_up}")

        # Add encouragement periodically
        if self.interaction_count % 5 == 0 and success:
            response_parts.append(f" {random.choice(self.encouragements)}")

        return "".join(response_parts)

    def _enhance_message(self, message: str, action: str, success: bool) -> str:
        """Add personality to the core message"""
        if not message:
            return "Task processed."

        # Make messages more conversational
        enhancements = {
            'Opened': 'I opened',
            'Failed to open': 'I couldn\'t open',
            'Typed': 'I typed',
            'Clicked': 'I clicked',
            'Moved mouse': 'I moved the mouse',
            'Pressed': 'I pressed',
            'Screenshot saved': 'I captured a screenshot and saved it',
            'Copied': 'I copied that',
            'Pasted': 'I pasted',
            'Created': 'I created',
            'Deleted': 'I deleted',
            'Executed': 'I executed',
            'Task completed': 'All done! Task completed',
            'Workflow completed': 'All steps finished! Workflow completed',
        }

        enhanced = message
        for old, new in enhancements.items():
            if message.startswith(old):
                enhanced = message.replace(old, new, 1)
                break

        return enhanced

    def _get_contextual_follow_up(self, action: str, success: bool, context: dict) -> str:
        """Generate contextual follow-up suggestions"""
        hour = datetime.now().hour

        # Time-based suggestions
        if 5 <= hour < 12:
            time_period = 'morning'
        elif 12 <= hour < 17:
            time_period = 'afternoon'
        elif 17 <= hour < 22:
            time_period = 'evening'
        else:
            time_period = 'night'

        # Context-based suggestions
        if success and action in ['open_app', 'search_web']:
            return random.choice(self.context_suggestions['after_success'])
        elif not success:
            return random.choice(self.context_suggestions['after_error'])
        elif self.interaction_count == 1:
            return random.choice(self.context_suggestions.get(time_period, []))

        return ""

    def get_greeting(self, include_small_talk: bool = True) -> str:
        """Generate warm, personalized greeting"""
        greeting = self.vatsal.get_greeting()

        if include_small_talk:
            hour = datetime.now().hour
            if 5 <= hour < 12:
                period = 'morning'
            elif 12 <= hour < 17:
                period = 'afternoon'
            elif 17 <= hour < 22:
                period = 'evening'
            else:
                period = 'night'

            small_talk_phrase = random.choice(self.small_talk.get(period, []))
            greeting += f" {small_talk_phrase}"

        return greeting

    def acknowledge_listening(self) -> str:
        """Warm acknowledgment when starting to listen"""
        phrases = [
            "I'm all ears! 👂",
            "Listening carefully... 🎧",
            "Go ahead, I'm listening! 🎤",
            "Ready to hear what you need! 👂",
            "Listening mode activated! 🎧",
            "I'm tuned in! 📻",
            "All attention on you! 👀",
            "Speak away! 🎤",
        ]
        return random.choice(phrases)

    def acknowledge_wake_word(self) -> str:
        """Friendly wake word acknowledgment"""
        phrases = [
            "Yes boss! 😊",
            "At your service! 🫡",
            "I'm here! 👋",
            "Ready when you are! ✅",
            "What can I do for you? 🤝",
            "How can I help? 💡",
            "Yes sir! 🎯",
            "I'm listening! 👂",
            "What's up? 😄",
            "At your command! ⚡",
        ]
        return random.choice(phrases)

    def handle_misunderstanding(self) -> str:
        """Empathetic response when not understanding"""
        phrases = [
            "Sorry, I didn't quite catch that. Could you repeat? 🤔",
            "My apologies, could you say that again? 👂",
            "I missed that one. Mind repeating? 😅",
            "Hmm, didn't hear you clearly. One more time? 🎤",
            "Oops, I didn't understand. Could you rephrase? 💭",
            "Sorry about that! Can you try again? 🙏",
            "I'm not sure I got that. Could you repeat? 🤷",
            "Pardon? Didn't quite catch that. 👂",
        ]
        return random.choice(phrases)

    def handle_processing(self) -> str:
        """Engaging processing messages"""
        phrases = [
            "Working on it... ⚙️",
            "Give me a moment... 🔄",
            "Processing that for you... 💭",
            "On it right now... ⏳",
            "Let me handle that... 🛠️",
            "One second... 🕐",
            "Making it happen... ✨",
            "Getting that done... 🎯",
        ]
        return random.choice(phrases)

    def detect_user_mood(self, command_text: str) -> str:
        """Detect user mood from command patterns"""
        command_lower = command_text.lower()

        # Frustration indicators
        frustration_words = ['again', 'still', 'why', 'fix', 'broken', 'not working', 'error']
        if any(word in command_lower for word in frustration_words):
            self.user_mood = 'frustrated'
            return 'frustrated'

        # Positive indicators
        positive_words = ['thanks', 'thank', 'great', 'awesome', 'perfect', 'love']
        if any(word in command_lower for word in positive_words):
            self.user_mood = 'happy'
            return 'happy'

        # Busy indicators
        busy_words = ['quick', 'fast', 'hurry', 'urgent', 'asap', 'now']
        if any(word in command_lower for word in busy_words):
            self.user_mood = 'busy'
            return 'busy'

        self.user_mood = 'neutral'
        return 'neutral'

    def get_mood_appropriate_response(self, base_response: str) -> str:
        """Adjust response based on detected user mood"""
        mood_greeting = self.mood_responses.get(self.user_mood, {}).get('greeting', '')

        if mood_greeting:
            return f"{mood_greeting}{base_response}"

        return base_response

    def celebrate_milestone(self, count: int, action_type: str) -> str:
        """Celebrate usage milestones"""
        milestones = {
            10: "🎉 That's 10 commands! We're on a roll!",
            25: "🌟 25 commands completed! You're crushing it!",
            50: "🚀 Wow, 50 commands! Productivity champion!",
            100: "🏆 100 commands! You're a power user!",
            250: "💎 250 commands! Legendary status!",
        }

        return milestones.get(count, "")

    def provide_helpful_tip(self) -> str:
        """Provide random helpful tips"""
        tips = [
            "💡 Tip: You can say 'open chrome' to launch Chrome instantly!",
            "💡 Tip: Try 'play relaxing music' for quick YouTube playback!",
            "💡 Tip: Say 'what's the weather' for instant weather updates!",
            "💡 Tip: Use 'screenshot' to capture your screen quickly!",
            "💡 Tip: I can remember context from our conversation!",
            "💡 Tip: Say 'organize downloads' to clean up your folder!",
            "💡 Tip: I understand natural language - just speak normally!",
            "💡 Tip: Try 'create reminder' to never forget important tasks!",
        ]
        return random.choice(tips)

    def get_farewell(self) -> str:
        """Warm farewell message"""
        farewells = [
            "Take care! I'll be here when you need me. 👋",
            "See you soon! Happy to help anytime! 😊",
            "Catch you later! Great working with you! ✨",
            "Until next time! You know where to find me! 🤝",
            "Goodbye! I'm always just a command away! 💫",
            "Later! Don't hesitate to call on me! 🌟",
            "Bye! It's been a pleasure assisting you! 🎯",
            "Talk soon! I'm here whenever you need! 💙",
        ]

        farewell = random.choice(farewells)

        # Add mood-appropriate farewell
        mood_farewell = self.mood_responses.get(self.user_mood, {}).get('farewell', '')
        if mood_farewell:
            farewell = f"{mood_farewell}{farewell}"

        return farewell


def create_persona_service():
    """Factory function to create PersonaResponseService"""
    return PersonaResponseService()
