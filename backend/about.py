from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class About(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.setGeometry(300, 300, 300, 350)
        self.setWindowTitle("Add from YouTube")

        self.UIComponents()

    def UIComponents(self):
        self.title = QLabel(self)
        self.title.setText("About the project")
        self.title.setFont(QFont("Arial", 20))
        self.title.move(10, 10)
        self.title.resize(300, 30)

        self.text = QLabel(self)
        self.text.setText("""
Hello! I'm Patrick Sørensen. 
Thanks for checking out my project.
This project is a music player that I made for my own use.
The project came to life when I had songs from multiple sources and didn't have a way
to play them all at once.
Using this music player you can play music from Soundcloud, YouTube, and from local files.
Due to the limits of the Soundcloud API, you can't stream music from Soundcloud but only download it.
The music player is still in development and I'm working on it.
If you have any suggestions, feedback, questions or found a bug, please raise an issue on the GitHub page.
I hope you enjoy the project!
        """)
        self.text.setGeometry(10, 50, 280, 250)
        self.text.setWordWrap(True)

        self.close_btn = QPushButton(self)
        self.close_btn.setText("Close")
        self.close_btn.move(10, 300)
        self.close_btn.resize(280, 30)
        self.close_btn.clicked.connect(self.close_window)

    def close_window(self):
        self.window_closed.emit()
        self.close()
