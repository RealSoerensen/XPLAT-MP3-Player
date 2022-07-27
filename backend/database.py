from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///backend/songs.sqlite', echo=True)
base = declarative_base()


class Song(base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    thumbnail = Column(String)


Session = sessionmaker(bind=engine)
session = Session()
