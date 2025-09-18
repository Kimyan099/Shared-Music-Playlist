# Shared Music Playlist
Share awesome music playlists with your friends

---

## 1. Service Description

The service is a collaborative music playlist platform. Multiple clients can connect, create playlists, and add/remove tracks. Updates are synchronized across clients in real time, and clients only download new/changed records since their last sync.

### Core features for the prototype:
- Create/update/delete playlists  
- Add/remove tracks from a playlist  
- Synchronize changes incrementally across clients  

**Why it fits the assignment:**
- Each playlist/track is a data record  
- Incremental synchronization is enabled via timestamps/versioning  
- Demonstrates batch operations (insert, update, delete)  

---

## 2. System Architecture

### Components

**Server (FastAPI in Python)**  
- Provides REST endpoints  
- Stores data in SQLite (simple, portable)  
- Tracks changes with timestamps and soft deletes  

**Client (CLI or simple web client)**  
- Can request incremental updates from server  
- Can batch upload changes (new tracks, updated playlists)  

### Sync Mechanism
- Each record has `updatedAt`  
- Clients keep a `lastSyncedAt`  
- On sync:  
```sql
SELECT * FROM records WHERE updatedAt > lastSyncedAt;
```

## 3. Data Model

User Record (basic for prototype)

User {
  id: string,          // UUID
  name: string,
  createdAt: timestamp
}

Note:
“I didn’t implement authentication for the prototype, but a production-ready version would have JWT/OAuth.”
For now, we just pass a userId when creating data.

Playlist Record

Playlist {
  id: string,          // UUID
  name: string,
  createdBy: string,   // userId
  createdAt: timestamp,
  updatedAt: timestamp,
  deleted: boolean
}

Track Record

Track {
  id: string,          // UUID
  playlistId: string,  // Foreign key to Playlist
  title: string,
  artist: string,
  duration: int,       // seconds
  addedBy: string,     // userId
  createdAt: timestamp,
  updatedAt: timestamp,
  deleted: boolean
}

## 4. API Endpoints

Playlist
- POST /playlists/batch → insert/update/delete playlists
- GET /playlists/sync?since=<timestamp> → return playlists updated after since

Track
- POST /tracks/batch → insert/update/delete tracks
- GET /tracks/sync?since=<timestamp> → return tracks updated after since

User (prototype only)
- POST /users → create a user
- GET /users → list users

## 5. Synchronization Flow
Initial Sync
- Client sends lastSyncedAt = null
- Server returns all playlists + tracks

Incremental Sync
- Client stores timestamp of last successful sync
- On next request, client sends lastSyncedAt
- Server returns only changed records (updatedAt > lastSyncedAt)

Conflict Handling (prototype)
- Last write wins
- Future improvement: version numbers or merge policies

Sync Flow Diagram

sequenceDiagram
    participant Client
    participant Server
    participant DB

    Client->>Server: Send lastSyncedAt=null
    Server->>DB: SELECT * FROM playlists, tracks
    DB-->>Server: Return all data
    Server-->>Client: Send all playlists + tracks

    Client->>Server: Send lastSyncedAt=timestamp
    Server->>DB: SELECT * FROM playlists, tracks WHERE updatedAt > lastSyncedAt
    DB-->>Server: Return changed records
    Server-->>Client: Send incremental updates

## 6. Known Limitations

- Conflict resolution is simplistic (last write wins)

- No authentication (any client can change playlists)

- No media storage – only metadata of tracks (title, artist, duration)

- Scalability – SQLite is fine for prototype, but not for production

## 7. Potential Next Steps

- WebSocket endpoints for clients instead of API

- Add authentication & user accounts (JWT/OAuth)

- Store uploaded audio snippets (e.g., S3, local file system)

- Add real-time push updates (WebSocket/pub-sub) instead of polling

- Support multiple playlists per user

- Implement more advanced sync strategies (vector clocks, CRDTs)

## 8. WebSocket vs REST API
REST (Polling/Sync) Approach

- How it works: Client asks the server periodically: “Do you have any updates since my last sync?”

Pros:
- Simple to implement
- Works everywhere (HTTP only)
- Easy to debug

Cons:
- Wastes bandwidth and server resources if there are no updates
- Updates are delayed until the next poll (not instant)
- Doesn’t scale well with many active clients polling frequently

### ⚡ WebSocket (Push) Approach

- How it works: Client opens a persistent connection (socket) to the server. The server pushes updates as soon as they happen.

Pros:
- Real-time sync: Clients see new tracks/playlists immediately (like Spotify or Google Docs style collaboration)
- Efficient: No need to constantly poll; server only sends data when changes happen
- Scales better for collaborative/multi-user use cases (especially if combined with pub/sub backend)
- Bi-directional: Client can also push changes instantly instead of batching

Cons:
- More complex to implement and maintain
- Requires keeping connections alive (stateful server)
- Some environments (older firewalls/proxies) may block WebSocket traffic



  

