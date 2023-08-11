"""
yay

easily add songs to your spotify library
"""
import argparse
import subprocess
import tempfile
import os
from pathlib import Path

import eyed3
import inquirer
from bson import ObjectId
from youtube_dl import YoutubeDL

from id3.__main__ import main


def entry():
    """the main cli entrypoint"""
    parser = argparse.ArgumentParser(prog='yay', description='The most easy way to add songs to your Spotify library.')

    parser.add_argument("--ffmpeg", "-f", action="store", type=str, required=False, default=None,
                        help="The path to the `ffmpeg` executable, ('ffmpeg' by default)")
    parser.add_argument("--output", "-o", action="store", type=str, required=False, default=None,
                        help="The output directory for the song (the env var 'YAY_SONGS_OUTPUT_DIRECTORY' or './output' will be used by default)")
    args = parser.parse_args()

    def log_step(*messages):
        print()
        print("\033[96m[*]", " ".join([str(m) for m in messages]), "\033[0m")

    log_step("Setting output directory...")
    if args.output is None:
        OUTPUT_DIRECTORY = Path(os.environ.get("YAY_SONGS_OUTPUT_DIRECTORY", "output"))
    else:
        OUTPUT_DIRECTORY = Path(args.output)

    SONG_LINK = inquirer.prompt([
        inquirer.Text("song", "Song Link")
    ])["song"]
    SONG_LINK = str(SONG_LINK).strip("'")  # if pasted with quotes

    SONG_ID = str(ObjectId())
    SONG_PATH = str(tempfile.gettempdir()) + "/" + SONG_ID
    log_step("New song ID:", SONG_ID)

    try:
        if Path(SONG_LINK).is_file():
            log_step("Copying the given file to a temp directory")
            subprocess.run(f'{args.ffmpeg or "ffmpeg"} -y -i "{Path(SONG_LINK).resolve()}" "{SONG_PATH}.mp3"', check=True, shell=True)
            # subprocess.run([args.ffmpeg or "ffmpeg", "-y", "-i", f'"{Path(SONG_LINK).resolve()}"',
            #                f'"{os.path.splitext(SONG_PATH)[0]}.mp3"', "-y"], check=True)
            SONG_PATH += ".mp3"
        else:
            with YoutubeDL({
                'format': 'bestaudio/best',
                'outtmpl': SONG_PATH,
                'noplaylist': True,
                'audio_quality': 0
            }) as ydl:
                ydl.download([SONG_LINK])

                # ensuring the format to be mp3
                for file in Path(SONG_PATH).parent.iterdir():
                    if file.stem.startswith(SONG_ID):
                        if file.suffix == ".mp3":  # no need for conversion
                            break
                        subprocess.run(
                            f'{args.ffmpeg or "ffmpeg"} -y -i "{Path(SONG_PATH + file.suffix).resolve()}" "{SONG_PATH}.mp3"', check=True, shell=True)
                        path = Path(SONG_PATH + file.suffix)
                        if path.is_file() and path.suffix != ".mp3":  # removing the old file
                            path.unlink()
                        SONG_PATH += ".mp3"
                        break

        # main(sys.argv + [SONG_PATH])
        print()
        main([SONG_PATH])

        log_step("Moving file to the output directory...")
        try:
            data = eyed3.load(SONG_PATH)
            if data.tag.title is None:
                raise ValueError("No title found")
            output = OUTPUT_DIRECTORY / (str(data.tag.title).replace("/", "_") + ".mp3")
            if Path(output).is_file():
                print("\033[93m{} already exists and the file will be outputted with its song ID.\033[0m".format(output))
                output = OUTPUT_DIRECTORY / (str(data.tag.title).replace("/", "_") + SONG_ID + ".mp3")
        except Exception:
            print("\033[93mAn error occured while creating the path for the output so the final filename will be the song ID.\033[0m")
            output = OUTPUT_DIRECTORY / (SONG_ID + ".mp3")
        Path(SONG_PATH).rename(output)
        print()
        print("\033[92m[✓] Added 1 song to your Spotify library\033[0m")
    except Exception as e:
        print("\033[93m[✘] An error occured while adding the song to your Spotify library.\033[0m")
        from traceback import print_exc
        print_exc()
        print()

    SONG_PATH = Path(SONG_PATH)
    if SONG_PATH.is_file():
        log_step("Removing the temp file...")
        SONG_PATH.unlink()
    print("\033[92m[✓] Removed the temp file\033[0m")


if __name__ == "__main__":
    entry()
