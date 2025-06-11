import hashlib
import sqlite3

class Auth:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password_hash TEXT NOT NULL)')
        conn.commit()
        conn.close()

    def add_user(self, username: str, password: str):
        pw_hash = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, pw_hash))
            conn.commit()
        except sqlite3.IntegrityError:
            pass
        conn.close()

    def verify_user(self, username: str, password: str) -> bool:
        pw_hash = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect(self.db_path)
        cur = conn.execute('SELECT password_hash FROM users WHERE username=?', (username,))
        row = cur.fetchone()
        conn.close()
        return row is not None and row[0] == pw_hash
