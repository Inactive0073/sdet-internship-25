from src.services.db.base_dao import BaseDAO
from src.api.models import PostCreationRequest
from src.services.db.queries.posts import (
    GET_POST_BY_ID,
    CHECK_POST_EXISTS,
    DELETE_POST_BY_ID,
    GET_POST_STATUS,
    COUNT_NON_TRASH_POSTS,
    GET_ALL_POSTS,
    CREATE_POST_DB,
)


class PostDAO(BaseDAO):
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

    def create_post_direct(self, post: PostCreationRequest) -> int:
        """
        Прямое создание поста в БД.
        Возвращает ID созданного поста.
        """
        post = PostCreationRequest.random()

        params = (
            1,  # post_author admin
            post.content,
            post.title,
            post.status,
            post.title.lower().replace(" ", "-"),
        )
        post_id = self.execute_and_return_id(CREATE_POST_DB, params)
        return post_id

    def delete(self, post_id: int):
        self.db.execute(DELETE_POST_BY_ID, (post_id,))
