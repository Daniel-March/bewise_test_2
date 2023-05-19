from app.config import Config, setup_config
from app.managers import Managers, setup_managers
from app.store import Store, setup_store
from app.store.database import Database, setup_database


class App:
    store: Store | None = None
    database: Database | None = None
    managers: Managers | None = None
    config: Config | None = None


async def create_app():
    return App()


async def setup_app(app: App):
    await setup_config(app)
    await setup_store(app)
    await setup_database(app)
    await setup_managers(app)
