import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import mysql.connector
from app.config import Config
from app.database.connection import get_db

def init_db():
    # First, connect without database to create it if it doesn't exist
    try:
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME}")
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        print(f"Error creating database: {e}")
        return

    # Now connect to the database and create the table
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                price DECIMAL(10,2),
                quantity INT
            );
        """)

        db.commit()
        cursor.close()
        db.close()
        print("Database initialized successfully!")
    except mysql.connector.Error as e:
        print(f"Error creating table: {e}")

if __name__ == "__main__":
    init_db()
