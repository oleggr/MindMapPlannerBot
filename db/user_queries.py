from datetime import datetime
import logging
from typing import Optional

from db.models import User, UserState, UserMessage


logger = logging.getLogger(__name__)


class UserQueriesMixin:
    def _get_connection(self):
        raise NotImplemented(
            'Call _get_connection from user mixin'
        )

    def write_user(self, user: User):
        logger.debug(f'Write user {user.user_id}')

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

    def write_message(self, user_message: UserMessage):
        logger.debug(f'Write user message {user_message.user_id}')

        conn = self._get_connection()

        sql = f"""
        INSERT INTO user_messages (
            `user_id`,
            `message`
        ) VALUES (
            '{user_message.user_id}',
            '{user_message.message}'
        );
        """

        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

    def get_user(self, user_id: int) -> Optional[User]:
        logger.debug(f'Fetch user {user_id}')

        conn = self._get_connection()
        sql = f'SELECT * from users WHERE user_id={user_id};'

        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        row = cur.fetchone()

        if row:
            return User(
                user_id=row[0],
                username=row[1],
                created_at=row[2],
                updated_at=row[3],
            )

    def upsert_user_state(self, user_state: UserState):
        logger.debug(f'Upsert user state {user_state.user_id}')

        user_state.updated_at = datetime.now()

        conn = self._get_connection()

        sql = f"""
        INSERT INTO user_state (
            `user_id`,
            `state`,
            `action`
        ) VALUES (
            '{user_state.user_id}',
            '{user_state.state}',
            '{user_state.action}'
        ) ON CONFLICT do UPDATE SET
            state={user_state.state},
            action={user_state.action},
            updated_at='{user_state.updated_at}'
        ;
        """

        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

    def get_user_state(self, user_id: int) -> Optional[UserState]:
        logger.debug(f'Fetch user state {user_id}')

        conn = self._get_connection()
        sql = f'SELECT * from user_state WHERE user_id={user_id};'

        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        row = cur.fetchone()

        if row:
            return UserState(
                user_id=row[0],
                state=row[1],
                action=row[2],
                created_at=row[3],
                updated_at=row[4],
            )
