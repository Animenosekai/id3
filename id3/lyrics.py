from typing import Union
from translatepy import Language
from id3.provider import Track


class Lyrics:
    def __init__(self, value: str, language: Language = "eng") -> None:
        self.value = str(value)
        self.language = Language(language)


class LyricsProvider:
    def search(self, query: str) -> Lyrics:
        """Search for a track by name."""
        raise NotImplementedError

    def get(self, track: Union[str, Track]) -> Lyrics:
        """Get the lyrics of a track by id."""
        raise NotImplementedError
