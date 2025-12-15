import allure
import pytest
from requests import Response

from src.api.actions.yandex_disk_action import DiskActions
from src.api.models.yandex_disk import LinkResponse, ResourceItem
from src.api.models.yandex_disk.trash import YandexTrashItemsResponse


@allure.epic("API Yandex Disk")
@allure.feature("Trash Management")
@allure.story("Управление Корзиной")
@allure.suite("Trash API Tests")
@allure.link(
    "https://yandex.ru/dev/disk/poligon",
    name="Yandex Disk API Documentation",
)
@allure.label("owner", "Alexey Yumanov")
@pytest.mark.api
@pytest.mark.yandex_disk
class TestYandexDiskTrash:
    @pytest.mark.positive
    @allure.title("TC-YD3: Мягкое удаление папки (Soft Delete)")
    @allure.tag("delete", "soft_delete", "trash")
    def test_delete_folder_soft(
        self,
        yandex_disk_actions: DiskActions,
        temp_created_folder: tuple[str, Response],
    ):
        folder_name, _ = temp_created_folder

        response = yandex_disk_actions.delete_file_or_folder(
            file_or_folder_path=folder_name, permanently="false"
        )
        assert response.status_code == 204, (
            f"Ожидался статус код 204, получен {response.status_code}"
        )
        trash_items_data = yandex_disk_actions.get_trash_items().json()
        assert YandexTrashItemsResponse.model_validate(trash_items_data), (
            "Ответ не соответствует модели YandexTrashItemsResponse"
        )

    @pytest.mark.positive
    @allure.title("TC-YD4: Восстановление элемента из корзины")
    @allure.tag("restore", "trash")
    def test_restore_trash_item(
        self,
        yandex_disk_actions: DiskActions,
        temp_created_folder: tuple[str, Response],
    ):
        folder_name, _ = temp_created_folder

        delete_response = yandex_disk_actions.delete_file_or_folder(
            file_or_folder_path=folder_name, permanently="false"
        )
        assert delete_response.status_code == 204, (
            f"Ожидался статус код 204 при удалении, получен {delete_response.status_code}"
        )
        path_name_in_trash = yandex_disk_actions.get_path_from_trash_by_original_path(
            original_path=folder_name
        )
        assert path_name_in_trash, "Не удалось найти удалённый элемент в корзине"
        restore_response = yandex_disk_actions.restore_trash_item(
            item_path=path_name_in_trash
        )
        assert restore_response.status_code == 201, (
            f"Ожидался статус код 201 при восстановлении, получен {restore_response.status_code}"
        )
        assert LinkResponse.model_validate(restore_response.json()), (
            "Ответ не соответствует модели LinkResponse"
        )

        # Проверяем, что папка снова доступна на диске
        resource_info_response = yandex_disk_actions.get_resource_info(
            resource_path=folder_name
        )
        assert resource_info_response.status_code == 200, (
            f"Ожидался статус код 200 при получении информации о ресурсе, получен {resource_info_response.status_code}"
        )
        assert ResourceItem.model_validate(resource_info_response.json()), (
            "Ответ не соответствует модели ResourceItem"
        )

    @pytest.mark.positive
    @allure.title("TC-YD5: Жесткое удаление папки (Permanent Delete)")
    @allure.tag("delete", "hard_delete", "cleanup")
    def test_delete_folder_permanently(
        self,
        yandex_disk_actions: DiskActions,
        temp_created_folder: tuple[str, Response],
    ):
        folder_name, _ = temp_created_folder

        delete_response = yandex_disk_actions.delete_file_or_folder(
            file_or_folder_path=folder_name, permanently="true"
        )
        assert delete_response.status_code == 204, (
            f"Ожидался статус код 204 при удалении, получен {delete_response.status_code}"
        )

        assert (
            yandex_disk_actions.get_resource_info(resource_path=folder_name).status_code
            == 404
        ), "Папка всё ещё существует на Яндекс Диске после удаления навсегда"

        assert not yandex_disk_actions.is_resource_in_trash(
            original_path=folder_name
        ), "Удалённый элемент доступен для восстановления после удаления навсегда"
