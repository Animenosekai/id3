"""
__main__

The CLI interface for id3
"""
import argparse
import multiprocessing
import os
from pathlib import Path

import eyed3
import inquirer
import magic
from playsound import playsound

import id3
from id3 import complete
from id3.providers.interactive import (SpotifyInteractive,
                                       SpotifyInteractiveTrack)
from id3.providers.spotify import Spotify

providers = [
    inquirer.List(
        name='provider',
        message="Which provider do you want to use?",
        choices=['Spotify', 'Interactive', 'Copy', 'Quit'],
        carousel=True
    )
]


class SameAlbumProvider(SpotifyInteractive):
    def __init__(self, track_path: Path = None, hint: str = None) -> None:
        super().__init__()
        if track_path is None:
            track_path = inquirer.prompt([
                inquirer.Path(
                    "base",
                    message="What is the song to copy the information from?",
                    path_type=inquirer.Path.ANY,
                    exists=True,
                    default=hint or os.getcwd()
                )
            ])["base"]
            self.hint = track_path
        track_path = Path(track_path).resolve().absolute()
        if not track_path.is_file():
            raise ValueError("{} should be a file".format(track_path))
        data = eyed3.load(str(track_path))
        self.track_data = {
            "image": data.tag.images[0].image_data if len(data.tag.images) > 0 else None,
            "album": {
                "name": data.tag.album
            },
            "artists": [{
                "name": data.tag.artist
            }]
        }

    def search(self, query: str):
        return SpotifyInteractiveTrack(self.track_data)

    def get(self, track: str):
        return SpotifyInteractiveTrack(self.track_data)


def manage(audiofile: Path, provider: str, album: str = None, hint: str = None, spotify_id: str = None):
    print("\033[96m*\033[0m", "Adding tags to", audiofile.stem)
    try:
        p = multiprocessing.Process(target=playsound, args=(str(audiofile),))
        p.start()  # start playing the song

        # getting the right provider and hint
        if provider == "spotify":
            if spotify_id is None:
                spotify_id = inquirer.prompt([
                    inquirer.Text("spotify_id", "Spotify ID of the song")
                ])["spotify_id"]
            try:
                provider = Spotify(os.environ["SPOTIFY_CLIENT_ID"], os.environ["SPOTIFY_CLIENT_SECRET"])
            except KeyError as err:
                raise ValueError("You need to set the 'SPOTIFY_CLIENT_ID' and 'SPOTIFY_CLIENT_SECRET' environment variables to use the Spotify API") from err
        elif provider == "copy":
            provider = SameAlbumProvider(album, hint=hint)
            hint = provider.hint
        else:
            provider = SpotifyInteractive()

        # adding the tags
        spotify_id = str(spotify_id).replace(" ", "").removeprefix("spotify:track:").removeprefix("https://open.spotify.com/track/").split("?")[0]
        is_id = spotify_id.lower() != "search"
        tag = complete(
            title=spotify_id if is_id else audiofile.stem,
            provider=provider,
            is_id=is_id
        )
        tag.save(str(audiofile.resolve().absolute()))

        p.terminate()  # stop the sound
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("\033[93mAn error occured while processing {} ({})\033[0m".format(audiofile, e))
    try:
        p.terminate()
    except Exception:  # "p" does not exist
        pass
    return hint


def main(arguments: list[str] = None):
    parser = argparse.ArgumentParser(prog='id3', description='The most easy way to add ID3 tags to your music.')

    parser.add_argument('--version', '-v', action='version', version=id3.__version__)

    # required
    parser.add_argument('song', nargs="?", default=None, type=str, help='the song or directory of songs to add ID3 tags to.')

    # optional
    parser.add_argument('--provider', '-p', action='store', type=str, required=False,
                        default=None, help='the metadata provider to use. one of {spotify, interactive, copy}')
    parser.add_argument('--ignore', '-i', action='append', required=False,
                        help="a file to ignore if a directory is passed (can be used multiple times).")
    parser.add_argument("--album", action="store", type=str, required=False, default=None,
                        help="(this implies --provider copy) the song to copy the album information from. if not provided, it will be asked when needed (useful for multiple album directories).")
    parser.add_argument("--spotify-id", action="store", type=str, required=False, default=None,
                        help="if using --provider Spotify, the spotify ID to use for the metadata. if 'search', the filename will be searched. if None, it will be asked when needed.")

    if arguments is not None:
        args = parser.parse_intermixed_args(arguments)
    else:
        args = parser.parse_intermixed_args()

    if args.song is None:
        args.song = inquirer.prompt([
            inquirer.Path(
                "song",
                message="Which song do you want to add ID3 tags to?",
                path_type=inquirer.Path.ANY,
                exists=True,
                default=os.getcwd()
            )
        ])["song"]

    song = Path(args.song).resolve()

    if args.provider is None:
        if args.album is not None:
            args.provider = "copy"
        else:
            answers = inquirer.prompt(providers)
            args.provider = answers["provider"]
    args.provider = str(args.provider).lower().replace(" ", "")

    if args.provider == "quit":
        exit(0)

    counter = 0
    if song.is_file():
        counter = 1
        manage(song, args.provider, album=args.album, hint=None, spotify_id=args.spotify_id)
        print("")

    if song.is_dir():
        ignore = args.ignore if args.ignore else []
        hint = str(song)
        for audiofile in song.iterdir():
            if audiofile.name in ignore:
                continue
            if magic.from_file(str(audiofile), mime=True) != "audio/mpeg":  # ignoring non-mp3 files
                continue
            counter += 1
            manage(audiofile, args.provider, album=args.album, hint=hint, spotify_id=args.spotify_id)
            print("")
    print("\033[96m[*]", "Done adding tags to", counter, f"file{'s' if counter > 1 else ''}", "\033[0m")
