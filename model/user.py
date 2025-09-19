from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[str]
    username: str
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None
    deleted: bool = False
