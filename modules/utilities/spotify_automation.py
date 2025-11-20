"""
Spotify Automation using Replit Connector
Controls Spotify via Web API with OAuth handled by Replit
"""

import os
import requests
import json


class SpotifyAutomation:
    """Control Spotify using Web API with Replit connector authentication"""
    
    def __init__(self):
        self.base_url = "https://api.spotify.com/v1/"
        self.connector_hostname = os.getenv('REPLIT_CONNECTORS_HOSTNAME')
        
    def _get_access_token(self):
        """Get access token from Replit connector"""
        try:
            x_replit_token = None
            repl_identity = os.getenv('REPL_IDENTITY')
            web_repl_renewal = os.getenv('WEB_REPL_RENEWAL')
            
            if repl_identity:
                x_replit_token = 'repl ' + repl_identity
            elif web_repl_renewal:
                x_replit_token = 'depl ' + web_repl_renewal
            
            if not x_replit_token or not self.connector_hostname:
                return None
            
            url = f"https://{self.connector_hostname}/api/v2/connection?include_secrets=true&connector_names=spotify"
            headers = {
                'Accept': 'application/json',
                'X_REPLIT_TOKEN': x_replit_token
            }
            
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])
                if items:
                    connection = items[0]
                    access_token = connection.get('settings', {}).get('access_token')
                    if not access_token:
                        oauth_creds = connection.get('settings', {}).get('oauth', {}).get('credentials', {})
                        access_token = oauth_creds.get('access_token')
                    return access_token
            return None
        except Exception as e:
            print(f"Error getting access token: {e}")
            return None
    
    def _make_spotify_request(self, endpoint, method='GET', data=None):
        """Make authenticated request to Spotify API"""
        try:
            access_token = self._get_access_token()
            if not access_token:
                return {"success": False, "message": "Failed to get Spotify access token. Make sure Spotify is connected."}
            
            url = self.base_url + endpoint
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data)
            elif method == 'PUT':
                response = requests.put(url, headers=headers, json=data)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)
            else:
                return {"success": False, "message": f"Unsupported HTTP method: {method}"}
            
            if response.status_code in [200, 201, 204]:
                if response.status_code == 204:
                    return {"success": True, "data": {}}
                try:
                    return {"success": True, "data": response.json()}
                except:
                    return {"success": True, "data": {}}
            elif response.status_code == 404:
                return {"success": False, "message": "No active Spotify device found. Please open Spotify on a device."}
            else:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                    return {"success": False, "message": f"Spotify API error: {error_msg}"}
                except:
                    return {"success": False, "message": f"Spotify API error: Status {response.status_code}"}
        except Exception as e:
            return {"success": False, "message": f"Request failed: {str(e)}"}
    
    def play(self, uri=None):
        """Start/resume playback or play specific track/playlist"""
        data = {"uris": [uri]} if uri else None
        result = self._make_spotify_request('me/player/play', 'PUT', data)
        if result.get('success'):
            return {"success": True, "message": "▶️ Resumed playback" if not uri else f"▶️ Playing"}
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
            return {"success": True, "message": "⏭️ Next track"}
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
    
    def play_song(self, song_name):
        """Search for a song and play it"""
        # Use the existing play_track method which handles this correctly
        return self.play_track(song_name)
    
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
        
        if not search_result.get('success'):
            return {
                "success": False,
                "message": f"Spotify search failed: {search_result.get('message', 'Unknown error')}"
            }
        
        if search_result.get('results'):
            track = search_result['results'][0]
            play_result = self.play(track['uri'])
            if play_result.get('success'):
                return {
                    "success": True,
                    "message": f"🎵 Playing: {track['display']}"
                }
            return play_result
        
        return {"success": False, "message": f"Track '{query}' not found on Spotify. Try being more specific or check the spelling."}
    
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
