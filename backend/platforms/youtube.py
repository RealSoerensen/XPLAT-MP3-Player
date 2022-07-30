from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from __init__ import ROOT
from backend.database import session, Songs
import youtube_dl


class YouTube(QMainWindow):
    window_closed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.setGeometry(300, 300, 300, 300)
        self.setFixedSize(self.size())
        self.setWindowTitle("Add from YouTube")

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

        video_info = youtube_dl.YoutubeDL().extract_info(url=url, download=False)

        for x in session.query(Songs).all():
            if video_info['title'] == x.title:
                msgbox = QMessageBox.warning(
                    self,
                    "Warning",
                    "Song already exists\nDo you wish to add it anyway?",
                    QMessageBox.Yes | QMessageBox.No,
                )
                if msgbox == QMessageBox.No:
                    return

        choice = QMessageBox.question(
            self, "Question", "Yes: Download\nNo: Online", QMessageBox.Yes | QMessageBox.No)

        if choice == QMessageBox.Yes:

            filename = f"{video_info['title']}.mp3"
            full_url = f"{ROOT}\\assets\\downloads{filename}"
            options = {
                'format': 'bestaudio/best',
                'keepvideo': False,
                'outtmpl': f"{ROOT}\\assets\\downloads\\{filename}",
            }

            try:
                with youtube_dl.YoutubeDL(options) as ydl:
                    ydl.download([video_info['webpage_url']])
            except Exception:
                QMessageBox.warning(self, "Warning", "Error downloading song")
                return

            self.add_song_to_list(
                False, video_info['title'], full_url, None)

        elif choice == QMessageBox.No:
            self.add_song_to_list(
                True, video_info['title'], video_info["webpage_url"], video_info['thumbnail'])

    def add_song_to_list(self, online, title, url, thumbnail=None):
        session.add(Songs(online=online, title=title,
                    url=url, thumbnail=thumbnail))
        session.commit()
        QMessageBox.information(self, "Success", "Song added successfully")

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()
