from typing import Any

import allure
import pytest

from src.api.actions import PostActions
from src.api.models.wordpress import PostCreationRequest
from src.api.models.wordpress.post import PostCreationResponse
from src.services.db.dao import PostDAO


@allure.parent_suite("API WordPress")
@allure.suite("Post Management")
@allure.sub_suite("POST /wp-json/wp/v2/posts")
@allure.epic("API WordPress")
@allure.feature("Post Creation")
@allure.label("owner", "Alexey Yumanov")
@pytest.mark.api
@pytest.mark.wordpress
class TestCreatePost:
    @allure.story("Создание нового поста")
    @allure.title("TC-P1. Создание поста через API с валидными данными")
    @allure.testcase("Создание поста через API")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "positive", "posts", "create", "v1.0")
    @allure.description("""
    <b>Цель:</b> Проверить успешное создание поста через эндпоинт `/wp-json/wp/v2/posts`.

    <b>Ожидаемый результат:</b>
    - HTTP 201
    - Возвращён корректный объект `PostResponse`
    - Поля совпадают с данными запроса
    """)
    @pytest.mark.positive
    def test_create_post(self, post_actions: PostActions, post_dao: PostDAO):
        request_data = PostCreationRequest.random()

        created = post_actions.create_post(request_data)
        assert isinstance(created, PostCreationResponse), (
            "Ответ не соответствует модели PostResponse"
        )
        assert created.id > 0, "ID должен быть положительным числом"
        assert request_data.title in (created.title.raw, created.title.rendered), (
            "Title не совпадает с исходными данными"
        )
        assert created.status == request_data.status, "Флаг status должен совпадать"

        post_in_db = post_dao.get_post(created.id)
        assert post_in_db is not None, "Пост не найден в БД"

        assert post_in_db["post_title"] == request_data.title, (
            "Title поста в БД не совпадает с исходными данными"
        )
        assert post_in_db["post_content"] == request_data.content, (
            "Content поста в БД не совпадает с исходными данными"
        )

    @allure.story("Создание поста — валидация данных")
    @allure.title("TC-P2. Создание поста с пустыми полями title и content")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api", "negative", "posts", "create", "validation", "v1.0")
    @allure.description("""
    <b>Цель:</b> Проверить корректность валидации при создании поста 
    с пустыми полями `title` и `content`.

    <b>Ожидаемый результат:</b>
    - HTTP 400
    - Возвращена ошибка валидации
    - В теле ответа есть код ошибки, связанный с пустыми полями
    """)
    @pytest.mark.negative
    def test_create_post_with_empty_fields(
        self, post_actions: PostActions, post_dao: PostDAO
    ):
        request_data = PostCreationRequest.random(empty=True)

        count_post = post_dao.count_posts()
        with allure.step("Пытаемся создать пост с пустым title, content"):
            created = post_actions.create_post_with_empty_fields(request_data)

            assert created.status_code == 400, (
                f"Ожидался статус код 400, получен {created.status_code}"
            )
            response_json: dict[str, Any] = created.json()
            assert "empty_content" in response_json.get("code", "").lower(), (
                "В сообщении об ошибке должен быть указан 'empty_content'"
            )

            assert post_dao.count_posts() == count_post, (
                "Количество постов в БД изменилось после попытки создания с пустыми полями"
            )
