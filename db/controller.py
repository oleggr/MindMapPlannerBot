import logging
import typing
import sqlite3

from db.models import User


logger = logging.getLogger(__name__)


class DbController:
    DB_PARAMS: typing.Dict[str, str]
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

    def write_user(self, user: User):
        logger.info(f'Write user {user.user_id}')

        conn = self._get_connection()

        sql = f"""
        INSERT INTO users (
            `user_id`,
            `username`
        ) VALUES (
            '{user.user_id}',
            '{user.username}'
        );
        """

        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

    def get_user(self, user_id: int):
        logger.info(f'Fetch user {user_id}')

        conn = self._get_connection()
        sql = f'SELECT * from users WHERE user_id={user_id};'

        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        row = cur.fetchone()

        logger.info(row)
        return row

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

            conn.commit()

        conn.close()
