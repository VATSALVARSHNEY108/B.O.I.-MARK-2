#!/usr/bin/env python3
"""
Simple Spotify Controller - Run this on your local computer
"""

import os
import sys

def check_setup():
    """Check if everything is set up correctly"""
    from dotenv import load_dotenv
    load_dotenv()
    
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("\n❌ Setup Required!")
        print("\nYou need to set up your Spotify credentials first.")
        print("\nQuick Setup Steps:")
        print("1. Read QUICK_START_SPOTIFY.txt")
        print("2. Copy .env.example to .env")
        print("3. Add your Spotify credentials to .env")
        print("\nFor detailed instructions, see: SPOTIFY_LOCAL_SETUP.md")
        return False
    
    try:
        import requests
    except ImportError:
        print("\n❌ Missing required package!")
        print("\nPlease install dependencies:")
        print("  pip install requests python-dotenv")
        return False
    
    return True

def main():
    """Main function"""
    print("\n" + "="*60)
    print("   🎵 SPOTIFY LOCAL CONTROLLER")
    print("="*60)
    
    if not check_setup():
        sys.exit(1)
    
    from spotify_local import SpotifyLocal
    
    spotify = SpotifyLocal()
    
    print("\n📱 Authenticating with Spotify...")
    print("   (This opens your browser for authorization)\n")
    
    if not spotify.authenticate():
        print("\n❌ Authentication failed!")
        print("   Please try again or check SPOTIFY_LOCAL_SETUP.md for help")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("   🎯 TESTING SPOTIFY CONTROLS")
    print("="*60)
    
    while True:
        print("\n" + "-"*60)
        print("What would you like to do?\n")
        print("  1. Show current track")
        print("  2. Play/Resume")
        print("  3. Pause")
        print("  4. Next track")
        print("  5. Previous track")
        print("  6. Set volume")
        print("  7. Search for a song")
        print("  8. Show my playlists")
        print("  9. Exit")
        print("-"*60)
        
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == '1':
            print("\n" + spotify.get_current_track())
        
        elif choice == '2':
            print("\n" + spotify.play())
        
        elif choice == '3':
            print("\n" + spotify.pause())
        
        elif choice == '4':
            print("\n" + spotify.next_track())
        
        elif choice == '5':
            print("\n" + spotify.previous_track())
        
        elif choice == '6':
            volume = input("Enter volume (0-100): ").strip()
            try:
                print("\n" + spotify.set_volume(int(volume)))
            except:
                print("Invalid volume number")
        
        elif choice == '7':
            query = input("Enter song or artist name: ").strip()
            print("\n" + spotify.search(query))
        
        elif choice == '8':
            print("\n" + spotify.get_playlists())
        
        elif choice == '9':
            print("\n👋 Goodbye! Enjoy your music! 🎵\n")
            break
        
        else:
            print("\n❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nFor help, see: SPOTIFY_LOCAL_SETUP.md")
