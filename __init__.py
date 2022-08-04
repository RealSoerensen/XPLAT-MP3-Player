from backend.database import session, Songs
import os
import requests
import sys
from PyQt5.QtWidgets import *
from configparser import ConfigParser

VERSION = "0.1.2"
ROOT = os.path.dirname(os.path.abspath(__file__))
r = requests.get("https://aboutme.soerensen.repl.co/version.txt")

if not os.path.exists(f"{ROOT}\\config.ini"):
    config = ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "launch_on_startup", "False")
    with open(f"{ROOT}\\backend\\config.ini", "w") as configfile:
        config.write(configfile)

app = QApplication(sys.argv)
try:
    with open(f"{ROOT}/assets/stylesheet", "r") as f:
        app.setStyleSheet(f.read())
except FileNotFoundError:
    QMessageBox.warning(None, "Error", "Could not load stylesheet")
    app.Exit()

outdated = False
if r.text != VERSION:
    outdated = True
    from backend.update_check import UpdateCheckWindow
    update_check_window = UpdateCheckWindow()
    update_check_window.show()
    app.exec_()


session.execute(
    "CREATE TABLE IF NOT EXISTS songs (id INTEGER PRIMARY KEY, title TEXT, url TEXT, thumbnail TEXT)")
session.commit()

os.add_dll_directory(f"{ROOT}\\assets\\dll")

for song in os.listdir(f"{ROOT}\\assets\\downloads"):
    if song.endswith(".part"):
        os.remove(f"{ROOT}\\assets\\downloads\\" + song)
    if song.endswith(".mp3") and session.query(Songs).filter(Songs.title == song).first() is None:
        session.add(Songs(title=song,
                    url=f"{ROOT}\\assets\\downloads\\{song}"))
        session.commit()
        print(f"Added {song}")
