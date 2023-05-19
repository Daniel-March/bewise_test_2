import typing
from abc import ABC, abstractmethod

if typing.TYPE_CHECKING:
    from app import App


class BaseConfig(ABC):
    def __init__(self, app: "App"):
        self.__app = app

    @property
    def app(self) -> "App":
        return self.__app

    @abstractmethod
    async def setup(self) -> None: ...
