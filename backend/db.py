import sqlite3

DB_PATH = 'landkreis_assignments.db'

def get_connection():
    """Return a SQLite connection and ensure the assignments table exists."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS assignments(
            rs TEXT PRIMARY KEY,
            wirtschaftsregion TEXT,
            fkt JSON
        )
        """
    )
    return conn
