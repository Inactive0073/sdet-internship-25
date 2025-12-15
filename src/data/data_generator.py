from uuid import uuid4


def generate_random_folder_name() -> str:
    """Генерирует случайное имя папки для тестов."""
    unique_id = str(uuid4())[:8]
    return f"test_folder_{unique_id}"
