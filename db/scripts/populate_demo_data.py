from db.db import Database
from db.db_manager import DBManager
from db import crud_user, crud_playlist, crud_track
from model.user import User
from model.playlist import Playlist
from model.track import Track
from util.common_util import now
import uuid


# --- Connect to the persistent DB ---
database = Database("playlist.db")
db_manager = DBManager(database)

# --- Inject DB manager into CRUD ---
crud_user.db = db_manager
crud_playlist.db = db_manager
crud_track.db = db_manager

# --- Create some users ---
now_time = now()
users = [
    User(id=str(uuid.uuid4()), username="alice", createdAt=now_time, updatedAt=now_time, deleted=False),
    User(id=str(uuid.uuid4()), username="bob", createdAt=now_time, updatedAt=now_time, deleted=False),
]
crud_user.upsert_users(db_manager, users)

# --- Create playlists ---
playlists = [
    Playlist(id=str(uuid.uuid4()), name="Chill Vibes", createdBy=users[0].id, createdAt=now_time, updatedAt=now_time, deleted=False),
    Playlist(id=str(uuid.uuid4()), name="Workout", createdBy=users[1].id, createdAt=now_time, updatedAt=now_time, deleted=False),
]
crud_playlist.upsert_playlists(db_manager, playlists)

# --- Create tracks ---
tracks = [
    Track(
        id=str(uuid.uuid4()),
        playlistId=playlists[0].id,
        title="Track 1",
        artist="Artist A",
        duration=180,
        addedBy=users[0].id,
        createdAt=now_time,
        updatedAt=now_time,
        deleted=False
    ),
    Track(
        id=str(uuid.uuid4()),
        playlistId=playlists[1].id,
        title="Track 2",
        artist="Artist B",
        duration=200,
        addedBy=users[1].id,
        createdAt=now_time,
        updatedAt=now_time,
        deleted=False
    )
]
crud_track.upsert_tracks(db_manager, tracks)

print("Demo data inserted into playlist.db")
