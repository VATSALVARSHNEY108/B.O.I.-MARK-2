"""
Simple Spotify Controller for Local Use
Works with https://open.spotify.com/ redirect URI
"""

import os
import requests
import webbrowser
from urllib.parse import urlencode

class SpotifyLocal:
    """Control Spotify on your local computer"""
    
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI', 'https://open.spotify.com/')
        self.access_token = None
        self.base_url = "https://api.spotify.com/v1/"
        
        if not self.client_id or not self.client_secret:
            print("⚠️  Warning: SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET not found in environment")
            print("   Make sure your credentials are set in Replit Secrets or .env file")
    
    def authenticate(self):
        """Authenticate with Spotify"""
        scope = 'user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-private user-library-read'
        
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": scope
        }
        auth_url = f'https://accounts.spotify.com/authorize?{urlencode(params)}'
        
        print("\n🎵 Spotify Authentication")
        print("=" * 60)
        print("1. Opening browser for Spotify authorization...")
        webbrowser.open(auth_url)
        
        print(f"\n2. After you authorize, Spotify will redirect you to:")
        print(f"   {self.redirect_uri}")
        print("\n3. Look at the URL in your browser address bar")
        print("   It should have '?code=' somewhere in it")
        print("\n4. Copy the FULL URL from your browser")
        
        callback_url = input("\nPaste the full URL here: ").strip()
        
        if 'code=' not in callback_url:
            print("❌ No authorization code found in URL")
            print("   Make sure you copied the complete URL from the address bar")
            return False
        
        try:
            code = callback_url.split('code=')[1].split('&')[0]
        except:
            print("❌ Could not extract code from URL")
            return False
        
        token_url = 'https://accounts.spotify.com/api/token'
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        try:
            response = requests.post(token_url, data=data)
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data['access_token']
                print("\n✅ Successfully authenticated with Spotify!")
                print("   You can now control your music!\n")
                return True
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error during authentication: {e}")
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
                try:
                    return {"success": True, "data": response.json() if response.text else {}}
                except:
                    return {"success": True, "data": {}}
            elif response.status_code == 404:
                return {"success": False, "message": "No active device. Open Spotify on any device and start playing."}
            else:
                error_msg = f"API Error {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', {}).get('message', error_msg)
                except:
                    pass
                return {"success": False, "message": error_msg}
        except Exception as e:
            return {"success": False, "message": f"Request failed: {str(e)}"}
    
    def play(self, uri=None):
        """Resume playback or play specific track/playlist"""
        data = {"uris": [uri]} if uri else None
        result = self._make_request('me/player/play', 'PUT', data)
        if result.get('success'):
            return "▶️ Playing music"
        return result.get('message')
    
    def pause(self):
        """Pause playback"""
        result = self._make_request('me/player/pause', 'PUT')
        if result.get('success'):
            return "⏸️ Paused"
        return result.get('message')
    
    def next_track(self):
        """Skip to next track"""
        result = self._make_request('me/player/next', 'POST')
        if result.get('success'):
            return "⏭️ Next track"
        return result.get('message')
    
    def previous_track(self):
        """Go to previous track"""
        result = self._make_request('me/player/previous', 'POST')
        if result.get('success'):
            return "⏮️ Previous track"
        return result.get('message')
    
    def set_volume(self, volume_percent):
        """Set volume (0-100)"""
        volume = max(0, min(100, int(volume_percent)))
        result = self._make_request(f'me/player/volume?volume_percent={volume}', 'PUT')
        if result.get('success'):
            return f"🔊 Volume set to {volume}%"
        return result.get('message')
    
    def get_current_track(self):
        """Get currently playing track info"""
        result = self._make_request('me/player/currently-playing')
        if result.get('success'):
            data = result.get('data', {})
            if data and data.get('item'):
                item = data['item']
                artists = ', '.join([a['name'] for a in item.get('artists', [])])
                track_name = item['name']
                album = item.get('album', {}).get('name', 'Unknown')
                is_playing = data.get('is_playing', False)
                status = "▶️ Playing" if is_playing else "⏸️ Paused"
                return f"{status}: {track_name} by {artists}\nAlbum: {album}"
            return "Nothing currently playing"
        return result.get('message', 'Could not get current track')
    
    def search(self, query, search_type='track', limit=5):
        """Search Spotify for tracks, artists, albums, or playlists"""
        from urllib.parse import quote
        encoded_query = quote(query)
        endpoint = f'search?q={encoded_query}&type={search_type}&limit={limit}'
        
        result = self._make_request(endpoint)
        if result.get('success'):
            data = result.get('data', {})
            items = data.get(f'{search_type}s', {}).get('items', [])
            
            if not items:
                return f"No {search_type}s found for '{query}'"
            
            results = []
            for i, item in enumerate(items, 1):
                if search_type == 'track':
                    artists = ', '.join([a['name'] for a in item.get('artists', [])])
                    results.append(f"{i}. {item['name']} - {artists}")
                elif search_type == 'artist':
                    results.append(f"{i}. {item['name']}")
                elif search_type == 'playlist':
                    owner = item.get('owner', {}).get('display_name', 'Unknown')
                    results.append(f"{i}. {item['name']} (by {owner})")
            
            return f"🔍 Found {len(items)} {search_type}(s):\n" + "\n".join(results)
        return result.get('message', 'Search failed')
    
    def get_playlists(self, limit=10):
        """Get user's playlists"""
        result = self._make_request(f'me/playlists?limit={limit}')
        if result.get('success'):
            data = result.get('data', {})
            items = data.get('items', [])
            
            if not items:
                return "No playlists found"
            
            playlists = []
            for i, item in enumerate(items, 1):
                tracks = item.get('tracks', {}).get('total', 0)
                playlists.append(f"{i}. {item['name']} ({tracks} tracks)")
            
            return f"📚 Your playlists:\n" + "\n".join(playlists)
        return result.get('message', 'Could not get playlists')
    
    def open_spotify(self):
        """Open Spotify web player"""
        try:
            webbrowser.open('https://open.spotify.com/')
            return "🎵 Opening Spotify web player..."
        except Exception as e:
            return f"❌ Could not open Spotify: {str(e)}"


def main():
    """Example usage"""
    print("\n🎵 Spotify Local Controller")
    print("=" * 60)
    print("Using redirect URI: https://open.spotify.com/")
    print("=" * 60)
    
    spotify = SpotifyLocal()
    
    if not spotify.client_id:
        print("\n❌ Credentials not found!")
        print("\nMake sure SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET")
        print("are set in your environment (Replit Secrets or .env file)")
        return
    
    if spotify.authenticate():
        print("\n🎯 Testing Spotify Controls...")
        print("-" * 60)
        
        print("\n1. Current track:")
        print("  ", spotify.get_current_track())
        
        print("\n2. Your playlists:")
        print("  ", spotify.get_playlists(5))
        
        print("\n✅ Spotify is working!")
        print("\nYou can now use these commands:")
        print("  spotify.play()              # Resume playback")
        print("  spotify.pause()             # Pause")
        print("  spotify.next_track()        # Next song")
        print("  spotify.previous_track()    # Previous song")
        print("  spotify.set_volume(50)      # Set volume")
        print("  spotify.get_current_track() # What's playing")
        print("  spotify.search('song')      # Search")
        print("  spotify.get_playlists()     # Your playlists")


if __name__ == "__main__":
    main()
