from pydantic import Field

from .base import YandexDiskBaseModel


class TrashItem(YandexDiskBaseModel):
    path: str
    type: str
    origin_path: str = Field(alias="origin_path")
    name: str


class TrashEmbedded(YandexDiskBaseModel):
    path: str
    limit: int
    offset: int
    sort: str
    total: int
    items: list[TrashItem]


class YandexTrashItemsResponse(YandexDiskBaseModel):
    path: str
    type: str
    name: str
    created: str
    modified: str
    embedded_content: TrashEmbedded = Field(alias="_embedded")
