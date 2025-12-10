from .base import YandexDiskBaseModel


class TrashItem(YandexDiskBaseModel):
    path: str
    type: str
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
    _embedded: TrashEmbedded
