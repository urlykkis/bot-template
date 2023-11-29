from pydantic_settings import (BaseSettings, SettingsConfigDict)


class GlobalSettings(BaseSettings):
    """Основные настройки"""
    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env`
        env_file=('.env.prod', '.env', '.env.dev'),
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )
