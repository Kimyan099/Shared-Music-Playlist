import uuid
from typing import List, Optional
from db.db import Database
from model.playlist import Playlist
from util.common_util import now


def upsert_playlists(database: Database, playlists: List[Playlist]) -> List[Playlist]:
    with database.get_connection() as conn:
        cursor = conn.cursor()
        current_time = now()

        for p in playlists:
            p.id = p.id or str(uuid.uuid4())
            p.createdAt = p.createdAt or current_time
            p.updatedAt = current_time
            cursor.execute("""
                INSERT OR REPLACE INTO playlists (id, name, createdBy, createdAt, updatedAt, deleted)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (p.id, p.name, p.createdBy, p.createdAt, p.updatedAt, int(p.deleted)))
    return playlists


def get_playlists_since(database: Database, since: Optional[str] = None):
    with database.get_connection() as conn:
        cursor = conn.cursor()
        if since:
            cursor.execute("SELECT * FROM playlists WHERE updatedAt > ?", (since,))
        else:
            cursor.execute("SELECT * FROM playlists")
        return cursor.fetchall()
