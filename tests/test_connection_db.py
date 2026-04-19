import os
import sys
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import psycopg2

sys.path.append(str(Path(__file__).parents[1] / "src"))

from database.Database import Database

load_dotenv(find_dotenv())

def test_connection():
    try:
        db = Database()
        db.connect()
        db.disconnect()
    except Exception as e:
        print(f"❌ Connection failed: {e}")


test_connection()

