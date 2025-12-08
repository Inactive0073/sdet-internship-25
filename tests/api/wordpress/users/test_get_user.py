import allure
import pytest

from src.api.actions import UserActions
from src.api.models.wordpress import UserCreationRequest
from src.services.db.dao import UserDAO


@allure.parent_suite("API WordPress")
@allure.suite("User Management")
@allure.sub_suite("GET /wp-json/wp/v2/users")
@allure.epic("API WordPress")
@allure.feature("Get User by ID")
@allure.label("owner", "Alexey Yumanov")
@pytest.mark.api
@pytest.mark.wordpress
class TestGetEntityById:
    @allure.title("TC-P3: Получение существующего юзера (позитивный)")
    @allure.story("Получение юзера по ID")
    @allure.testcase("Получение юзера по ID через API")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "positive", "users", "get", "v1.0")
    @allure.description("""
    <b>Цель:</b> Проверить успешное получение юзера по `id` через эндпоинт `/wp-json/wp/v2/users/{id}`.
    
    <b>Ожидаемый результат:</b>
        - HTTP 200""")
    def test_user_by_id(self, user_in_db, user_dao: UserDAO, user_actions: UserActions):
        user_obj, user_id = user_in_db
        user_obj: UserCreationRequest

        fetched = user_actions.get_user_by_id(user_id)

        assert user_id == fetched.id, (
            f"ID должен совпадать: ожидали {user_id}, получили {fetched.id}"
        )
        assert user_obj.username == fetched.name, "Никнейм должен совпадать"

        assert user_dao.email_exists(user_obj.email), "Пользователь не найден в БД"
