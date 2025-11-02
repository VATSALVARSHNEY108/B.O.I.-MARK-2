"""
Test the enhanced fullscreen notepad feature
Opens notepad in TRUE fullscreen before writing
"""

from modules.utilities.notepad_writer import write_to_notepad

def test_fullscreen_notepad():
    """Test opening notepad in fullscreen before writing"""
    
    print("=" * 60)
    print("TESTING: Fullscreen Notepad Feature")
    print("=" * 60)
    print()
    print("This will:")
    print("1. Open Notepad")
    print("2. Put it in FULL SCREEN mode (F11)")
    print("3. Write content to it")
    print()
    
    content = """Hello! This is a test of the fullscreen notepad feature.

✅ Notepad opened in FULL SCREEN first
✅ Then content was written

Features:
- Opens notepad in true fullscreen (F11)
- Maximizes window first for better visibility
- Proper timing to ensure smooth operation
- Works on Windows and Linux

This ensures notepad is fully visible before any content is written!
"""
    
    result = write_to_notepad(
        content=content,
        fullscreen=True,
        title="Fullscreen Notepad Test"
    )
    
    print()
    print("=" * 60)
    if result["success"]:
        print(f"✅ SUCCESS!")
        print(f"   Characters written: {result['chars_written']}")
        print(f"   Fullscreen mode: {result['fullscreen']}")
        print(f"   Message: {result['message']}")
    else:
        print(f"❌ ERROR: {result.get('error', 'Unknown error')}")
    print("=" * 60)

if __name__ == "__main__":
    test_fullscreen_notepad()
