from pydantic import BaseModel

class SongBase(BaseModel):
    title: str
    danceability: float
    energy: float
    tempo: float
    duration_ms: int
    num_sections: int
    num_segments: int

class SongCreate(SongBase):
    pass

class Song(SongBase):
    id: str

    class Config:
        from_attributes = True

class SongWithRatings(BaseModel):
    song: Song
    average_rating: float
    rating_count: int

    class Config:
        from_attributes = True

class RatingUpdate(BaseModel):
    rating: float


class RatingBase(BaseModel):
    song_id: str
    star_rating: float

class RatingCreate(RatingBase):
    pass

class Rating(RatingBase):
    id: int

    class Config:
        from_attributes = True