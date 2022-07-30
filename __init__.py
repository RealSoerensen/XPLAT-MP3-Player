from backend.database import session, Songs
import os
import requests
import webbrowser
import sys
from PyQt5.QtWidgets import *

VERSION = "0.1.0"
# Check if version is up to date

r = requests.get("https://aboutme.soerensen.repl.co/version.txt")
outdated = False
if r.text != VERSION:
    outdated = True
    app = QApplication(sys.argv)
    msgbox = QMessageBox.warning(
        None,
        "Warning",
        f"Version {r.text} is available.\nDo you wish to update?",
        QMessageBox.Yes | QMessageBox.No,
    )
    if msgbox == QMessageBox.Yes:
        webbrowser.open("https://github.com/RealSoerensen/XPLAT-MusicPlayer")
        exit()


ROOT = os.path.dirname(os.path.abspath(__file__))

session.execute(
    "CREATE TABLE IF NOT EXISTS songs (id INTEGER PRIMARY KEY, online BOOLEAN, title TEXT, url TEXT, thumbnail TEXT)")
session.commit()

os.add_dll_directory(ROOT + r"\\assets\\dll")

for song in os.listdir(ROOT + r"\\assets\\downloads"):
    if song.endswith(".part"):
        os.remove(ROOT + r"\\assets\\downloads\\" + song)
    if song.endswith(".mp3") and session.query(Songs).filter(Songs.title == song).first() is None:
        session.add(Songs(online=False, title=song,
                    url=f"{ROOT}\\assets\\downloads\\{song}"))
        session.commit()
        print(f"Added {song}")
