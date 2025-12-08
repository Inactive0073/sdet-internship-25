import base64
from typing import Generator

import allure
import pytest
from requests import Response

from src.api.actions import DiskActions, PostActions, UserActions
from src.api.client import APIClient
from src.api.models.wordpress import PostCreationRequest, UserCreationRequest
from src.data.db_config import db_config
from src.data.yandex_endpoints import YandexEndpoints
from src.services.db.dao import PostDAO, UserDAO
from src.services.db.db_client import DBClient
from src.utils.config import Config


@pytest.fixture(scope="session")
def wp_api_client(auth_headers) -> Generator[APIClient, None, None]:
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
def post(wp_api_client, post_dao: PostDAO):
    """Создаёт тестовую сущность перед каждым тестом и удаляет после."""
    actions = PostActions(wp_api_client)
    post = actions.create_post(PostCreationRequest.random())
    yield post
    post_dao.delete(post.id)


@pytest.fixture(scope="function")
def user(wp_api_client, user_dao: UserDAO):
    """Создаёт тестовую сущность перед каждым тестом и удаляет после."""
    actions = UserActions(wp_api_client)
    user = actions.create_user(UserCreationRequest.random())
    yield user
    user_dao.delete(user.id)


@pytest.fixture(scope="session")
def post_actions(wp_api_client):
    return PostActions(wp_api_client)


@pytest.fixture(scope="session")
def user_actions(wp_api_client):
    return UserActions(wp_api_client)


@pytest.fixture(scope="session")
def db():
    client = DBClient(db_config)
    yield client
    client.close()


@pytest.fixture(scope="session")
def post_dao(db):
    return PostDAO(db)


@pytest.fixture(scope="session")
def user_dao(db):
    return UserDAO(db)


@pytest.fixture(scope="function")
def user_in_db(
    user_dao: UserDAO,
) -> Generator[tuple[UserCreationRequest, int], None, None]:
    req = UserCreationRequest.random()
    user_id = user_dao.create_user(req)
    yield req, user_id
    user_dao.delete(user_id)


@pytest.fixture(scope="function")
def post_in_db(
    post_dao: PostDAO,
) -> Generator[tuple[PostCreationRequest, int], None, None]:
    req = PostCreationRequest.random()
    post_id = post_dao.create_post_direct(req)
    yield req, post_id
    post_dao.delete(post_id)


# Yandex Disk fixtures


@pytest.fixture(scope="session")
def yandex_api_client() -> Generator[APIClient, None, None]:
    with allure.step("Создаём экземпляр APIClient для Яндекс Диска"):
        api_client = APIClient(
            base_url=YandexEndpoints.BASE,
            headers={"Authorization": f"OAuth {Config.YANDEX_DISK_TOKEN}"},
        )
        yield api_client


@pytest.fixture(scope="session")
def yandex_api_client_no_auth() -> APIClient:
    return APIClient(base_url=YandexEndpoints.BASE)


@pytest.fixture(scope="session")
def yandex_disk_actions(yandex_api_client):
    return DiskActions(yandex_api_client)


@pytest.fixture(scope="session")
def yandex_disk_actions_no_auth(yandex_api_client_no_auth):
    return DiskActions(client=yandex_api_client_no_auth)


@pytest.fixture(scope="function")
def yandex_disk_info(
    yandex_disk_actions: DiskActions,
) -> Generator[Response, None, None]:
    """Получает информацию о диске перед каждым тестом."""
    with allure.step("Получение информации о диске пользователя"):
        response = yandex_disk_actions.get_disk_info()
        yield response
