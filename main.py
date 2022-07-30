import sys
import os
import random
import requests
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import vlc
import __init__
from backend.database import session, Songs
from backend.player import Player
from backend.platforms import spotify, youtube, soundcloud


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 600, 450)
        self.setWindowTitle("X-Platform Music Player")
        self._player = Player()
        self.UiComponents()

        self.show()

    # method for widgets
    def UiComponents(self):
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

        # Create Image Label
        self.image = QLabel(self)
        self.image.setGeometry(100, 50, 200, 200)
        self.get_image()
        self.image.setScaledContents(True)

        # Create slider for song
        self.progress_bar = QSlider(Qt.Horizontal, self)
        self.progress_bar.setGeometry(125, 275, 250, 30)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTickPosition(QSlider.TicksBelow)
        self.progress_bar.setTickInterval(1000)
        self.progress_bar.setValue(0)

        self.time_label = QLabel(self)
        self.time_label.setGeometry(160, 300, 250, 30)
        self.time = str(datetime.timedelta(seconds=0))[2:]
        self.total_time = str(datetime.timedelta(seconds=0))[2:]
        self.time_label.setText(f"{self.time} / {self.total_time}")

        # Create volume slider
        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setGeometry(25, 275, 75, 30)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)
        self.volume_slider.setTickPosition(QSlider.TicksBelow)
        self.volume_slider.setTickInterval(10)
        self.volume_slider.valueChanged.connect(self.volume_change)

        # Create buttons
        self.prev_btn = QPushButton(self)
        self.prev_btn.setGeometry(25, 325, 100, 100)
        self.prev_btn.clicked.connect(self.prev_song)
        self.prev_btn.setIcon(QIcon("./assets/prev.png"))
        self.prev_btn.setIconSize(QSize(100, 100))

        self.play_btn = QPushButton(self)
        self.play_btn.setGeometry(150, 325, 100, 100)
        self.play_btn.clicked.connect(self.get_song)
        self.play_btn.setIcon(QIcon("./assets/play.png"))
        self.play_btn.setIconSize(QSize(100, 100))

        next_btn = QPushButton(self)
        next_btn.setGeometry(275, 325, 100, 100)
        next_btn.clicked.connect(self.next_song)
        next_btn.setIcon(QIcon("./assets/next.png"))
        next_btn.setIconSize(QSize(100, 100))

        shuffle_btn = QPushButton(self)
        shuffle_btn.setGeometry(425, 375, 50, 50)
        shuffle_btn.clicked.connect(self.shuffle_music)
        shuffle_btn.setIcon(QIcon("./assets/shuffle.png"))
        shuffle_btn.setIconSize(QSize(50, 50))

        repeat_btn = QPushButton(self)
        repeat_btn.setGeometry(500, 375, 50, 50)
        repeat_btn.clicked.connect(self.repeat_music)
        repeat_btn.setIcon(QIcon("./assets/repeat.png"))
        repeat_btn.setIconSize(QSize(50, 50))

        # Create widget with songs
        self.song_widget = QListWidget(self)
        self.song_widget.setGeometry(400, 25, 175, 330)

        self.repeat = False
        self.get_songs()

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
        self.song_widget.clear()
        new_list = random.sample(self.songs, len(self.songs))
        for song in new_list:
            self.song_widget.addItem(song.title)
            self.song_widget.item(self.song_widget.count() - 1).setData(
                Qt.UserRole, song
            )
        self.songs = new_list
        self.current_row = 0

    def repeat_music(self):
        self.repeat = not self.repeat

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
        if not self.repeat:
            self.current_row += 1
        self.song_widget.setCurrentRow(self.current_row)

        self.get_song()

    def prev_song(self):
        self.current_row -= 1
        self.song_widget.setCurrentRow(self.current_row)

        self.get_song()

    def get_song(self):
        try:
            self.song = self.song_widget.currentItem().data(Qt.UserRole)
            self.current_row = self.song_widget.currentRow()
        except AttributeError:
            self.current_row = 0
            self.song_widget.setCurrentRow(self.current_row)
            self.song = self.song_widget.currentItem().data(Qt.UserRole)

        self._player.player.set_pause(1)
        self._player.get_song(self.song)
        self.get_image(self.song.thumbnail)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_slider)
        self.timer.start(200)

        # Get total lenght of player
        lenght = self._player.player.get_length()
        self.progress_bar.setRange(0, int(lenght))

        self.play_song()
        # If song ended, play next song
        if self._player.player.get_state() == vlc.State.Ended:
            self.next_song()

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

    def update_slider(self):
        if self.progress_bar.value() == int(self._player.player.get_length()):
            self.next_song()

        self.progress_bar.setValue(self._player.player.get_time())

        # Update progress_bar with current time
        self.time = str(datetime.timedelta(
            seconds=int(self._player.player.get_time() / 1000)))[2:]
        self.total_time = str(datetime.timedelta(
            seconds=int(self._player.player.get_length() / 1000)))[2:]
        self.time_label.setText(f"{self.time} / {self.total_time}")

    def volume_change(self):
        self._player.player.audio_set_volume(self.volume_slider.value())


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
