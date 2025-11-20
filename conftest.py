
from typing import Generator

import allure
import pytest
import requests

from src.api.actions.post_aciton import EntityActions
from src.api.client import APIClient
from src.api.models import EntityRequest


@pytest.fixture(scope="session")
def api_client() -> Generator[APIClient, None, None]:
    """Создаёт и возвращает экземпляр APIClient."""
    with allure.step("Создаём экземпляр APIClient"):
        api_client = APIClient()
        yield api_client


@pytest.fixture(scope="function")
def entity(api_client):
    """Создаёт тестовую сущность перед каждым тестом и удаляет после."""
    actions = EntityActions(api_client)
    entity = actions.create_entity_synthetic(EntityRequest.random())
    yield entity
    try:
        actions.delete_entity(entity.id)
    except requests.HTTPError: # пропускаем если сущность уже была удалена, в тестах отлавливается этот случай
        pass                   # test_delete_entity XFAIL (Known backend issue: GET by non-existing ID returns 500 instead of 404)   

@pytest.fixture(scope="function")
def entity_actions(api_client):
    return EntityActions(api_client)
