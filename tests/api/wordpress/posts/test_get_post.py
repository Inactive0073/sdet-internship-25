import allure
import pytest

from src.api.actions import PostActions
from src.api.models.wordpress.post import PostCreationResponse
from src.services.db.dao import PostDAO


@allure.parent_suite("API WordPress")
@allure.suite("Post Management")
@allure.sub_suite("GET /wp-json/wp/v2/posts")
@allure.epic("API WordPress")
@allure.feature("Get Post by ID")
@allure.label("owner", "Alexey Yumanov")
@pytest.mark.api
@pytest.mark.wordpress
class TestGetEntityById:
    @allure.title("TC-P3: Получение существующего поста (позитивный)")
    @allure.story("Получение поста по ID")
    @allure.testcase("Получение поста по ID через API")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "positive", "posts", "get", "v1.0")
    @allure.description("""
    <b>Цель:</b> Проверить успешное получение поста по `id` через эндпоинт `/wp-json/wp/v2/posts/{id}`.
    
    <b>Ожидаемый результат:</b>
        - HTTP 200""")
    @pytest.mark.positive
    def test_post_by_id(self, post_in_db, post_actions: PostActions, post_dao: PostDAO):
        _, post_id = post_in_db

        fetched = post_actions.get_post_by_id(post_id)

        post_in_db = post_dao.get_post(post_id)

        assert post_in_db is not None, "Пост не найден в БД"

        assert isinstance(fetched, PostCreationResponse), (
            "Ответ не соответствует модели EntityResponse"
        )
        assert fetched.id == post_id, (
            f"ID должен совпадать: ожидали {post_id}, получили {fetched.id}"
        )
        assert post_in_db.get("post_title") == fetched.title.rendered, (
            "Title поста в БД не совпадает с полученными данными"
        )
        assert post_in_db.get("post_content") == fetched.content.text, (
            "Content поста в БД не совпадает с полученными данными"
        )

    @allure.title("TC-P6: Получение несуществующего поста (негативный)")
    @allure.story("Получение поста по несуществующему ID")
    @allure.testcase("Получение поста по несуществующему ID через API")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api", "negative", "posts", "get", "v1.0")
    @allure.description(
        """<b>Цель:</b> Проверить корректность обработки запроса на получение поста 
        по несуществующему `id` через эндпоинт `/wp-json/wp/v2/posts/{id}`.
        
        <b>Ожидаемый результат:</b>
        - HTTP 404
        - Сообщение об ошибке в теле ответа
        """
    )
    @pytest.mark.negative
    def test_get_post_by_nonexistent_id(
        self, post_actions: PostActions, post_dao: PostDAO
    ):
        nonexistent_id = 99999999  # Предполагается, что такого ID нет

        with allure.step(
            f"Пытаемся получить пост с несуществующим ID={nonexistent_id}"
        ):
            response = post_actions.get_post_by_id_no_raise(nonexistent_id)
            allure.attach(
                str(response.text or response.status_code),
                name="get_nonexistent_post_response",
                attachment_type=allure.attachment_type.TEXT,
            )
            post_in_db = post_dao.get_post(nonexistent_id)
            assert post_in_db is None, "Пост с несуществующим ID найден в БД"
            assert response.status_code == 404, (
                f"Ожидался статус код 404, получен {response.status_code}"
            )
