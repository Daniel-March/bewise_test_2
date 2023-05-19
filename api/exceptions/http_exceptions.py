from api.exceptions._base import DefaultException


class BadRequest(DefaultException):
    TYPE = "HTTP_400"


class Unauthorized(DefaultException):
    TYPE = "HTTP_401"


class NotFound(DefaultException):
    TYPE = "HTTP_404"


class Forbidden(DefaultException):
    TYPE = "HTTP_403"


class Conflict(DefaultException):
    TYPE = "HTTP_409"


class UnprocessableEntity(DefaultException):
    TYPE = "HTTP_422"
