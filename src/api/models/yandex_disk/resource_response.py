from pydantic import BaseModel


class LinkResponse(BaseModel):
    """Модель для ответов, содержащих href (например, создание папки или upload)"""

    href: str
    method: str
    templated: bool


class ResourceItem(BaseModel):
    """Модель ресурса (папка/файл)"""

    name: str
    path: str
    type: str
