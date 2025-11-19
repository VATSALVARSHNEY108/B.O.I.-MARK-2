#!/usr/bin/env python3
"""
Quick test to verify Spotify open command works
"""

from modules.utilities.spotify_local import SpotifyLocal
from modules.core.command_executor import CommandExecutor

print("=" * 60)
print("🎵 Testing Spotify Open Command")
print("=" * 60)

print("\n1️⃣  Testing SpotifyLocal.open_spotify() directly...")
spotify = SpotifyLocal()
result = spotify.open_spotify()
print(f"   Result: {result}")

print("\n2️⃣  Testing via CommandExecutor...")
executor = CommandExecutor()
result = executor.execute_command({
    "action": "spotify_open"
})
print(f"   Result: {result}")

print("\n✅ Test complete!")
print("   Spotify web player should open in your browser at:")
print("   https://open.spotify.com/")
print("=" * 60)
