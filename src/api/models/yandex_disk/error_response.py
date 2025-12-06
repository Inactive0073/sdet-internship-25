from .base import YandexDiskBaseModel


class YandexDiskInfoErrorResponse(YandexDiskBaseModel):
    error: str
    description: str
    message: str
