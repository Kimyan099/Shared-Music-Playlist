PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    username TEXT UNIQUE,
    createdAt TEXT,
    updatedAt TEXT,
    deleted INTEGER
);

CREATE TABLE IF NOT EXISTS playlists (
    id TEXT PRIMARY KEY,
    name TEXT,
    createdBy TEXT,
    createdAt TEXT,
    updatedAt TEXT,
    deleted INTEGER,
    FOREIGN KEY (createdBy) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS tracks (
    id TEXT PRIMARY KEY,
    playlistId TEXT,
    title TEXT,
    artist TEXT,
    duration INTEGER,
    addedBy TEXT,
    createdAt TEXT,
    updatedAt TEXT,
    deleted INTEGER,
    FOREIGN KEY (playlistId) REFERENCES playlists(id),
    FOREIGN KEY (addedBy) REFERENCES users(id)
);
