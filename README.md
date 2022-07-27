# XPlat-MP

XPlat-MP is a cross-platform music player designed to play music from your favorite music providers.

## Features

Currently you can only add songs from YouTube to your music collection.

See [TODO](TODO.md) for upcoming features.

If you think the project is interesting, don't hesistate making a PR.

## Requirements

- [`Python 3.6+`](https://www.python.org/downloads/)
- [`PyQt5`](https://www.riverbankcomputing.com/software/pyqt/download5)
- [`youtube-dl`](https://rg3.github.io/youtube-dl/)
- [`Python-VLC`](https://www.videolan.org/vlc/index.html)
- [`requests`](https://requests.readthedocs.io/en/master/)
- [`pafy`](https://pafy.readthedocs.io/en/latest/)

## Installation

Most of the dependencies can be installed by running

```sh
pip install -r requirements.txt
```

However, Pafy is currently outdated and we are currently using a fork of it.

Install the missing library by running:

```sh
pip install git+https://github.com/Cupcakus/pafy
```

## Bugs

If you find a bug, please report it under [issues](https://github.com/RealSoerensen/XPLAT-MusicPlayer/issues).

If you think you can fix the bug, please assign the issue to yourself and make a PR when fixed.

## License

XPlat-MP is licensed under the [MIT license](LICENSE.md).
