"""
Python ID3\n
The most easy way to add ID3 tags to your music.

© Anime no Sekai — 2022
"""

from id3.tags import complete, add_lyrics


__version_tuple__ = (1, 0)


def __version_string__():
    if isinstance(__version_tuple__[-1], str):
        return '.'.join(map(str, __version_tuple__[:-1])) + __version_tuple__[-1]
    return '.'.join(str(i) for i in __version_tuple__)


__author__ = 'Anime no Sekai'
__copyright__ = 'Copyright 2022, id3'
__credits__ = ['animenosekai']
__license__ = 'MIT License'
__version__ = 'id3 v{}'.format(__version_string__())
__maintainer__ = 'Anime no Sekai'
__email__ = 'niichannomail@gmail.com'
__status__ = 'Beta'
