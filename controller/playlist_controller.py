from fastapi import APIRouter
from typing import List, Optional
from model.playlist import Playlist
from db.db_manager import DBManager
from db import crud_playlist

router = APIRouter()
db: DBManager = None  # Will be injected from main.py

@router.get("/")
def list_playlists():
    return crud_playlist.get_playlists_since(db)

@router.post("/batch")
def upsert_playlists(playlists: List[Playlist]):
    return crud_playlist.upsert_playlists(db, playlists)


@router.get("/sync")
def sync_playlists(since: Optional[str] = None):
    return crud_playlist.get_playlists_since(db)


