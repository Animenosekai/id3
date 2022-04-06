from eyed3.id3 import Tag
from id3.lyrics import LyricsProvider

from id3.provider import Provider


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
    """
    if tag is None:
        tag = Tag()
    if is_id:
        result = provider.get(title)
    else:
        result = provider.search(title)
    tag.artist = ", ".join(artist.name for artist in result.artists)
    tag.album_artist = tag.artist
    tag.album = result.album.name
    tag.title = result.name
    tag.track_num = result.track_number
    tag.disc_num = result.disc_number
    if result.analysis.tempo is not None:
        tag.bpm = result.analysis.tempo
    tag.release_date = result.album.release_date
    tag.genre = ", ".join([", ".join(artist.genres) for artist in result.artists])  # we are setting all of the artists genres
    tag.commercial_url = result.url
    tag.artist_url = result.artists[0].url
    tag.encoded_by = "© ID3, Anime no Sekai"
    r = provider.session.get(result.album.image)
    r.raise_for_status()
    tag.images.set(type_=3, img_data=r.content, mime_type=r.headers['Content-Type'], description="Cover Art", img_url=result.album.image)
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
