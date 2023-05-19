import typing

if typing.TYPE_CHECKING:
    from api import API


def setup_routes(api: "API", prefix: str = ""):
    from api.routes.user.views import UserView

    api.router.add_view(prefix, UserView)
