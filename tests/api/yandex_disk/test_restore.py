import allure
import pytest

from src.api.actions import DiskActions
from src.data.data_generator import generate_random_folder_name


@allure.suite("Yandex Disk — Restore")
class TestFolderRestore:

    def test_restore_folder(self, yandex_disk_actions: DiskActions):
        folder_name = generate_random_folder_name()
        yandex_disk_actions.create_folder(folder_name)

        # soft delete
        delete_response = yandex_disk_actions.delete_folder(folder_name)
        assert delete_response.status_code in (202, 204)

        # restore
        restore_response = yandex_disk_actions.restore_trash_item(folder_name)
        assert restore_response.status_code in (201, 202)
