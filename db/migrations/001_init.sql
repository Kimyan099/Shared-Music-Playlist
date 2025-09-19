CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    createdAt TEXT,
    updatedAt TEXT,
    deleted INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS playlists (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    createdBy TEXT NOT NULL,
    createdAt TEXT,
    updatedAt TEXT,
    deleted INTEGER DEFAULT 0,
    FOREIGN KEY(createdBy) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS tracks (
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
