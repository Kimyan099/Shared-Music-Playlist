import uuid
from typing import List, Optional
from model.track import Track
from db.db_manager import DBManager
from util.common_util import now


def upsert_tracks(db: DBManager, tracks: List[Track]) -> List[Track]:
    current_time = now()
    for t in tracks:
        t.id = t.id or str(uuid.uuid4())
        t.createdAt = t.createdAt or current_time
        t.updatedAt = current_time
        db.execute(
            """
            INSERT OR REPLACE INTO tracks
            (id, playlistId, title, artist, duration, addedBy, createdAt, updatedAt, deleted)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (t.id, t.playlistId, t.title, t.artist, t.duration, t.addedBy, t.createdAt, t.updatedAt, int(t.deleted)),
        )
    return tracks


def get_tracks_since(db: DBManager, since: Optional[str] = None):
    if since:
        return db.fetchall("SELECT * FROM tracks WHERE updatedAt > ?", (since,))
    return db.fetchall("SELECT * FROM tracks")


def select_tracks_by_ids(db: DBManager, ids: List[str]):
    if not ids:
        return []
    placeholders = ",".join("?" for _ in ids)
    sql = f"SELECT * FROM tracks WHERE id IN ({placeholders})"
    return db.fetchall(sql, tuple(ids))
