from PyQt5.QtWidgets import QPushButton, QLabel, QWidget
from PyQt5.QtGui import QFont
from __init__ import VERSION, ROOT, r
import webbrowser
from configparser import ConfigParser
import sys


class UpdateCheckWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 300, 350)
        self.setFixedSize(self.size())
        self.setWindowTitle("Update checker")
        self.config = ConfigParser()
        self.config.read(f"{ROOT}\\backend\\config.ini")
        self.UIComponents()

    def UIComponents(self):
        self.title = QLabel(self)
        self.title.setText("There is a new version of the program available!")
        self.title.setFont(QFont("Arial", 20))
        self.title.move(10, 10)
        self.title.resize(300, 30)

        self.sub_title = QLabel(self)
        self.sub_title.setText("Current version: " + VERSION)
        self.sub_title.setFont(QFont("Arial", 12))
        self.sub_title.move(10, 50)
        self.sub_title.resize(300, 30)

        self.sub_title_2 = QLabel(self)
        self.sub_title_2.setText("New version: " + r.text)
        self.sub_title_2.setFont(QFont("Arial", 12))
        self.sub_title_2.move(10, 80)
        self.sub_title_2.resize(300, 30)

        self.question = QLabel(self)
        self.question.setText("Do you want to download the new version?")
        self.question.move(10, 110)
        self.question.resize(300, 30)
        self.question.setFont(QFont("Arial", 10))
        self.question.wordWrap()

        self.yes_btn = QPushButton(self)
        self.yes_btn.setText("Yes")
        self.yes_btn.move(40, 150)
        self.yes_btn.resize(100, 30)
        self.yes_btn.clicked.connect(self.yes_btn_clicked)

        self.no_btn = QPushButton(self)
        self.no_btn.setText("No")
        self.no_btn.move(160, 150)
        self.no_btn.resize(100, 30)
        self.no_btn.clicked.connect(self.no_btn_clicked)

    def yes_btn_clicked(self):
        webbrowser.open("https://github.com/RealSoerensen/XPLAT-MusicPlayer")
        sys.exit()

    def no_btn_clicked(self):
        self.close()
