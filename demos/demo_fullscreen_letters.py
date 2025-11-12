#!/usr/bin/env python3
"""
🎯 VATSAL AI - Full Screen Letter & Code Demo
Demonstrates the new full screen Notepad feature with letter writing
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules', 'ai_features'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules', 'utilities'))

from letter_templates import generate_letter, list_letter_types
from notepad_writer import write_letter_to_notepad, write_code_to_notepad

def print_banner():
    print("\n" + "=" * 80)
    print(" " * 20 + "🤖 VATSAL AI - FULL SCREEN NOTEPAD DEMO 🤖")
    print("=" * 80)
    print("\n✨ This demo shows how VATSAL automatically writes to Notepad in FULL SCREEN\n")

def demo_letter_writing():
    """Demonstrate letter writing with full screen"""
    
    print("\n" + "=" * 80)
    print("📝 LETTER WRITING DEMO")
    print("=" * 80)
    
    print("\n📋 Available Letter Types:")
    letter_types = list_letter_types()
    for i, (key, name) in enumerate(letter_types.items(), 1):
        print(f"   {i:2d}. {name}")
    
    print("\n💡 Example Commands:")
    print("   • 'write a letter to principal for 2 days leave'")
    print("   • 'write a resignation letter'")
    print("   • 'write a thank you letter'")
    
    user_input = input("\n🎯 Enter your command (or press Enter for demo): ").strip()
    
    if not user_input:
        user_input = "write a letter to principal for 2 days leave"
        print(f"   Using demo: '{user_input}'")
    
    print("\n🤖 Processing your command...")
    result = generate_letter(user_input)
    
    if result["success"]:
        print(f"✅ Generated: {result['letter_name']}")
        print(f"   Letter Type: {result['letter_type']}")
        print(f"   Length: {len(result['letter'])} characters")
        
        print("\n" + "-" * 80)
        print("Preview:")
        print("-" * 80)
        print(result['letter'][:300] + "..." if len(result['letter']) > 300 else result['letter'])
        print("-" * 80)
        
        proceed = input("\n📝 Write this to Notepad in FULL SCREEN? (Y/n): ").strip().lower()
        
        if proceed != 'n':
            print("\n🚀 Opening Notepad in FULL SCREEN mode...")
            print("   1. Opening Notepad...")
            print("   2. Maximizing to full screen...")
            print("   3. Writing content...")
            
            write_result = write_letter_to_notepad(
                result['letter'],
                result['letter_name'],
                fullscreen=True
            )
            
            if write_result["success"]:
                print(f"\n✅ SUCCESS! {write_result['message']}")
                print(f"   Characters written: {write_result['chars_written']}")
            else:
                print(f"\n❌ Error: {write_result['error']}")
    else:
        print(f"\n❌ Error generating letter: {result.get('error')}")

def demo_code_writing():
    """Demonstrate code writing with full screen"""
    
    print("\n" + "=" * 80)
    print("💻 CODE WRITING DEMO")
    print("=" * 80)
    
    sample_code = '''def fibonacci(n):
    """
    Generate Fibonacci sequence up to n terms.
    
    The Fibonacci sequence is: 0, 1, 1, 2, 3, 5, 8, 13, 21, ...
    Each number is the sum of the two preceding ones.
    
    Args:
        n: Number of terms to generate.
    
    Returns:
        List containing the Fibonacci sequence.
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    # Initialize the sequence
    fib_sequence = [0, 1]
    
    # Generate remaining terms
    for i in range(2, n):
        next_term = fib_sequence[i-1] + fib_sequence[i-2]
        fib_sequence.append(next_term)
    
    return fib_sequence


# Example usage
if __name__ == "__main__":
    print(f"First 10 Fibonacci numbers: {fibonacci(10)}")
    print(f"First 15 Fibonacci numbers: {fibonacci(15)}")
'''
    
    print("\n📝 Sample Python Code Ready")
    print(f"   Lines of code: {len(sample_code.splitlines())}")
    print(f"   Characters: {len(sample_code)}")
    
    print("\n" + "-" * 80)
    print("Preview:")
    print("-" * 80)
    print(sample_code[:200] + "...")
    print("-" * 80)
    
    proceed = input("\n📝 Write this code to Notepad in FULL SCREEN? (Y/n): ").strip().lower()
    
    if proceed != 'n':
        print("\n🚀 Opening Notepad in FULL SCREEN mode...")
        print("   1. Opening Notepad...")
        print("   2. Maximizing to full screen...")
        print("   3. Writing code with title...")
        
        write_result = write_code_to_notepad(sample_code, "python", fullscreen=True)
        
        if write_result["success"]:
            print(f"\n✅ SUCCESS! {write_result['message']}")
            print(f"   Characters written: {write_result['chars_written']}")
        else:
            print(f"\n❌ Error: {write_result['error']}")

def main():
    """Main demo function"""
    
    print_banner()
    
    print("📋 Demo Options:")
    print("   1. Letter Writing Demo (Full Screen)")
    print("   2. Code Writing Demo (Full Screen)")
    print("   3. Both Demos")
    
    choice = input("\n🎯 Select option (1-3) or press Enter for both: ").strip()
    
    if choice == "1":
        demo_letter_writing()
    elif choice == "2":
        demo_code_writing()
    else:
        demo_letter_writing()
        
        another = input("\n\n🔄 Run code demo too? (Y/n): ").strip().lower()
        if another != 'n':
            demo_code_writing()
    
    print("\n" + "=" * 80)
    print("✅ DEMO COMPLETE!")
    print("=" * 80)
    
    print("\n💡 KEY FEATURES:")
    print("   ✅ Automatic full screen - No manual maximizing needed")
    print("   ✅ Professional titles - Each document gets a formatted header")
    print("   ✅ 13 letter types - Leave, complaint, resignation, and more")
    print("   ✅ Smart detection - AI understands your natural language")
    print("   ✅ Custom variables - Personalize every letter")
    
    print("\n🎯 TRY THESE VOICE COMMANDS:")
    print("   • 'Write a letter to principal for 3 days sick leave'")
    print("   • 'Write a resignation letter'")
    print("   • 'Write a thank you letter'")
    print("   • 'Generate a palindrome checker in Python'")
    
    print("\n🚀 All outputs automatically open in FULL SCREEN for better visibility!")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
