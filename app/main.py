import os
from fastapi import FastAPI
from app.api.v1 import endpoints as v1_endpoints
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI()

app.include_router(v1_endpoints.router, prefix="/api/v1", tags=["songs"])

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def landing_page(request: Request):
    return templates.TemplateResponse("landing_page.html", {"request": request})

@app.get("/upload", response_class=HTMLResponse)
def serve_upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})
    
@app.get("/songs", response_class=HTMLResponse)
def read_songs_page(request: Request):
    return templates.TemplateResponse("songs.html", {"request": request})

@app.get("/search", response_class=HTMLResponse)
def search_song_page(request: Request):
    return templates.TemplateResponse("search_song.html", {"request": request})