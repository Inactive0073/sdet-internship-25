import allure
import requests

from src.data.urls import APIUrls


class APIClient:
    def __init__(self, base_url: str = APIUrls.BASE_URL):
        self.base_url = base_url

    @allure.step("GET запрос: {endpoint}")
    def get(self, endpoint: str, **kwargs):
        return requests.get(f"{self.base_url}{endpoint}", **kwargs)

    @allure.step("POST запрос: {endpoint}")
    def post(self, endpoint: str, **kwargs):
        return requests.post(f"{self.base_url}{endpoint}", **kwargs)

    @allure.step("PATCH запрос: {endpoint}")
    def patch(self, endpoint: str, **kwargs):
        return requests.patch(f"{self.base_url}{endpoint}", **kwargs)

    @allure.step("DELETE запрос: {endpoint}")
    def delete(self, endpoint: str, **kwargs):
        return requests.delete(f"{self.base_url}{endpoint}", **kwargs)
