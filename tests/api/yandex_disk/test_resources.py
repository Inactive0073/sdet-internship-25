import allure
import pytest
from requests import Response

from src.api.actions import DiskActions
from src.api.models.yandex_disk import LinkResponse, YandexDiskInfoErrorResponse


@allure.epic("API Yandex Disk")
@allure.feature("Folders Management")
@allure.story("Создание и получение ресурсов (Папки)")
@allure.suite("Folders CRUD Operations")
@allure.sub_suite("PUT /v1/disk/resources")
@allure.link(
    "https://yandex.ru/dev/disk/poligon",
    name="Yandex Disk API Documentation",
)
@allure.label("owner", "Alexey Yumanov")
@pytest.mark.api
@pytest.mark.yandex_disk
class TestYandexDiskFolders:
    @allure.title("TC-YD1. Создание папки на Яндекс Диске")
    @allure.testcase("Проверка успешного создания папки на Яндекс Диске")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "positive", "yandex_disk", "resources", "v1.0")
    @allure.description("""
    <b>Цель:</b> Проверить успешное создание папки на Яндекс Диске.

    <b>Ожидаемый результат:</b>
    - статус: 201 Created
    - тело содержит поле "href" (операции)
    - папка существует через GET /v1/disk/resources?path=disk:/test_folder_<unique_id>
    """)
    @pytest.mark.positive
    def test_create_folder(
        self,
        temp_created_folder: tuple[str, Response],
        yandex_disk_actions: DiskActions,
    ):
        folder_name, response = temp_created_folder
        data = response.json()

        assert LinkResponse.model_validate(data), (
            "Ответ не является корректной моделью LinkResponse"
        )
        assert response.status_code == 201, (
            f"Ожидался статус код 201, получен {response.status_code}"
        )
        assert data.get("href"), "В ответе отсутствует поле 'href'"
        assert (
            yandex_disk_actions.get_resource_info(resource_path=folder_name).status_code
            == 200
        ), "Папка не была создана на Яндекс Диске"

    @allure.title("TC-YD2: Создание существующей папки (Conflict)")
    @allure.testcase("https://wiki.example.com/TC-YD2")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("negative", "conflict", "error_handling", "409")
    @pytest.mark.negative
    @allure.description("""
    <b>Цель:</b> Проверить корректную обработку сервером запроса на создание уже существующего ресурса.

    <b>Ожидаемый результат:</b>
    - статус: 409 Conflict
    - тело ошибки содержит "error": "DiskPathPointsToExistentDirectoryError"
    """)
    def test_create_existing_folder(
        self,
        temp_created_folder: tuple[str, Response],
        yandex_disk_actions: DiskActions,
    ):
        folder_name, _ = temp_created_folder

        response = yandex_disk_actions.create_folder(folder_path=folder_name)
        data = response.json()
        assert response.status_code == 409, (
            f"Ожидался статус код 409, получен {response.status_code}"
        )
        assert YandexDiskInfoErrorResponse.model_validate(data), (
            "Ответ не соответствует модели YandexDiskInfoErrorResponse"
        )
