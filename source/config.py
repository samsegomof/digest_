import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    min_popularity: int = 70

    DB_HOST: str = os.environ.get('DB_HOST')
    DB_PORT: int = os.environ.get('DB_PORT')
    DB_NAME: str = os.environ.get('DB_NAME')
    PG_USER: str = os.environ.get('PG_USER')
    PG_PWD: str = os.environ.get('PG_PWD')

    @property
    def database_url(self):
        user = f'{self.PG_USER}:{self.PG_PWD}'
        database = f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return f'postgresql+asyncpg://{user}@{database}'

    class Config:
        env_file = '.env'


settings = Settings()
