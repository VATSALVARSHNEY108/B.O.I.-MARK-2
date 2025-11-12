#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv
from modules.core.gemini_controller import parse_command, get_ai_suggestion
from modules.core.command_executor import CommandExecutor

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
        print("   🤖 AI Code Generation:")
        print("   • 'Write code for checking palindrome'")
        print("   • 'Run this code: print(\"Hello\")'")
        print("\n   🔍 AI Vision & Analysis:")
        print("   • 'Analyze screenshot.png'")
        print("   • 'Extract text from screenshot.png'")
        print("\n   📊 System Monitoring:")
        print("   • 'Show system report'")
        print("   • 'Check CPU usage'")
        print("\n   📁 File Management:")
        print("   • 'Search for *.txt files'")
        print("   • 'Find large files'")
        print("\n   💾 Workflow Templates:")
        print("   • 'List workflows'")
        print("   • 'Show history'")
        print("\n📌 Commands:")
        print("   • Type 'help' for full feature list")
        print("   • Type 'contacts' to list contacts")
        print("   • Type 'position' to see mouse coordinates")
        print("   • Type 'exit' or 'quit' to stop")
        print("=" * 70)
    
    def show_help(self):
        """Show help information"""
        print("\n📚 ENHANCED AUTOMATION CAPABILITIES:")
        print("\n🤖 AI Code Generation:")
        print("   • Write code for checking palindrome")
        print("   • Run this code: [your code]")
        print("   • Explain this code: [code]")
        print("\n🔍 AI Vision & Screenshot Analysis:")
        print("   • Analyze screenshot.png")
        print("   • Extract text from image.png")
        print("   • What's in this screenshot?")
        print("\n📊 System Monitoring:")
        print("   • Show system report (full health check)")
        print("   • Check CPU/memory/disk usage")
        print("   • What processes are running?")
        print("\n📁 Advanced File Management:")
        print("   • Search for *.py files")
        print("   • Find large files")
        print("   • How big is this folder?")
        print("\n💾 Workflow Templates:")
        print("   • Save workflow: [name]")
        print("   • List workflows")
        print("   • Run workflow: [name]")
        print("\n📜 Conversation Memory:")
        print("   • Show history (recent commands)")
        print("   • Show statistics")
        print("\n🖥️ Desktop Automation:")
        print("   • Open notepad, Type text, Take screenshot")
        print("   • Search the web, Create files")
        print("\n📱 Messaging:")
        print("   • Text/Email contacts")
        print("   • Send files")
        print("   • Note: Requires Twilio/Gmail")
    
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
                
                # Check if this is a simple greeting or general question
                simple_queries = ['hi', 'hello', 'hey', 'good morning', 'good evening', 'good afternoon',
                                'thanks', 'thank you', 'bye', 'goodbye', 'what is', 'who is', 
                                'tell me about', 'explain', 'how does', 'why', 'when']
                
                is_simple_query = any(user_input.lower().startswith(q) for q in simple_queries)
                
                # For simple queries, use chatbot directly
                if is_simple_query or len(user_input.split()) <= 5:
                    from modules.core.gemini_controller import chat_response
                    try:
                        response = chat_response(user_input)
                        print(f"\n🤖 {response}")
                        continue
                    except Exception as e:
                        print(f"\n💬 {user_input}")
                        # If chat fails, fall through to command parsing
                
                command_dict = parse_command(user_input)
                
                if command_dict.get("action") == "error":
                    # Instead of showing error, try chatbot as fallback
                    from modules.core.gemini_controller import chat_response
                    try:
                        response = chat_response(user_input)
                        print(f"\n🤖 {response}")
                    except Exception as e:
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
