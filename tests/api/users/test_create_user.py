import allure
import pytest

from src.api.actions import UserActions
from src.api.models import UserCreationRequest
from src.api.models.user import UserCreationResponse


@allure.parent_suite("API WordPress")
@allure.suite("User Management")
@allure.sub_suite("POST /wp-json/wp/v2/users")
@allure.epic("API WordPress")
@allure.feature("User Creation")
@allure.label("owner", "Alexey Yumanov")
@pytest.mark.api
class TestCreatePost:
    @allure.story("Создание нового юзера")
    @allure.title("TC-U1. Создание юзера через API с валидными данными")
    @allure.testcase("Создание юзера через API")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "positive", "users", "create", "v1.0")
    @allure.description("""
    <b>Цель:</b> Проверить успешное создание юзера через эндпоинт `/wp-json/wp/v2/users`.

    <b>Ожидаемый результат:</b>
    - HTTP 201
    - Возвращён корректный объект `UserResponse`
    - Поля совпадают с данными запроса
    """)
    @pytest.mark.positive
    def test_create_post(self, user_actions: UserActions):
        request_data = UserCreationRequest.random()

        created = user_actions.create_user(request_data)
        assert isinstance(created, UserCreationResponse), (
            "Ответ не соответствует модели UserResponse"
        )
        assert created.id > 0, "ID должен быть положительным числом"
        assert request_data.username == created.username, (
            "Username не совпадает с исходными данными"
        )
        assert created.email == request_data.email, "Email должен совпадать"
