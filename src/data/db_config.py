from dataclasses import dataclass, asdict
from environs import Env


@dataclass
class DBConfig:
    host: str = "db"
    port: int = 3306
    user: str = "wordpress"
    password: str = "wordpress"
    database: str = "wordpress"


def _load_config_to_dict() -> dict:
    env = Env()
    env.read_env(override=True)
    # In a real-world scenario, you might load these from environment variables or a config file
    host, port = env.str("WORDPRESS_DB_HOST", "db").split(":") if ":" in env.str("WORDPRESS_DB_HOST", "db") else (env.str("WORDPRESS_DB_HOST", "db"), "3306")
    return asdict(
        DBConfig(
            host=host,
            port=int(port),
            user=env.str("WORDPRESS_DB_USER"),
            password=env.str("WORDPRESS_DB_PASSWORD"),
            database=env.str("WORDPRESS_DB_NAME"),
        )
    )


db_config = _load_config_to_dict()
