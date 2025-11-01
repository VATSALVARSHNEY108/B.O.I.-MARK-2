"""
Test Full Screen Notepad Feature
Demonstrates opening Notepad in full screen and writing content
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'modules', 'utilities'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'modules', 'ai_features'))

from notepad_writer import write_to_notepad, write_code_to_notepad, write_letter_to_notepad
from letter_templates import generate_letter

def test_fullscreen_notepad():
    """Test the full screen notepad writing feature"""
    
    print("🎯 FULL SCREEN NOTEPAD WRITER TEST")
    print("=" * 80)
    
    print("\n📋 Test Menu:")
    print("1. Test simple text in full screen")
    print("2. Test letter writing in full screen")
    print("3. Test code writing in full screen")
    print("4. Test without full screen (normal window)")
    
    choice = input("\nSelect test (1-4) or press Enter for demo: ").strip()
    
    if not choice or choice == "1":
        print("\n" + "=" * 80)
        print("TEST 1: Simple Text in Full Screen")
        print("=" * 80)
        
        test_content = """Welcome to VATSAL AI Assistant!

This is a demonstration of the full screen Notepad feature.

Features:
✅ Automatically opens Notepad
✅ Maximizes to full screen
✅ Writes content beautifully
✅ Perfect for letters and code

The window will open maximized for better visibility!
"""
        
        print("\n🚀 Opening Notepad in FULL SCREEN and writing content...")
        result = write_to_notepad(test_content, fullscreen=True, title="VATSAL AI Demo")
        
        if result["success"]:
            print(f"\n✅ Success! {result['chars_written']} characters written")
            print(f"   {result['message']}")
        else:
            print(f"\n❌ Error: {result['error']}")
    
    elif choice == "2":
        print("\n" + "=" * 80)
        print("TEST 2: Letter Writing in Full Screen")
        print("=" * 80)
        
        print("\n🤖 Generating a leave letter...")
        letter_result = generate_letter("write a letter to principal for 2 days leave")
        
        if letter_result["success"]:
            print(f"✅ Letter generated: {letter_result['letter_name']}")
            print("\n🚀 Writing to Notepad in FULL SCREEN...")
            
            write_result = write_letter_to_notepad(
                letter_result["letter"],
                letter_result["letter_name"],
                fullscreen=True
            )
            
            if write_result["success"]:
                print(f"\n✅ {write_result['message']}")
            else:
                print(f"\n❌ Error: {write_result['error']}")
    
    elif choice == "3":
        print("\n" + "=" * 80)
        print("TEST 3: Code Writing in Full Screen")
        print("=" * 80)
        
        sample_code = '''def fibonacci(n):
    """
    Generate Fibonacci sequence up to n terms.
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib_sequence = [0, 1]
    
    for i in range(2, n):
        next_term = fib_sequence[i-1] + fib_sequence[i-2]
        fib_sequence.append(next_term)
    
    return fib_sequence


# Example usage
if __name__ == "__main__":
    print(f"First 10 Fibonacci numbers: {fibonacci(10)}")
'''
        
        print("\n🚀 Writing Python code to Notepad in FULL SCREEN...")
        write_result = write_code_to_notepad(sample_code, "python", fullscreen=True)
        
        if write_result["success"]:
            print(f"\n✅ {write_result['message']}")
        else:
            print(f"\n❌ Error: {write_result['error']}")
    
    elif choice == "4":
        print("\n" + "=" * 80)
        print("TEST 4: Normal Window (No Full Screen)")
        print("=" * 80)
        
        test_content = "This will open in a normal window, not full screen."
        
        print("\n🚀 Opening Notepad in NORMAL mode...")
        result = write_to_notepad(test_content, fullscreen=False, title="Normal Mode Test")
        
        if result["success"]:
            print(f"\n✅ {result['message']}")
        else:
            print(f"\n❌ Error: {result['error']}")
    
    print("\n" + "=" * 80)
    print("✅ TEST COMPLETE!")
    print("\n💡 TIP: The full screen feature is now integrated into:")
    print("   • Letter writing")
    print("   • Code generation")
    print("   • All Notepad outputs")
    print("\n   Just use your voice commands normally, and content will")
    print("   automatically open in full screen for better visibility!")

if __name__ == "__main__":
    test_fullscreen_notepad()
