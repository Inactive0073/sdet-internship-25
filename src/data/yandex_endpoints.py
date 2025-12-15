class YandexEndpoints:
    """Спецификации API для работы с Яндекс Диском."""

    BASE = "https://cloud-api.yandex.net"

    DISK_INFO = "/v1/disk/"
    RESOURCES = "/v1/disk/resources"
    UPLOAD = "/v1/disk/resources/upload"

    GET_TRASH_ITEMS = "/v1/disk/trash/resources"
    RESTORE_TRASH_ITEM = "/v1/disk/trash/resources/restore"
