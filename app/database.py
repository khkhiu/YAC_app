# app/database.py
import sqlite3
import os
from datetime import datetime
from app.config import DB_DIR, DB_PATH, logger

class Database:
    def __init__(self):
        self._ensure_data_directory()
        self.conn = sqlite3.connect(DB_PATH)
        self.create_tables()

    def _ensure_data_directory(self):
        os.makedirs(DB_DIR, exist_ok=True)

    def create_tables(self):
        try:
            with self.conn:
                self.conn.executescript('''
                    CREATE TABLE IF NOT EXISTS user_progress (
                        user_id INTEGER PRIMARY KEY,
                        self_awareness_count INTEGER DEFAULT 0,
                        connection_count INTEGER DEFAULT 0,
                        growth_count INTEGER DEFAULT 0,
                        last_challenge_date TEXT
                    );

                    CREATE TABLE IF NOT EXISTS completed_challenges (
                        user_id INTEGER,
                        challenge_type TEXT,
                        challenge_text TEXT,
                        completion_date TEXT,
                        reflection TEXT
                    );
                ''')
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            raise

    def get_user_progress(self, user_id: int) -> dict:
        try:
            cursor = self.conn.execute(
                'SELECT * FROM user_progress WHERE user_id = ?', 
                (user_id,)
            )
            result = cursor.fetchone()
            
            if not result:
                self._initialize_user(user_id)
                return {
                    'self_awareness_count': 0,
                    'connection_count': 0,
                    'growth_count': 0
                }
                
            return {
                'self_awareness_count': result[1],
                'connection_count': result[2],
                'growth_count': result[3]
            }
        except sqlite3.Error as e:
            logger.error(f"Error getting user progress: {e}")
            raise

    def _initialize_user(self, user_id: int):
        with self.conn:
            self.conn.execute(
                'INSERT INTO user_progress (user_id) VALUES (?)',
                (user_id,)
            )

    def update_progress(self, user_id: int, challenge_type: str):
        try:
            column = f'{challenge_type}_count'
            with self.conn:
                self.conn.execute(
                    f'UPDATE user_progress SET {column} = {column} + 1, last_challenge_date = ? WHERE user_id = ?',
                    (datetime.now().isoformat(), user_id)
                )
        except sqlite3.Error as e:
            logger.error(f"Error updating progress: {e}")
            raise

    def log_completion(self, user_id: int, challenge_type: str, challenge_text: str, reflection: str):
        try:
            with self.conn:
                self.conn.execute(
                    'INSERT INTO completed_challenges (user_id, challenge_type, challenge_text, completion_date, reflection) VALUES (?, ?, ?, ?, ?)',
                    (user_id, challenge_type, challenge_text, datetime.now().isoformat(), reflection)
                )
        except sqlite3.Error as e:
            logger.error(f"Error logging completion: {e}")
            raise