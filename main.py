from fastapi import FastAPI
from db.db import Database
from db.db_manager import DBManager
from db import crud_user, crud_playlist, crud_track
from controller import user_controller, playlist_controller, track_controller

# --- FastAPI app ---
app = FastAPI(title="Shared Playlist Service")

# --- Initialize DB ---
database = Database("db/playlist.db")  # file-based persistent DB
db_manager = DBManager(database)

# --- Inject DBManager into CRUD ---
crud_user.db = db_manager
crud_playlist.db = db_manager
crud_track.db = db_manager

# --- Include routers ---
app.include_router(user_controller.router, prefix="/users", tags=["users"])
app.include_router(playlist_controller.router, prefix="/playlists", tags=["playlists"])
app.include_router(track_controller.router, prefix="/tracks", tags=["tracks"])
