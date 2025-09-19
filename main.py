from pathlib import Path

from fastapi import FastAPI
from db.db import Database
from db.db_manager import DBManager
from controller import user_controller, playlist_controller, track_controller
app = FastAPI(title="Shared Playlist Service")

# --- DB Manager Setup ---
BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "db" / "playlist.db"

database = Database(DB_FILE)
db_manager = DBManager(database)

user_controller.db = db_manager
playlist_controller.db = db_manager
track_controller.db = db_manager

# --- Include routers ---
app.include_router(user_controller.router, prefix="/users", tags=["users"])
app.include_router(playlist_controller.router, prefix="/playlists", tags=["playlists"])
app.include_router(track_controller.router, prefix="/tracks", tags=["tracks"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
