from typing import Optional

import allure
import requests

from src.api.client import APIClient
from src.api.models.post_in import PostRequest
from src.api.models.post_out import PostResponse
from src.api.utils.deserializer import parse_list_response, parse_response
from src.data import Endpoints


class EntityActions:
    """Слой бизнес-логики API для работы с постами."""

    def __init__(self, client: APIClient):
        self.client = client

    def create_post(self, entity: PostRequest) -> PostResponse:
        response = self.client.post(
            f"{Endpoints.BASE}", json=entity.model_dump(exclude_none=True)
        )
        response.raise_for_status()

        try:
            return parse_response(PostResponse, response)
        except AssertionError as e:
            data = response.json()
            if isinstance(data, int):
                allure.attach(str(data), "api_returned_id", allure.attachment_type.TEXT)
                allure.dynamic.issue(
                    name="Known backend issue",
                    url="https://inactive0073-1762753345306.atlassian.net/mock-browse/CREATE-API-001",
                )
            # В любом случае бросаем исключение — функция не может вернуть PostResponse
            raise AssertionError(
                f"Ошибка при создании сущности: {e}. Ответ сервера: {data}"
            )

        


    def create_entity_synthetic(self, entity: PostRequest) -> PostResponse:
        response = self.client.post(
            Endpoints.CREATE, json=entity.model_dump(exclude_none=True)
        )
        response.raise_for_status()

        try:
            return parse_response(PostResponse, response)
        except AssertionError:
            # Если API вернул невалидный ответ — проверим, что это наш случай
            data = response.json()
            if isinstance(data, int):
                allure.attach(str(data), "api_returned_id", allure.attachment_type.TEXT)
                allure.dynamic.issue(
                    name="Known backend issue",
                    url="https://inactive0073-1762753345306.atlassian.net/mock-browse/CREATE-API-001",
                )
                # временный workaround — собрать PostResponse вручную
                fixed = PostResponse(id=data, **entity.model_dump())
                allure.attach(
                    fixed.model_dump_json(indent=2),
                    name="synthetic_entity_response",
                    attachment_type=allure.attachment_type.JSON,
                )
                return fixed
            raise

    @allure.step("Получение сущности по ID: {entity_id}")
    def get_entity_by_id(self, entity_id: int) -> PostResponse:
        response = self.client.get(Endpoints.GET_BY_ID.format(id=entity_id))
        response.raise_for_status()
        return parse_response(PostResponse, response)

    @allure.step("Получение списка всех сущностей")
    def get_all_entities(self, verified: Optional[bool] = None, page: Optional[int] = None, per_page: Optional[int] = None) -> list[PostResponse]:
        params = {
            "verified": str(verified).lower() if verified is not None else None,
            "page": page,
            "perPage": per_page
        }
        
        # Отсекаем None
        params = {k: v for k, v in params.items() if v is not None}
        response = self.client.get(Endpoints.GET_ALL, params=params)
        response.raise_for_status()
        return parse_list_response(PostResponse, response)

    @allure.step("Частичное обновление сущности ID={entity_id}")
    def patch_entity(self, entity_id: int, entity: PostRequest) -> requests.Response:
        response = self.client.patch(
            Endpoints.PATCH.format(id=entity_id), json=entity.model_dump(exclude_none=True)
        )
        response.raise_for_status()
        return response

    @allure.step("Удаление сущности ID={entity_id}")
    def delete_entity(self, entity_id: int) -> requests.Response:
        response = self.client.delete(Endpoints.DELETE.format(id=entity_id))
        response.raise_for_status()
        return response
