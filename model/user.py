from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: Optional[str]
    username: str
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None
    deleted: bool = False
