from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Track(BaseModel):
    id: Optional[str]
    playlistId: str
    title: str
    artist: str
    duration: int
    addedBy: str
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None
    deleted: bool = False