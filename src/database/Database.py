import os
import psycopg2
from psycopg2.extensions import connection, cursor
from dotenv import load_dotenv, find_dotenv
from typing import Optional
import logging

load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)


class Database:

    def __init__(self):
        self.conn: Optional[connection] = None
        self.cursor: Optional[cursor] = None

    def connect(self):
        self.conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        self.cursor = self.conn.cursor()
        logger.info("Connected to database")

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        logger.info("Disconnected from database")

    def execute(self, query, params=None):
        if self.cursor is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        try:
            self.cursor.execute(query, params)
            if self.conn:
                self.conn.commit()
        except psycopg2.Error as e:
            if self.conn:
                self.conn.rollback()
            raise

    def fetchall(self, query, params=None):
        if self.cursor is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetchone(self, query, params=None):
        if self.cursor is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        self.cursor.execute(query, params)
        return self.cursor.fetchone()
    
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            if self.conn:
                self.conn.rollback()
        self.disconnect()
        return False  # Propagate exception