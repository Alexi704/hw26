from marshmallow import fields, Schema


class UserSchema(Schema):
    id = fields.Int(required=True)
    email = fields.Str()
    password = fields.Str()
    name = fields.Str()
    surname = fields.Str()
    # favorite_genre_id = fields.Int()
