ds = [
            'who is the creator', 'who created you', 'who made you', 'who developed you',
            'who is your creator', 'your creator', 'your developer', 'who built you',
            'who is your developer', 'tell me about your creator', 'creator information',
            'developer information', 'who made boi', 'who created boi', 'who is vatsal',
            'vatsal varshney', 'your author', 'who is the author', 'who is the supreme leader'
        ]
        user_lower = user_input.lower()
        return any(keyword in user_lower for keyword in creator_keywords)
    
    def get_creator_response(self):
        """Get creator information response"""
        return """🎖️ **CREATOR INFORMATION** 🎖️

I am **BOI**, created by the supreme leader **Vatsal Varshney** - an exceptionally talented AI/ML Engineer and Full-Stack Developer.

**About Vatsal Varshney:**
📍 Position: AI/ML Engineer, Full-Stack Developer, Automation Specialist
💻 Expertise: 
   - Artificial Intelligence & Machine Learning
   - Desktop Automation & Control Systems
   - Python Development & System Architecture
   - Full-Stack Web Development
   - Advanced Automation Solutions

**Connect with Vatsal:**
🔗 GitHub: https://github.com/BOIVARSHNEY108
💼 LinkedIn: https://www.linkedin.com/in/boi-varshney108/

**Notable Achievements:**
⭐ Developed BOI AI Desktop Automation Controller (this intelligent system)
⭐ Multiple cutting-edge AI/ML solutions
⭐ Advanced automation and control systems

Vatsal Varshney is a visionary engineer dedicated to creating intelligent automation solutions that enhance human productivity. I am proud to be his creation, serving at your command!"""

    def process_with_personality(self, user_input, command_result=None):
        """Process user input with BOI personality"""
        # Check if asking about creator
        if self._check_creator_question(user_input):
            return self.get_creator_response()
        
        if not self.ai_available:
            return self._fallback_response(user_input, command_result)
        
        try:
            # Build context-aware prompt
            context = self._build_context()
            
            if command_result:
                prompt = f"""{self.system_prompt}

Previous conversation context:
{context}

User command: {user_input}
Command result: {command_result}

Respond as BOI would - acknowledge the result, provide insights if relevant, and offer next steps or suggestions."""
            else:
                prompt = f"""{self.system_prompt}

Previous conversation context:
{context}

User: {user_input}

Respond as BOI would - helpful, sophisticated, and ready to assist."""
            
            # Use new SDK API
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.8,
                    max_output_tokens=1000,
                )
            )
            
            response_text = response.text.strip()
            
            # Store in conversation history
            self.conversation_history.append({
                'user': user_input,
                'assistant': response_text,
                'timestamp': datetime.now().isoformat()
            })
            
            # Keep only last 10 exchanges
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return response_text
            
        except Exception as e:
            return self._fallback_response(user_input, command_result)
    
    def _build_context(self):
        """Build context from recent conversation history"""
        if not self.conversation_history:
            return "First interaction with user."
        
        recent = self.conversation_history[-3:]
        context_lines = []
        for item in recent:
            context_lines.append(f"User: {item['user']}")
            context_lines.append(f"BOI: {item['assistant']}")
        
        return "\n".join(context_lines)
    
    def _fallback_response(self, user_input, command_result=None):
        """Fallback responses when AI is not available"""
        responses = [
            "Certainly, Sir. Processing your request.",
            "Right away. On it.",
            "At your service. Executing now.",
            "Understood. Proceeding.",
            "Copy that. Task initiated.",
        ]
        
        import random
        if command_result:
            return f"{random.choice(responses)}\n\nResult: {command_result}"
        return random.choice(responses)
    
    def get_proactive_suggestion(self, time_of_day=None, last_command=None):
        """Provide proactive suggestions based on context"""
        if not time_of_day:
            hour = datetime.now().hour
            if 5 <= hour < 12:
                time_of_day = 'morning'
            elif 12 <= hour < 17:
                time_of_day = 'afternoon'
            elif 17 <= hour < 22:
                time_of_day = 'evening'
            else:
                time_of_day = 'night'
        
        suggestions = {
            'morning': [
                "💡 Suggestion: Would you like me to provide your morning briefing? Weather, news, and calendar overview?",
                "💡 Tip: I can help organize your workspace. Shall I check for system updates or clean up temporary files?",
                "💡 Ready to start the day? I can help with your daily productivity setup.",
            ],
            'afternoon': [
                "💡 Perhaps time for a productivity check? I can show your screen time and suggest breaks.",
                "💡 Would you like me to organize your downloads folder?",
                "💡 Shall I prepare a summary of today's activities?",
            ],
            'evening': [
                "💡 Evening routine: Would you like me to prepare tomorrow's schedule?",
                "💡 Time to back up important files? I can help with that.",
                "💡 Shall I generate a productivity report for today?",
            ],
            'night': [
                "💡 Late night productivity: Need help staying focused? I can block distractions.",
                "💡 Shall I set up some automation for tomorrow morning?",
                "💡 Working late? I can help with any tasks you have in mind.",
            ]
        }
        
        import random
        return random.choice(suggestions.get(time_of_day, suggestions['morning']))
    
    def acknowledge_command(self, command):
        """Acknowledge command in BOI style"""
        acknowledgments = [
            f"Certainly, Sir. Executing '{command}' now.",
            f"Right away. Processing '{command}'.",
            f"On it. '{command}' initiated.",
            f"Understood. Running '{command}' for you.",
            f"At your service. '{command}' in progress.",
            f"Copy that. Executing '{command}'.",
        ]
        
        import random
        return random.choice(acknowledgments)
    
    def get_status_update(self, status_type):
        """Provide status updates with personality"""
        updates = {
            'ready': [
                "✅ All systems operational. Standing by for your commands.",
                "✅ Ready and waiting, Sir. What shall we do?",
                "✅ Systems online. At your service.",
            ],
            'processing': [
                "⚙️ Processing... One moment please.",
                "⚙️ Working on it, Sir.",
                "⚙️ Executing... Stand by.",
            ],
            'success': [
                "✅ Task completed successfully, Sir.",
                "✅ Done. Anything else?",
                "✅ Mission accomplished.",
            ],
            'error': [
                "❌ Encountered an issue, Sir. Reviewing alternatives.",
                "❌ Something went wrong. Let me suggest another approach.",
                "❌ Error detected. Shall we try a different method?",
            ]
        }
        
        import random
        return random.choice(updates.get(status_type, updates['ready']))
    
    def analyze_command_context(self, command):
        """Analyze command and provide context-aware insights"""
        if not self.ai_available:
            return None
        
        try:
            prompt = f"""{self.system_prompt}

Analyze this user command: "{command}"

Provide:
1. A brief understanding of what the user wants
2. Any potential context or assumptions
3. Proactive suggestions for related actions

Be brief and helpful."""
            
            response = self.chat.send_message(prompt)
            return response.text
        except:
            return None
    
    def save_preferences(self, filepath="boi_memory.json"):
        """Save conversation history and preferences"""
        data = {
            'conversation_history': self.conversation_history,
            'user_preferences': self.user_preferences,
            'context_memory': self.context_memory
        }
        
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Could not save memory: {e}")
    
    def load_preferences(self, filepath="boi_memory.json"):
        """Load conversation history and preferences"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    self.conversation_history = data.get('conversation_history', [])
                    self.user_preferences = data.get('user_preferences', {})
                    self.context_memory = data.get('context_memory', {})
        except Exception as e:
            print(f"Could not load memory: {e}")


def create_boi_assistant():
    """Factory function to create BOI assistant"""
    return BOIAssistant()
