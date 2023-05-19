from app import App


class BaseManager:
    def __init__(self, app: App):
        self.__app = app

    @property
    def app(self) -> App:
        return self.__app
