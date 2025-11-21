import allure
import pytest

from src.api.actions.post_aciton import PostActions
from src.api.models import PostRequest, PostResponse


@allure.parent_suite("API test-service")
@allure.suite("Post Management")
@allure.sub_suite("POST /wp-json/wp/v2/posts")
@allure.epic("API test-service")
@allure.feature("Post")
@allure.story("Создание нового поста")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "create", "v1.0")
@allure.label("owner", "Alexey Yumanov")
@allure.testcase("Создание поста через API")
@allure.description("""
**Цель:** Проверить успешное создание поста через эндпоинт `/wp-json/wp/v2/posts`.

**Ожидаемый результат:**
- HTTP 201
- Возвращён объект `PostResponse` с корректным `id`
- Все поля совпадают с отправленными данными
""")
@pytest.mark.api
class TestCreatePost:
    @allure.title("TC-P1. Создание поста через API с валидными данными")
    def test_create_post(self, post_actions: PostActions):
        request_data = PostRequest.random()

        created = post_actions.create_post(request_data)
        assert isinstance(created, PostResponse), (
            "Ответ не соответствует модели PostResponse"
        )
        assert created.id > 0, "ID должен быть положительным числом"
        assert created.title == request_data.title, (
            "Title не совпадает с исходными данными"
        )
        assert created.status == request_data.status, (
            "Флаг status должен совпадать"
        )

    @allure.title("TC-P2. Создание поста с пустыми полями title и content")
    def test_create_post_with_empty_fields(self, post_actions: PostActions):
        request_data = PostRequest.random(empty=True)

        with allure.step("Пытаемся создать пост с пустым title, content"):
            created = post_actions.create_post(request_data)

        
