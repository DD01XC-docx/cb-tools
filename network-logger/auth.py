import sqlite3
import bcrypt
from datetime import datetime

class Auth:
    def __init__(self, db_path):
        self.db_path = db_path
        self._setup()

    def _setup(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password_hash BLOB NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    last_login TEXT
                )
            """)

    def add_user(self, username, password):
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, hashed)
                )
            return True
        except sqlite3.IntegrityError:
            return False

    def verify_user(self, username, password):
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                'SELECT password_hash FROM users WHERE username = ?',
                (username,)
            ).fetchone()

            if not row:
                return False
            
            if bcrypt.checkpw(password.encode(), row[0]):
                conn.execute(
                    'UPDATE users SET last_login = ? WHERE username = ?',
                    (datetime.utcnow().isoformat(), username)
                )
                return True
        return False 