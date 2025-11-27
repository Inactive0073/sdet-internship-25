import base64
from typing import Generator

import allure
import pytest

from src.api.actions import PostActions, UserActions
from src.api.client import APIClient
from src.api.models import PostCreationRequest, UserCreationRequest
from src.data.db_config import db_config
from src.services.db.dao import PostDAO, UserDAO
from src.services.db.db_client import DBClient


@pytest.fixture(scope="session")
def api_client(auth_headers) -> Generator[APIClient, None, None]:
    with allure.step("Создаём экземпляр APIClient с авторизацией"):
        api_client = APIClient(headers=auth_headers)
        yield api_client


@pytest.fixture(scope="session")
def auth_headers():
    username = "Firstname.LastName"
    password = "123-Test"
    token = base64.b64encode(f"{username}:{password}".encode()).decode()

    return {"Authorization": f"Basic {token}", "Content-Type": "application/json"}


@pytest.fixture(scope="function")
def post(api_client):
    """Создаёт тестовую сущность перед каждым тестом и удаляет после."""
    actions = PostActions(api_client)
    post = actions.create_post(PostCreationRequest.random())
    yield post


@pytest.fixture(scope="function")
def user(api_client):
    """Создаёт тестовую сущность перед каждым тестом и удаляет после."""
    actions = UserActions(api_client)
    user = actions.create_user(UserCreationRequest.random())
    yield user


@pytest.fixture(scope="session")
def post_actions(api_client):
    return PostActions(api_client)


@pytest.fixture(scope="session")
def user_actions(api_client):
    return UserActions(api_client)


@pytest.fixture(scope="function")
def db():
    client = DBClient(db_config)
    yield client
    client.close()


@pytest.fixture()
def post_dao(db):
    return PostDAO(db)


@pytest.fixture()
def user_dao(db):
    return UserDAO(db)
