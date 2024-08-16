from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import func
from typing import List, Optional

def get_songs(db: Session, skip: int = 0, limit: int = 10) -> List[schemas.SongWithRatings]:
    # Query to get songs along with their average rating and rating count
    songs_with_ratings = (
        db.query(
            models.Song,
            func.coalesce(func.avg(models.Rating.star_rating), 0).label("average_rating"),
            func.count(models.Rating.id).label("rating_count")
        )
        .outerjoin(models.Rating, models.Song.id == models.Rating.song_id)
        .group_by(models.Song.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    # Convert results to the expected format
    result = [
        schemas.SongWithRatings(
            song=song,
            average_rating=average_rating,
            rating_count=rating_count
        )
        for song, average_rating, rating_count in songs_with_ratings
    ]

    return result

def search_songs(
    db: Session,
    title: Optional[str] = None,
    danceability: Optional[float] = None,
    energy: Optional[float] = None,
    tempo: Optional[float] = None,
) -> List[models.Song]:
    query = db.query(models.Song)

    if title:
        query = query.filter(models.Song.title.ilike(f"%{title}%"))
    if danceability is not None:
        query = query.filter(models.Song.danceability == danceability)
    if energy is not None:
        query = query.filter(models.Song.energy == energy)
    if tempo is not None:
        query = query.filter(models.Song.tempo == tempo)
    
    return query.all()

def create_song(db: Session, song: schemas.SongCreate):
    db_song = models.Song(**song.dict())
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song

def create_or_update_rating(db: Session, rating_data: schemas.RatingCreate):
    existing_rating = db.query(models.Rating).filter(models.Rating.song_id == rating_data.song_id).first()

    # Create a new rating
    new_rating = models.Rating(**rating_data.dict())
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating