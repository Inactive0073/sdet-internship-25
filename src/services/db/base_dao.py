import hashlib
from typing import Sequence
from .db_client import DBClient


class BaseDAO:
    def __init__(self, db: DBClient):
        self.db = db

    def fetch_one(self, query: str, params: tuple | None = None) -> dict | None:
        return self.db.fetch_one(query, params)

    def fetch_all(self, query: str, params: tuple | None = None) -> Sequence[dict]:
        return self.db.fetch_all(query, params)

    def execute(self, query: str, params: tuple | None = None):
        return self.db.execute(query, params)

    def execute_and_return_id(self, query: str, params: tuple | None = None) -> int:
        return self.db.execute_and_return_id(query, params)

    def _hash_password(self, plain: str) -> str:
        return hashlib.md5(plain.encode()).hexdigest()
