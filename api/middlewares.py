import typing
import logging
from aiohttp.web_exceptions import HTTPNotFound, HTTPUnprocessableEntity
from aiohttp.web_middlewares import middleware
from aiohttp.web_response import Response
from aiohttp_apispec import validation_middleware

from api.exceptions.http_exceptions import (BadRequest, Unauthorized, NotFound, Forbidden, Conflict,
                                            UnprocessableEntity)
from api.utils import json_response

if typing.TYPE_CHECKING:
    from api import API
    from api import Request


@middleware
async def error_handling_middleware(request: "Request", handler):
    try:
        response = await handler(request)
        return response
    except HTTPNotFound as e:
        return json_response({"error": e.text}, status_code=404)
    except HTTPUnprocessableEntity as e:
        return json_response({"error": e.text}, status_code=422)
    except BadRequest as e:
        return json_response({"error": e.text, "type": e.TYPE}, status_code=400)
    except Unauthorized as e:
        return json_response({"error": e.text, "type": e.TYPE}, status_code=401)
    except NotFound as e:
        return json_response({"error": e.text, "type": e.TYPE}, status_code=404)
    except Forbidden as e:
        return json_response({"error": e.text, "type": e.TYPE}, status_code=403)
    except Conflict as e:
        return json_response({"error": e.text, "type": e.TYPE}, status_code=409)
    except UnprocessableEntity as e:
        return json_response({"error": e.text, "type": e.TYPE}, status_code=422)
    except NotImplementedError:
        return json_response({"error": "method hasn't been made yet"}, status_code=501)
    except Exception as e:
        raise e
    except BaseException as e:
        return json_response({"error": f"Shit happens, my friend, {e}"}, status_code=500)


@middleware
async def log_middleware(request: "Request", handler):
    response: Response = await handler(request)
    status = response.status // 100 - 1
    method = request.method
    path = request.path
    status_colors = ["\033[33m", "\033[32m", "\033[34m", "\033[31m", "\033[41m\033[30m\033[1m"]
    method_colors = {"PUT": "\033[33m",
                     "OPTIONS": "\033[34m",
                     "GET": "\033[32m",
                     "POST": "\033[34m",
                     "DELETE": "\033[31m", }
    logging.debug(f"{method_colors[method]}{method} {status_colors[status]}{path} {response.status}\033[0m")
    print(f"{method_colors[method]}{method} {status_colors[status]}{path} {response.status}\033[0m")
    return response


async def setup_middlewares(api: "API"):
    api.middlewares.append(log_middleware)
    api.middlewares.append(error_handling_middleware)
    api.middlewares.append(validation_middleware)
