#!/usr/bin/env python3
"""
Automatic Patch for system_control.py
Run this on your Windows machine to automatically fix the volume control
"""

import os
import sys

def patch_file(file_path):
    """Apply the fix to system_control.py"""
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        print("Please check the path and try again.")
        return False
    
    # Read the file
    print(f"📖 Reading {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Make backup
    backup_path = file_path + '.backup'
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Backup created: {backup_path}")
    
    # Apply the fix
    print("🔧 Applying fix...")
    original_content = content
    
    # Replace the problematic pattern
    content = content.replace(
        'volume = cast(interface, POINTER(IAudioEndpointVolume))',
        'volume = interface.QueryInterface(IAudioEndpointVolume)'
    )
    
    # Remove unnecessary imports (but keep comtypes)
    # This is a bit more complex - we'll do a line-by-line replacement
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        # Remove lines that only import cast and POINTER from ctypes
        if 'from ctypes import cast, POINTER' in line and 'IAudioEndpointVolume' not in line:
            # Skip this line or replace with just the comtypes import if needed
            continue
        new_lines.append(line)
    
    content = '\n'.join(new_lines)
    
    if content == original_content:
        print("⚠️  No changes needed - file might already be fixed!")
        return True
    
    # Write the fixed content
    print("💾 Saving fixed file...")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fix applied successfully!")
    print("\n" + "="*60)
    print("🎉 Volume control is now fixed!")
    print("="*60)
    print("\nNext steps:")
    print("1. Restart your VATSAL GUI application")
    print("2. Try the 'mute' command")
    print("3. Enjoy working volume control!")
    print("\nIf you need to restore the backup:")
    print(f"   Copy: {backup_path}")
    print(f"   To:   {file_path}")
    
    return True

def main():
    print("="*60)
    print("  Volume Control Automatic Fix")
    print("="*60)
    print()
    
    # Default path
    default_path = r"C:\Users\VATSAL VARSHNEY\PycharmProjects\V.A.T.S.A.L.23242\modules\system\system_control.py"
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = default_path
        print(f"Using default path:")
        print(f"  {file_path}")
        print()
        response = input("Is this correct? (y/n): ")
        if response.lower() != 'y':
            file_path = input("Enter the full path to system_control.py: ")
    
    print()
    success = patch_file(file_path)
    
    if success:
        print("\n✅ All done!")
    else:
        print("\n❌ Fix failed. Please apply the changes manually.")
        print("See QUICK_FIX_FOR_LOCAL_MACHINE.txt for instructions.")

if __name__ == "__main__":
    main()
