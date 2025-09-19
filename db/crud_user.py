import uuid
from typing import List, Optional
from model.user import User
from util.common_util import now
from db.db_manager import DBManager


def upsert_users(db: DBManager, users: List[User]) -> List[User]:
    current_time = now()
    for u in users:
        u.id = u.id or str(uuid.uuid4())
        u.createdAt = u.createdAt or current_time
        u.updatedAt = current_time
        db.execute(
            """
            INSERT OR REPLACE INTO users (id, username, createdAt, updatedAt, deleted)
            VALUES (?, ?, ?, ?, ?)
            """,
            (u.id, u.username, u.createdAt, u.updatedAt, int(u.deleted)),
        )
    return users


def get_users_since(db: DBManager, since: Optional[str] = None):
    if since:
        return db.fetchall("SELECT * FROM users WHERE updatedAt > ?", (since,))
    return db.fetchall("SELECT * FROM users")
