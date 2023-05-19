from abc import ABC, abstractmethod

from sqlalchemy import Table

from app import App


class BaseAccessor(ABC):
    def __init__(self, app: App):
        self.__app = app

    @abstractmethod
    async def get(self, *args, **kwargs) -> Table: ...

    @abstractmethod
    async def create(self, *args, **kwargs) -> Table: ...

    @abstractmethod
    async def update(self, *args, **kwargs) -> Table: ...

    @abstractmethod
    async def delete(self, *args, **kwargs) -> None: ...

    @property
    def app(self) -> App:
        return self.__app
