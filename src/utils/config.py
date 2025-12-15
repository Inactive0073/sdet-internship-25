from environs import Env

env = Env()
env.read_env(override=True)


class Config:
    YANDEX_DISK_TOKEN: str = env.str("YANDEX_DISK_TOKEN")
    USERNAME: str = env.str("YD_USERNAME", "SDET")
    PASSWORD: str = env.str("YD_PASSWORD", "secret_key")
