from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///backend/songs.sqlite')
base = declarative_base()


class Songs(base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    online = Column(String)
    title = Column(String)
    url = Column(String)
    thumbnail = Column(String)


Session = sessionmaker(bind=engine)
session = Session()
