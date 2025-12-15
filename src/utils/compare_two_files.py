import io
import zipfile


def extract_file_from_zip(
    zip_bytes: bytes, file_name: str
) -> bytes:
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zip_file:
        with zip_file.open(file_name) as extracted:
            return extracted.read()


def compare_texts(
    file_path: str, downloaded_content: bytes, zip_file_path: str = "sdet_data/data.txt"
) -> bool:
    """Вспомогательная функция для сравнения контента и файла"""
    with open(file_path, "rb") as f:
        original = f.read()
    return extract_file_from_zip(downloaded_content, zip_file_path) == original
