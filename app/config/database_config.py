import os

from dotenv import load_dotenv

from app.config._base import BaseConfig
from app.exceptions.config_exceptions import EnvVarNotFound


class DatabaseConfig(BaseConfig):
    url: str
    db_host: str
    db_user: str
    db_password: str
    db_database: str

    async def setup(self) -> None:
        load_dotenv()
        self.db_host = os.getenv("DATABASE_HOST")
        self.db_user = os.getenv("DATABASE_USER")
        self.db_password = os.getenv("DATABASE_PASSWORD")
        self.db_database = os.getenv("DATABASE_DATABASE")
        if None in (self.db_host, self.db_user, self.db_password, self.db_database):
            raise EnvVarNotFound(text="DatabaseConfig has None var in necessary field",
                                 data={"DATABASE_HOST": self.db_host,
                                       "DATABASE_USER": self.db_user,
                                       "DATABASE_PASSWORD": self.db_password,
                                       "DATABASE_DATABASE": self.db_database})

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_database}"
