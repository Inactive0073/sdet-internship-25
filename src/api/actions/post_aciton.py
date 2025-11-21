from typing import Optional

import allure
import requests

from src.api.client import APIClient
from src.api.models.post_in import PostRequest
from src.api.models.post_out import PostResponse
from src.data import Endpoints


class PostActions:
    """Слой бизнес-логики API для работы с постами."""

    def __init__(self, client: APIClient):
        self.client = client

    @allure.step("Создание сущности с данными: {post}")
    def create_post(self, post: PostRequest) -> PostResponse:
        response = self.client.post(
            f"{Endpoints.POSTS}", json=post.model_dump(exclude_none=True)
        )
        response.raise_for_status()
        return PostResponse.model_validate(response.json())


    @allure.step("Получение сущности по ID: {post_id}")
    def get_post_by_id(self, post_id: int) -> PostResponse:
        response = self.client.get(f"{Endpoints.POSTS}/{Endpoints.GET_BY_ID.format(id=post_id)}")
        response.raise_for_status()
        return PostResponse.model_validate(response.json())


    @allure.step("Частичное обновление сущности ID={post_id}")
    def patch_post(self, post_id: int, post: PostRequest) -> requests.Response:
        response = self.client.patch(
            f"{Endpoints.POSTS}/{Endpoints.GET_BY_ID.format(id=post_id)}", json=post.model_dump(exclude_none=True)
        )
        response.raise_for_status()
        return response


    @allure.step("Удаление сущности ID={post_id}")
    def delete_post(self, post_id: int) -> requests.Response:
        response = self.client.delete(f"{Endpoints.POSTS}/{Endpoints.GET_BY_ID.format(id=post_id)}")
        response.raise_for_status()
        return response
