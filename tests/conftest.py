import pytest
import uuid
import sqlite3
from db.db import Database
from db.db_manager import DBManager
from model.user import User
from model.playlist import Playlist
from model.track import Track
from util.common_util import now

# --- Fixture: fresh in-memory DB per test with persistent connection ---
@pytest.fixture
def db_instance():
    # Create Database object
    db = Database(":memory:")

    # Persistent connection
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")

    # Create tables
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE users (
            id TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            createdAt TEXT,
            updatedAt TEXT,
            deleted INTEGER DEFAULT 0
        );
    """)
    cur.execute("""
        CREATE TABLE playlists (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            createdBy TEXT NOT NULL,
            createdAt TEXT,
            updatedAt TEXT,
            deleted INTEGER DEFAULT 0,
            FOREIGN KEY(createdBy) REFERENCES users(id)
        );
    """)
    cur.execute("""
        CREATE TABLE tracks (
            id TEXT PRIMARY KEY,
            playlistId TEXT NOT NULL,
            title TEXT NOT NULL,
            artist TEXT,
            duration INTEGER,
            addedBy TEXT NOT NULL,
            createdAt TEXT,
            updatedAt TEXT,
            deleted INTEGER DEFAULT 0,
            FOREIGN KEY(playlistId) REFERENCES playlists(id),
            FOREIGN KEY(addedBy) REFERENCES users(id)
        );
    """)

    # Patch Database.get_connection to return the persistent connection
    original_get_connection = db.get_connection
    def persistent_connection():
        class DummyContext:
            def __enter__(self_):
                return conn
            def __exit__(self_, exc_type, exc_val, exc_tb):
                pass
        return DummyContext()
    db.get_connection = persistent_connection

    yield db

    conn.close()
    db.get_connection = original_get_connection

# --- Fixture: DBManager for CRUD ---
@pytest.fixture
def db_manager(db_instance):
    return DBManager(db_instance)

# --- Sample users ---
@pytest.fixture
def sample_users():
    now_time = now()
    return [
        User(id=str(uuid.uuid4()), username="alice", createdAt=now_time, updatedAt=now_time, deleted=False),
        User(id=str(uuid.uuid4()), username="bob", createdAt=now_time, updatedAt=now_time, deleted=False),
    ]

# --- Sample playlists ---
@pytest.fixture
def sample_playlists(sample_users):
    now_time = now()
    return [
        Playlist(id=str(uuid.uuid4()), name="Chill Vibes", createdBy=sample_users[0].id, createdAt=now_time, updatedAt=now_time, deleted=False),
        Playlist(id=str(uuid.uuid4()), name="Workout", createdBy=sample_users[1].id, createdAt=now_time, updatedAt=now_time, deleted=False),
    ]

# --- Sample tracks ---
@pytest.fixture
def sample_tracks(sample_users, sample_playlists):
    now_time = now()
    return [
        Track(
            id=str(uuid.uuid4()),
            playlistId=sample_playlists[0].id,
            title="Track 1",
            artist="Artist A",
            duration=180,
            addedBy=sample_users[0].id,
            createdAt=now_time,
            updatedAt=now_time,
            deleted=False
        ),
        Track(
            id=str(uuid.uuid4()),
            playlistId=sample_playlists[1].id,
            title="Track 2",
            artist="Artist B",
            duration=200,
            addedBy=sample_users[1].id,
            createdAt=now_time,
            updatedAt=now_time,
            deleted=False
        )
    ]
