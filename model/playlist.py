from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Playlist(BaseModel):
    id: Optional[str]
    name: str
    createdBy: str
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None
    deleted: bool = False