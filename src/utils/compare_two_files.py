def compare_texts(
    file_path: str, downloaded_content: bytes, encoding: str = "utf-8"
) -> bool:
    """Вспомогательная функция для сравнения контента и файла"""
    with open(file_path, "rb") as f:
        original = f.read()  # тоже bytes!
    return downloaded_content == original
