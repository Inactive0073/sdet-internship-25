
from typing import Generator

import allure
import pytest
import requests

from src.api.actions.post_aciton import PostActions
from src.api.client import APIClient
from src.api.models import PostRequest


@pytest.fixture(scope="session")
def api_client() -> Generator[APIClient, None, None]:
    """Создаёт и возвращает экземпляр APIClient."""
    with allure.step("Создаём экземпляр APIClient"):
        api_client = APIClient()
        yield api_client


@pytest.fixture(scope="function")
def post(api_client):
    """Создаёт тестовую сущность перед каждым тестом и удаляет после."""
    actions = PostActions(api_client)
    post = actions.create_post(PostRequest.random())
    yield post

@pytest.fixture(scope="function")
def post_actions(api_client):
    return PostActions(api_client)
