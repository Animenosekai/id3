import inquirer
from id3.provider import Provider, Track, Album, Artist, DEFAULT_IMAGE


class SpotifyInteractiveAlbum(Album):
    def __init__(self, album: dict = None):
        album = album or {}
        self.name = album.get('name')
        if not self.name:
            self.name = inquirer.prompt([
                inquirer.Text("album_name", "Album Name")
            ])["album_name"]


class SpotifyInteractiveArtist(Artist):
    def __init__(self, artist: dict = None):
        artist = artist or {}
        self.name = artist.get('name')
        if not self.name:
            self.name = inquirer.prompt([
                inquirer.Text("artist_name", "Artist Name")
            ])["artist_name"]


class SpotifyInteractiveTrack(Track):
    def __init__(self, track: dict = None):
        track = track or {}
        self.name = track.get('name')
        if not self.name:
            self.name = inquirer.prompt([
                inquirer.Text("track_name", "Track Name")
            ])["track_name"]
        self.image = track.get('image')
        if not self.image:
            self.image = inquirer.prompt([
                inquirer.Text("track_image", "Image URL")
            ])["track_image"]
        self.album = SpotifyInteractiveAlbum(track.get('album'))
        artists = track.get('artists', [])
        self.artists = [SpotifyInteractiveArtist(artist) for artist in artists] if len(artists) > 0 else [SpotifyInteractiveArtist()]


class SpotifyInteractive(Provider):
    def search(self, query: str) -> Track:
        return SpotifyInteractiveTrack()

    def get(self, track: str) -> Track:
        return SpotifyInteractiveTrack()
