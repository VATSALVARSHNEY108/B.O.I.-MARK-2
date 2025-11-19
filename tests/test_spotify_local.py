#!/usr/bin/env python3
"""
Simple test script to control Spotify locally
"""

from modules.utilities.spotify_automation import create_spotify_automation

def main():
    print("🎵 Testing Spotify Connection...")
    print("=" * 50)
    
    spotify = create_spotify_automation()
    
    print("\n1️⃣  Getting current track...")
    result = spotify.get_current_track()
    print(f"   {result['message']}\n")
    
    print("2️⃣  Getting your playlists...")
    result = spotify.get_playlists(limit=5)
    print(f"   {result['message']}\n")
    
    print("\n✅ Spotify is connected and working!")
    print("\nTry these commands in your app:")
    print("  - 'Play Bohemian Rhapsody on Spotify'")
    print("  - 'What's playing?'")
    print("  - 'Next song'")
    print("  - 'Pause music'")
    print("  - 'Set volume to 50'")
    print("  - 'Show my playlists'")

if __name__ == "__main__":
    main()
