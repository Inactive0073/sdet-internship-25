from typing import Literal

import allure
from requests import Response

from src.api.client import APIClient
from src.api.models.yandex_disk import YandexTrashItemsResponse
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

    @allure.step("Создание папки на Яндекс Диске по пути {folder_path}")
    def create_folder(self, folder_path: str) -> Response:
        params = {"path": folder_path}
        return self.client.put(YandexEndpoints.RESOURCES, params=params)

    @allure.step("Получение информации о файле или каталоге по пути {resource_path}")
    def get_resource_info(self, resource_path: str) -> Response:
        params = {"path": resource_path}
        return self.client.get(YandexEndpoints.RESOURCES, params=params)

    @allure.step("Получение списка удалённых элементов на Яндекс Диске")
    def get_trash_items(self) -> Response:
        return self.client.get(YandexEndpoints.GET_TRASH_ITEMS)

    @allure.step(
        "Удаление файла или папки на Яндекс Диске по пути {file_or_folder_path}"
    )
    def delete_file_or_folder(
        self, file_or_folder_path: str, permanently: Literal["true", "false"] = "false"
    ) -> Response:
        params = {"path": file_or_folder_path, "permanently": permanently}
        return self.client.delete(YandexEndpoints.RESOURCES, params=params)

    @allure.step(
        "Восстановление удалённого элемента на Яндекс Диске по пути {item_path}"
    )
    def restore_trash_item(self, item_path: str) -> Response:
        params = {"path": item_path}
        return self.client.put(YandexEndpoints.RESTORE_TRASH_ITEM, params=params)

    @allure.step(
        "Получение ссылки для загрузки файла на Яндекс Диск по пути {file_path}"
    )
    def get_upload_link(
        self, file_path: str, overwrite: Literal["true", "false"] = "true"
    ) -> Response:
        params = {"path": file_path, "overwrite": overwrite}
        return self.client.get(YandexEndpoints.UPLOAD, params=params)

    @allure.step("Загрузка файла на Яндекс Диск по ссылке {upload_url}")
    def upload_file(self, upload_url: str, file_data) -> Response:
        return self.client.put(upload_url, data=file_data)

    @allure.step("Получение ссылки для скачивания с Яндекс диска по пути {file_path}")
    def get_download_url(self, file_path: str):
        params = {"path": file_path}
        return self.client.get(YandexEndpoints.DOWNLOAD, params=params)

    @allure.step("Скачиваем файл по ссылке {url}")
    def download_file_by_url(self, url: str):
        return self.client.get(url)

    @allure.step("Создание копии файла или папки из {_from} в {to}")
    def copy_resource(
        self, _from: str, to: str, overwrite: Literal["true", "false"] = "false"
    ):
        params = {"from": _from, "path": to, "overwrite": overwrite}
        return self.client.post(YandexEndpoints.COPY, params=params)

    @allure.step("Проверка наличия файла/папки в корзине по {original_path}")
    def is_resource_in_trash(self, original_path: str) -> bool:
        response = self.get_trash_items()
        if response.status_code != 200:
            return False
        trash_items = YandexTrashItemsResponse(**response.json())
        for item in trash_items.embedded_content.items:
            if item.origin_path == original_path:
                return True
        return False

    @allure.step("Получение path из корзины по {original_path}")
    def get_path_from_trash_by_original_path(self, original_path: str) -> str | None:
        response = self.get_trash_items()
        if response.status_code != 200:
            return None
        trash_items = YandexTrashItemsResponse(**response.json())
        for item in trash_items.embedded_content.items:
            if item.origin_path == original_path:
                return item.path
        return None
