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

    def _build_url(self, endpoint: str) -> str:
        """Собирает конечный URL для запроса."""
        if endpoint.startswith(("http://", "https://")):
            return endpoint
        return f"{self.base_url}{endpoint}"

    @allure.step("GET запрос: {endpoint}")
    def get(self, endpoint: str, **kwargs):
        url = self._build_url(endpoint)
        return self.session.get(url, **kwargs)

    @allure.step("POST запрос: {endpoint}")
    def post(self, endpoint: str, **kwargs):
        url = self._build_url(endpoint)
        return self.session.post(url, **kwargs)

    @allure.step("PATCH запрос: {endpoint}")
    def patch(self, endpoint: str, **kwargs):
        url = self._build_url(endpoint)
        return self.session.patch(url, **kwargs)

    @allure.step("DELETE запрос: {endpoint}")
    def delete(self, endpoint: str, **kwargs):
        url = self._build_url(endpoint)
        return self.session.delete(url, **kwargs)

    @allure.step("PUT запрос: {endpoint}")
    def put(self, endpoint: str, **kwargs):
        url = self._build_url(endpoint)
        return self.session.put(url, **kwargs)
