from src.services.db.db_client import DBClient
from src.services.db.queries.users import (
    GET_USER_BY_ID,
    CHECK_USER_BY_EMAIL,
    DELETE_USER_BY_ID,
)


class UserDAO:
    def __init__(self, db: DBClient):
        self.db = db

    def get_user(self, user_id: int):
        return self.db.fetch_one(GET_USER_BY_ID, (user_id,))

    def email_exists(self, email: str) -> bool:
        row = self.db.fetch_one(CHECK_USER_BY_EMAIL, (email,))
        return row["total"] > 0 if row else False

    def delete(self, user_id: int):
        self.db.execute(DELETE_USER_BY_ID, (user_id,))
