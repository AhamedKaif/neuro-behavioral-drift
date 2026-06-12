import sqlite3
import os
import psycopg2
from psycopg2.extras import RealDictCursor

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database', 'database.db')
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database', 'schema.sql')

# Check for Render's Database URL
DATABASE_URL = os.environ.get('DATABASE_URL')

class SmartCursorWrapper:
    """Wraps a cursor to translate SQLite bindings (?) to PostgreSQL bindings (%s) if needed."""
    def __init__(self, cursor, is_postgres):
        self.cursor = cursor
        self.is_postgres = is_postgres
        
    def execute(self, query, params=None):
        if self.is_postgres and '?' in query:
            query = query.replace('?', '%s')
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self
        
    def fetchone(self):
        return self.cursor.fetchone()
        
    def fetchall(self):
        return self.cursor.fetchall()

class SmartConnectionWrapper:
    """Wraps the database connection to provide our SmartCursorWrapper."""
    def __init__(self, conn, is_postgres):
        self.conn = conn
        self.is_postgres = is_postgres
        
    def execute(self, query, params=None):
        cursor = self.cursor()
        return cursor.execute(query, params)
        
    def cursor(self):
        if self.is_postgres:
            return SmartCursorWrapper(self.conn.cursor(cursor_factory=RealDictCursor), True)
        else:
            return SmartCursorWrapper(self.conn.cursor(), False)
            
    def commit(self):
        self.conn.commit()
        
    def close(self):
        self.conn.close()

def get_db_connection():
    """Establish a connection to the database (PostgreSQL or SQLite)."""
    if DATABASE_URL and DATABASE_URL.startswith('postgres'):
        conn = psycopg2.connect(DATABASE_URL)
        return SmartConnectionWrapper(conn, True)
    else:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return SmartConnectionWrapper(conn, False)

def init_db():
    """Create directories and run the schema SQL script to initialize tables."""
    is_postgres = DATABASE_URL and DATABASE_URL.startswith('postgres')
    
    if not is_postgres:
        db_dir = os.path.dirname(DB_PATH)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            
    conn = get_db_connection()
    
    with open(SCHEMA_PATH, 'r') as f:
        schema_sql = f.read()
        
    if is_postgres:
        # Translate SQLite schema syntax to PostgreSQL on the fly
        schema_sql = schema_sql.replace("INTEGER PRIMARY KEY AUTOINCREMENT", "SERIAL PRIMARY KEY")
        
        # Split statements and execute individually for psycopg2
        statements = schema_sql.split(';')
        cursor = conn.conn.cursor()
        for statement in statements:
            if statement.strip():
                cursor.execute(statement)
    else:
        # SQLite can execute the whole script
        conn.conn.executescript(schema_sql)
        
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()
