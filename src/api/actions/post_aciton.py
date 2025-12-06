import allure
import requests

from src.api.client import APIClient
from src.api.models.wordpress import PostCreationRequest
from src.api.models.wordpress.post import PostCreationResponse
from src.data import Endpoints


class PostActions:
    """Слой бизнес-логики API для работы с постами."""

    def __init__(self, client: APIClient):
        self.client = client

    @allure.step("Создание сущности с данными: {post}")
    def create_post(self, post: PostCreationRequest) -> PostCreationResponse:
        response = self.client.post(
            f"{Endpoints.POSTS}", json=post.model_dump(exclude_none=True)
        )
        response.raise_for_status()
        return PostCreationResponse.model_validate(response.json())

    @allure.step("Создание поста с пустыми полями: {post}")
    def create_post_with_empty_fields(
        self, post: PostCreationRequest
    ) -> requests.Response:
        return self.client.post(
            f"{Endpoints.POSTS}", json=post.model_dump(exclude_none=True)
        )

    @allure.step("Получение сущности по ID: {post_id}")
    def get_post_by_id(self, post_id: int) -> PostCreationResponse:
        response = self.client.get(
            f"{Endpoints.POSTS}/{Endpoints.GET_BY_ID.format(id=post_id)}"
        )
        response.raise_for_status()
        return PostCreationResponse.model_validate(response.json())

    @allure.step("Получение сущности по ID (без raise_for_status): {post_id}")
    def get_post_by_id_no_raise(self, post_id: int) -> requests.Response:
        return self.client.get(
            f"{Endpoints.POSTS}/{Endpoints.GET_BY_ID.format(id=post_id)}"
        )

    @allure.step("Частичное обновление сущности ID={post_id}")
    def patch_post(self, post_id: int, post: PostCreationRequest) -> requests.Response:
        response = self.client.patch(
            f"{Endpoints.POSTS}/{Endpoints.GET_BY_ID.format(id=post_id)}",
            json=post.model_dump(exclude_none=True),
        )
        response.raise_for_status()
        return response

    @allure.step("Частичное обновление сущности ID={post_id} с некорректными данными")
    def patch_post_with_invalid_data(
        self, post_id: int, post: PostCreationRequest
    ) -> requests.Response:
        return self.client.patch(
            f"{Endpoints.POSTS}/{Endpoints.GET_BY_ID.format(id=post_id)}",
            json=post.model_dump(exclude_none=True),
        )

    @allure.step("Удаление сущности ID={post_id}")
    def delete_post(self, post_id: int, force: bool = True) -> requests.Response:
        force_param = "true" if force else "false"
        response = self.client.delete(
            f"{Endpoints.POSTS}/{Endpoints.GET_BY_ID.format(id=post_id)}?force={force_param}"
        )
        response.raise_for_status()
        return response

    @allure.step("Удаление сущности ID={post_id} без raise_for_status")
    def delete_post_no_raise(self, post_id: int) -> requests.Response:
        return self.client.delete(
            f"{Endpoints.POSTS}/{Endpoints.GET_BY_ID.format(id=post_id)}"
        )
