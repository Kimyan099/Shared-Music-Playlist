import uuid
from typing import List, Optional

from db.db import Database
from model.user import User
from util.common_util import now

def upsert_users(database: Database, users: List[User]) -> List[User]:
    with database.get_connection() as conn:
        cursor = conn.cursor()
        current_time = now()

        for u in users:
            u.id = u.id or str(uuid.uuid4())
            u.createdAt = u.createdAt or current_time
            u.updatedAt = current_time
            cursor.execute("""
                INSERT OR REPLACE INTO users (id, username, createdAt, updatedAt, deleted)
                VALUES (?, ?, ?, ?, ?)
            """, (u.id, u.username, u.createdAt, u.updatedAt, int(u.deleted)))
    return users

def get_users_since(database: Database, since: Optional[str] = None):
    with database.get_connection() as conn:
        cursor = conn.cursor()
        if since:
            cursor.execute("SELECT * FROM users WHERE updatedAt > ?", (since,))
        else:
            cursor.execute("SELECT * FROM users")
        return cursor.fetchall()

