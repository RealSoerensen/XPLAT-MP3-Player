# XPlat-MP

XPlat-MP is a cross-platform music player designed to play music from your favorite music providers.

## Features

Currently you can only add songs from YouTube to your music collection and play them via VLC.

See [TODO](TODO.md) for upcoming features.

If you think the project is interesting, don't hesistate making a PR.

## Installation

First you need [`Python`](https://www.python.org/downloads/) version 3.8+ or higher.

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

XPlat-MP is licensed under the [GPL-3.0](LICENSE.md) license.
