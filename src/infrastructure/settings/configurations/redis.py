from pydantic import RedisDsn, BaseModel


class RedisConfiguration(BaseModel):
    """Настройки для Redis"""
    host: str
    port: int
    db: int

    @property
    def dsn(cls):
        """Ссылка"""
        return RedisDsn(f"redis://@{cls.host}:{cls.port}")
