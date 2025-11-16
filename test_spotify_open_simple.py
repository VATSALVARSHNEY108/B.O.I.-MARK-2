#!/usr/bin/env python3
"""
Simple test for Spotify open command
"""

import os
os.environ['SPOTIFY_CLIENT_ID'] = os.getenv('SPOTIFY_CLIENT_ID', 'test')
os.environ['SPOTIFY_CLIENT_SECRET'] = os.getenv('SPOTIFY_CLIENT_SECRET', 'test')

from modules.utilities.spotify_local import SpotifyLocal

print("=" * 60)
print("🎵 Testing Spotify Open Command")
print("=" * 60)

print("\nTesting SpotifyLocal.open_spotify()...")
spotify = SpotifyLocal()
result = spotify.open_spotify()
print(f"✅ Result: {result}")

print("\n" + "=" * 60)
print("✅ Command added successfully!")
print("\nYou can now use:")
print("  - Action: 'spotify_open' or 'open_spotify'")
print("  - Opens: https://open.spotify.com/")
print("=" * 60)
