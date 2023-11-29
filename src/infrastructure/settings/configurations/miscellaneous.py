from pydantic import BaseModel


class MiscConfiguration(BaseModel):
    """Дополнительные настройки"""
    use_redis: bool
    use_utc: bool
    admins: list[int]
    owners: list[int]
    notify_admins: bool = False
    global_timeout: int = 10
