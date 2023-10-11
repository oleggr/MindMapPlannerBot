import logging
from typing import Dict, List
import sqlite3

from db.user_queries import UserQueriesMixin
from db.models import Leaf


logger = logging.getLogger(__name__)


class DbController(UserQueriesMixin):
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

    def get_leaves(self, user_id: int, parent_id: int) -> List[Leaf]:
        logger.debug(
            f'Get leaves with parent_id {parent_id} for user {user_id}'
        )

        conn = self._get_connection()
        sql = f"""
        SELECT * FROM leaves 
        WHERE user_id={user_id} AND parent_id={parent_id};
        """

        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        rows = cur.fetchall()
        leaves = []

        for row in rows:
            leaves.append(
                Leaf(
                    leaf_id=row[0],
                    user_id=row[1],
                    name=row[2],
                    parent_id=row[3],
                    target_value=row[4],
                    current_value=row[5],
                    deadline=row[6],
                    created_at=row[7],
                    updated_at=row[8],
                )
            )

        return leaves

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
