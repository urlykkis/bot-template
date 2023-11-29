from pydantic import SecretStr, BaseModel


class TelegramConfiguration(BaseModel):
    """Настройки для Telegram бота"""
    token: SecretStr
    tag: str
