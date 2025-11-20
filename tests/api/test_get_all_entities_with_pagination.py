import allure
import pytest

from src.api.actions.post_aciton import EntityActions
from src.api.models.post_in import EntityRequest


@allure.parent_suite("API test-service")
@allure.suite("Entity Management")
@allure.sub_suite("GET /api/get_all")
@allure.epic("API test-service")
@allure.feature("Entity")
@allure.story("Получение списка всех сущностей с пагинацией")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("api", "positive", "list", "v1.0")
@allure.label("owner", "Alexey Yumanov")
@allure.testcase("TC-006")
@allure.description("""
**Цель:** Проверить корректное возвращение списка всех сущностей с дополнительными параметрами verified, page и perPage.  

**Ожидаемый результат:**  
- HTTP 200  
- Ответ — список объектов `EntityResponse`
- Количество соответствует ранее созданным сущностям с ограничениям по параметрам заданным в эндпоинте
""")
@pytest.mark.api
class TestGetAllEntitiesPagination:
    @allure.title("TC-006: Проверка пагинации в getAll")
    @pytest.mark.parametrize("verified, expected_count", [(True, 3), (False, 3)])
    def test_get_all_with_pagination(self, entity_actions: EntityActions, verified, expected_count):
        for _ in range(3):
            entity_actions.create_entity_synthetic(EntityRequest.random(verified=verified))

        page1 = entity_actions.get_all_entities(verified=verified, page=1, per_page=3)
        assert len(page1) == expected_count, f"Ожидали {expected_count} элементов для verified={verified}"

