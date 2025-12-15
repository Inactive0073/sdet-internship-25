import allure
import pytest

from src.api.actions import DiskActions
from src.api.models.yandex_disk import YandexDiskInfoErrorResponse


@allure.suite("Authentication")
@allure.sub_suite("GET /v1/disk/")
@allure.epic("API Yandex Disk")
@allure.feature("Authentication Validation")
@allure.label("owner", "Alexey Yumanov")
@allure.link(
    "https://yandex.ru/dev/disk/poligon",
    name="Yandex Disk API Documentation",
)
@pytest.mark.api
@pytest.mark.yandex_disk
class TestYandexDiskAuthInvalid:
    @allure.story("Проверка аутентификации с невалидным токеном")
    @allure.title("TC-D2. Получение информации о диске с невалидным токеном")
    @allure.testcase("Проверка аутентификации Яндекс Диск с невалидным токеном")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "negative", "yandex_disk", "auth", "v1.0")
    @allure.description("""
    <b>Цель:</b> Проверить неуспешное получение информации о диске с невалидным токеном.

    <b>Ожидаемый результат:</b>
    - HTTP 200
    - Возвращён корректный объект `YandexDiskInfoResponse`
    - Поля объекта содержат ожидаемые значения
    """)
    @pytest.mark.negative
    def test_get_disk_info_with_invalid_token(
        self,
        yandex_disk_actions_no_auth: DiskActions,
    ):
        response = yandex_disk_actions_no_auth.get_disk_info_without_auth()
        model = YandexDiskInfoErrorResponse.model_validate(response.json())
        assert response.status_code == 401, (
            f"Ожидался статус код 401, получен {response.status_code}"
        )
        assert model.error, "Поле error не должно быть пустым"
        assert model.message, "Поле message не должно быть пустым"
        assert model.description, "Поле description не должно быть пустым"
