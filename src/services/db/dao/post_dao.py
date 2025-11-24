from src.services.db.db_client import DBClient
from src.services.db.queries.posts import (
    GET_POST_BY_ID,
    CHECK_POST_EXISTS,
    DELETE_POST_BY_ID,
    GET_POST_STATUS,
)


class PostDAO:
    def __init__(self, db: DBClient):
        self.db = db

    def get_post(self, post_id: int):
        return self.db.fetch_one(GET_POST_BY_ID, (post_id,))

    def exists(self, post_id: int) -> bool:
        row = self.db.fetch_one(CHECK_POST_EXISTS, (post_id,))
        return row["total"] > 0 if row else False

    def get_status(self, post_id: int) -> str | None:
        row = self.db.fetch_one(GET_POST_STATUS, (post_id,))
        return row["post_status"] if row else None

    def delete(self, post_id: int):
        self.db.execute(DELETE_POST_BY_ID, (post_id,))
