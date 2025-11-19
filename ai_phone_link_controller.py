#!/usr/bin/env python3
"""
AI-Powered Phone Link Controller
Uses Google Gemini AI to understand commands and control Phone Link
"""

import os
import sys
import time
from typing import Dict, Optional
from modules.communication.phone_dialer import create_phone_dialer
from modules.core.command_executor import CommandExecutor

# Try to import Google Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ Google Gemini not available. Install with: pip install google-generativeai")


class AIPhoneLinkController:
    """AI-powered controller for Phone Link operations"""
    
    def __init__(self):
        self.phone_dialer = create_phone_dialer()
        self.executor = CommandExecutor()
        self.ai_enabled = False
        self.conversation_history = []
        
        # Initialize AI if available
        if GEMINI_AVAILABLE:
            self._setup_gemini()
    
    def _setup_gemini(self):
        """Setup Google Gemini AI"""
        api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
        
        if api_key:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.ai_enabled = True
                print("✅ AI Engine Ready (Google Gemini)")
            except Exception as e:
                print(f"⚠️ AI setup failed: {e}")
                self.ai_enabled = False
        else:
            print("⚠️ No GOOGLE_API_KEY or GEMINI_API_KEY found")
            print("   Set it to enable AI features")
    
    def understand_command(self, user_input: str) -> Dict:
        """
        Use AI to understand user's phone-related command
        
        Args:
            user_input: Natural language command from user
            
        Returns:
            Dict with interpreted action and parameters
        """
        if not self.ai_enabled:
            # Fallback to simple parsing
            return self._simple_parse(user_input)
        
        try:
            # Create AI prompt to understand the command
            prompt = f"""
You are a phone control assistant. Analyze this command and extract the action and phone number if any.

User command: "{user_input}"

Response format (JSON):
{{
    "action": "dial" | "open_phone_link" | "send_message" | "unknown",
    "phone_number": "extracted phone number or null",
    "message": "message content if any or null",
    "confidence": 0.0 to 1.0
}}

Examples:
- "Call mom at +1234567890" → {{"action": "dial", "phone_number": "+1234567890", "message": null, "confidence": 0.9}}
- "Open Phone Link" → {{"action": "open_phone_link", "phone_number": null, "message": null, "confidence": 1.0}}
- "Dial 9876543210" → {{"action": "dial", "phone_number": "9876543210", "message": null, "confidence": 0.95}}

Only respond with valid JSON.
"""
            
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
                result_text = result_text.strip()
            
            # Parse JSON response
            import json
            result = json.loads(result_text)
            
            return result
            
        except Exception as e:
            print(f"⚠️ AI parsing failed: {e}")
            return self._simple_parse(user_input)
    
    def _simple_parse(self, text: str) -> Dict:
        """Simple fallback parser without AI"""
        text_lower = text.lower()
        
        # Extract phone number
        import re
        phone_match = re.search(r'[\+\d][\d\-\(\)\s]{7,}', text)
        phone_number = phone_match.group(0).strip() if phone_match else None
        
        # Determine action
        if any(word in text_lower for word in ['dial', 'call', 'phone', 'ring']):
            action = "dial"
        elif any(word in text_lower for word in ['open', 'launch', 'start']):
            action = "open_phone_link"
        elif any(word in text_lower for word in ['message', 'text', 'sms']):
            action = "send_message"
        else:
            action = "unknown"
        
        return {
            "action": action,
            "phone_number": phone_number,
            "message": None,
            "confidence": 0.7
        }
    
    def execute_phone_command(self, command: Dict) -> Dict:
        """
        Execute the parsed phone command
        
        Args:
            command: Parsed command dict from understand_command()
            
        Returns:
            Execution result
        """
        action = command.get("action", "unknown")
        phone_number = command.get("phone_number")
        
        print(f"\n🤖 AI Understanding:")
        print(f"   Action: {action}")
        print(f"   Phone: {phone_number or 'N/A'}")
        print(f"   Confidence: {command.get('confidence', 0):.0%}")
        print()
        
        if action == "dial" and phone_number:
            return self.phone_dialer.dial_with_phone_link(phone_number)
        
        elif action == "open_phone_link":
            return self.phone_dialer.open_phone_link()
        
        elif action == "send_message":
            return {
                "success": False,
                "message": "SMS messaging not yet implemented. Use dial for calls."
            }
        
        else:
            return {
                "success": False,
                "message": "Could not understand command. Try: 'Call +1234567890' or 'Open Phone Link'"
            }
    
    def process_command(self, user_input: str) -> Dict:
        """
        Complete flow: understand and execute command
        
        Args:
            user_input: Natural language command
            
        Returns:
            Execution result
        """
        print(f"\n💬 You: {user_input}")
        
        # Step 1: Understand with AI
        command = self.understand_command(user_input)
        
        # Step 2: Execute
        result = self.execute_phone_command(command)
        
        # Step 3: Save to history
        self.conversation_history.append({
            "input": user_input,
            "command": command,
            "result": result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
        
        return result
    
    def interactive_mode(self):
        """Run interactive AI phone controller"""
        print("=" * 70)
        print("🤖 AI PHONE LINK CONTROLLER")
        print("=" * 70)
        print()
        print("Status:")
        print(f"  AI Engine: {'✅ Active' if self.ai_enabled else '⚠️ Basic mode'}")
        print(f"  Phone Link: {'✅ Available' if self.phone_dialer.is_windows else '❌ Windows only'}")
        print()
        print("Commands you can try:")
        print("  • 'Call +1234567890'")
        print("  • 'Dial mom at 9876543210'")
        print("  • 'Open Phone Link'")
        print("  • 'Ring +91 98765 43210'")
        print("  • Type 'quit' to exit")
        print("=" * 70)
        print()
        
        while True:
            try:
                user_input = input("🎤 Enter command: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye', 'stop']:
                    print("\n👋 Goodbye!")
                    break
                
                # Process the command
                result = self.process_command(user_input)
                
                # Show result
                print(f"\n✅ {result.get('message', 'Done')}")
                print()
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
    
    def quick_dial(self, phone_number: str):
        """Quick dial without AI parsing"""
        return self.phone_dialer.dial_with_phone_link(phone_number)
    
    def get_history(self, limit: int = 5):
        """Get recent command history"""
        return self.conversation_history[-limit:]


def main():
    """Main entry point"""
    controller = AIPhoneLinkController()
    
    # Check if command provided via arguments
    if len(sys.argv) > 1:
        # Use command line arguments
        command = " ".join(sys.argv[1:])
        result = controller.process_command(command)
        print(f"\n{result.get('message', 'Done')}")
    else:
        # Interactive mode
        controller.interactive_mode()


if __name__ == "__main__":
    main()
