from functools import lru_cache

from src.infrastructure.settings.configurations import \
    GlobalSettings, TelegramConfiguration, \
    DatabaseConfiguration, MiscConfiguration, \
    RedisConfiguration, WebConfiguration


class Config(GlobalSettings):
    """Конфиг"""
    telegram_bot: TelegramConfiguration
    web: WebConfiguration
    database: DatabaseConfiguration
    redis: RedisConfiguration
    misc: MiscConfiguration


@lru_cache
def load_config(env_file: str = ".env") -> "Config":
    """Загрузка конфига"""
    return Config(_env_file=env_file)
