import allure
import pytest
from requests import Response

from src.api.models.yandex_disk import YandexDiskInfoResponse


@allure.parent_suite("API Yandex Disk")
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
class TestYandexDiskAuthValid:
    @allure.story("Проверка аутентификации с валидным токеном")
    @allure.title("TC-D1. Получение информации о диске с валидным токеном")
    @allure.testcase("Проверка аутентификации Яндекс Диск")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "positive", "yandex_disk", "auth", "v1.0")
    @allure.description("""
    <b>Цель:</b> Проверить успешное получение информации о диске с валидным токеном.

    <b>Ожидаемый результат:</b>
    - HTTP 200
    - Возвращён корректный объект `YandexDiskInfoResponse`
    - Поля объекта содержат ожидаемые значения
    """)
    @pytest.mark.positive
    def test_get_disk_info_with_valid_token(self, yandex_disk_info: Response):
        assert yandex_disk_info.status_code == 200, (
            f"Ожидался статус код 200, получен {yandex_disk_info.status_code}"
        )

        model = YandexDiskInfoResponse.model_validate(yandex_disk_info.json())
        assert isinstance(model, YandexDiskInfoResponse), (
            "Ответ не соответствует модели YandexDiskInfoResponse"
        )
        assert model.user.login, "Логин пользователя не должен быть пустым"
        assert model.user.display_name, (
            "Отображаемое имя пользователя не должно быть пустым"
        )
