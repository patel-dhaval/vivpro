import json
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.api.v1.endpoints import get_db
from app.main import app
from app.db import Base
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://vivpro:vivprodemo@localhost:3306/vivproTest"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_upload_json():
    files = {
        'file': (
            'test.json',
            json.dumps({
                "id": {"0": "05KfyCEE6otdlT1pp2VIjP"},
                "title": {"0": "Test Song"},
                "danceability": {"0": 0.75},
                "energy": {"0": 0.8},
                "tempo": {"0": 120.0},
                "duration_ms": {"0": 200000},
                "num_sections": {"0": 4},
                "num_segments": {"0": 10},
                "star_rating": {"0": 0.0}
            }),
            'application/json'
        )
    }
    response = client.post("/api/v1/upload-json/", files=files)
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_read_song_by_title():
    
    response = client.get("/api/v1/songs/Test Song")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Song"

def test_read_song_not_found():
    response = client.get("/api/v1/songs/NonExistentTitle")
    assert response.status_code == 404
    assert response.json()["detail"] == "Song not found"

def test_rate_song():
    response = client.get("/api/v1/songs/")
    song_id = response.json()[0]["id"]

    rating_update = {"rating": 4.5}
    response = client.put(f"/api/v1/songs/{song_id}/rate", json=rating_update)
    assert response.status_code == 200
    assert response.json()["star_rating"] == 4.5

def test_rate_song_not_found():

    rating_update = {"rating": 4.5}
    response = client.put("/api/v1/songs/999/rate", json=rating_update)
    assert response.status_code == 404
    assert response.json()["detail"] == "Song not found"
