# 🎵 Step-by-Step: Connect Spotify Locally

Follow these steps to get Spotify working on your local computer.

## Prerequisites

Before you start, make sure you have:
- ✅ Python 3.11 or newer installed
- ✅ Spotify account (free or premium)
- ✅ Spotify app installed on your computer OR access to Spotify Web Player

---

## Step 1: Download This Project to Your Computer

### Option A: Download as ZIP
1. On Replit, click the **three dots menu** (⋮) at the top
2. Select **"Download as ZIP"**
3. Extract the ZIP file to a folder on your computer
4. Open Terminal/Command Prompt and navigate to that folder:
   ```bash
   cd path/to/your/project
   ```

### Option B: Using Git (if you have it)
```bash
git clone <your-replit-url>
cd your-project-folder
```

---

## Step 2: Install Python Dependencies

Open Terminal/Command Prompt in your project folder and run:

```bash
# Install all required packages
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, install manually:
```bash
pip install requests python-dotenv google-generativeai flask flask-cors streamlit
```

---

## Step 3: Get Your Spotify API Credentials

Since you're running locally, you need to create a Spotify App to get API access:

### 3.1 Create Spotify Developer App

1. Go to: **https://developer.spotify.com/dashboard**
2. Log in with your Spotify account
3. Click **"Create App"**
4. Fill in the details:
   - **App name**: "My Local Music Controller" (or any name)
   - **App description**: "Local Spotify automation"
   - **Redirect URI**: `http://localhost:8888/callback`
   - Check the Terms of Service box
5. Click **"Save"**

### 3.2 Get Your Credentials

1. Click on your new app
2. Click **"Settings"** button
3. You'll see:
   - **Client ID** (copy this)
   - **Client Secret** (click "View client secret" and copy)

---

## Step 4: Set Up Environment Variables

Create a file named `.env` in your project folder:

```bash
# On Windows, use Notepad:
notepad .env

# On Mac/Linux, use nano or any text editor:
nano .env
```

Add these lines to the `.env` file:

```env
# Spotify Credentials
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback

# Gemini API (if you're using AI features)
GEMINI_API_KEY=your_gemini_key_here
```

**Replace** `your_client_id_here` and `your_client_secret_here` with the credentials from Step 3.2

Save the file and close it.

---

## Step 5: Update the Spotify Code for Local Use

The current code uses Replit's connector. For local use, we need to modify it slightly.

I've created a local version for you. Create a new file called `spotify_local.py`:

```python
import os
import requests
from dotenv import load_dotenv
import webbrowser
from urllib.parse import urlencode

load_dotenv()

class SpotifyLocal:
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:8888/callback')
        self.access_token = None
        self.base_url = "https://api.spotify.com/v1/"
        
    def authenticate(self):
        """Authenticate with Spotify (one-time setup)"""
        # This will open browser for authorization
        scope = 'user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-private'
        
        auth_url = f'https://accounts.spotify.com/authorize?{urlencode({
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": scope
        })}'
        
        print("Opening browser for Spotify authorization...")
        webbrowser.open(auth_url)
        print(f"\nAfter authorizing, you'll be redirected to: {self.redirect_uri}")
        print("Copy the FULL URL from your browser and paste it here:")
        
        callback_url = input("Paste the full URL: ")
        
        # Extract code from URL
        code = callback_url.split('code=')[1].split('&')[0] if 'code=' in callback_url else None
        
        if code:
            # Exchange code for access token
            token_url = 'https://accounts.spotify.com/api/token'
            data = {
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': self.redirect_uri,
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
            
            response = requests.post(token_url, data=data)
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data['access_token']
                print("✅ Successfully authenticated!")
                return True
        
        print("❌ Authentication failed")
        return False
    
    def _make_request(self, endpoint, method='GET', data=None):
        """Make authenticated request to Spotify API"""
        if not self.access_token:
            return {"success": False, "message": "Not authenticated. Run authenticate() first."}
        
        url = self.base_url + endpoint
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, headers=headers, json=data)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data)
            
            if response.status_code in [200, 201, 204]:
                return {"success": True, "data": response.json() if response.text else {}}
            elif response.status_code == 404:
                return {"success": False, "message": "No active device. Open Spotify on any device."}
            else:
                return {"success": False, "message": f"Error: {response.status_code}"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def play(self):
        """Resume playback"""
        result = self._make_request('me/player/play', 'PUT')
        return "▶️ Playing" if result.get('success') else result.get('message')
    
    def pause(self):
        """Pause playback"""
        result = self._make_request('me/player/pause', 'PUT')
        return "⏸️ Paused" if result.get('success') else result.get('message')
    
    def next_track(self):
        """Next track"""
        result = self._make_request('me/player/next', 'POST')
        return "⏭️ Next track" if result.get('success') else result.get('message')
    
    def previous_track(self):
        """Previous track"""
        result = self._make_request('me/player/previous', 'POST')
        return "⏮️ Previous track" if result.get('success') else result.get('message')
    
    def get_current_track(self):
        """Get current track info"""
        result = self._make_request('me/player/currently-playing')
        if result.get('success'):
            data = result.get('data', {})
            if data and data.get('item'):
                item = data['item']
                artists = ', '.join([a['name'] for a in item.get('artists', [])])
                return f"🎵 {item['name']} by {artists}"
        return result.get('message', 'Nothing playing')

# Example usage
if __name__ == "__main__":
    spotify = SpotifyLocal()
    
    # First time: authenticate
    if spotify.authenticate():
        # Now you can control Spotify!
        print("\n" + spotify.get_current_track())
        
        # Try commands:
        # print(spotify.play())
        # print(spotify.pause())
        # print(spotify.next_track())
```

