import typing
from abc import ABC, abstractmethod

if typing.TYPE_CHECKING:
    from api import API


class BaseConfig(ABC):
    def __init__(self, api: "API"):
        self.__api = api

    @property
    def api(self) -> "API":
        return self.__api

    @abstractmethod
    async def setup(self) -> None: ...
