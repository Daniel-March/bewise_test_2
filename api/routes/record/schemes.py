from marshmallow import Schema, fields

from api.routes.user.schemes import ResponseUserSchema


class RecordGetSchema(Schema):
    uuid = fields.UUID(required=True)


class RecordPutSchema(Schema):
    room_uuid = fields.UUID(required=True)
    title = fields.String(required=True)


class ResponseRecordSchema(Schema):
    uuid = fields.UUID()
    user = fields.Nested(ResponseUserSchema())
