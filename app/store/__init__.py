import typing

if typing.TYPE_CHECKING:
    from app import App


class Store:
    def __init__(self, app: "App"):
        from app.store.user import UserAccessor
        from app.store.record import RecordAccessor

        self.user_accessor = UserAccessor(app)
        self.record_accessor = RecordAccessor(app)


async def setup_store(app: "App"):
    app.store = Store(app)
