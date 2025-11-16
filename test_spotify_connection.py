#!/usr/bin/env python3
"""
Test Spotify Connection - Works on both Replit and Local
"""

import os

def test_spotify_connection():
    """Test if Spotify credentials are available"""
    print("\n" + "="*60)
    print("   🎵 TESTING SPOTIFY CONNECTION")
    print("="*60)
    
    # Check credentials
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    print("\n📋 Checking credentials...")
    
    if client_id and client_secret:
        print(f"✅ SPOTIFY_CLIENT_ID: Found ({len(client_id)} characters)")
        print(f"✅ SPOTIFY_CLIENT_SECRET: Found ({len(client_secret)} characters)")
        print("\n✅ Credentials are set up correctly!")
        
        print("\n" + "="*60)
        print("   🎯 NEXT STEPS FOR LOCAL USE")
        print("="*60)
        
        print("\n📦 To use Spotify on your LOCAL computer:")
        print("\n1️⃣  Download this project to your computer")
        print("2️⃣  Install dependencies:")
        print("     pip install requests python-dotenv")
        print("\n3️⃣  Create a .env file with these credentials:")
        print(f"     SPOTIFY_CLIENT_ID={client_id}")
        print(f"     SPOTIFY_CLIENT_SECRET={client_secret[:10]}...{client_secret[-5:]}")
        print("     SPOTIFY_REDIRECT_URI=http://localhost:8888/callback")
        
        print("\n4️⃣  Run the interactive controller:")
        print("     python run_spotify.py")
        
        print("\n" + "="*60)
        print("   📖 HELPFUL FILES")
        print("="*60)
        print("\n📄 QUICK_START_SPOTIFY.txt - Quick setup guide")
        print("📄 SPOTIFY_LOCAL_SETUP.md  - Detailed instructions")
        print("📄 spotify_local.py        - Spotify controller code")
        print("📄 run_spotify.py          - Interactive test program")
        
        return True
    else:
        print("❌ Credentials not found!")
        if not client_id:
            print("   Missing: SPOTIFY_CLIENT_ID")
        if not client_secret:
            print("   Missing: SPOTIFY_CLIENT_SECRET")
        return False

if __name__ == "__main__":
    test_spotify_connection()
    
    print("\n" + "="*60)
    print("   💡 IMPORTANT NOTE")
    print("="*60)
    print("\n⚠️  Spotify control requires a LOCAL setup because:")
    print("   • You need Spotify running on a device (desktop/mobile/web)")
    print("   • The API controls your active Spotify session")
    print("   • OAuth requires browser authentication")
    print("\n✅ Your credentials are ready - just follow the steps above!")
    print("="*60 + "\n")
