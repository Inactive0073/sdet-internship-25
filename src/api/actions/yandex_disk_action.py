from typing import Literal
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

    @allure.step("Создание папки на Яндекс Диске")
    def create_folder(self, folder_path: str) -> Response:
        params = {"path": folder_path}
        return self.client.put(YandexEndpoints.RESOURCES, params=params)

    @allure.step("Получение информации о файле или каталоге")
    def get_resource_info(self, resource_path: str) -> Response:
        params = {"path": resource_path}
        return self.client.get(YandexEndpoints.RESOURCES, params=params)

    @allure.step("Получение списка удалённых элементов на Яндекс Диске")
    def get_trash_items(self) -> Response:
        return self.client.get(YandexEndpoints.GET_TRASH_ITEMS)

    @allure.step("Удаление папки на Яндекс Диске")
    def delete_folder(
        self, folder_path: str, permanently: Literal["true", "false"] = "false"
    ) -> Response:
        params = {"path": folder_path, "permanently": permanently}
        return self.client.delete(YandexEndpoints.RESOURCES, params=params)

    @allure.step("Восстановление удалённого элемента на Яндекс Диске")
    def restore_trash_item(self, item_path: str) -> Response:
        params = {"path": item_path}
        return self.client.post(YandexEndpoints.RESTORE_TRASH_ITEM, params=params)

    @allure.step("Получение ссылки для загрузки файла на Яндекс Диск")
    def get_upload_link(
        self, file_path: str, overwrite: Literal["true", "false"] = "true"
    ) -> Response:
        params = {"path": file_path, "overwrite": overwrite}
        return self.client.get(YandexEndpoints.UPLOAD, params=params)

    @allure.step("Загрузка файла на Яндекс Диск по ссылке")
    def upload_file(self, upload_url: str, file_data: bytes) -> Response:
        headers = {"Content-Type": "application/octet-stream"}
        return self.client.post(upload_url, data=file_data, headers=headers)
