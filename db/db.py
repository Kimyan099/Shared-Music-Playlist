
import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Iterator

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "playlist.db"
MIGRATIONS_DIR = BASE_DIR / "migrations"

class Database:
    def __init__(self, db_path: Path = DB_PATH, migrations_dir: Path = MIGRATIONS_DIR):
        self.db_path = str(db_path)
        self.migrations_dir = migrations_dir

        print("[DEBUG] Database path:", self.db_path)
        print("[DEBUG] Migrations dir:", self.migrations_dir)
        self._init_db()

    @contextmanager
    def get_connection(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_db(self) -> None:
        """Run migrations at startup (executed once)."""
        sql_files = sorted(self.migrations_dir.glob("*.sql"))
        if not sql_files:
            return
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            for sqlfile in sql_files:
                cursor.executescript(sqlfile.read_text(encoding="utf-8"))
            conn.commit()

# Global instance
db = Database()
