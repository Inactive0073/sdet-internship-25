import time


def generate_random_folder_name() -> str:
    """Генерирует случайное имя папки для тестов."""
    timestamp = int(time.time())
    return f"test_folder_{timestamp}"
