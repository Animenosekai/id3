from pathlib import Path
import magic
from eyed3.id3 import Tag
from id3.lyrics import LyricsProvider

from id3.provider import DEFAULT_IMAGE, Provider


def complete(title: str, provider: Provider, tag: Tag = None, is_id: bool = False) -> Tag:
    """
    Complete the given tag with the given provider.

    Parameters
    ----------
    title: str
        The title of the track. This will be used to search for the track.
    provider: Provider
        The data provider.
    tag: Tag
        The tag to complete. If None, a new tag will be created.

    Returns
    -------
    Tag
        The completed tag.

    Examples
    --------
    >>> from id3.providers.spotify import Spotify
    >>> from id3.tags import complete
    >>> s = Spotify(CLIENT_ID, CLIENT_SECRET)
    >>> complete("Renai Circulation", s)

    Notes
    -----
    Here is a list of the fields that will be used
        - artist.name
        - album.name
        - name
        - track_number
        - disc_number
        - analysis.tempo
        - album.release_date
        - artist.genres
        - url
        - artist.url
        - image or album.image

    Here are the fields used by Spotify
        - artist.name
        - album.name
        - name
        - image or album.image
    """
    if tag is None:
        tag = Tag()
    if is_id:
        result = provider.get(title)
    else:
        result = provider.search(title)
    if len(result.artists) > 0:
        if hasattr(result.artists[0], "url"):
            tag.artist_url = result.artists[0].url
        tag.artist = ", ".join(artist.name for artist in result.artists if hasattr(artist, "name"))
        tag.genre = ", ".join([", ".join(artist.genres) for artist in result.artists])  # we are setting all of the artists genres
    tag.album_artist = tag.artist
    if hasattr(result, "album"):
        album = result.album
        if hasattr(album, "name"):
            tag.album = album.name
        if hasattr(album, "release_date"):
            tag.release_date = album.release_date
    if hasattr(result, "name"):
        tag.title = result.name
    if hasattr(result, "track_number"):
        tag.track_num = result.track_number
    tag.disc_num = result.disc_number
    if result.analysis is not None and result.analysis.tempo is not None:
        tag.bpm = result.analysis.tempo
    if hasattr(result, "url"):
        tag.commercial_url = result.url
    tag.encoded_by = "© ID3, Anime no Sekai"

    if hasattr(result, "image") and result.image:
        image = result.image
    elif hasattr(result, "album") and hasattr(result.album, "image") and result.album.image:
        image = result.album.image
    else:
        image = DEFAULT_IMAGE

    if hasattr(image, "read"):
        image = image.read()
    if isinstance(image, bytes):
        content = image
    else:
        image = str(image)
        path = Path(image).resolve()
        if path.is_file():
            with open(path, "r+b") as f:
                content = f.read()
        else:
            r = provider.session.get(image)
            if r.status_code >= 400:
                return tag
            content = r.content
    tag.images.set(type_=3, img_data=content, mime_type=magic.from_buffer(content, mime=True), description="Cover Art")
    return tag


def add_lyrics(title: str, provider: LyricsProvider, tag: Tag = None, is_id: bool = False) -> None:
    """
    Add the lyrics to the given tag.

    Parameters
    ----------
    title: str
        The title of the track. This will be used to search for the track.
    provider: LyricsProvider
        The lyrics provider.

    Returns
    -------
    Tag
        The completed tag.
    """
    if tag is None:
        tag = Tag()
    if is_id:
        result = provider.get(title)
    else:
        result = provider.search(title)
    tag.lyrics.set(text=result.value, description=f"Lyrics provided by {provider.__class__.__name__}", lang=result.language.alpha3.encode("utf-8"))
    return tag
