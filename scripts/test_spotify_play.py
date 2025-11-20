#!/usr/bin/env python3
"""
Test Spotify Song Playing
Quick test to play songs on Spotify
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.utilities.spotify_automation import SpotifyAutomation

def main():
    print("=" * 60)
    print("SPOTIFY SONG PLAYER TEST")
    print("=" * 60)
    
    spotify = SpotifyAutomation()
    
    print("\n📋 Available Commands:")
    print("  1. Play a specific song")
    print("  2. Search for songs")
    print("  3. Get current track")
    print("  4. Control playback")
    print("  5. Exit")
    print()
    
    while True:
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            song = input("Enter song name (e.g., 'Bohemian Rhapsody'): ").strip()
            if song:
                print(f"\n🔍 Searching for '{song}'...")
                result = spotify.play_song(song)
                print(f"\n{result.get('message', 'Done')}")
        
        elif choice == "2":
            query = input("Search for (song/artist/album): ").strip()
            if query:
                print(f"\n🔍 Searching Spotify...")
                result = spotify.search(query, 'track', limit=5)
                print(f"\n{result.get('message', 'Done')}")
        
        elif choice == "3":
            print(f"\n📻 Getting current track...")
            result = spotify.get_current_track()
            print(f"\n{result.get('message', 'No track playing')}")
        
        elif choice == "4":
            print("\nPlayback Controls:")
            print("  a. Play/Resume")
            print("  b. Pause")
            print("  c. Next track")
            print("  d. Previous track")
            control = input("Select (a-d): ").strip().lower()
            
            if control == "a":
                result = spotify.play()
            elif control == "b":
                result = spotify.pause()
            elif control == "c":
                result = spotify.next_track()
            elif control == "d":
                result = spotify.previous_track()
            else:
                result = {"message": "Invalid option"}
            
            print(f"\n{result.get('message', 'Done')}")
        
        elif choice == "5":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option. Please select 1-5")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
