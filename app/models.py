from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Song(Base):
    __tablename__ = "songs"
    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    danceability = Column(Float)
    energy = Column(Float)
    tempo = Column(Float)
    duration_ms = Column(Integer)
    num_sections = Column(Integer)
    num_segments = Column(Integer)
    star_rating = Column(Float, default=0.0)  # Nice-to-have feature
