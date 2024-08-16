from sqlalchemy.orm import Session
from . import models, schemas

def get_songs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Song).offset(skip).limit(limit).all()

def get_song_by_title(db: Session, title: str):
    return db.query(models.Song).filter(models.Song.title == title).first()

def create_song(db: Session, song: schemas.SongCreate):
    db_song = models.Song(**song.dict())
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song

def update_star_rating(db: Session, song_id: int, rating: float):
    db_song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if db_song:
        db_song.star_rating = rating
        db.commit()
        db.refresh(db_song)
    return db_song
