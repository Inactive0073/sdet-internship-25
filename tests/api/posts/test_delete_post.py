import json

import allure
import pytest

from src.api.actions.post_aciton import PostActions
from src.api.models.post_out import PostResponse


@allure.parent_suite("API WordPress")
@allure.suite("Post Management")
@allure.sub_suite("DELETE /wp-json/wp/v2/posts")
@allure.epic("API WordPress")
@allure.feature("Post Deletion")
@allure.label("owner", "Alexey Yumanov")
@pytest.mark.api
class TestDeleteEntity:
    @allure.story("Удаление сущности по ID")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "positive", "delete", "v1.0")
    @allure.testcase("TC-P7. Удаление поста")
    @allure.description_html("""
    <b>Цель:</b> Проверить успешное удаление сущности по `id`.

    <b>Ожидаемый результат:</b>
    - HTTP 200 или 204
    - Повторный GET по `id` возвращает 404
    """)
    def test_delete_post(self, post: PostResponse, post_actions: PostActions):
        # --- Первичное удаление ---
        with allure.step("Удаляем созданную сущность"):
            delete_response = post_actions.delete_post(post.id)
            allure.attach(
                json.dumps(dict(delete_response.headers), indent=2),
                name="delete_response_headers",
                attachment_type=allure.attachment_type.JSON,
            )
            assert delete_response.status_code == 200, (
                f"Удаление не подтверждено, статус: {delete_response.status_code}"
            )

        # --- Проверка удаления ---
        with allure.step("Проверяем, что сущность удалена"):
            get_response = post_actions.get_post_by_id_no_raise(post.id)
            allure.attach(
                json.dumps(dict(get_response.headers), indent=2),
                name="get_response_headers_after_delete",
                attachment_type=allure.attachment_type.JSON,
            )
            assert get_response.status_code == 404, (
                f"Сущность не удалена, статус: {get_response.status_code}"
            )

    @allure.story("Удаление несуществующей сущности")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api", "negative", "delete", "v1.0")
    @allure.testcase("TC-P8. Удаление несуществующего поста")
    @allure.description_html("""
    <b>Цель:</b> Проверить корректность обработки попытки удаления несуществующей сущности.
    <b>Ожидаемый результат:</b>
    - HTTP 404
    - В теле ответа есть код ошибки, связанный с отсутствующей сущностью
    """)
    @pytest.mark.negative
    def test_delete_nonexistent_post(self, post_actions: PostActions):
        nonexistent_id = 99999999  # Предполагаемый несуществующий ID

        with allure.step("Пытаемся удалить несуществующую сущность"):
            delete_response = post_actions.delete_post_no_raise(nonexistent_id)
            allure.attach(
                json.dumps(dict(delete_response.headers), indent=2),
                name="delete_response_headers_nonexistent",
                attachment_type=allure.attachment_type.JSON,
            )
            assert delete_response.status_code == 404, (
                f"Ожидался статус код 404, получен {delete_response.status_code}"
            )
            response_json = delete_response.json()
            assert "rest_post_invalid_id" in response_json.get("code", "").lower(), (
                "В сообщении об ошибке должен быть указан 'rest_post_invalid_id'"
            )
