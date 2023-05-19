import asyncio

from api import create_api, setup_api
from app import create_app, setup_app


async def main():
    app = await create_app()
    await setup_app(app)

    api = await create_api()
    await setup_api(api, app=app)

    await api.run()


if __name__ == '__main__':
    asyncio.run(main())
