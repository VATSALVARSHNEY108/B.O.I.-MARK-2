#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv
from gemini_controller import parse_command, get_ai_suggestion
from command_executor import CommandExecutor

load_dotenv()

class DesktopAutomationCLI:
    """Command-line interface for AI-powered desktop automation"""
    
    def __init__(self):
        self.executor = CommandExecutor()
        self.running = True
    
    def print_banner(self):
        """Print welcome banner"""
        print("=" * 70)
        print("  🤖 AI Desktop Automation Controller")
        print("  Powered by Gemini AI")
        print("=" * 70)
        print("\n💡 Tell me what you want to do in plain English!")
        print("   🤖 AI Code Generation (NEW!):")
        print("   • 'Write code for checking palindrome'")
        print("   • 'Generate Python code for bubble sort'")
        print("   • 'Create JavaScript code for form validation'")
        print("\n   Desktop Automation:")
        print("   • 'Open notepad and type Hello World'")
        print("   • 'Take a screenshot'")
        print("   • 'Search Google for Python tutorials'")
        print("\n   📱 Messaging (Advanced):")
        print("   • 'Send this photo to John' (send files)")
        print("   • 'Text Sarah that I'm running late' (SMS)")
        print("   • 'Email my boss the report' (Email)")
        print("   • 'Add contact Mom with phone 555-1234'")
        print("\n📌 Commands:")
        print("   • Type 'help' for full feature list")
        print("   • Type 'contacts' to list contacts")
        print("   • Type 'position' to see mouse coordinates")
        print("   • Type 'exit' or 'quit' to stop")
        print("=" * 70)
    
    def show_help(self):
        """Show help information"""
        print("\n📚 Available Automation Capabilities:")
        print("\n🔹 AI Code Generation (NEW!):")
        print("   • Generate code in any language")
        print("   • 'Write code for checking palindrome'")
        print("   • 'Generate JavaScript code for calculator'")
        print("   • 'Create Python code for web scraping'")
        print("   • Automatically opens editor and types code")
        print("\n🔹 Application Control:")
        print("   • Open applications (e.g., 'open chrome')")
        print("   • Close windows with hotkeys")
        print("\n🔹 Text & Typing:")
        print("   • Type text ('type Hello World')")
        print("   • Copy/paste operations")
        print("\n🔹 Mouse Control:")
        print("   • Click at positions ('click at 500, 300')")
        print("   • Move mouse ('move mouse to 100, 200')")
        print("\n🔹 Keyboard:")
        print("   • Press keys ('press enter')")
        print("   • Hotkey combinations ('press ctrl and c')")
        print("\n🔹 Utilities:")
        print("   • Take screenshots")
        print("   • Search the web")
        print("   • Create files")
        print("   • Wait/pause")
        print("\n🔹 Messaging & Contacts:")
        print("   • Send SMS: 'text John that I'm on my way'")
        print("   • Send Email: 'email Sarah about the meeting'")
        print("   • Send Files: 'send report.pdf to my boss'")
        print("   • Manage Contacts: 'add contact [name]', 'list contacts'")
        print("   • Note: Requires Twilio (SMS) or Gmail setup")
        print("\n🔹 Multi-Step Workflows:")
        print("   • Combine actions in one command")
        print("   • Example: 'Open notepad, type Hello, and save as test.txt'")
    
    def get_mouse_position(self):
        """Display current mouse position"""
        pos = self.executor.gui.get_mouse_position()
        print(f"\n🖱️  Mouse Position: X={pos[0]}, Y={pos[1]}")
        print("   (Move your mouse and run 'position' again to see updates)")
    
    def run(self):
        """Main CLI loop"""
        self.print_banner()
        
        if not os.environ.get("GEMINI_API_KEY"):
            print("\n❌ Error: GEMINI_API_KEY not found in environment variables")
            print("   Please add your Gemini API key to continue.")
            return
        
        print("\n✅ Connected to Gemini AI\n")
        
        while self.running:
            try:
                user_input = input("\n🎯 What would you like to do? ").strip()
                
                if not user_input:
                    continue
                
                user_input_lower = user_input.lower()
                
                if user_input_lower in ['exit', 'quit', 'q']:
                    print("\n👋 Goodbye! Automation controller stopped.")
                    self.running = False
                    break
                
                elif user_input_lower == 'help':
                    self.show_help()
                    continue
                
                elif user_input_lower == 'position':
                    self.get_mouse_position()
                    continue
                
                elif user_input_lower == 'contacts':
                    result = self.executor.execute_single_action("list_contacts", {})
                    print(f"\n{result['message']}")
                    continue
                
                print("\n🤔 Processing your command with AI...")
                
                command_dict = parse_command(user_input)
                
                if command_dict.get("action") == "error":
                    print(f"\n❌ {command_dict.get('description', 'Error processing command')}")
                    suggestion = get_ai_suggestion(f"User tried: {user_input}, but got error. Suggest alternatives.")
                    print(f"\n💡 Suggestion: {suggestion}")
                    continue
                
                result = self.executor.execute(command_dict)
                
                if result["success"]:
                    print(f"\n✅ {result['message']}")
                else:
                    print(f"\n❌ {result['message']}")
            
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!")
                self.running = False
                break
            
            except Exception as e:
                print(f"\n❌ Unexpected error: {str(e)}")
                print("   Please try again or type 'help' for assistance.")

def main():
    """Entry point"""
    cli = DesktopAutomationCLI()
    cli.run()

if __name__ == "__main__":
    main()
