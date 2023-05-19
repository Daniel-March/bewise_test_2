from app.exceptions._base import DefaultException


class NotFound(DefaultException):
    TYPE = "DB_RECORD_NOT_FOUND"


class Conflict(DefaultException):
    TYPE = "DB_RECORD_CONFLICT"
