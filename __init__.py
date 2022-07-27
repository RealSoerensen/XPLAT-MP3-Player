from backend.database import session

session.execute(
    "CREATE TABLE IF NOT EXISTS songs (id INTEGER PRIMARY KEY, title TEXT, url TEXT, thumbnail TEXT)")
session.commit()
