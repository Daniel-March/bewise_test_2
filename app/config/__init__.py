import typing

from app.config.database_config import DatabaseConfig

if typing.TYPE_CHECKING:
    from app import App


class Config:
    def __init__(self, app: "App"):
        self.database = DatabaseConfig(app)


async def setup_config(app: "App"):
    app.config = Config(app)
    await app.config.database.setup()
