import allure
import pytest

from src.api.actions.post_aciton import PostActions
from src.api.models.post_in import EntityRequest
from src.api.models.post_out import EntityResponse


@allure.parent_suite("API test-service")
@allure.suite("Entity Management")
@allure.sub_suite("GET /api/get")
@allure.epic("API test-service")
@allure.feature("Entity")
@allure.story("Получение сущности по ID")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "positive", "get", "v1.0")
@allure.label("owner", "Alexey Yumanov")
@allure.testcase("TC-002")
@allure.description("""
**Цель:** Проверить получение ранее созданной сущности по `id`.

**Ожидаемый результат:**
- HTTP 200
- В теле ответа корректная сущность с нужным `id`
""")
@pytest.mark.api
class TestGetEntityById:
    @allure.title("TC-002: Получение сущности по ID")
    def test_get_entity_by_id(self, post: EntityResponse, post_actions: PostActions):
        fetched = post_actions.get_entity_by_id(post.id)

        assert isinstance(fetched, EntityResponse), (
            "Ответ не соответствует модели EntityResponse"
        )
        assert fetched.id == post.id, (
            f"ID должен совпадать: ожидали {post.id}, получили {fetched.id}"
        )
        assert fetched.title == post.title, "Title должен совпадать"
