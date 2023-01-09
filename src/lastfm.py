from . import DL as http
from typing import Dict, Optional, Any


API_KEY = ''

class LastFM:
    def __init__(self, username: str, artist: Optional[str] = None, track: Optional[str] = None):
        self.username = username # this is required
        self.artist = artist # optional but required for functions regarding getting information on an artist
        self.track = track # optional but required for functions regarding getting information on a track


    async def now_playing(self) -> Optional[Dict[str, Dict[str, Any]]]:
        """Get information about the user's currently playing track, returns None if no track is playing"""
        
        try:
            data = await http.get('https://ws.audioscrobbler.com/2.0/', params={'method': 'user.getRecentTracks', 'user': self.username, 'api_key': API_KEY, 'format': 'json', 'limit': '1'})
            track = data['recenttracks']['track'][0]

            if track.get('@attr') is None:
                return None

            trackinfo = await http.get('https://ws.audioscrobbler.com/2.0/', params={'method': 'track.getInfo', 'username': self.username, 'api_key': API_KEY, 'artist': track['artist']['#text'], 'track': track['name'], 'format': 'json', 'autocorrect': '1'})
            artistinfo = await http.get('https://ws.audioscrobbler.com/2.0/', params={'method': 'artist.getInfo', 'username': self.username, 'api_key': API_KEY, 'artist': track['artist']['#text'], 'format': 'json', 'autocorrect': '1'})

            trackinfo['track'].setdefault('album', {'title': ''})
            trackinfo['track'].setdefault('userplaycount', 0)
            artistinfo['artist']['stats'].setdefault('userplaycount', 0)

            ret = {
                'artist': {
                    'name': artistinfo['artist']['name'],
                    'url': artistinfo['artist']['url'],
                    'hyper': f"[{artistinfo['artist']['name']}]({artistinfo['artist']['url']})",
                    'hyper.lower': f"[{artistinfo['artist']['name'].lower()}]({artistinfo['artist']['url']})",
                    'image': artistinfo['artist']['image'][3]['#text'],
                    'plays': int(artistinfo['artist']['stats']['userplaycount'])
                },
                'track': {
                    'name': trackinfo['track']['name'],
                    'url': trackinfo['track']['url'],
                    'hyper': f"[{trackinfo['track']['name']}]({trackinfo['track']['url']})",
                    'hyper.lower': f"[{trackinfo['track']['name'].lower()}]({trackinfo['track']['url']})",
                    'image': track['image'][3]['#text'],
                    'album': trackinfo['track']['album']['title'],
                    'plays': int(trackinfo['track']['userplaycount'])
                },
                'scrobbles': int(data['recenttracks']['@attr']['total'])
            }

            return ret
        except:
            return None


    async def top_artists(self) -> Dict[str, Dict[str, Any]]:
        """Get a list of the user's top artists"""
        
        data = await http.get('https://ws.audioscrobbler.com/2.0/', params={'method': 'user.gettopartists', 'user': self.username, 'api_key': API_KEY, 'format': 'json', 'limit': '10'})
        
        ret = list()
        for artist in data['topartists']['artist']:
            ret.append(
                {
                    'name': artist['name'],
                    'hyper': f"[{artist['name']}]({artist['url']})",
                    'hyper.lower': f"[{artist['name'].lower()}]({artist['url']})",
                    'image': artist['image'][3]['#text'],
                    'rank': int(artist['@attr']['rank']),
                    'plays': int(artist.get('playcount')) or 0
                }
            )

        return ret


    async def top_albums(self) -> Dict[str, Dict[str, Any]]:
        """Get a list of the user's top albums"""
        
        data = await http.get('https://ws.audioscrobbler.com/2.0/', params={'method': 'user.gettopalbums', 'user': self.username, 'api_key': API_KEY, 'format': 'json', 'limit': '10'})
        
        ret = list()
        for album in data['topalbums']['album']:
            ret.append(
                {
                    'artist': album['artist']['name'],
                    'artist.hyper': f"[{album['artist']['name']}]({album['artist']['url']})",
                    'name': album['name'],
                    'hyper': f"[{album['name']}]({album['url']})",
                    'hyper.lower': f"[{album['name'].lower()}]({album['url']})",
                    'image': album['image'][3]['#text'],
                    'rank': int(album['@attr']['rank']),
                    'plays': int(album.get('playcount')) or 0
                }
            )

        return ret


    async def top_tracks(self) -> Dict[str, Dict[str, Any]]:
        """Get a list of the user's top tracks"""
        
        data = await http.get('https://ws.audioscrobbler.com/2.0/', params={'method': 'user.gettoptracks', 'user': self.username, 'api_key': API_KEY, 'format': 'json', 'limit': '10'})
        
        ret = list()
        for track in data['toptracks']['track']:
            ret.append(
                {
                    'name': track['name'],
                    'artist.hyper': f"[{track['artist']['name']}]({track['artist']['url']})",
                    'hyper': f"[{track['name']}]({track['url']})",
                    'hyper.lower': f"[{track['name'].lower()}]({track['url']})",
                    'image': track['image'][3]['#text'],
                    'rank': int(track['@attr']['rank']),
                    'plays': int(track.get('playcount')) or 0
                }
            )

        return ret


    async def recent_tracks(self) -> Dict[str, Dict[str, Any]]:
        """Get a list of the user's recent tracks, kind of like `now_playing` but less information and returns 10 tracks (can be changed)"""
        
        data = await http.get('https://ws.audioscrobbler.com/2.0/', params={'method': 'user.getRecentTracks', 'user': self.username, 'api_key': API_KEY, 'format': 'json', 'limit': '10'})
        ret = list()
        num = 0
        for track in data['recenttracks']['track']:
            trackk = await http.get('https://ws.audioscrobbler.com/2.0/', params={'method': 'track.getInfo', 'username': self.username, 'api_key': API_KEY, 'artist': track['artist']['#text'], 'track': track['name'], 'format': 'json', 'autocorrect': '1'})
            num += 1
            ret.append(
                {
                    'name': trackk['track']['name'],
                    'artist.hyper': f"[{trackk['track']['artist']['name']}]({trackk['track']['artist']['url']})",
                    'hyper': f"[{trackk['track']['name']}]({trackk['track']['url']})",
                    'hyper.lower': f"[{trackk['track']['name'].lower()}]({trackk['track']['url']})",
                    'image': track['image'][3]['#text'],
                    'rank': num,
                    'plays': int(trackk['track'].get('userplaycount', 0))
                }
            )

        return ret


    async def artist_plays(self) -> int:
        """Get the user's play count for an artist, returns 0 if no artist was provided"""

        if self.artist is None:
            return 0

        try:
            artistinfo = await http.get('https://ws.audioscrobbler.com/2.0/', params={'method': 'artist.getInfo', 'username': self.username, 'api_key': API_KEY, 'artist': self.artist, 'format': 'json', 'autocorrect': '1'})
            return int(artistinfo['artist']['stats']['userplaycount'])
        except:
            return 0


    async def track_plays(self) -> int:
        """Get the user's play count for a track, returns 0 if no artist or track was provided"""

        if self.artist is None or self.track is None:
            return 0

        try:
            trackinfo = await http.get('https://ws.audioscrobbler.com/2.0/', params={'method': 'track.getInfo', 'username': self.username, 'api_key': API_KEY, 'artist': self.artist, 'track': self.track, 'format': 'json', 'autocorrect': '1'})
            return int(trackinfo['track']['userplaycount'])
        except:
            return 0


    async def artist_info(self) -> Optional[Dict[str, Dict[str, Any]]]:
        """Get information about the provided artist, kind of like now_playing but only for artist. Returns None if no artist was provided"""

        if self.artist is None:
            return None

        try:
            artistinfo = await http.get('https://ws.audioscrobbler.com/2.0/', params={'method': 'artist.getInfo', 'username': self.username, 'api_key': API_KEY, 'artist': self.artist, 'format': 'json', 'autocorrect': '1'})
            artistinfo['artist']['stats'].setdefault('userplaycount', 0)

            ret = {
                'artist': {
                    'name': artistinfo['artist']['name'],
                    'url': artistinfo['artist']['url'],
                    'hyper': f"[{artistinfo['artist']['name']}]({artistinfo['artist']['url']})",
                    'hyper.lower': f"[{artistinfo['artist']['name'].lower()}]({artistinfo['artist']['url']})",
                    'image': artistinfo['artist']['image'][3]['#text'],
                    'plays': int(artistinfo['artist']['stats']['userplaycount'])
                }
            }

            return ret
        except:
            return None


    async def track_info(self) -> Optional[Dict[str, Dict[str, Any]]]:
        """Get information about the provided track, kind of like now_playing but only for track. Returns None if no track was provided"""

        if self.artist is None or self.track is None:
            return None

        try:
            trackinfo = await http.get('https://ws.audioscrobbler.com/2.0/', params={'method': 'track.getInfo', 'username': self.username, 'api_key': API_KEY, 'artist': self.artist, 'track': self.track, 'format': 'json', 'autocorrect': '1'}) 
            trackinfo['track'].setdefault('album', {'title': ''})
            trackinfo['track'].setdefault('userplaycount', 0)

            ret = {
                'track': {
                    'name': trackinfo['track']['name'],
                    'url': trackinfo['track']['url'],
                    'hyper': f"[{trackinfo['track']['name']}]({trackinfo['track']['url']})",
                    'hyper.lower': f"[{trackinfo['track']['name'].lower()}]({trackinfo['track']['url']})",
                    'image': trackinfo['track']['image'][3]['#text'],
                    'album': trackinfo['track']['album']['title'],
                    'plays': int(trackinfo['track']['userplaycount'])
                }
            }

            return ret
        except:
            return None
