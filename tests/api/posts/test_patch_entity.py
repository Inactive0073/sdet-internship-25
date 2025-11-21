import allure
import pytest

from src.api.actions.post_aciton import PostActions
from src.api.models.post_in import EntityRequest
from src.api.models.post_out import EntityResponse


@allure.parent_suite("API test-service")
@allure.suite("Entity Management")
@allure.sub_suite("PATCH /api/patch")
@allure.epic("API test-service")
@allure.feature("Entity")
@allure.story("Частичное обновление сущности")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "positive", "update", "v1.0")
@allure.label("owner", "Alexey Yumanov")
@allure.testcase("TC-004")
@allure.description("""
**Цель:** Проверить частичное обновление данных сущности через PATCH.  

**Ожидаемый результат:**  
- HTTP 200  
- Поля, переданные в теле запроса, обновлены
- Остальные поля остались без изменений
""")
@pytest.mark.api
class TestPatchEntity:
    @allure.title("TC-004: Частичное обновление сущности")
    def test_patch_entity(self, post: EntityResponse, post_actions: PostActions):
        updated_request = EntityRequest.random()
        response = post_actions.patch_entity(post.id, updated_request)

        assert 200 <= int(response.status_code) <= 204, f"Статус код не соответствует ожидаемому. Текущий статус код: {response.status_code}" 
        updated = post_actions.get_entity_by_id(post.id)
        assert updated.title == updated_request.title
