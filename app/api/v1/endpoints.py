from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
import pandas as pd
from sqlalchemy.orm import Session
from typing import List
import json
from app import crud, schemas, db, models

router = APIRouter()

def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


@router.post("/upload-json/")
async def upload_json(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload a JSON file, process it, and insert the data into the database.
    """
    try:
        contents = await file.read()
        data = json.loads(contents)
        
        df = pd.DataFrame(data)
        
        print(df)

        if 'star_rating' not in df.columns:
            df['star_rating'] = 0.0

        for _, row in df.iterrows():
            song = models.Song(
                id=row['id'],
                title=row['title'],
                danceability=row['danceability'],
                energy=row['energy'],
                tempo=row['tempo'],
                duration_ms=row['duration_ms'],
                num_sections=row['num_sections'],
                num_segments=row['num_segments'],
                star_rating=row['star_rating']
            )
            db.add(song)
        db.commit()
        
        return {"status": "success", "message": "Data uploaded and processed successfully."}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred while processing the file: {e}")


@router.get("/songs/", response_model=List[schemas.Song])
def read_songs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve all songs with pagination.
    """
    songs = crud.get_songs(db, skip=skip, limit=limit)
    return songs


@router.get("/songs/{title}", response_model=schemas.Song)
def read_song(title: str, db: Session = Depends(get_db)):
    """
    Retrieve a song by its title.
    """
    song = crud.get_song_by_title(db, title=title)
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return song


@router.put("/songs/{song_id}/rate", response_model=schemas.Song)
def rate_song(song_id: str, rating_data: schemas.RatingUpdate, db: Session = Depends(get_db)):
    """
    Update the rating of a song by its ID.
    """
    song = crud.update_star_rating(db, song_id=song_id, rating=rating_data.rating)
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return song
