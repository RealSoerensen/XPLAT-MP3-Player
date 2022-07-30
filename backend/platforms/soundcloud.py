from urllib import response
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from sclib import SoundcloudAPI, Playlist
import os
from __init__ import ROOT
from backend.database import session, Songs


class SoundCloud(QWidget):
    window_closed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle("Add from SoundCloud")

        self.UIComponents()

    def UIComponents(self):
        self.title = QLabel(self)
        self.title.setText("Enter a URL/Playlist URL")
        self.title.setFont(QFont("Arial", 20))
        self.title.move(10, 10)
        self.title.resize(300, 30)

        self.input = QLineEdit(self)
        self.input.move(10, 50)
        self.input.resize(280, 30)

        self.add_btn = QPushButton(self)
        self.add_btn.setText("Add")
        self.add_btn.move(10, 90)
        self.add_btn.resize(280, 30)
        self.add_btn.clicked.connect(self.add_song)

    def add_song(self):
        url = self.input.text()
        self.input.clear()
        api = SoundcloudAPI()
        response = api.resolve(url)
        print(response)
        if type(response) is Playlist:
            for track in response.tracks:
                self.add_song_to_list(track, track.artwork_url)
        else:
            self.add_song_to_list(response, response.artwork_url)

    def add_song_to_list(self, track, thumbnail=None):
        filename = f"{track.artist} - {track.title}.mp3"
        if "/" or "\\" in filename:
            filename = filename.replace("/", "").replace("\\", "")

        path = rf"{ROOT}\\assets\\downloads\\{filename}"
        if os.path.exists(path):
            msgbox = QMessageBox.warning(
                self,
                "Warning",
                "Song already exists\nDo you wish to add it anyway?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if msgbox == QMessageBox.No:
                return

        with open(path, 'wb+') as fp:
            track.write_mp3_to(fp)

        session.add(Songs(online=False, title=filename,
                    url=path, thumbnail=thumbnail))
        session.commit()
        QMessageBox.information(self, "Success", "Song(s) added")

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()
