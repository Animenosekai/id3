from datetime import datetime
from id3.request import Session
from id3.types import ALBUM_TYPE, MODALITY


# DEFAULT_IMAGE = "https://i.pinimg.com/564x/e9/c5/c7/e9c5c72d35ee6bcdd8ae3fca2ba0919e.jpg"
DEFAULT_IMAGE = "/Users/animenosekai/Documents/Coding/Projects/id3/ninym_hmm.jpg"


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
        if hasattr(self, 'tempo'):
            return f"Analaysis(tempo={self.tempo}, ...)"
        return "Analaysis(...)"


class Artist:
    genres: list = []
    """the genres of the artist"""
    id: str
    """the id of the artist"""
    name: str
    """the name of the artist"""
    image: str = DEFAULT_IMAGE
    """the url of the artist's image"""
    url: str
    """the url of the artist"""

    def __repr__(self) -> str:
        if hasattr(self, "name") and hasattr(self, "id"):
            return f"Artist(name='{self.name}', id='{self.id}')"
        if hasattr(self, "name"):
            return f"Artist(name='{self.name}')"
        if hasattr(self, "id"):
            return f"Artist(id='{self.id}')"
        return "Artist()"


class Album:
    type: ALBUM_TYPE
    """the type of the album"""
    total: int
    """the total number of tracks"""
    name: str
    """the name of the album"""
    id: str
    """the id of the album"""
    image: str = DEFAULT_IMAGE
    """the url of the album image"""
    release_date: datetime
    """the release date of the album"""
    url: str
    """the url of the album"""

    def __repr__(self) -> str:
        if hasattr(self, "name") and hasattr(self, "id"):
            return f"Album(name='{self.name}', id='{self.id}')"
        if hasattr(self, "name"):
            return f"Album(name='{self.name}')"
        if hasattr(self, "id"):
            return f"Album(id='{self.id}')"
        return "Album()"


class Track:
    artists: list[Artist] = []
    """the artists of the track"""
    id: str
    """the id of the track"""
    name: str
    """the name of the track"""
    image: str
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
        if hasattr(self, "name") and hasattr(self, "id"):
            return f"Track(name='{self.name}', id='{self.id}')"
        if hasattr(self, "name"):
            return f"Track(name='{self.name}')"
        if hasattr(self, "id"):
            return f"Track(id='{self.id}')"
        return "Track()"


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
