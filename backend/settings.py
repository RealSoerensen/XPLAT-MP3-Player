from PyQt5.QtWidgets import QPushButton, QLabel, QWidget, QCheckBox, QMessageBox
from PyQt5.QtGui import QFont
from __init__ import VERSION, r, session, Songs, ROOT
import os
from configparser import ConfigParser
from backend.update_check import UpdateCheckWindow
import getpass

USER_NAME = getpass.getuser()


class Settings(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 300, 350)
        self.setFixedSize(self.size())
        self.setWindowTitle("Settings")

        self.config = ConfigParser()
        self.config.read(rf"{ROOT}\\backend\\config.ini")
        self.launch = self.config.getboolean("Settings", "launch_on_startup")

        self.UIComponents()

    def UIComponents(self):
        self.title = QLabel(self)
        self.title.setText("Settings")
        self.title.setFont(QFont("Arial", 20))
        self.title.move(10, 10)
        self.title.resize(300, 30)

        # Check for updates
        self.check_version = QPushButton(self)
        self.check_version.setText("Check for updates")
        self.check_version.move(10, 50)
        self.check_version.resize(280, 30)
        self.check_version.clicked.connect(self.check_version_clicked)

        # Delete all songs
        self.delete_all_songs = QPushButton(self)
        self.delete_all_songs.setText("Delete all songs")
        self.delete_all_songs.move(10, 90)
        self.delete_all_songs.resize(280, 30)
        self.delete_all_songs.clicked.connect(self.delete_all_songs_clicked)

        # Launch on startup
        self.launch_on_startup = QCheckBox(self)
        self.launch_on_startup.setText("Launch on startup")
        self.launch_on_startup.move(10, 130)
        self.launch_on_startup.resize(280, 30)
        if self.launch:
            self.launch_on_startup.setChecked(True)
        self.launch_on_startup.clicked.connect(self.launch_on_startup_clicked)

        self.close_btn = QPushButton(self)
        self.close_btn.setText("Close")
        self.close_btn.move(10, 300)
        self.close_btn.resize(280, 30)
        self.close_btn.clicked.connect(self.close_window)

    def check_version_clicked(self):
        if r.text != VERSION:
            self.update_check_window = UpdateCheckWindow()
            self.update_check_window.show()
        else:
            self.version_box = QMessageBox.information(
                None,
                "Information",
                "You are running the latest version.",
                QMessageBox.Ok,
            )

    def delete_all_songs_clicked(self):
        self.delete_all_songs_box = QMessageBox.warning(
            None,
            "Warning",
            "Are you sure you want to delete all songs?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if self.delete_all_songs_box == QMessageBox.Yes:
            self.songs = session.query(Songs).all()
            for song in self.songs:
                os.remove(
                    rf"{ROOT}\\assets\\downloads\\{song.title}")
                session.delete(song)
                session.commit()

    def launch_on_startup_clicked(self):
        bat_path = rf'C:\Users\{USER_NAME}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'
        if self.launch_on_startup.isChecked():
            self.config.set("Settings", "launch_on_startup", "True")
            with open(rf"{bat_path}\X-PlatPlayer.bat", "w") as f:
                f.write(f"@echo off\npython {ROOT}\\main.py")

        else:
            self.config.set("Settings", "launch_on_startup", "False")
            os.remove(
                rf"{bat_path}\\X-PlatPlayer.bat")

        with open(rf"{ROOT}\\backend\\config.ini", "w") as configfile:
            self.config.write(configfile)

    def close_window(self):
        self.close()
