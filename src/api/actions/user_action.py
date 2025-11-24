import allure

from src.api.client import APIClient
from src.api.models import UserCreationRequest, UserCreationResponse, UserPublicResponse
from src.data import Endpoints


class UserActions:
    """Слой бизнес-логики API для работы с пользователями."""

    def __init__(self, client: APIClient):
        self.client = client

    @allure.step("Создание сущности с данными: {post}")
    def create_user(self, post: UserCreationRequest) -> UserCreationResponse:
        response = self.client.post(
            f"{Endpoints.USERS}", json=post.model_dump(exclude_none=True)
        )
        response.raise_for_status()
        return UserCreationResponse.model_validate(response.json())

    @allure.step("Получение сущности по ID: {post_id}")
    def get_user_by_id(self, post_id: int) -> UserPublicResponse:
        response = self.client.get(
            f"{Endpoints.USERS}/{Endpoints.GET_BY_ID.format(id=post_id)}"
        )
        response.raise_for_status()
        return UserPublicResponse.model_validate(response.json())
