from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


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
    ratings = relationship("Rating", back_populates="song")


class Rating(Base):
    __tablename__ = "rating"
    id = Column(Integer, primary_key=True, index=True)
    song_id = Column(String, ForeignKey("songs.id"), nullable=False)
    star_rating = Column(Float, default=0.0)
    song = relationship("Song", back_populates="ratings")