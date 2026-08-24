import sqlite3
import os

try:
    import mysql.connector
    HAS_MYSQL_LIB = True
except ImportError:
    HAS_MYSQL_LIB = False

DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "Rudra@123"
DB_NAME = "face_recognition_database"
SQLITE_PATH = os.path.join(os.path.dirname(__file__), "face_recognition.db")

class DBConnection:
    def __init__(self, mode, conn):
        self.mode = mode # 'mysql' or 'sqlite'
        self.conn = conn

    def cursor(self):
        return DBCursor(self.mode, self.conn.cursor())

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

class DBCursor:
    def __init__(self, mode, cursor):
        self.mode = mode
        self.cursor = cursor

    def execute(self, query, params=None):
        if self.mode == 'sqlite':
            # Convert %s placeholders to ? placeholders for SQLite
            query = query.replace("%s", "?")
            # SQLite query adaptations if any
            if params is None:
                return self.cursor.execute(query)
            else:
                return self.cursor.execute(query, params)
        else:
            if params is None:
                return self.cursor.execute(query)
            else:
                return self.cursor.execute(query, params)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()

def get_db_connection():
    """
    Attempts to connect to MySQL first.
    If MySQL server is unavailable or driver is missing, falls back to local SQLite.
    Automatically initializes required tables if they don't exist.
    """
    if HAS_MYSQL_LIB:
        try:
            # First try connecting to MySQL server directly
            mysql_conn = mysql.connector.connect(
                host=DB_HOST,
                username=DB_USER,
                password=DB_PASS
            )
            cursor = mysql_conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            cursor.execute(f"USE {DB_NAME}")
            cursor.close()
            
            # Now connect specifically to the database
            conn = mysql.connector.connect(
                host=DB_HOST,
                username=DB_USER,
                password=DB_PASS,
                database=DB_NAME
            )
            _init_tables('mysql', conn)
            return DBConnection('mysql', conn)
        except Exception as e:
            # MySQL connection failed, fallback to SQLite
            pass

    # SQLite fallback
    conn = sqlite3.connect(SQLITE_PATH)
    _init_tables('sqlite', conn)
    return DBConnection('sqlite', conn)

def _init_tables(mode, conn):
    cursor = conn.cursor()
    if mode == 'sqlite':
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS student (
            studentId TEXT PRIMARY KEY,
            studentName TEXT,
            dep TEXT,
            course TEXT,
            section TEXT,
            year TEXT,
            sem TEXT,
            gender TEXT,
            photo TEXT
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS register (
            username TEXT PRIMARY KEY,
            pass TEXT,
            confpass TEXT,
            security TEXT,
            ans TEXT
        )
        """)
        # Insert default admin if table is empty
        cursor.execute("SELECT COUNT(*) FROM register")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO register VALUES (?, ?, ?, ?, ?)",
                ("admin", "admin123", "admin123", "In which city did you born?", "Delhi")
            )
    else:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS student (
            studentId VARCHAR(50) PRIMARY KEY,
            studentName VARCHAR(100),
            dep VARCHAR(100),
            course VARCHAR(100),
            section VARCHAR(50),
            year VARCHAR(50),
            sem VARCHAR(50),
            gender VARCHAR(50),
            photo VARCHAR(50)
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS register (
            username VARCHAR(50) PRIMARY KEY,
            pass VARCHAR(100),
            confpass VARCHAR(100),
            security VARCHAR(200),
            ans VARCHAR(200)
        )
        """)
        cursor.execute("SELECT COUNT(*) FROM register")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO register VALUES ('admin', 'admin123', 'admin123', 'In which city did you born?', 'Delhi')"
            )
    conn.commit()
    cursor.close()

if __name__ == "__main__":
    db = get_db_connection()
    print("Database connected successfully using mode:", db.mode)
    cur = db.cursor()
    cur.execute("SELECT * FROM register")
    print("Register users:", cur.fetchall())
    db.close()
