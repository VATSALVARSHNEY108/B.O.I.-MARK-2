#!/usr/bin/env python3
"""
Diagnostic script to test Spotify connection and search
"""

from spotify_automation import create_spotify_automation
import json

def test_connection():
    """Test Spotify connection and search functionality"""
    
    print("=" * 70)
    print("🔍 SPOTIFY CONNECTION DIAGNOSTIC")
    print("=" * 70)
    print()
    
    # Create Spotify instance
    print("1. Creating Spotify automation instance...")
    spotify = create_spotify_automation()
    print("   ✅ Instance created")
    print()
    
    # Test token retrieval
    print("2. Testing access token retrieval...")
    token = spotify._get_access_token()
    if token:
        print(f"   ✅ Access token retrieved (length: {len(token)})")
    else:
        print("   ❌ Failed to get access token")
        print("   This might mean:")
        print("   - Spotify integration is not set up")
        print("   - Token has expired")
        print("   - Connection environment variables are missing")
        return
    print()
    
    # Test current playback
    print("3. Testing current playback info...")
    current = spotify.get_current_track()
    print(f"   Result: {current}")
    print()
    
    # Test search with detailed output
    print("4. Testing search for 'Shape of You'...")
    search_result = spotify.search("Shape of You", "track", 5)
    
    if search_result.get('success'):
        results = search_result.get('results', [])
        print(f"   ✅ Search succeeded!")
        print(f"   Found {len(results)} results")
        if results:
            print("\n   Results:")
            for i, track in enumerate(results, 1):
                print(f"      {i}. {track['display']}")
                print(f"         URI: {track['uri']}")
        else:
            print("   ⚠️  No tracks found (API call succeeded but returned empty results)")
    else:
        print(f"   ❌ Search failed!")
        print(f"   Error: {search_result.get('message')}")
    print()
    
    # Test getting playlists
    print("5. Testing playlists retrieval...")
    playlists_result = spotify.get_playlists(5)
    print(f"   Result: {playlists_result.get('message', 'No message')[:100]}...")
    print()
    
    print("=" * 70)
    print("Diagnostic complete!")
    print("=" * 70)

if __name__ == "__main__":
    test_connection()
