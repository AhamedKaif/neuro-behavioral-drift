import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database', 'database.db')
print("DB Path:", db_path)

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = 'comprehensive_user'")
    conn.commit()
    conn.close()
    print("Successfully deleted comprehensive_user.")
else:
    print("Database file not found.")
