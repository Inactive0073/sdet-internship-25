import json

import allure
from pydantic import ValidationError
from requests import Response


def parse_response(model, response: Response):
    """Безопасно конвертирует ответ API в модель, даже если контракт частично нарушен."""
    allure.step(f"Десериализация ответа в {model.__name__}")
    try:
        data = response.json()
        if not isinstance(data, dict):
            raise TypeError(
                f"Ожидался JSON-объект (dict), но получен {type(data).__name__ if type(data).__name__ else data}: {data}"
            )
        return model(**data)
    except (ValidationError, TypeError) as e:
        allure.attach(
            response.text,
            name="invalid_response_body",
            attachment_type=allure.attachment_type.JSON,
        )
        raise AssertionError(
            f"Ошибка валидации или структуры ответа API:\n{e}\nОтвет сервера: {response.text}"
        )


def parse_list_response(model, response: Response):
    """Парсит список ответов API в список моделей. Работает как с `[{}, {}]`, так и с `{'entity': [...]}`."""
    allure.step(f"Десериализация списка объектов в {model.__name__}")
    try:
        data = response.json()
    except json.JSONDecodeError:
        # 🔹 Если сервер вернул строку, но не JSON
        text = response.text.strip()
        allure.attach(
            text,
            name="invalid_json_body",
            attachment_type=allure.attachment_type.TEXT,
        )

        if not text:
            raise AssertionError(
                f"Пустое тело ответа от API. Ожидался JSON объект модели {model.__name__}."
            )

        raise AssertionError(
            f"Ответ не является корректным JSON.\n"
            f"Получено: {text[:200]}...\n"
            f"URL: {response.url}\n"
            f"Status: {response.status_code}"
        )
    except ValueError as e:
        raise AssertionError(
            f"Ответ не является корректным JSON: {e}\nТело: {response.text}"
        )

    # Универсальная логика: поддерживаем оба формата — list и dict с ключом entity
    if isinstance(data, dict):
        data = data.get("entity", [])

    if not isinstance(data, list):
        raise TypeError(
            f"Ожидался список объектов, но получен {type(data).__name__}: {data}"
        )

    try:
        return [model(**item) for item in data]
    except ValidationError as e:
        allure.attach(
            json.dumps(data, ensure_ascii=False, indent=2),
            "invalid_list_body",
            allure.attachment_type.JSON,
        )
        raise AssertionError(f"Ошибка валидации списка объектов: {e}")
