import uuid
from typing import List, Optional
from model.playlist import Playlist
from db.db_manager import DBManager
from util.common_util import now


def upsert_playlists(db: DBManager, playlists: List[Playlist]) -> List[Playlist]:
    current_time = now()
    for p in playlists:
        p.id = p.id or str(uuid.uuid4())
        p.createdAt = p.createdAt or current_time
        p.updatedAt = current_time
        db.execute(
            """
            INSERT OR REPLACE INTO playlists
            (id, name, createdBy, createdAt, updatedAt, deleted)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (p.id, p.name, p.createdBy, p.createdAt, p.updatedAt, int(p.deleted)),
        )
    return playlists


def get_playlists_since(db: DBManager, since: Optional[str] = None):
    if since:
        return db.fetchall("SELECT * FROM playlists WHERE updatedAt > ?", (since,))
    return db.fetchall("SELECT * FROM playlists")
