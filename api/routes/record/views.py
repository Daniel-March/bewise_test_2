import io
from uuid import UUID

import pydub
from aiohttp.web import FileResponse
from aiohttp_apispec import request_schema

from api import View
from api.exceptions.http_exceptions import Forbidden, UnprocessableEntity
from api.routes.record.schemes import (RecordGetSchema, ResponseRecordSchema)
from api.utils import json_response, check_auth, dict_get


class RecordView(View):
    @request_schema(RecordGetSchema)
    @check_auth
    async def get(self):
        record_uuid: UUID = dict_get(self.data, "uuid", required=True)
        record = await self.api.app.managers.record_manager.get(uuid=record_uuid)

        if record.user.uuid != self.token_data.profile_uuid:
            raise Forbidden(text="You have no access to get this record",
                            data={"record_uuid": record.uuid})

        return FileResponse(f"/app/storage/{record.uuid.hex}", headers={"Content-Type": "audio/mp3"})

    @check_auth
    async def post(self):
        wav = io.BytesIO(await self.request.content.read())
        mp3 = io.BytesIO()
        try:
            pydub.AudioSegment.from_wav(wav).export(mp3, format="mp3")
        except pydub.exceptions.CouldntDecodeError:
            raise UnprocessableEntity(text="Wrong file format. Wav required")

        record = await self.api.app.managers.record_manager.create(user=self.token_data.profile_uuid)
        with open(f"/app/storage/{record.uuid.hex}", "wb") as f:
            f.write(mp3.read())

        return json_response({"record": {**ResponseRecordSchema().dump(record),
                                         "url": f"/record?uuid={record.uuid}"}})
