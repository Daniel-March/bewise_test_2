import os

from dotenv import load_dotenv

from api.config._base import BaseConfig
from api.exceptions.config_exceptions import EnvVarNotFound


class ServerConfig(BaseConfig):
    host: str
    port: int

    async def setup(self) -> None:
        load_dotenv()
        self.host = os.getenv("HOST")
        self.port = int(os.getenv("PORT"))
        if None in (self.host, self.port):
            raise EnvVarNotFound(text="ServerConfig has None var in necessary field",
                                 data={"HOST": self.host,
                                       "PORT": self.port})
