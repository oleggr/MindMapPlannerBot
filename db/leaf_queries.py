import logging
from typing import List, Optional

from db.models import Leaf


logger = logging.getLogger(__name__)


class LeafQueriesMixin:
    def _get_connection(self):
        raise NotImplemented(
            'Call _get_connection from user mixin'
        )

    def write_leaf(self, leaf: Leaf):
        logger.debug(f'Write leaf {leaf.leaf_id}')

        conn = self._get_connection()

        sql = f"""
        INSERT INTO leaves (
            `user_id`,
            `name`,
            `parent_id`,
            `target_value`,
            `current_value`
        ) VALUES (
            '{leaf.user_id}',
            '{leaf.name}',
            '{leaf.parent_id}',
            '{leaf.target_value}',
            '{leaf.current_value}'
        );
        """

        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

    def update_leaf(self, leaf_id: int, leaf_name: str):
        logger.debug(f'Update leaf name {leaf_id}')

        conn = self._get_connection()

        sql = f"UPDATE leaves SET name='{leaf_name}' WHERE leaf_id={leaf_id};"

        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

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

    def get_leaf_by_id(self, leaf_id: int) -> Optional[Leaf]:
        logger.debug(f'Fetch leaf {leaf_id}')

        conn = self._get_connection()
        sql = f'SELECT * from leaves WHERE leaf_id={leaf_id};'

        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        row = cur.fetchone()

        if row:
            return Leaf(
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
