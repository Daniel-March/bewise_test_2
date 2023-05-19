import base64
import json
from datetime import datetime
from hashlib import sha256
from typing import Optional, Any, Callable

from aiohttp.web_response import json_response as aiohttp_json_response

from api.exceptions.http_exceptions import Unauthorized
from api.models import TokenModel


def json_encoder(data: dict):
    return json.dumps(data, ensure_ascii=False)


def dict_get(dict: dict, param: str, *, required: bool, cast: Any = None, default: object = None,
             on_error: dict[Exception: Any] = None) -> Optional[Any]:
    """dict.get method witch cast to necessary type"""
    value = dict.get(param)

    try:
        if value is not None:
            if cast is not None:
                value = cast(value)
        else:
            value = default
    except Exception as e:
        if on_error is not None:
            for key, value in on_error.items():
                if isinstance(e, key):
                    if isinstance(value, Callable):
                        return value()
                    if isinstance(value, BaseException):
                        raise value
                    return value
        raise e

    if required and value is None:
        raise ValueError("Value can't be None")
    return value


def json_response(data: dict, status_code: int = 200, message: str = None, headers: dict = None, cookies: dict = None):
    if headers is None and cookies is not None:
        headers = {}
    if cookies is not None:
        headers["set-cookie"] = ";".join([f"{k}= {v}; Path=/" for k, v in cookies.items()])

    return aiohttp_json_response(data=data, status=status_code, text=message, headers=headers, dumps=json_encoder)


def error_json_response(data: dict, status_code: int = 500, message: str = "server error", headers=None):
    return aiohttp_json_response(data=data, status=status_code, text=message, headers=headers, dumps=json_encoder)


def encode_token(data: TokenModel, salt: str) -> str:
    data_base64 = base64.b64encode(data.json().encode()).decode()
    sign = sha256(f"{data_base64}{salt}".encode()).hexdigest()
    return f"{data_base64}.{sign}"


def check_token(token: str, salt: str) -> bool:
    token_data, token_sign = [*token.split("."), None][:2]
    return sha256(f"{token_data}{salt}".encode()).hexdigest() == token_sign


def decode_token(token) -> TokenModel:
    token_data = token.split(".")[0]
    data = json.loads(base64.b64decode(token_data.encode()).decode())
    return TokenModel(**data)


def check_auth(func):
    from api import View

    async def inner(view: View, *args, **kwargs):
        auth_token = view.request.cookies.get("auth_token")
        if not auth_token:
            raise Unauthorized(text="Authentication failed. auth_token not found in cookies",
                               data={"auth_token": auth_token})
        token_data = decode_token(auth_token)

        if token_data.expires_in < datetime.utcnow():
            raise Unauthorized(text="Authentication failed. auth_token expired",
                               data={"auth_token": auth_token, "token_data": token_data})

        view.token_data = token_data
        return await func(view, *args, **kwargs)

    return inner
