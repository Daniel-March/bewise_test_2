from datetime import datetime, timedelta

from aiohttp_apispec import request_schema

from api import View, TokenModel
from api.exceptions.http_exceptions import UnprocessableEntity
from api.routes.user.schemes import (ResponseUserSchema, UserPostSchema)
from api.utils import json_response, dict_get, encode_token


class UserView(View):
    @request_schema(UserPostSchema)
    async def post(self):
        name: str = dict_get(self.data, "name", required=True)

        if len(name) < 2:
            raise UnprocessableEntity(text="Name must be longer than 1 char")

        user = await self.api.app.managers.user_manager.create(name=name)
        current_datetime = datetime.utcnow()
        expires_in = current_datetime + timedelta(seconds=self.config.tokens.lifetime)
        token_data = {"profile_uuid": user.uuid,
                      "created_at": current_datetime,
                      "expires_in": expires_in}
        auth_token = encode_token(TokenModel(**token_data),
                                  self.config.tokens.salt)
        return json_response(ResponseUserSchema().dump(user), cookies={"auth_token": auth_token})
