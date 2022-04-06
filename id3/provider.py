from datetime import datetime
from id3.request import Session
from id3.types import ALBUM_TYPE, MODALITY


class Analysis:
    tempo: float
    """the estimated tempo of the audio file"""
    key: int
    """the estimated key of the audio file"""
    loudness: float
    """the estimated loudness of the audio file"""
    time_signature: int
    """the estimated time signature of the audio file"""
    mode: MODALITY

    def __repr__(self) -> str:
        return f"Analaysis(tempo={self.tempo}, ...)"


class Artist:
    genres: list
    """the genres of the artist"""
    id: str
    """the id of the artist"""
    name: str
    """the name of the artist"""
    image: str
    """the url of the artist's image"""
    url: str
    """the url of the artist"""

    def __repr__(self) -> str:
        return f"Artist(name='{self.name}', id='{self.id}')"


class Album:
    type: ALBUM_TYPE
    """the type of the album"""
    total: int
    """the total number of tracks"""
    name: str
    """the name of the album"""
    id: str
    """the id of the album"""
    image: str
    """the url of the album image"""
    release_date: datetime
    """the release date of the album"""
    url: str
    """the url of the album"""

    def __repr__(self) -> str:
        return f"Album(name='{self.name}', id='{self.id}')"


class Track:
    artists: list[Artist]
    """the artists of the track"""
    id: str
    """the id of the track"""
    name: str
    """the name of the track"""
    image: str = None
    """the url of the track image"""
    album: Album
    """the album of the track"""
    analysis: Analysis = None
    """the analysis of the track"""
    duration: int
    """the duration of the track in seconds"""
    explicit: bool = False
    """whether the track is explicit"""
    popularity: int = None
    """the popularity of the track"""
    preview: str = None
    """the url of the track's preview"""
    track_number: int
    """the track number of the track"""
    disc_number: int = 1
    """the disc number of the track"""
    url: str
    """the url of the track"""
    isrc: str = None

    def __repr__(self) -> str:
        return f"Track(name='{self.name}', id='{self.id}')"


class Provider:
    def __init__(self) -> None:
        self.session = Session()

    def search(self, query: str) -> Track:
        """
        Search for a track by name.
        """
        raise NotImplementedError

    def get(self, track: str) -> Track:
        """
        Get a track by id.
        """
        raise NotImplementedError
