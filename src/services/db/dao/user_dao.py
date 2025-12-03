from src.services.db.base_dao import BaseDAO
from src.api.models import UserCreationRequest
from src.services.db.queries.users import (
    GET_USER_BY_ID,
    CHECK_USER_BY_EMAIL,
    DELETE_USER_BY_ID,
    CREATE_USER,
    CREATE_USER_META_CAP,
    CREATE_USER_META_LEVEL,
)


class UserDAO(BaseDAO):
    def create_user(self, user: UserCreationRequest) -> int:
        hashed_pass = self._hash_password(user.password)

        params = (user.username, hashed_pass, user.email, user.username, user.username)

        user_id = self.db.execute_and_return_id(CREATE_USER, params)

        if user_id is None:
            raise ValueError(f"User is none: {user_id=}")

        self.db.execute(CREATE_USER_META_CAP, (user_id,))
        self.db.execute(CREATE_USER_META_LEVEL, (user_id,))

        return user_id

    def get_user(self, user_id: int):
        return self.db.fetch_one(GET_USER_BY_ID, (user_id,))

    def email_exists(self, email: str) -> bool:
        row = self.db.fetch_one(CHECK_USER_BY_EMAIL, (email,))
        return row["total"] > 0 if row else False

    def delete(self, user_id: int):
        self.db.execute(DELETE_USER_BY_ID, (user_id,))
