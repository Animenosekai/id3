from base64 import b64encode
from datetime import datetime
from id3.provider import Analysis, Provider, Track, Album, Artist


class SpotifyAnalysis(Analysis):
    def __init__(self, analysis: dict) -> None:
        self.key = analysis.get('key', None)
        self.mode = analysis.get('mode', None)
        if self.mode == 0:
            self.mode = 'minor'
        elif self.mode == 1:
            self.mode = 'major'
        self.time_signature = analysis.get('time_signature', None)
        self.tempo = analysis.get('tempo', None)
        self.loudness = analysis.get('loudness', None)


class SpotifyArtist(Artist):
    def __init__(self, artist: dict):
        self.genres = artist.get('genres', [])
        self.id = artist.get('id', '')
        self.name = artist.get('name', '')
        self.image = artist.get('images', [{'url': ''}])[0].get('url', '')

    @property
    def url(self) -> str:
        return f"https://open.spotify.com/artist/{self.id}"


class SpotifyAlbum(Album):
    def __init__(self, album: dict):
        self.type = album.get('album_type', '')
        self.total = album.get('total_tracks', 0)
        self.name = album.get('name', '')
        self.id = album.get('id', '')
        self.image = album.get('images', [{'url': ''}])[0].get('url', '')
        self.release_date = album.get('release_date', '')  # TODO: datetime

    @property
    def url(self) -> str:
        return f"https://open.spotify.com/album/{self.id}"


class SpotifyTrack(Track):
    def __init__(self, track: dict):
        self.artists = [SpotifyArtist(artist) for artist in track.get('artists', [])]
        self.id = track.get('id', '')
        self.name = track.get('name', '')
        self.image = track.get('images', [{'url': ''}])[0].get('url', '')
        self.album = SpotifyAlbum(track.get('album', {}))
        self.analysis = SpotifyAnalysis(track.get('analysis', {}))
        self.duration = track.get('duration_ms', 0) / 1000
        self.explicit = track.get('explicit', False)
        self.popularity = track.get('popularity', 0)
        self.preview = track.get('preview_url', '')
        self.track_number = track.get('track_number', 0)
        self.disc_number = track.get('disc_number', 0)

    @property
    def url(self) -> str:
        return f"https://open.spotify.com/track/{self.id}"


class Spotify(Provider):
    def __init__(self, client_id: str, client_secret: str, analysis: bool = False) -> None:
        super().__init__()
        self.analysis = bool(analysis)
        self.client_id = str(client_id)
        self.client_secret = str(client_secret)
        r = self.session.post(
            url="https://accounts.spotify.com/api/token",
            headers={
                "Authorization": f"Basic {b64encode(f'{self.client_id}:{self.client_secret}'.encode()).decode()}",
            },
            data={
                "grant_type": "client_credentials"
            }
        )
        r.raise_for_status()
        self.access_token = r.json()['access_token']

    def search(self, query: str) -> Track:
        r = self.session.get(
            url=f'https://api.spotify.com/v1/search?q={query}&type=track&limit=1',
            headers={
                "Authorization": f"Bearer {self.access_token}"
            }
        )
        r.raise_for_status()
        data = r.json()
        return SpotifyTrack(data["tracks"]["items"][0])

    def get(self, track_id: str) -> Track:
        r = self.session.get(
            url=f'https://api.spotify.com/v1/tracks/{track_id}',
            headers={
                "Authorization": f"Bearer {self.access_token}"
            }
        )
        r.raise_for_status()
        data = r.json()
        return SpotifyTrack(data)
