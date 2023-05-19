import os

from dotenv import load_dotenv

from api.config._base import BaseConfig
from api.exceptions.config_exceptions import EnvVarNotFound


class TokensConfig(BaseConfig):
    lifetime: int
    salt: str

    async def setup(self) -> None:
        load_dotenv()
        self.lifetime = int(os.getenv("TOKENS_LIFETIME"))
        self.salt = os.getenv("SALT")
        if None in (self.lifetime, self.salt):
            raise EnvVarNotFound(text="TokensConfig has None var in necessary field",
                                 data={"TOKENS_LIFETIME": self.lifetime,
                                       "SALT": self.salt})
