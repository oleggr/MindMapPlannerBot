import logging
from typing import Dict
import sqlite3

from db.leaf_queries import LeafQueriesMixin
from db.user_queries import UserQueriesMixin
from db.models import Leaf


logger = logging.getLogger(__name__)


class DbController(UserQueriesMixin, LeafQueriesMixin):
    DB_PARAMS: Dict[str, str]
    db_filename: str = 'storage.db'

    def __init__(self):
        self.DB_PARAMS = {
            'database': self.db_filename
        }
        self._create_tables()

    def _get_connection(self):
        """Open connection"""
        conn = None
        try:
            conn = sqlite3.connect(**self.DB_PARAMS)
        except Exception as e:
            print(e)

        return conn

    def _create_tables(self):
        logger.info('Creating tables')

        conn = self._get_connection()
        with conn:
            cur = conn.cursor()

            sql = """
            CREATE TABLE IF NOT EXISTS leaves (
                `leaf_id`                   INTEGER PRIMARY KEY,
                `user_id`                   INTEGER,
                `name`                      TEXT,
                `parent_id`                 INTEGER DEFAULT 0,
                `target_value`              TEXT,
                `current_value`             TEXT,    
                `deadline`                  DATETIME,    
                `created_at`                DATETIME DEFAULT current_timestamp,
                `updated_at`                DATETIME DEFAULT current_timestamp
            );
            """
            cur.execute(sql)

            sql = """CREATE INDEX IF NOT EXISTS leaves_userId_parentId ON leaves(`user_id`, `parent_id`);"""
            cur.execute(sql)

            sql = """
            CREATE TABLE IF NOT EXISTS users (
                `user_id`                   INTEGER PRIMARY KEY,
                `username`                  TEXT,
                `created_at`                DATETIME DEFAULT current_timestamp,
                `updated_at`                DATETIME DEFAULT current_timestamp
            );
            """
            cur.execute(sql)

            sql = """
            CREATE TABLE IF NOT EXISTS user_state (
                `user_id`                   INTEGER PRIMARY KEY,
                `state`                     INTEGER,
                `action`                    INTEGER,
                `created_at`                DATETIME DEFAULT current_timestamp,
                `updated_at`                DATETIME DEFAULT current_timestamp
            );
            """
            cur.execute(sql)

            conn.commit()

        conn.close()
