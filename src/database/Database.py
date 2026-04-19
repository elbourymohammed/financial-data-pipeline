import os
import psycopg2
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Database:

    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        self.cursor = self.conn.cursor()
        print("==> Connected to database")

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("==> Disconnected from database")

    def execute(self, query, params=None):
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetchall(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetchone(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()
    
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type):
        if exc_type:
            self.conn.rollback()
        self.disconnect()