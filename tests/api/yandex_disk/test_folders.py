from typing import Any

import allure
import pytest
from requests import Response

from src.api.models.yandex_disk import YandexTrashItemsResponse
from src.api.actions import DiskActions
from src.data.data_generator import generate_random_folder_name


@allure.parent_suite("API Yandex Disk")
@allure.suite("Yandex Disk - Folders CRUD Operations")
@allure.sub_suite("PUT /v1/disk/resources")
@allure.epic("API Yandex Disk")
@allure.feature("Folders CRUD Operations")
@allure.label("owner", "Alexey Yumanov")
@pytest.mark.api
@pytest.mark.yandex_disk
class TestYandexDiskFolders:
    @allure.story("Проверка аутентификации с валидным токеном")
    @allure.title("TC-YD1. Создание папки с валидным именем")
    @allure.testcase("Проверка успешного создания папки на Яндекс Диске")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "positive", "yandex_disk", "auth", "v1.0")
    @allure.description("""
    <b>Цель:</b> Проверить успешное создание папки с валидным именем на Яндекс Диске.

    <b>Ожидаемый результат:</b>
    - статус: 201 Created
    - тело содержит поле "href" (операции)
    - папка существует через GET /v1/disk/resources?path=disk:/test_folder_<timestamp>
    """)
    @pytest.mark.positive
    def test_get_disk_info_with_valid_token(
        self,
        yandex_created_folder_response: tuple[str, Response],
        yandex_disk_actions: DiskActions,
    ):
        folder_name, response = yandex_created_folder_response
        data = response.json()

        assert isinstance(data, dict), "Ответ не является корректным JSON объектом"
        assert response.status_code == 201, (
            f"Ожидался статус код 201, получен {response.status_code}"
        )
        assert data.get("href"), "В ответе отсутствует поле 'href'"
        assert (
            yandex_disk_actions.get_resource_info(
                resource_path=f"disk:/{folder_name}"
            ).status_code
            == 200
        ), "Папка не была создана на Яндекс Диске"

    @allure.title("TC-YD2. Создание папки, которая уже существует")
    def test_create_existing_folder(
        self,
        yandex_created_folder_response: tuple[str, Response],
        yandex_disk_actions: DiskActions,
    ):
        folder_name, response = yandex_created_folder_response

        response = yandex_disk_actions.create_folder(folder_path=f"disk:/{folder_name}")
        assert response.status_code == 409, (
            f"Ожидался статус код 409, получен {response.status_code}"
        )

    @allure.title("TC-YD5. Мягкое удаление папки в корзину")
    def test_delete_folder_permanently(self, yandex_disk_actions: DiskActions):
        folder_name = generate_random_folder_name()
        yandex_disk_actions.create_folder(folder_path=f"disk:/{folder_name}")

        response = yandex_disk_actions.delete_folder(
            folder_path=f"disk:/{folder_name}", permanently="false"
        )
        assert response.status_code == 204, (
            f"Ожидался статус код 204, получен {response.status_code}"
        )
        trash_items_data = yandex_disk_actions.get_trash_items().json()
        assert YandexTrashItemsResponse.model_validate(trash_items_data), (
            "Ответ не соответствует модели YandexTrashItemsResponse"
        )
