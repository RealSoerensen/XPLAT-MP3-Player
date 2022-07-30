from backend.database import session, Songs
import os

session.execute(
    "CREATE TABLE IF NOT EXISTS songs (id INTEGER PRIMARY KEY, online BOOLEAN, title TEXT, url TEXT, thumbnail TEXT)")
session.commit()

ROOT = os.path.dirname(os.path.abspath(__file__))
os.add_dll_directory(ROOT + r"\\assets\\dll")

for song in os.listdir(ROOT + r"\\assets\\downloads"):
    if song.endswith(".part"):
        os.remove(ROOT + r"\\assets\\downloads\\" + song)
    if song.endswith(".mp3") and session.query(Songs).filter(Songs.title == song).first() is None:
        session.add(Songs(online=False, title=song,
                    url=f"{ROOT}\\assets\\downloads\\{song}"))
        session.commit()
        print(f"Added {song}")
