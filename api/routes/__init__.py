import typing

if typing.TYPE_CHECKING:
    from api import API


async def setup_routes(api: "API"):
    from api.routes.record.routes import setup_routes as setup_record_routes
    from api.routes.user.routes import setup_routes as setup_user_routes

    setup_record_routes(api, prefix="/record")
    setup_user_routes(api, prefix="/user")
