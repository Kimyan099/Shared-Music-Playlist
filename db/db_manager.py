from .db import Database

class DBManager:
    def __init__(self, db: Database):
        self.db = db

    def execute(self, sql: str, params: tuple = ()):
        with self.db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            conn.commit()
            return cur

    def fetchall(self, sql: str, params: tuple = ()):
        with self.db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            return cur.fetchall()

    def fetchone(self, sql: str, params: tuple = ()):
        with self.db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            return cur.fetchone()