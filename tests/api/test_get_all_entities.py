import allure
import pytest

from src.api.actions.post_aciton import EntityActions
from src.api.models.post_in import EntityRequest
from src.api.models.post_out import EntityResponse


@allure.parent_suite("API test-service")
@allure.suite("Entity Management")
@allure.sub_suite("GET /api/get_all")
@allure.epic("API test-service")
@allure.feature("Entity")
@allure.story("Получение списка всех сущностей")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("api", "positive", "list", "v1.0")
@allure.label("owner", "Alexey Yumanov")
@allure.testcase("TC-003")
@allure.description("""
**Цель:** Проверить корректное возвращение списка всех сущностей.  

**Ожидаемый результат:**  
- HTTP 200  
- Ответ — список объектов `EntityResponse`
- Количество соответствует ранее созданным сущностям
""")
@pytest.mark.api
class TestGetAllEntities:
    @allure.title("TC-003: Получение списка всех сущностей")
    def test_get_all_entities(self, entity_actions: EntityActions):
        created_entities = [
            entity_actions.create_entity_synthetic(EntityRequest.random()) for _ in range(3)
        ]
        entities = entity_actions.get_all_entities()

        assert isinstance(entities, list), "Ответ должен быть списком"
        assert all(isinstance(e, EntityResponse) for e in entities), (
            "Все элементы должны быть EntityResponse"
        )

        returned_ids = {e.id for e in entities}
        for created in created_entities:
            assert created.id in returned_ids, (
                f"Созданный id={created.id} отсутствует в списке"
            )
