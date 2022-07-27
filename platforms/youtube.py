from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pafy
from backend.database import session, Song


class YouTube(QMainWindow):
    window_closed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle("Add from YouTube")
        self.songs = session.query(Song).all()

        self.UIComponents()

    def UIComponents(self):
        self.title = QLabel(self)
        self.title.setText("Enter a YouTube URL")
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

        if not url:
            QMessageBox.warning(self, "Warning", "Please enter a URL")
            return

        try:
            video = pafy.new(url)
        except Exception:
            QMessageBox.warning(self, "Warning", "Invalid URL")
            return
        try:
            title = video.title
            thumbnail = video.thumb
        except:
            pass

        for x in self.songs:
            if title == x.title:
                msgbox = QMessageBox.warning(
                    self,
                    "Warning",
                    "Song already exists\nDo you wish to add it anyway?",
                    QMessageBox.Yes | QMessageBox.No,
                )
                if msgbox == QMessageBox.No:
                    return

        self.add_song_to_list(title, url, thumbnail)

        QMessageBox.information(self, "Success", "Song added successfully")

    def add_song_to_list(self, title, url, thumbnail=None):
        session.add(Song(platform="youtube", title=title, url=url, thumbnail=thumbnail))
        session.commit()
        self.songs = session.query(Song).all()

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()
