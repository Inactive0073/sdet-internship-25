import allure
from requests import Response

from src.api.client import APIClient
from src.data.yandex_endpoints import YandexEndpoints


class DiskActions:
    """Слой бизнес-логики API для работы с Яндекс Диском."""

    def __init__(self, client: APIClient):
        self.client = client

    @allure.step("Получение метаинформации о диске пользователя")
    def get_disk_info(self) -> Response:
        return self.client.get(YandexEndpoints.DISK_INFO)

    @allure.step("Получение метаинформации о диске пользователя без авторизации")
    def get_disk_info_without_auth(self) -> Response:
        # без токена
        return self.client.get(YandexEndpoints.DISK_INFO)
