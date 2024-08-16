from pydantic import BaseModel

class SongBase(BaseModel):
    title: str
    danceability: float
    energy: float
    tempo: float
    duration_ms: int
    num_sections: int
    num_segments: int
    star_rating: float = 0.0

class SongCreate(SongBase):
    pass

class Song(SongBase):
    id: str

    class Config:
        from_attributes = True

class RatingUpdate(BaseModel):
    rating: float