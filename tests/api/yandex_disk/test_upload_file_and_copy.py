import allure
import pytest
from requests import Response

from src.api.actions import DiskActions
from src.api.models.yandex_disk.data_classes import (
    ErrorDataClass,
    LinkDataClass,
    ResourceDataClass,
)
from src.utils import compare_texts


@allure.epic("Cloud API")
@allure.feature("Yandex Disk Management")
@allure.story("Создание и получение ресурсов (Папки)")
@allure.suite("Folders CRUD Operations")
@allure.sub_suite("PUT /v1/disk/resources")
@allure.label("owner", "Alexey Yumanov")
@pytest.mark.api
@pytest.mark.yandex_disk
@pytest.mark.test
class TestDiskItemManager:
    def test_upload_and_copy(
        self,
        yandex_disk_actions: DiskActions,
        local_file: str,
        temp_created_folder: tuple[str, Response],
    ):
        unique_folder_name, _ = temp_created_folder

        input_folder = f"{unique_folder_name}/input_data"
        output_folder = f"{unique_folder_name}/output_data"
        disk_path_input = f"{input_folder}/data.txt"
        disk_path_output = f"{output_folder}/data.txt"

        created_folder_response = yandex_disk_actions.create_folder(input_folder)
        assert created_folder_response.status_code == 201, (
            f"Ожидался код статуса 201, получен {created_folder_response.status_code}"
        )

        created_folder_response = yandex_disk_actions.create_folder(output_folder)
        assert created_folder_response.status_code == 201, (
            f"Ожидался код статуса 201, получен {created_folder_response.status_code}"
        )

        link_obj = LinkDataClass.from_dict(created_folder_response.json())
        assert link_obj.href, "Ссылка для загрузки файла пустая"

        with allure.step("Загружауем файл в папку input_data"):
            upload_link_resp = yandex_disk_actions.get_upload_link(disk_path_input)
            with open(local_file, "rb") as f:
                upload_response = yandex_disk_actions.upload_file(
                    LinkDataClass.from_dict(upload_link_resp.json()).href, f
                )
            assert upload_response.status_code == 201, (
                f"Ожидался 201, получен {upload_response.status_code}"
            )

        with allure.step(f"Копируем файл из {disk_path_input} в {disk_path_output}"):
            copy_response = yandex_disk_actions.copy_resource(
                _from=disk_path_input, to=disk_path_output
            )
            assert copy_response.status_code in (201, 202), (
                f"Копирование не удалось, код статуса: {copy_response.status_code}"
            )

        resource_obj = ResourceDataClass.from_dict(
            yandex_disk_actions.get_resource_info(disk_path_output).json()
        )
        with allure.step("Проверяем значения скопированного объекта на bool"):
            assert resource_obj.mime_type, (
                f"Скопированный объект не имеет значения для поля name: {resource_obj.name=}"
            )
            assert resource_obj.mime_type, (
                f"Скопированный объект не имеет значения для поля mime_type: {resource_obj.mime_type=}"
            )
            assert resource_obj.mime_type, (
                f"Скопированный объект не имеет значения для поля media_type: {resource_obj.media_type=}"
            )

        with allure.step(
            "Повторно пытаемся скопировать data.txt в output_input из input_data"
        ):
            copy_response = yandex_disk_actions.copy_resource(
                _from=disk_path_input, to=disk_path_output
            )
            assert copy_response.status_code == 409, (
                f"Копирование удалось, ожидалось, что копирование будет не выполнено, код статуса: {copy_response.status_code}"
            )
            err_response = ErrorDataClass.from_dict(copy_response.json())
            assert err_response.error, (
                f"Ожидалось, что значение не пустое: {err_response.error}"
            )
            assert err_response.description, (
                f"Ожидалось, что значение не пустое: {err_response.description}"
            )
            assert err_response.message, (
                f"Ожидалось, что значение не пустое: {err_response.message}"
            )

    @pytest.mark.positive
    def test_download_file(
        self,
        yandex_disk_actions: DiskActions,
        local_file: str,
        temp_created_folder: tuple[str, Response],
    ):
        unique_folder_name, _ = temp_created_folder
        sdet_folder = f"{unique_folder_name}/sdet_data"

        created_folder_response = yandex_disk_actions.create_folder(sdet_folder)
        assert created_folder_response.status_code == 201, (
            f"Ожидался код статуса 201, получен {created_folder_response.status_code}"
        )

        link_obj = LinkDataClass.from_dict(created_folder_response.json())
        assert link_obj.href, "Ссылка для загрузки файла пустая"

        with allure.step("Загружауем файл в папку {sdet_folder}"):
            upload_link_resp = yandex_disk_actions.get_upload_link(
                f"{sdet_folder}/data.txt"
            )
            with open(local_file, "rb") as f:
                upload_response = yandex_disk_actions.upload_file(
                    LinkDataClass.from_dict(upload_link_resp.json()).href, f
                )
            assert upload_response.status_code == 201, (
                f"Ожидался 201, получен {upload_response.status_code}"
            )

        with allure.step("Получаем ссылку для скачивания файла"):
            download_file_response = yandex_disk_actions.get_download_url(sdet_folder)
            assert download_file_response.status_code == 200, (
                f"Ожидался 200, получен {download_file_response.status_code}"
            )
        with allure.step(
            "Скачиваем файл по ссылке {link_obj.href} и начинаем сравнение"
        ):
            link_obj = LinkDataClass.from_dict(download_file_response.json())
            file = yandex_disk_actions.download_file_by_url(link_obj.href)
            assert compare_texts(local_file, file.content), "Файлы не совпадают."
