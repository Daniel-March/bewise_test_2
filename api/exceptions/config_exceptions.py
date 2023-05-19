from api.exceptions._base import DefaultException


class EnvVarNotFound(DefaultException):
    TYPE = "CONFIG_ENV_VAR_NOT_FOUND"
