"""
Common Sense Reasoning Module for VATSAL AI
Provides logical reasoning, context awareness, and practical knowledge
"""

import os
import json
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, time
from google import genai
from google.genai import types


class CommonSenseReasoning:
    """Enhanced common sense reasoning for intelligent decision making"""
    
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key) if api_key else None
        
        # Context awareness
        self.current_context = {
            'time_of_day': None,
            'recent_actions': [],
            'user_goals': [],
            'environment_state': {}
        }
        
        # Common sense rules
        self.safety_rules = {
            'file_operations': [
                "Don't delete system files",
                "Warn before deleting important files",
                "Confirm destructive operations",
                "Don't overwrite without backup"
            ],
            'system_control': [
                "Don't shutdown during important tasks",
                "Warn before force-closing apps with unsaved work",
                "Check if updates will interrupt workflow"
            ],
            'automation': [
                "Don't send messages/emails without confirmation",
                "Don't post to social media automatically",
                "Verify recipients before sending"
            ]
        }
        
        # Practical knowledge
        self.practical_knowledge = {
            'time_awareness': {
                'work_hours': (9, 17),
                'sleep_hours': (22, 6),
                'meal_times': {'breakfast': (7, 9), 'lunch': (12, 14), 'dinner': (18, 20)}
            },
            'app_purposes': {
                'code_editors': ['vscode', 'pycharm', 'sublime', 'atom', 'notepad++'],
                'browsers': ['chrome', 'firefox', 'edge', 'safari'],
                'communication': ['slack', 'teams', 'discord', 'whatsapp'],
                'productivity': ['notion', 'trello', 'asana', 'todoist']
            },
            'file_extensions': {
                'code': ['.py', '.js', '.java', '.cpp', '.c', '.html', '.css'],
                'documents': ['.docx', '.pdf', '.txt', '.md'],
                'media': ['.jpg', '.png', '.mp4', '.mp3', '.gif'],
                'data': ['.csv', '.json', '.xml', '.db']
            }
        }
    
    def validate_action(self, action: str, context: Dict) -> Dict[str, Any]:
        """
        Validate if an action makes sense in the current context
        Returns: validation result with warnings/suggestions
        """
        if not self.client:
            return self._simple_validation(action, context)
        
        try:
            current_time = datetime.now()
            hour = current_time.hour
            
            prompt = f"""You are a common sense reasoning system. Analyze if this action makes sense:

ACTION: {action}

CONTEXT:
- Current time: {current_time.strftime('%I:%M %p')}
- Day: {current_time.strftime('%A')}
- Recent actions: {context.get('recent_actions', [])}

Use common sense to evaluate:
1. Is this action safe? (no data loss, no privacy issues)
2. Is this the right time? (consider work hours, sleep time)
3. Are there better alternatives?
4. Any potential problems or unintended consequences?
5. Does this conflict with recent actions?

Provide JSON response:
{{
  "makes_sense": true/false,
  "confidence": 0.0-1.0,
  "warnings": ["list of warnings if any"],
  "suggestions": ["better alternatives or tips"],
  "reasoning": "brief explanation",
  "time_appropriate": true/false,
  "safety_level": "safe/caution/dangerous"
}}"""

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            return json.loads(response.text)
            
        except Exception as e:
            print(f"⚠️ Common sense validation failed: {e}")
            return self._simple_validation(action, context)
    
    def _simple_validation(self, action: str, context: Dict) -> Dict[str, Any]:
        """Fallback simple validation using rules"""
        action_lower = action.lower()
        warnings = []
        suggestions = []
        safety_level = "safe"
        
        # Time-based checks
        hour = datetime.now().hour
        if 'send email' in action_lower or 'send message' in action_lower:
            if hour < 8 or hour > 21:
                warnings.append("It's quite late/early to send messages. Recipient might be sleeping.")
                suggestions.append("Consider scheduling this for normal hours (9 AM - 9 PM)")
            safety_level = "caution"
        
        if 'delete' in action_lower or 'remove' in action_lower:
            warnings.append("This action is destructive and cannot be undone")
            suggestions.append("Consider backing up or moving to trash instead")
            safety_level = "caution"
        
        if 'shutdown' in action_lower or 'restart' in action_lower:
            warnings.append("Make sure all work is saved before shutting down")
            safety_level = "caution"
        
        # Check for conflicts with recent actions
        recent = context.get('recent_actions', [])
        if recent and 'close' in action_lower:
            for recent_action in recent[-3:]:
                if 'open' in recent_action.lower():
                    warnings.append("You just opened something. Are you sure you want to close it?")
        
        return {
            'makes_sense': len(warnings) == 0,
            'confidence': 0.7,
            'warnings': warnings,
            'suggestions': suggestions,
            'reasoning': 'Basic rule-based validation',
            'time_appropriate': not (hour < 6 or hour > 23),
            'safety_level': safety_level
        }
    
    def infer_user_intent(self, message: str, context: Dict) -> Dict[str, Any]:
        """
        Infer what the user actually wants, even if they didn't say it clearly
        """
        if not self.client:
            return {'intent': message, 'confidence': 0.5}
        
        try:
            prompt = f"""Analyze this user message and infer their true intent:

MESSAGE: "{message}"

CONTEXT:
- Recent actions: {context.get('recent_actions', [])}
- Time: {datetime.now().strftime('%I:%M %p, %A')}

What does the user REALLY want? Consider:
1. Implicit requests (e.g., "I'm tired" might mean "help me automate this")
2. Incomplete requests (e.g., "open chrome" might mean "open chrome and go to last website")
3. Contextual clues from recent actions
4. Common patterns (e.g., asking for time often means checking schedule)

Provide JSON:
{{
  "explicit_intent": "what they literally said",
  "inferred_intent": "what they probably mean",
  "confidence": 0.0-1.0,
  "suggested_actions": ["concrete actions to help"],
  "assumptions": ["what we're assuming about their goal"]
}}"""

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            return json.loads(response.text)
            
        except Exception as e:
            return {'intent': message, 'confidence': 0.5, 'error': str(e)}
    
    def check_logical_consistency(self, new_request: str, conversation_history: List[Dict]) -> Dict[str, Any]:
        """
        Check if new request is logically consistent with conversation history
        Detect contradictions or illogical sequences
        """
        if len(conversation_history) < 2:
            return {'consistent': True, 'issues': []}
        
        # Extract recent user messages
        recent_messages = [
            msg['content'] for msg in conversation_history[-5:]
            if msg['role'] == 'user'
        ]
        
        if not self.client:
            return {'consistent': True, 'issues': []}
        
        try:
            prompt = f"""Check if this new request is logically consistent:

CONVERSATION HISTORY:
{chr(10).join(f"- {msg}" for msg in recent_messages)}

NEW REQUEST: {new_request}

Identify any:
1. Contradictions (e.g., "open chrome" then immediately "open chrome" again)
2. Redundancy (asking for same thing twice)
3. Illogical sequences (e.g., "close all apps" then "switch to notepad")
4. Missing steps (e.g., asking to save file before opening editor)

JSON response:
{{
  "consistent": true/false,
  "issues": ["list of logical problems"],
  "clarifications_needed": ["questions to ask user"],
  "suggested_fix": "what probably makes more sense"
}}"""

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            return json.loads(response.text)
            
        except Exception as e:
            return {'consistent': True, 'issues': []}
    
    def apply_world_knowledge(self, query: str) -> Dict[str, Any]:
        """
        Apply real-world knowledge to understand context and provide better answers
        """
        if not self.client:
            return {'knowledge': 'Limited knowledge available'}
        
        try:
            prompt = f"""Apply common sense and world knowledge to this query:

QUERY: {query}

Provide relevant context, facts, and practical knowledge:
1. What background knowledge is relevant?
2. What are common patterns or best practices?
3. What do most people do in this situation?
4. Any cultural or contextual considerations?

JSON response:
{{
  "relevant_facts": ["key facts or knowledge"],
  "best_practices": ["recommended approaches"],
  "common_pitfalls": ["things to avoid"],
  "context_tips": ["helpful contextual information"]
}}"""

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            return json.loads(response.text)
            
        except Exception as e:
            return {'knowledge': f'Error: {e}'}
    
    def suggest_smarter_approach(self, task: str, current_approach: str) -> Dict[str, Any]:
        """
        Suggest a smarter or more efficient way to do something
        """
        if not self.client:
            return {'suggestion': current_approach}
        
        try:
            prompt = f"""Suggest a smarter approach to this task:

TASK: {task}
CURRENT APPROACH: {current_approach}

Think about:
1. Is there a faster way?
2. Is there a safer way?
3. Can this be automated better?
4. What would an expert do?
5. Are there tools or shortcuts?

JSON response:
{{
  "smarter_approach": "better way to do this",
  "why_better": "explanation of benefits",
  "time_saved": "estimated time savings",
  "difficulty": "easy/medium/hard",
  "worth_it": true/false
}}"""

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            return json.loads(response.text)
            
        except Exception as e:
            return {'suggestion': current_approach}
    
    def detect_missing_information(self, request: str) -> Dict[str, Any]:
        """
        Detect what information is missing to fulfill a request properly
        """
        if not self.client:
            return {'missing': [], 'can_proceed': True}
        
        try:
            prompt = f"""Analyze what information is missing from this request:

REQUEST: {request}

What details are needed to complete this properly?
- Specific parameters?
- File names or paths?
- Preferences or options?
- Confirmation for destructive actions?

JSON response:
{{
  "missing_info": ["list of missing details"],
  "critical": ["info that MUST be provided"],
  "optional": ["nice-to-have details"],
  "can_proceed_without": true/false,
  "questions_to_ask": ["questions to get missing info"]
}}"""

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            return json.loads(response.text)
            
        except Exception as e:
            return {'missing': [], 'can_proceed': True}
    
    def update_context(self, action: str, result: Dict):
        """Update context with recent actions"""
        self.current_context['recent_actions'].append({
            'action': action,
            'timestamp': datetime.now().isoformat(),
            'success': result.get('success', False)
        })
        
        # Keep only last 20 actions
        if len(self.current_context['recent_actions']) > 20:
            self.current_context['recent_actions'] = self.current_context['recent_actions'][-20:]
    
    def get_context_summary(self) -> str:
        """Get summary of current context"""
        recent = self.current_context['recent_actions'][-5:]
        if not recent:
            return "No recent actions"
        
        summary = "Recent actions:\n"
        for action in recent:
            status = "✅" if action['success'] else "❌"
            summary += f"  {status} {action['action']}\n"
        
        return summary


def create_common_sense() -> CommonSenseReasoning:
    """Factory function to create CommonSenseReasoning instance"""
    return CommonSenseReasoning()


if __name__ == "__main__":
    # Test the common sense reasoning
    cs = create_common_sense()
    
    test_cases = [
        ("Delete all my files", {}),
        ("Send email to my boss", {'recent_actions': []}),
        ("Open notepad", {'recent_actions': ['opened notepad 2 seconds ago']}),
    ]
    
    print("🧠 Common Sense Reasoning Test\n")
    for action, context in test_cases:
        print(f"Action: '{action}'")
        validation = cs.validate_action(action, context)
        print(f"Safe: {validation['safety_level']}")
        if validation['warnings']:
            print(f"Warnings: {validation['warnings']}")
        if validation['suggestions']:
            print(f"Suggestions: {validation['suggestions']}")
        print()
