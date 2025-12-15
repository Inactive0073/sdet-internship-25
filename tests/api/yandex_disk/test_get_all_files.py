import json

import allure
import pytest
from jsonschema import validate

from src.api.actions.yandex_disk_action import DiskActions


@allure.epic("Yandex Disk API")
@allure.feature("Files")
@allure.story("JSON Schema Validation")
@allure.sub_suite("GET /v1/disk/resources/files")
@allure.title("Валидация структуры ответа списка файлов по JSON Schema")
@allure.description(
    """
    Проверка контракта API получения списка файлов пользователя.

    Ожидается:
    - код ответа 200 OK
    - тело ответа соответствует описанной JSON Schema
    - структура ответа не зависит от количества файлов
    """
)
@allure.link(
    "https://yandex.ru/dev/disk/poligon",
    name="Yandex Disk API Documentation",
)
@pytest.mark.positive
@pytest.mark.yandex_disk
def test_get_files_list_schema_validation(
    yandex_disk_actions: DiskActions,
):
    with allure.step("Получаем список файлов пользователя"):
        response = yandex_disk_actions.get_files_list()
        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}"
        )

    with allure.step("Проверяем тело ответа на соответствие JSON Schema"):
        schema_path = "src/api/json_schemas/yandex_disk/files_list.schema.json"
        with open(schema_path, encoding="utf-8") as schema_file:
            schema = json.load(schema_file)

        validate(
            instance=response.json(),
            schema=schema,
        )
