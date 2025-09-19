from fastapi import APIRouter
from typing import List, Optional
from model.playlist import Playlist
from db import crud_playlist

router = APIRouter()

@router.post("/batch")
def upsert_playlists(playlists: List[Playlist]):
    return crud_playlist.upsert_playlists(playlists)

@router.get("/sync")
def sync_playlists(since: Optional[str] = None):
    return crud_playlist.get_playlists_since(since)
