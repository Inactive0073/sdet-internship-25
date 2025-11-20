import json

import allure
import pytest

from src.api.actions.post_aciton import EntityActions
from src.api.models.post_out import EntityResponse
from src.data.endpoints import Endpoints


@allure.parent_suite("API test-service")
@allure.suite("Entity Management")
@allure.sub_suite("DELETE /api/delete")
@allure.epic("API test-service")
@allure.feature("Entity")
@allure.story("Удаление сущности по ID")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "delete", "v1.0")
@allure.label("owner", "Alexey Yumanov")
@allure.testcase("TC-005")
@allure.description("""
**Цель:** Проверить успешное удаление сущности по `id`.

**Ожидаемый результат:**
- HTTP 200 или 204
- Повторный GET по `id` возвращает 404
""")
@pytest.mark.api
class TestDeleteEntity:
    @allure.title("TC-005: Удаление сущности по ID")
    def test_delete_entity(self, entity: EntityResponse, entity_actions: EntityActions):
        # --- Первичное удаление ---
        with allure.step("Удаляем созданную сущность"):
            delete_response = entity_actions.delete_entity(entity.id)
            allure.attach(
                json.dumps(dict(delete_response.headers), indent=2),
                name="delete_response_headers",
                attachment_type=allure.attachment_type.JSON,
            )
            assert delete_response.status_code == 204, (
                f"Удаление не подтверждено, статус: {delete_response.status_code}"
            )

        # --- GET после удаления ---
        with allure.step("Проверяем, что объект действительно удалён"):
            get_after_delete = entity_actions.client.get(
                Endpoints.GET_BY_ID.format(id=entity.id)
            )
            allure.attach(
                str(get_after_delete.text or get_after_delete.status_code),
                name="get_after_delete_response",
                attachment_type=allure.attachment_type.TEXT,
            )

            if get_after_delete.status_code == 500:
                allure.attach(
                    get_after_delete.text,
                    name="backend_bug_500_on_get",
                    attachment_type=allure.attachment_type.TEXT,
                )
                pytest.xfail(
                    "Known backend issue: GET by non-existing ID returns 500 instead of 404"
                )
            else:
                assert get_after_delete.status_code in (404, 410), (
                    f"Ожидали 404 или 410, получили {get_after_delete.status_code}"
                )

        # --- Повторное удаление ---
        with allure.step("Повторное удаление той же сущности"):
            second_delete = entity_actions.delete_entity(entity.id)
            allure.attach(
                json.dumps(dict(second_delete.headers), indent=2),
                name="second_delete_response_headers",
                attachment_type=allure.attachment_type.JSON,
            )

            if second_delete.status_code == 500:
                pytest.xfail(
                    "Known backend issue: повторное удаление возвращает 500 вместо 204/404"
                )
            else:
                # Если бекенд исправят, допускаем 204 или 404
                assert second_delete.status_code in (204, 404), (
                    f"Ожидали 204 или 404, получили {second_delete.status_code}"
                )
