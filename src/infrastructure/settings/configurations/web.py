from pydantic import BaseModel


class WebConfiguration(BaseModel):
    """Настройки для Web app"""
    WEBHOOK_URL: str
    WEBHOOK_PATH: str = "/bot/"

    HOST: str = "localhost"
    PORT: int = 8080
