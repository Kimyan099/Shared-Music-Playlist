import sqlite3
from pathlib import Path
import html

DB_PATH = Path(__file__).resolve().parent.parent / "playlist.db"
OUTPUT_HTML = Path(__file__).resolve().parent / "demo.html"

def fetch_data():
    """Fetch users, playlists, and tracks from the database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Fetch users
    cursor.execute("SELECT * FROM users WHERE deleted = 0")
    users = cursor.fetchall()

    # Fetch playlists
    cursor.execute("SELECT * FROM playlists WHERE deleted = 0")
    playlists = cursor.fetchall()

    # Fetch tracks
    cursor.execute("SELECT * FROM tracks WHERE deleted = 0")
    tracks = cursor.fetchall()

    conn.close()
    return users, playlists, tracks

def generate_html(users, playlists, tracks):
    """Generate a simple HTML file displaying the hierarchy."""
    html_parts = [
        "<!DOCTYPE html>",
        "<html><head><meta charset='utf-8'><title>Shared Playlist Demo</title>",
        "<style>body{font-family:sans-serif;} h2{color: #2c3e50;} ul{list-style:none; padding-left:20px;} li{margin-bottom:5px;}</style>",
        "</head><body>",
        "<h1>Shared Playlist Demo</h1>"
    ]

    for user in users:
        html_parts.append(f"<h2>User: {html.escape(user['username'])}</h2>")
        user_playlists = [p for p in playlists if p["createdBy"] == user["id"]]
        if not user_playlists:
            html_parts.append("<p>No playlists</p>")
        else:
            html_parts.append("<ul>")
            for pl in user_playlists:
                html_parts.append(f"<li>Playlist: {html.escape(pl['name'])}")
                pl_tracks = [t for t in tracks if t["playlistId"] == pl["id"]]
                if pl_tracks:
                    html_parts.append("<ul>")
                    for tr in pl_tracks:
                        html_parts.append(f"<li>Track: {html.escape(tr['title'])} by {html.escape(tr['artist'])} ({tr['duration']}s)</li>")
                    html_parts.append("</ul>")
                html_parts.append("</li>")
            html_parts.append("</ul>")

    html_parts.append("</body></html>")
    return "\n".join(html_parts)

def main():
    users, playlists, tracks = fetch_data()
    html_content = generate_html(users, playlists, tracks)
    OUTPUT_HTML.write_text(html_content, encoding="utf-8")
    print(f"Demo HTML generated: {OUTPUT_HTML}")

if __name__ == "__main__":
    main()
