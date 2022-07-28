import sys
import os
import random
from typing import final

try:
    import requests
    from PyQt5.QtWidgets import *
    from PyQt5.QtMultimedia import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    import __init__
    from backend.database import session, Songs
    from backend.player import Player
    from platforms import spotify, youtube, soundcloud
except ImportError as e:
    os.system("pip install -r requirements.txt")


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle("X-Platform Music Player")
        self._player = Player()
        self.UiComponents()

        self.show()

    # method for widgets
    def UiComponents(self):
        # Create Image Label
        self.image = QLabel(self)
        self.image.setGeometry(100, 50, 200, 200)
        self.get_image()
        self.image.setScaledContents(True)

        # create a menu bar
        menu_bar = self.menuBar()
        add_menu = menu_bar.addMenu("Add")
        spotify_menu = QAction("From Spotify", self)
        add_menu.addAction(spotify_menu)
        spotify_menu.triggered.connect(self.add_spotify)
        yt_menu = QAction("From Youtube", self)
        add_menu.addAction(yt_menu)
        yt_menu.triggered.connect(self.add_yt)
        sc_menu = QAction("From SoundCloud", self)
        add_menu.addAction(sc_menu)
        sc_menu.triggered.connect(self.add_sc)

        # Create widget with songs
        self.song_widget = QListWidget(self)
        self.song_widget.setGeometry(400, 25, 175, 175)
        self.get_songs()

        # Create widget with queue
        self.queue_widget = QListWidget(self)
        self.queue_widget.setGeometry(400, 200, 175, 175)

        # Create buttons
        self.prev_btn = QPushButton(self)
        self.prev_btn.setGeometry(25, 275, 100, 100)
        self.prev_btn.clicked.connect(self.prev_song)
        self.prev_btn.setIcon(QIcon("./assets/prev.png"))
        self.prev_btn.setIconSize(QSize(100, 100))

        self.play_btn = QPushButton(self)
        self.play_btn.setGeometry(150, 275, 100, 100)
        self.play_btn.clicked.connect(self.get_song)
        self.play_btn.setIcon(QIcon("./assets/play.png"))
        self.play_btn.setIconSize(QSize(100, 100))

        next_btn = QPushButton(self)
        next_btn.setGeometry(275, 275, 100, 100)
        next_btn.clicked.connect(self.next_song)
        next_btn.setIcon(QIcon("./assets/next.png"))
        next_btn.setIconSize(QSize(100, 100))

    def get_image(self, url=None):
        default = QPixmap("./assets/default.png")
        if url is None:
            self.image.setPixmap(default)
            self.image.repaint()
            return

        try:
            thumbnail = requests.get(url)
            if thumbnail.status_code != 200:
                QMessageBox.warning(self, "Error", "Could not load image")
                self.image.setPixmap(default)

            else:
                with open("./assets/thumbnail.png", "wb") as f:
                    f.write(thumbnail.content)
                self.image.setPixmap(QPixmap("./assets/thumbnail.png"))
                self.image.keepAspectRatio = False
                os.remove("./assets/thumbnail.png")

        except Exception:
            self.image.setPixmap(default)

        self.image.repaint()

    def get_songs(self):
        self.song_widget.clear()
        self.songs = session.query(Songs).all()
        for song in self.songs:
            self.song_widget.addItem(song.title)
            self.song_widget.item(self.song_widget.count() - 1).setData(
                Qt.UserRole, song
            )

    def get_queue(self):
        pass

    def shuffle_music(self):
        new_list = random.sample(self.songs, len(self.songs))
        self.songs = new_list
        self.get_songs()

    def add_spotify(self):
        self.spotify_win = spotify.Spotify()
        self.spotify_win.window_closed.connect(self.get_songs)
        self.spotify_win.show()

    def add_yt(self):
        self.yt_win = youtube.YouTube()
        self.yt_win.window_closed.connect(self.get_songs)
        self.yt_win.show()

    def add_sc(self):
        self.sc_win = soundcloud.SoundCloud()
        self.sc_win.window_closed.connect(self.get_songs)
        self.sc_win.show()

    def next_song(self):
        pass

    def prev_song(self):
        pass

    def get_song(self):
        self.song = self.song_widget.currentItem().data(Qt.UserRole)
        self._player.player.set_pause(1)
        self._player.get_song(self.song)
        self.get_image(self.song.thumbnail)
        self._player.player.set_pause(0)
        self.play_song()

    def play_song(self):
        self._player.player.set_pause(0)
        self.play_btn.setIcon(QIcon("./assets/pause.png"))
        self.play_btn.clicked.disconnect()
        self.play_btn.clicked.connect(self.pause_song)
        if self.song != self.song_widget.currentItem().data(Qt.UserRole):
            self.get_song()

    def pause_song(self):
        self._player.player.set_pause(1)
        self.play_btn.setIcon(QIcon("./assets/play.png"))
        self.play_btn.clicked.disconnect()
        self.play_btn.clicked.connect(self.play_song)
        if self.song != self.song_widget.currentItem().data(Qt.UserRole):
            self.get_song()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        with open("./Assets/stylesheet", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        QMessageBox.warning(None, "Error", "Could not load stylesheet")
        app.Exit()

    window = Window()
    sys.exit(app.exec_())
