#!/usr/bin/env python3
"""Quick test - just shows if credentials are set"""
import os

print("\n🔍 Checking Spotify Setup...")
print("=" * 50)

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

if client_id and client_secret:
    print("✅ SPOTIFY_CLIENT_ID: Set")
    print("✅ SPOTIFY_CLIENT_SECRET: Set")
    print("✅ Redirect URI: https://open.spotify.com/")
    print("\n✅ All credentials ready!")
    print("\n📖 Next steps:")
    print("   1. Download project to your computer")
    print("   2. Run: pip install requests python-dotenv")
    print("   3. Create .env file (see SPOTIFY_SETUP_WITH_OPEN_URI.md)")
    print("   4. Run: python run_spotify.py")
else:
    print("❌ Credentials not found")
    
print("=" * 50)
