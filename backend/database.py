from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

ROOT = os.path.dirname(os.path.abspath(__file__))


engine = create_engine(f'sqlite:///{ROOT}\songs.sqlite')
base = declarative_base()


class Songs(base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    thumbnail = Column(String)


Session = sessionmaker(bind=engine)
session = Session()
