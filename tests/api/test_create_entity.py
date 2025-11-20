import allure
import pytest

from src.api.actions.post_aciton import EntityActions
from src.api.models import EntityRequest, EntityResponse


@allure.parent_suite("API test-service")
@allure.suite("Entity Management")
@allure.sub_suite("POST /api/create")
@allure.epic("API test-service")
@allure.feature("Entity")
@allure.story("Создание новой сущности")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "create", "v1.0")
@allure.label("owner", "Alexey Yumanov")
@allure.testcase("TC-001")
@allure.description("""
**Цель:** Проверить успешное создание сущности через эндпоинт `/api/create`.

**Ожидаемый результат:**
- HTTP 201
- Возвращён объект `EntityResponse` с корректным `id`
- Все поля совпадают с отправленными данными
""")
@pytest.mark.api
class TestCreateEntity:
    @allure.title("TC-001: Создание новой сущности")
    @pytest.mark.xfail(
        reason="API возвращает только ID, а не полный EntityResponse",
    )
    def test_create_entity(self, entity_actions: EntityActions):
        request_data = EntityRequest.random()

        created = entity_actions.create_entity(request_data)
        assert isinstance(created, EntityResponse), (
            "Ответ не соответствует модели EntityResponse"
        )
        assert created.id > 0, "ID должен быть положительным числом"
        assert created.title == request_data.title, (
            "Title не совпадает с исходными данными"
        )
        assert created.verified == request_data.verified, (
            "Флаг verified должен совпадать"
        )
