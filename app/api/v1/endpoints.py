from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
import pandas as pd
from sqlalchemy.orm import Session
from typing import List, Optional
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
            )
            db.add(song)
        db.commit()
        
        return {"status": "success", "message": "Data uploaded and processed successfully."}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred while processing the file: {e}")


@router.get("/songs/", response_model=List[schemas.SongWithRatings])
def read_songs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve all songs with pagination.
    """
    songs = crud.get_songs(db, skip=skip, limit=limit)
    return songs


@router.get("/songs/search", response_model=List[schemas.Song])
def search_songs(
    title: Optional[str] = None,
    danceability: Optional[float] = None,
    energy: Optional[float] = None,
    tempo: Optional[float] = None,
    db: Session = Depends(get_db),
):
    """
    Search for songs based on various optional parameters.
    """
    songs = crud.search_songs(
        db,
        title=title,
        danceability=danceability,
        energy=energy,
        tempo=tempo,
    )
    
    if not songs:
        raise HTTPException(status_code=404, detail="No songs found")
    
    return songs


@router.post("/ratings", response_model=schemas.Rating)
def create_or_update_rating(rating_data: schemas.RatingCreate, db: Session = Depends(get_db)):
    """
    Create or update a rating for a song.
    """
    rating = crud.create_or_update_rating(db=db, rating_data=rating_data)
    return rating