from typing import Any, Dict, Optional, Sequence, Union

import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

ParamsType = Union[Sequence[Any], Dict[str, Any]]


class DBClient:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._connection: Optional[MySQLConnection | PooledMySQLConnection] = None

    def connect(self) -> MySQLConnection | PooledMySQLConnection:
        if self._connection is None:
            self._connection = mysql.connector.connect(**self.config)  # type: ignore
        return self._connection  # type: ignore

    def execute(self, query: str, params: Optional[ParamsType] = None) -> None:
        conn = self.connect()
        cursor = conn.cursor()

        if params is not None:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        conn.commit()
        cursor.close()

    def execute_and_return_id(self, query: str, params: tuple):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid

    def fetch_one(
        self, query: str, params: Optional[ParamsType] = None
    ) -> Optional[Dict[str, Any]]:
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)

        if params is not None:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        row = cursor.fetchone()
        cursor.close()
        return row

    def fetch_all(
        self, query: str, params: Optional[ParamsType] = None
    ) -> Sequence[Dict[str, Any]]:
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)

        if params is not None:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        rows = cursor.fetchall()
        cursor.close()
        return rows

    def close(self) -> None:
        if self._connection is not None:
            self._connection.close()
            self._connection = None
