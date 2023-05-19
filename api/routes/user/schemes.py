from marshmallow import Schema, fields


class UserPostSchema(Schema):
    name = fields.String(required=True)


class ResponseUserSchema(Schema):
    uuid = fields.UUID()
    name = fields.String()
