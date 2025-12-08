from typing import Optional

import allure
import requests

from src.data.wp_endpoints import Endpoints


class APIClient:
    def __init__(self, base_url: str = Endpoints.BASE, headers: Optional[dict] = None):
        self.base_url = base_url
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)

    @allure.step("GET запрос: {endpoint}")
    def get(self, endpoint: str, **kwargs):
        return self.session.get(f"{self.base_url}{endpoint}", **kwargs)

    @allure.step("POST запрос: {endpoint}")
    def post(self, endpoint: str, **kwargs):
        return self.session.post(f"{self.base_url}{endpoint}", **kwargs)

    @allure.step("PATCH запрос: {endpoint}")
    def patch(self, endpoint: str, **kwargs):
        return self.session.patch(f"{self.base_url}{endpoint}", **kwargs)

    @allure.step("DELETE запрос: {endpoint}")
    def delete(self, endpoint: str, **kwargs):
        return self.session.delete(f"{self.base_url}{endpoint}", **kwargs)

    @allure.step("PUT запрос: {endpoint}")
    def put(self, endpoint: str, **kwargs):
        return self.session.put(f"{self.base_url}{endpoint}", **kwargs)
