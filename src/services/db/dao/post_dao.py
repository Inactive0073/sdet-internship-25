from src.services.db.db_client import DBClient
from src.services.db.queries.posts import (
    GET_POST_BY_ID,
    CHECK_POST_EXISTS,
    DELETE_POST_BY_ID,
    GET_POST_STATUS,
    COUNT_NON_TRASH_POSTS,
    GET_ALL_POSTS,
)


class PostDAO:
    def __init__(self, db: DBClient):
        self.db = db

    def get_post(self, post_id: int):
        return self.db.fetch_one(GET_POST_BY_ID, (post_id,))

    def get_all_posts(self):
        return self.db.fetch_all(GET_ALL_POSTS)

    def count_posts(self) -> int:
        row = self.db.fetch_one(COUNT_NON_TRASH_POSTS)
        if not row:
            return 0
        return row.get("cnt", 0)

    def get_post_status(self, post_id: int) -> str | None:
        row = self.db.fetch_one(GET_POST_STATUS, (post_id,))
        return row["post_status"] if row else None

    def exists(self, post_id: int) -> bool:
        row = self.db.fetch_one(CHECK_POST_EXISTS, (post_id,))
        return row["total"] > 0 if row else False

    def get_status(self, post_id: int) -> str | None:
        row = self.db.fetch_one(GET_POST_STATUS, (post_id,))
        return row["post_status"] if row else None

    def delete(self, post_id: int):
        self.db.execute(DELETE_POST_BY_ID, (post_id,))
