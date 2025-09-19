from fastapi import APIRouter
from typing import List, Optional
from model.user import User
from db import crud_user

router = APIRouter()

@router.post("/batch")
def upsert_users(users: List[User]):
    return crud_user.upsert_users(users)

@router.get("/sync")
def sync_users(since: Optional[str] = None):
    return crud_user.get_users_since(since)
