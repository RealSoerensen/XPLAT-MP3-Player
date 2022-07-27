from backend.database import session
import os

session.execute(
    "CREATE TABLE IF NOT EXISTS songs (id INTEGER PRIMARY KEY, platform TEXT, title TEXT, url TEXT, thumbnail TEXT)")
session.commit()

ROOT = os.path.dirname(os.path.abspath(__file__))