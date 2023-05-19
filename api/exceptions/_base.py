import json
from abc import abstractmethod, ABC
from datetime import datetime


class DefaultException(BaseException, ABC):
    @property
    @abstractmethod
    def TYPE(self) -> str: ...

    def __init__(self, *, text: str, data: dict = None):
        self.__text = text
        self.__data = data

    @property
    def text(self):
        return self.__text

    @property
    def data(self):
        return self.__data

    def __str__(self):
        _data_dump = json.dumps(self.data)

        _type = self.TYPE
        _datetime = datetime.utcnow().strftime('%H:%M:%S-%d.%m.%Y')
        _text = f"{len(self.text)}[{self.text}]"
        _data = f"{len(_data_dump)}[{_data_dump}]"

        return f"{_type} {_datetime} {_text} {_data}"
