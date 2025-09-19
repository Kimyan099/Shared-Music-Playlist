# main.py
from fastapi import FastAPI
from db.db import db  # your global Database instance
from db.db_manager import DBManager
from controller import user_controller, playlist_controller, track_controller

app = FastAPI(title="Shared Playlist Service")

# Use DBManager wrapper to interact with the database
db_manager = DBManager(db)

# --- Routers ---
app.include_router(user_controller.router, prefix="/users", tags=["users"])
app.include_router(playlist_controller.router, prefix="/playlists", tags=["playlists"])
app.include_router(track_controller.router, prefix="/tracks", tags=["tracks"])

# --- Simple health check ---
@app.get("/")
def root():
    return {"message": "Shared Playlist Service is running"}