---

## Step 6: Run the Local Setup

### 6.1 First Time: Authenticate

Open Terminal in your project folder and run:

```bash
python spotify_local.py
```

This will:
1. Open your browser for Spotify authorization
2. Ask you to copy the callback URL
3. Save your access token

### 6.2 Test Spotify Control

After authentication, you can test basic commands:

```python
# In the same terminal or create a new script
from spotify_local import SpotifyLocal

spotify = SpotifyLocal()
spotify.authenticate()  # One time only

# Control Spotify
print(spotify.get_current_track())
print(spotify.pause())
print(spotify.play())
print(spotify.next_track())
```

---

## Step 7: Integrate with Your Main App

To use Spotify in your main application (`gui_app.py` or `main.py`):

1. **Import the local Spotify module:**
   ```python
   from spotify_local import SpotifyLocal
   ```

2. **Initialize once:**
   ```python
   spotify = SpotifyLocal()
   spotify.authenticate()  # First time only
   ```

3. **Use in commands:**
   ```python
   # When user says "play music"
   spotify.play()
   
   # When user says "what's playing"
   spotify.get_current_track()
   ```

---

## Step 8: Make Sure Spotify is Running

For Spotify controls to work, you need Spotify running on at least one device:

- ✅ Spotify Desktop App (Windows/Mac/Linux)
- ✅ Spotify Web Player (https://open.spotify.com)
- ✅ Spotify Mobile App (on the same network)

The API will control whichever device is currently active.

---

## Quick Test Commands

Once everything is set up, try these:

```python
from spotify_local import SpotifyLocal

spotify = SpotifyLocal()
spotify.authenticate()

# Play/Pause
print(spotify.play())
print(spotify.pause())

# Navigate
print(spotify.next_track())
print(spotify.previous_track())

# Check what's playing
print(spotify.get_current_track())
```

---

## Troubleshooting

### "No module named 'requests'"
```bash
pip install requests python-dotenv
```

### "No active device found"
- Open Spotify Desktop App OR
- Open Spotify Web Player (https://open.spotify.com)
- Start playing any song

### "Invalid client credentials"
- Double-check your `.env` file
- Make sure Client ID and Secret are correct
- No extra spaces or quotes

### "Redirect URI mismatch"
- In Spotify Developer Dashboard, make sure redirect URI is exactly: `http://localhost:8888/callback`

---

## Summary

✅ **You're all set!** Here's what you did:

1. Downloaded project to your computer
2. Installed Python packages
3. Created Spotify Developer App
4. Set up `.env` file with credentials
5. Created local Spotify controller
6. Authenticated with Spotify
7. Can now control Spotify from your Python app!

## Next Steps

- Add more Spotify features (volume control, search, playlists)
- Integrate with your voice assistant
- Create custom playlists
- Build music automation workflows

**Enjoy controlling your music! 🎵**
