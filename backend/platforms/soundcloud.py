from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from sclib import SoundcloudAPI
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
        self.title.setText("Enter a SoundCloud URL")
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
        api = SoundcloudAPI()
        track = api.resolve(self.input.text())
        filename = f"{track.artist} - {track.title}.mp3"
        path = rf"{ROOT}\assets\downloads\{filename}"
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

        self.add_song_to_list(
            track.title, path, track.artwork_url)

        QMessageBox.information(self, "Success", "Song added successfully")

    def add_song_to_list(self, title, path, thumbnail=None):
        session.add(Songs(platform="soundcloud", title=title,
                    url=path, thumbnail=thumbnail))
        session.commit()

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()
