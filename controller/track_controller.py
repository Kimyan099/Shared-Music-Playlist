from fastapi import APIRouter
from typing import List, Optional
from model.track import Track
from db import crud_track

router = APIRouter()

@router.post("/batch")
def upsert_tracks(tracks: List[Track]):
    return crud_track.upsert_tracks(tracks)

@router.get("/sync")
def sync_tracks(since: Optional[str] = None):
    return crud_track.get_tracks_since(since)
