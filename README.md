# id3

<img align="right" src="assets/ryou.png" height="220px">

***The most easy way to add ID3 tags to your music.***

<br>
<br>

[![GitHub - License](https://img.shields.io/github/license/Animenosekai/id3)](https://github.com/Animenosekai/id3/blob/master/LICENSE)
[![GitHub top language](https://img.shields.io/github/languages/top/Animenosekai/id3)](https://github.com/Animenosekai/id3)
![Code Size](https://img.shields.io/github/languages/code-size/Animenosekai/id3)
![Repo Size](https://img.shields.io/github/repo-size/Animenosekai/id3)
![Issues](https://img.shields.io/github/issues/Animenosekai/id3)

## Index

- [Index](#index)
- [Purpose](#purpose)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
- [Installing](#installing)
  - [From Git](#from-git)
- [Usage](#usage)
- [Contributing](#contributing)
- [Authors](#authors)
- [Licensing](#licensing)

## Purpose

`id3` is a simple script to add ID3 tags to your songs and add them to your Spotify library.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

You will need Python 3 to use this module

```bash
# vermin output
Minimum required versions: 3.8
Incompatible versions:     2
```

## Installing

### From Git

```bash
pip install --upgrade git+https://github.com/Animenosekai/id3.git
```

> This will install the latest development version from the git repository

You can check if you successfully installed it by printing out its version:

```bash
$ id3 --version
1.0
```

## Usage

You can use the `id3` script to add ID3 tags to your songs or `yay` to download and manage your songs in your song library.

```bash
🧃❯ id3 --help
usage: id3 [-h] [--version] [--provider PROVIDER] [--ignore IGNORE] [--album ALBUM] [--spotify-id SPOTIFY_ID] [song]

The most easy way to add ID3 tags to your music.

positional arguments:
  song                  the song or directory of songs to add ID3 tags to.

options:
  -h, --help            show this help message and exit
  --version, -v         show program's version number and exit
  --provider PROVIDER, -p PROVIDER
                        the metadata provider to use. one of {spotify, interactive, copy}
  --ignore IGNORE, -i IGNORE
                        a file to ignore if a directory is passed (can be used multiple times).
  --album ALBUM         (this implies --provider copy) the song to copy the album information from. if not provided, it will be asked when needed (useful for multiple album directories).
  --spotify-id SPOTIFY_ID
                        if using --provider Spotify, the spotify ID to use for the metadata. if 'search', the filename will be searched. if None, it will be asked when needed.

```

> **Note**  
> If you want to use the Spotify API as a provider for your tags, you will need to set the `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` environment variables.

```bash
🧃❯ yay --help
usage: yay [-h] [--ffmpeg FFMPEG] [--output OUTPUT]

The most easy way to add songs to your Spotify library.

options:
  -h, --help            show this help message and exit
  --ffmpeg FFMPEG, -f FFMPEG
                        The path to the `ffmpeg` executable, ('ffmpeg' by default)
  --output OUTPUT, -o OUTPUT
                        The output directory for the song (the env var 'YAY_SONGS_OUTPUT_DIRECTORY' or './output' will be used by default)

```

Everything should be interactive, and you will be prompted to enter stuff when needed.

> **Warning**  
> Please keep in mind that it might play sound without warning for you to confirm that this was the song you were looking for so try to set the volume down a bit when running the scripts.

## Contributing

Pull requests are welcome. For major changes, please open a discussion first to discuss what you would like to change.

## Authors

- **Animenosekai** - *Initial work* - [Animenosekai](https://github.com/Animenosekai)

## Licensing

This software is licensed under the MIT License. See the [*LICENSE*](./LICENSE) file for more information.
