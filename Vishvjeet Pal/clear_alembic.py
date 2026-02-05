import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()
# Connect to your SQLite database

conn = sqlite3.connect("task_tracker.db")  # Replace with your actual database file path
cursor = conn.cursor()

# Delete the alembic_version table (if it exists)
try:
    cursor.execute("DROP TABLE IF EXISTS alembic_version;")
    conn.commit()
    print("Alembic version table cleared.")
except sqlite3.OperationalError as e:
    print(f"Error: {e}")
finally:
    cursor.close()
    conn.close()
