import allure
import pytest

from src.api.actions.post_aciton import PostActions
from src.api.models.post_in import PostRequest
from src.api.models.post_out import PostResponse


@allure.parent_suite("API WordPress")
@allure.suite("Post Management")
@allure.sub_suite("PATCH /wp-json/wp/v2/posts")
@allure.epic("API WordPress")
@allure.feature("Post Patch")
@allure.label("owner", "Alexey Yumanov")
@pytest.mark.api
class TestPatchEntity:
    @allure.story("Частичное обновление сущности")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api", "positive", "update", "v1.0")
    @allure.testcase("TC-P5. Редактирование поста ")
    @allure.description("""
    **Цель:** Проверить частичное обновление данных сущности через PATCH.  

    <b>Ожидаемый результат:</b> 
    - HTTP 200  
    - Поля, переданные в теле запроса, обновлены
    - Остальные поля остались без изменений
    """)
    @allure.title("TC-P5. Частичное обновление сущности через PATCH")
    @pytest.mark.positive
    def test_patch_entity(self, post: PostResponse, post_actions: PostActions):
        updated_request = PostRequest.random()
        response = post_actions.patch_post(post.id, updated_request)

        assert 200 <= int(response.status_code) <= 204, (
            f"Статус код не соответствует ожидаемому. Текущий статус код: {response.status_code}"
        )
        updated = post_actions.get_post_by_id(post.id)
        assert updated.title.rendered == updated_request.title

    @allure.story("Редактирование поста с некорректным типом данных")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api", "negative", "update", "validation", "v1.0")
    @allure.testcase("TC-P6. Редактирование поста с некорректным типом данных")
    @allure.description("""
    **Цель:** Проверить корректность валидации при частичном обновлении поста с некорректным типом данных.
    <b>Ожидаемый результат:</b>  
    - HTTP 400
    - Возвращена ошибка валидации
    - В теле ответа есть код ошибки, связанный с некорректным типом данных
    """)
    @allure.title("TC-P6. Редактирование поста с некорректным типом данных")
    @pytest.mark.negative
    def test_patch_entity_with_invalid_data(
        self, post: PostResponse, post_actions: PostActions
    ):
        invalid_request = PostRequest.random(
            status="123"
        )  # Некорректный тип данных для поля status

        with allure.step("Пытаемся частично обновить пост с некорректными данными"):
            response = post_actions.patch_post_with_invalid_data(
                post.id, invalid_request
            )

            assert response.status_code == 400, (
                f"Ожидался статус код 400, получен {response.status_code}"
            )
            response_json = response.json()
            assert "rest_invalid_param" in response_json.get("code", "").lower(), (
                "В сообщении об ошибке должен быть указан 'invalid_data'"
            )
