# 🎵 Spotify Setup with https://open.spotify.com/ Redirect URI

## ✅ What's Already Done:

1. ✅ Your Spotify credentials are saved in Replit Secrets
2. ✅ Your redirect URI is set to `https://open.spotify.com/`
3. ✅ Code is updated to use your redirect URI

---

## 🚀 How to Use on Your Local Computer:

### Step 1: Download Project
Download this entire project to your computer

### Step 2: Install Python Packages
```bash
pip install requests python-dotenv
```

### Step 3: Create .env File
Create a file named `.env` in your project folder:

```env
SPOTIFY_CLIENT_ID=b4b253f00f1b40e18a2f430975abaa53
SPOTIFY_CLIENT_SECRET=your_secret_here
SPOTIFY_REDIRECT_URI=https://open.spotify.com/
```

**Note:** Replace `your_secret_here` with your actual Spotify Client Secret

### Step 4: Run the Controller
```bash
python run_spotify.py
```

---

## 🎯 How Authentication Works:

1. **Script opens your browser** → Takes you to Spotify authorization page
2. **You click "Agree"** → Spotify redirects you to `https://open.spotify.com/`
3. **Copy the URL from browser** → It will look like:
   ```
   https://open.spotify.com/?code=AQD8x7y...very_long_code_here
   ```
4. **Paste the URL** → The script extracts the authorization code
5. **You're authenticated!** → Now you can control Spotify

---

## 📝 Example Session:

```
🎵 Spotify Authentication
============================================================
1. Opening browser for Spotify authorization...

2. After you authorize, Spotify will redirect you to:
   https://open.spotify.com/

3. Look at the URL in your browser address bar
   It should have '?code=' somewhere in it

4. Copy the FULL URL from your browser

Paste the full URL here: https://open.spotify.com/?code=AQD8x7y...

✅ Successfully authenticated with Spotify!
   You can now control your music!
```

---

## 🎮 Available Commands:

Once authenticated, you can:

```python
from spotify_local import SpotifyLocal

spotify = SpotifyLocal()
spotify.authenticate()  # One-time authentication

# Control your music
spotify.play()              # ▶️ Resume playback
spotify.pause()             # ⏸️ Pause
spotify.next_track()        # ⏭️ Next song
spotify.previous_track()    # ⏮️ Previous song
spotify.set_volume(50)      # 🔊 Set volume to 50%
spotify.get_current_track() # 🎵 What's playing?
spotify.search('Bohemian Rhapsody')  # 🔍 Search
spotify.get_playlists()     # 📚 Show playlists
```

---

## ⚠️ Important Notes:

1. **Spotify must be running** on at least one device:
   - Desktop app (Windows/Mac/Linux)
   - Web player (https://open.spotify.com)
   - Mobile app (on same account)

2. **Start playing music first** before using the API controls

3. **The URL you paste** must include the `?code=` parameter

---

## 🐛 Troubleshooting:

### "No authorization code found in URL"
- Make sure you copy the **complete URL** from the browser address bar
- It should contain `?code=` in it

### "No active device"
- Open Spotify and start playing any song
- Then try the command again

### "Authentication failed"
- Double-check your Client ID and Secret in `.env`
- Make sure redirect URI in Spotify Dashboard is exactly: `https://open.spotify.com/`

---

## ✅ You're All Set!

Your Spotify integration is ready to use with `https://open.spotify.com/` redirect URI!

Run `python run_spotify.py` to get started! 🎵
