import asyncio

from aiohttp import web
from aiohttp.web import (Application,
                         Request as AiohttpRequest)
from aiohttp.web_response import json_response
from aiohttp.web_urldispatcher import View as AiohttpView
from aiohttp_apispec import setup_aiohttp_apispec

from api.config import Config, setup_config
from api.middlewares import setup_middlewares
from api.models import TokenModel
from api.routes import setup_routes
from app import App


class API(Application):
    app: App | None = None
    config: Config | None = None

    async def run(self) -> None:
        runner = web.AppRunner(self)
        await runner.setup()
        site = web.TCPSite(runner, host=self.config.server.host, port=self.config.server.port)
        await site.start()
        await asyncio.Future()


class Request(AiohttpRequest):
    @property
    def api(self) -> API:
        return super().app()


class View(AiohttpView):
    token_data: TokenModel | None = None

    @property
    def request(self) -> Request:
        return super().request

    @property
    def api(self) -> API:
        return super().request.app

    @property
    def config(self) -> Config:
        return self.api.config

    @property
    def data(self) -> dict:
        return self.request.get("data", {})

    @property
    def query(self) -> dict:
        return self.request.__getattribute__("query")

    @staticmethod
    async def options():
        return json_response({})


async def create_api():
    return API(client_max_size=1024*1024*8*20)


async def setup_api(api: API, app: App):
    api.app = app
    await setup_config(api)
    await setup_routes(api)
    setup_aiohttp_apispec(api)
    await setup_middlewares(api)
