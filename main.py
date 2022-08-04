import sys
import os
import random
import requests
import datetime
import webbrowser
from __init__ import ROOT, VERSION, outdated, app
from backend.database import session, Songs
from backend.player import Player
from backend.platforms import soundcloud, youtube
from backend.about import About
from backend.settings import Settings
from PyQt5.QtWidgets import QMessageBox, QPushButton, QFrame, QListWidget, QMenu, QLabel, QAction, QSlider, QApplication, QMainWindow
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer, QSize, QEvent


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 600, 450)
        self.setFixedSize(self.size())
        self.setWindowTitle("MP3 Player")
        self._player = Player()
        self.UiComponents()

        self.show()

    def UiComponents(self):
        # create a menu bar
        menu_bar = self.menuBar()
        add_menu = menu_bar.addMenu("Add")
        yt_menu = QAction("From Youtube", self)
        add_menu.addAction(yt_menu)
        yt_menu.triggered.connect(self.add_yt)
        sc_menu = QAction("From SoundCloud", self)
        add_menu.addAction(sc_menu)
        sc_menu.triggered.connect(self.add_sc)

        control_menu = menu_bar.addMenu("Control")
        shuffle_menu = QAction("Shuffle", self)
        control_menu.addAction(shuffle_menu)
        shuffle_menu.triggered.connect(self.shuffle_music)
        repeat_menu = QAction("Repeat", self)
        control_menu.addAction(repeat_menu)
        repeat_menu.triggered.connect(self.repeat_music)

        about_menu = menu_bar.addMenu("Options")
        settings = QAction("Settings", self)
        about_menu.addAction(settings)
        settings.triggered.connect(self.settings)
        project = QAction("About the project", self)
        about_menu.addAction(project)
        project.triggered.connect(self.about_project)
        exit = QAction("Exit", self)
        about_menu.addAction(exit)
        exit.triggered.connect(self.close)

        self.videoframe = QFrame()
        self.videoframe.setObjectName("videoframe")
        self.videoframe.setAutoFillBackground(True)

        # Create Image Label
        self.image = QLabel(self)
        self.image.setGeometry(100, 50, 200, 200)
        self.get_image()
        self.image.setScaledContents(True)

        # Create slider for song
        self.progress_bar = QSlider(Qt.Horizontal, self)
        self.progress_bar.setGeometry(125, 275, 250, 30)
        self.progress_bar.setTickInterval(100)
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
        self.volume_slider.setTickInterval(10)
        self.volume_slider.valueChanged.connect(self.volume_change)

        # Create buttons
        self.prev_btn = QPushButton(self)
        self.prev_btn.setGeometry(25, 325, 100, 100)
        self.prev_btn.clicked.connect(self.prev_song)
        self.prev_btn.setIcon(QIcon(f"{ROOT}/assets/prev.png"))
        self.prev_btn.setIconSize(QSize(100, 100))

        self.play_btn = QPushButton(self)
        self.play_btn.setGeometry(150, 325, 100, 100)
        self.play_btn.clicked.connect(self.get_song)
        self.play_btn.setIcon(QIcon(f"{ROOT}/assets/play.png"))
        self.play_btn.setIconSize(QSize(100, 100))

        next_btn = QPushButton(self)
        next_btn.setGeometry(275, 325, 100, 100)
        next_btn.clicked.connect(self.next_song)
        next_btn.setIcon(QIcon(f"{ROOT}/assets/next.png"))
        next_btn.setIconSize(QSize(100, 100))

        shuffle_btn = QPushButton(self)
        shuffle_btn.setGeometry(425, 375, 50, 50)
        shuffle_btn.clicked.connect(self.shuffle_music)
        shuffle_btn.setIcon(QIcon(f"{ROOT}/assets/shuffle.png"))
        shuffle_btn.setIconSize(QSize(50, 50))

        repeat_btn = QPushButton(self)
        repeat_btn.setGeometry(500, 375, 50, 50)
        repeat_btn.clicked.connect(self.repeat_music)
        repeat_btn.setIcon(QIcon(f"{ROOT}/assets/repeat.png"))
        repeat_btn.setIconSize(QSize(50, 50))

        # Create widget with songs
        self.song_widget = QListWidget(self)
        self.song_widget.setGeometry(400, 25, 175, 330)
        self.song_widget.installEventFilter(self)

        # Create a label for version
        self.version_label = QLabel(self)
        self.version_label.setGeometry(560, 430, 100, 20)
        self.version_label.setText(f"v{VERSION}")
        if outdated:
            self.version_label.setToolTip("Update available")
            self.version_label.setStyleSheet("color: red")
            # make label clickable
            self.version_label.mousePressEvent = self.update_available

        self.repeat = False
        self.get_songs()

    def get_image(self, url=None):
        default = QPixmap(f"{ROOT}/assets/default.png")
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
                with open(f"{ROOT}/assets/thumbnail.png", "wb") as f:
                    f.write(thumbnail.content)
                self.image.setPixmap(QPixmap(f"{ROOT}/assets/thumbnail.png"))
                self.image.keepAspectRatio = False
                os.remove(f"{ROOT}/assets/thumbnail.png")

        except Exception:
            self.image.setPixmap(default)

    def get_songs(self):
        self.song_widget.clear()
        try:
            self.songs = session.query(Songs).all()
            for song in self.songs:
                self.song_widget.addItem(song.title)
                self.song_widget.item(self.song_widget.count() - 1).setData(
                    Qt.UserRole, song
                )
        except Exception:
            return

    def shuffle_music(self):
        self.song_widget.clear()
        new_list = random.sample(self.songs, len(self.songs))
        for song in new_list:
            self.song_widget.addItem(song.title)
            self.song_widget.item(self.song_widget.count() - 1).setData(
                Qt.UserRole, song
            )
        self.songs = new_list
        self.get_song()

    def repeat_music(self):
        self.repeat = not self.repeat

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
            if len(self.songs) == 0:
                return
            self.current_row = 0
            self.song_widget.setCurrentRow(self.current_row)
            self.song = self.song_widget.currentItem().data(Qt.UserRole)

        self._player.player.set_pause(1)
        self._player.play_song(self.song)
        self.get_image(self.song.thumbnail)

        self._player.player.set_hwnd(self.videoframe.winId())

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_slider)
        self.timer.start(200)

        # timer to check if song is finished
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.check_song_finished)
        self.timer2.start(1000)

        self.play_song()

    def play_song(self):
        self._player.player.set_pause(0)
        self.play_btn.setIcon(QIcon(f"{ROOT}/assets/pause.png"))
        self.play_btn.clicked.disconnect()
        self.play_btn.clicked.connect(self.pause_song)

    def pause_song(self):
        self._player.player.set_pause(1)
        self.play_btn.setIcon(QIcon(f"{ROOT}/assets/play.png"))
        self.play_btn.clicked.disconnect()
        self.play_btn.clicked.connect(self.play_song)

    def update_slider(self):
        length = self._player.player.get_length()
        self.progress_bar.setRange(0, length)
        self.progress_bar.setValue(self._player.player.get_time())

        self.progress_bar.sliderMoved.connect(self.slider_moved)

        # Update progress_bar with current time
        self.time = str(datetime.timedelta(
            seconds=int(self._player.player.get_time() / 1000)))[2:]
        self.total_time = str(datetime.timedelta(
            seconds=int(self._player.player.get_length() / 1000)))[2:]
        self.time_label.setText(f"{self.time} / {self.total_time}")

        try:
            if self.song != self.song_widget.currentItem().data(Qt.UserRole):
                self.get_song()
        except AttributeError:
            pass

    def slider_moved(self):
        self.timer.stop()
        self._player.player.set_time(self.progress_bar.value())
        self.timer.start()

    def check_song_finished(self):
        if int(self._player.player.get_time() / 1000) == int(self._player.player.get_length() / 1000):
            self.next_song()

    def volume_change(self):
        self._player.player.audio_set_volume(self.volume_slider.value())

    def delete_song(self):
        try:
            song = self.song_widget.currentItem().data(Qt.UserRole)
            # get song in database
            song = session.query(Songs).filter_by(id=song.id).first()
            # delete song from downloads
            os.remove(
                rf"{ROOT}\\assets\\downloads\\{song.title}")
            session.delete(song)
            session.commit()
            self.get_songs()
        except AttributeError:
            pass

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self.song_widget:
            menu = QMenu()
            menu.addAction("Delete")
            if menu.exec_(event.globalPos()):
                self.delete_song()
                return True
        return super().eventFilter(source, event)

    def update_available(self, _):
        webbrowser.open(
            "https://github.com/RealSoerensen/XPLAT-MusicPlayer")

    def settings(self):
        self.settings_win = Settings()
        self.settings_win.show()

    def about_project(self):
        self.about_win = About()
        self.about_win.show()

    def close(self):
        self._player.player.stop()
        sys.exit()


if __name__ == "__main__":
    window = Window()
    sys.exit(app.exec_())
