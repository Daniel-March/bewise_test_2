import typing

if typing.TYPE_CHECKING:
    from app import App


class Managers:
    def __init__(self, app: "App"):
        from app.managers.user_manager import UserManager
        from app.managers.record_manager import RecordManager

        self.user_manager = UserManager(app)
        self.record_manager = RecordManager(app)


async def setup_managers(app: "App"):
    app.managers = Managers(app)
