import uuid
from typing import List, Optional
from db.db import Database
from model.track import Track
from util.common_util import now


def upsert_tracks(database: Database, tracks: List[Track]) -> List[Track]:
    with database.get_connection() as conn:
        cursor = conn.cursor()
        current_time = now()

        for t in tracks:
            t.id = t.id or str(uuid.uuid4())
            t.createdAt = t.createdAt or current_time
            t.updatedAt = current_time
            cursor.execute("""
                INSERT OR REPLACE INTO tracks 
                (id, playlistId, title, artist, duration, addedBy, createdAt, updatedAt, deleted)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (t.id, t.playlistId, t.title, t.artist, t.duration, t.addedBy, t.createdAt, t.updatedAt, int(t.deleted)))
    return tracks


def get_tracks_since(database: Database, since: Optional[str] = None):
    with database.get_connection() as conn:
        cursor = conn.cursor()
        if since:
            cursor.execute("SELECT * FROM tracks WHERE updatedAt > ?", (since,))
        else:
            cursor.execute("SELECT * FROM tracks")
        return cursor.fetchall()


def select_tracks_by_ids(database: Database, ids: List[str]):
    if not ids:
        return []
    placeholders = ",".join("?" for _ in ids)
    sql = f"SELECT * FROM tracks WHERE id IN ({placeholders})"
    with database.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, tuple(ids))
        return cursor.fetchall()
