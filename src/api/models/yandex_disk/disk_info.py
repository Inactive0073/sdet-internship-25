from .base import YandexDiskBaseModel


class UserDiskInfo(YandexDiskBaseModel):
    uid: str
    login: str
    display_name: str
    country: str
    is_child: bool
    reg_time: str


class YandexDiskInfoResponse(YandexDiskBaseModel):
    user: UserDiskInfo
    system_folders: dict[str, str]
    total_space: int
    used_space: int
    trash_size: int
    is_paid: bool
    revision: int
