from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    MYSQL_HOST          : str
    MYSQL_PORT          : int
    MYSQL_ROOT_PASSWORD : str
    MYSQL_DATABASE      : str
    MYSQL_USER          : str
    MYSQL_PASSWORD      : str

    class Config:
        env_file = "/app/backend/.env"

@lru_cache()  # 한 번만 실행
def get_setting():
    return Settings()