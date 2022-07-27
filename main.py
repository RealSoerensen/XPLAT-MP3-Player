from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import pickle
import os
import random
from platforms import spotify, youtube, soundcloud


class Window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__()
        with open("./assets/songs.pkl", "rb") as f:
            self.songs = pickle.load(f)

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle("X-Platform Music Player")
        self.UiComponents()

        self.show()

    # method for widgets
    def UiComponents(self):
        # Create Image Label
        self.image = QLabel(self)
        self.image.setGeometry(100, 50, 200, 200)
        self.image.setPixmap(QPixmap(self.get_image()))
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
        self.song_widget.setGeometry(400, 25, 175, 350)
        self.get_songs()

        # Create buttons
        prev_btn = QPushButton(self)
        prev_btn.setGeometry(25, 275, 100, 100)
        prev_btn.clicked.connect(self.prev_song)
        prev_btn.setIcon(QIcon("./assets/prev.png"))
        prev_btn.setIconSize(QSize(100, 100))

        play_btn = QPushButton(self)
        play_btn.setGeometry(150, 275, 100, 100)
        play_btn.clicked.connect(self.play_song)
        play_btn.setIcon(QIcon("./assets/play.png"))
        play_btn.setIconSize(QSize(100, 100))

        next_btn = QPushButton(self)
        next_btn.setGeometry(275, 275, 100, 100)
        next_btn.clicked.connect(self.next_song)
        next_btn.setIcon(QIcon("./assets/next.png"))
        next_btn.setIconSize(QSize(100, 100))
        self.repaint()

    def get_image(self):
        return "./assets/default.png"

    def get_songs(self):
        for x in self.songs:
            print(x)
            self.song_widget.addItem(str(x))
        self.song_widget.repaint()

    def shuffle_music(self):
        new_list = random.sample(self.songs, len(self.songs))
        self.songs = new_list
        self.song_widget.clear()
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

    def play_song(self):
        pass


if __name__ == '__main__':
    # check if songs.pkl exists
    if not os.path.exists("./assets/songs.pkl"):
        with open("./assets/songs.pkl", "wb") as f:
            pickle.dump({}, f)

    app = QApplication(sys.argv)
    try:
        with open('./Assets/stylesheet', 'r') as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        pass

    window = Window()
    sys.exit(app.exec_())
