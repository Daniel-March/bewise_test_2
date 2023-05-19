import typing

from api.config.server_config import ServerConfig
from api.config.tokens_config import TokensConfig

if typing.TYPE_CHECKING:
    from api import API


class Config:
    def __init__(self, api: "API"):
        self.tokens = TokensConfig(api)
        self.server = ServerConfig(api)


async def setup_config(api: "API"):
    api.config = Config(api)
    await api.config.tokens.setup()
    await api.config.server.setup()
