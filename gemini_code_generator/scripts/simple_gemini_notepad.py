"""
Simple Gemini to Notepad - Quick Code Generation
Ultra-simple script to generate code and write it to Notepad
"""

from code_generator import generate_code
import subprocess
import time
import pyperclip
import pyautogui

def generate_and_write(description):
    """Generate code with Gemini and write to Notepad"""
    
    print(f"🤖 Generating code: {description}...")
    
    result = generate_code(description)
    
    if result.get("success"):
        code = result["code"]
        
        print(f"✅ Generated {result['language']} code ({len(code)} chars)")
        print("📝 Opening Notepad and writing code...")
        
        subprocess.Popen(['notepad.exe'])
        time.sleep(2)
        
        pyperclip.copy(code)
        time.sleep(0.3)
        
        pyautogui.hotkey('ctrl', 'v')
        
        print("✅ Done! Code written to Notepad!")
        print("\n" + "="*60)
        print(code)
        print("="*60)
    else:
        print(f"❌ Error: {result.get('error')}")

if __name__ == "__main__":
    description = input("What code do you want to generate? ")
    generate_and_write(description)
