"""
Spotify Automation Module
Provides Spotify control and automation features
"""

import os
import json
import requests


class SpotifyAutomation:
    """Handles Spotify playback and playlist control"""
    
    def __init__(self):
        self.connection_settings = None
        self.hostname = os.environ.get('REPLIT_CONNECTORS_HOSTNAME')
        
    def _get_access_token(self):
        """Get fresh access token from Replit connector"""
        try:
            # Check if token is still valid
            if (self.connection_settings and 
                self.connection_settings.get('settings', {}).get('expires_at')):
                from datetime import datetime
                expires_at = datetime.fromisoformat(
                    self.connection_settings['settings']['expires_at'].replace('Z', '+00:00')
                )
                if datetime.now(expires_at.tzinfo) < expires_at:
                    return self.connection_settings['settings']['access_token']
            
            # Get X_REPLIT_TOKEN
            x_replit_token = None
            repl_identity = os.environ.get('REPL_IDENTITY')
            web_repl_renewal = os.environ.get('WEB_REPL_RENEWAL')
            
            if repl_identity:
                x_replit_token = 'repl ' + repl_identity
            elif web_repl_renewal:
                x_replit_token = 'depl ' + web_repl_renewal
            
            if not x_replit_token:
                return None
            
            # Fetch connection settings
            url = f'https://{self.hostname}/api/v2/connection?include_secrets=true&connector_names=spotify'
            headers = {
                'Accept': 'application/json',
                'X_REPLIT_TOKEN': x_replit_token
            }
            
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])
                if items:
                    self.connection_settings = items[0]
                    return self.connection_settings['settings']['access_token']
            
            return None
            
        except Exception as e:
            print(f"Error getting access token: {e}")
            return None
    
    def _make_spotify_request(self, endpoint, method='GET', data=None):
        """Make authenticated request to Spotify API"""
        token = self._get_access_token()
        if not token:
            return {
                "success": False,
                "message": "Failed to get Spotify access token. Please reconnect Spotify."
            }
        
        url = f'https://api.spotify.com/v1/{endpoint}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = None
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data)
            elif method == 'PUT':
                response = requests.put(url, headers=headers, json=data)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)
            
            if response is not None and response.status_code in [200, 201, 204]:
                if response.text:
                    return {"success": True, "data": response.json()}
                return {"success": True, "data": {}}
            else:
                if response is not None:
                    error_msg = response.text
                    try:
                        error_data = response.json()
                        error_msg = error_data.get('error', {}).get('message', error_msg)
                    except:
                        pass
                    return {
                        "success": False,
                        "message": f"Spotify API error: {error_msg}"
                    }
                else:
                    return {
                        "success": False,
                        "message": "Failed to make Spotify API request"
                    }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Request failed: {str(e)}"
            }
    
    def play(self, uri=None):
        """Play current track or specific URI (track/playlist/album)"""
        data = {}
        if uri:
            if uri.startswith('spotify:'):
                data = {"context_uri": uri}
            else:
                data = {"uris": [uri]}
        
        result = self._make_spotify_request('me/player/play', 'PUT', data)
        if result.get('success'):
            if uri:
                return {"success": True, "message": f"🎵 Playing Spotify content"}
            return {"success": True, "message": "▶️ Resumed playback"}
        return result
    
    def pause(self):
        """Pause playback"""
        result = self._make_spotify_request('me/player/pause', 'PUT')
        if result.get('success'):
            return {"success": True, "message": "⏸️ Paused playback"}
        return result
    
    def next_track(self):
        """Skip to next track"""
        result = self._make_spotify_request('me/player/next', 'POST')
        if result.get('success'):
            return {"success": True, "message": "⏭️ Skipped to next track"}
        return result
    
    def previous_track(self):
        """Go to previous track"""
        result = self._make_spotify_request('me/player/previous', 'POST')
        if result.get('success'):
            return {"success": True, "message": "⏮️ Previous track"}
        return result
    
    def set_volume(self, volume_percent):
        """Set volume (0-100)"""
        volume = max(0, min(100, int(volume_percent)))
        result = self._make_spotify_request(f'me/player/volume?volume_percent={volume}', 'PUT')
        if result.get('success'):
            return {"success": True, "message": f"🔊 Volume set to {volume}%"}
        return result
    
    def get_current_track(self):
        """Get currently playing track info"""
        result = self._make_spotify_request('me/player/currently-playing')
        if result.get('success'):
            data = result.get('data', {})
            if not data or not data.get('item'):
                return {"success": True, "message": "No track currently playing"}
            
            item = data['item']
            artists = ', '.join([artist['name'] for artist in item.get('artists', [])])
            track_name = item.get('name', 'Unknown')
            album = item.get('album', {}).get('name', 'Unknown')
            is_playing = data.get('is_playing', False)
            
            status = "▶️ Playing" if is_playing else "⏸️ Paused"
            message = f"{status}: {track_name} by {artists}\nAlbum: {album}"
            
            return {
                "success": True,
                "message": message,
                "track_info": {
                    "name": track_name,
                    "artists": artists,
                    "album": album,
                    "is_playing": is_playing,
                    "uri": item.get('uri')
                }
            }
        return result
    
    def search(self, query, search_type='track', limit=5):
        """Search Spotify (track/artist/album/playlist)"""
        from urllib.parse import quote
        encoded_query = quote(query)
        endpoint = f'search?q={encoded_query}&type={search_type}&limit={limit}'
        
        result = self._make_spotify_request(endpoint)
        if result.get('success'):
            data = result.get('data', {})
            items = data.get(f'{search_type}s', {}).get('items', [])
            
            if not items:
                return {"success": True, "message": f"No {search_type}s found for '{query}'"}
            
            results_list = []
            for item in items:
                if search_type == 'track':
                    artists = ', '.join([a['name'] for a in item.get('artists', [])])
                    results_list.append({
                        "name": item['name'],
                        "artists": artists,
                        "uri": item['uri'],
                        "display": f"{item['name']} - {artists}"
                    })
                elif search_type == 'artist':
                    results_list.append({
                        "name": item['name'],
                        "uri": item['uri'],
                        "display": item['name']
                    })
                elif search_type == 'playlist':
                    results_list.append({
                        "name": item['name'],
                        "owner": item.get('owner', {}).get('display_name', 'Unknown'),
                        "uri": item['uri'],
                        "display": f"{item['name']} (by {item.get('owner', {}).get('display_name', 'Unknown')})"
                    })
                elif search_type == 'album':
                    artists = ', '.join([a['name'] for a in item.get('artists', [])])
                    results_list.append({
                        "name": item['name'],
                        "artists": artists,
                        "uri": item['uri'],
                        "display": f"{item['name']} - {artists}"
                    })
            
            message = f"🔍 Found {len(results_list)} {search_type}(s):\n"
            for i, item in enumerate(results_list, 1):
                message += f"  {i}. {item['display']}\n"
            
            return {
                "success": True,
                "message": message.strip(),
                "results": results_list
            }
        return result
    
    def play_track(self, query):
        """Search and play first matching track"""
        search_result = self.search(query, 'track', 1)
        if search_result.get('success') and search_result.get('results'):
            track = search_result['results'][0]
            play_result = self.play(track['uri'])
            if play_result.get('success'):
                return {
                    "success": True,
                    "message": f"🎵 Playing: {track['display']}"
                }
            return play_result
        return {"success": False, "message": f"Track '{query}' not found"}
    
    def get_playlists(self, limit=20):
        """Get user's playlists"""
        result = self._make_spotify_request(f'me/playlists?limit={limit}')
        if result.get('success'):
            data = result.get('data', {})
            items = data.get('items', [])
            
            if not items:
                return {"success": True, "message": "No playlists found"}
            
            playlists = []
            message = f"📚 Your playlists ({len(items)}):\n"
            for i, item in enumerate(items, 1):
                playlists.append({
                    "name": item['name'],
                    "tracks": item.get('tracks', {}).get('total', 0),
                    "uri": item['uri']
                })
                message += f"  {i}. {item['name']} ({item.get('tracks', {}).get('total', 0)} tracks)\n"
            
            return {
                "success": True,
                "message": message.strip(),
                "playlists": playlists
            }
        return result
    
    def shuffle(self, state=True):
        """Toggle shuffle on/off"""
        state_str = 'true' if state else 'false'
        result = self._make_spotify_request(f'me/player/shuffle?state={state_str}', 'PUT')
        if result.get('success'):
            status = "on" if state else "off"
            return {"success": True, "message": f"🔀 Shuffle {status}"}
        return result
    
    def repeat(self, state='context'):
        """Set repeat mode: track, context (playlist/album), or off"""
        result = self._make_spotify_request(f'me/player/repeat?state={state}', 'PUT')
        if result.get('success'):
            modes = {'track': 'one track', 'context': 'playlist/album', 'off': 'off'}
            return {"success": True, "message": f"🔁 Repeat {modes.get(state, state)}"}
        return result


def create_spotify_automation():
    """Factory function to create SpotifyAutomation instance"""
    return SpotifyAutomation()
