#!/usr/bin/env python3
"""
Interactive Spotify Controller
Works with https://open.spotify.com/ redirect URI
"""

import os
import sys

def check_setup():
    """Check if everything is set up correctly"""
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("\n❌ Credentials not found!")
        print("\nMake sure you have:")
        print("  • SPOTIFY_CLIENT_ID set in environment")
        print("  • SPOTIFY_CLIENT_SECRET set in environment")
        print("\nOn Replit: Use Secrets panel")
        print("On Local: Create .env file with these values")
        return False
    
    try:
        import requests
    except ImportError:
        print("\n❌ Missing 'requests' package!")
        print("\nInstall it with: pip install requests")
        return False
    
    return True

def main():
    """Main interactive menu"""
    print("\n" + "="*60)
    print("   🎵 SPOTIFY INTERACTIVE CONTROLLER")
    print("="*60)
    print("Using redirect URI: https://open.spotify.com/")
    print("="*60)
    
    if not check_setup():
        sys.exit(1)
    
    from modules.utilities.spotify_local import SpotifyLocal
    
    spotify = SpotifyLocal()
    
    print("\n📱 Starting Spotify authentication...")
    print("   Your browser will open for authorization\n")
    
    if not spotify.authenticate():
        print("\n❌ Authentication failed!")
        print("   Please try again")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("   🎯 SPOTIFY CONTROLS ACTIVE")
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
                print("❌ Invalid volume number")
        
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
