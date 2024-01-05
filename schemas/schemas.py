from extensions import ma
from marshmallow import fields

class dbSchema(ma.Schema):
    id = fields.Integer(dump_only = True)

class UserSchema(dbSchema):
    name = fields.String()
    email = fields.String()

class UserAdminSchema(UserSchema):
    password = fields.String()
    is_admin = fields.Boolean()
    date_created = fields.DateTime()

class TagSchema(dbSchema):
    name = fields.String()

class ReplySchema(dbSchema):
    post_id = fields.Integer()
    content = fields.String()
    date = fields.DateTime()
    user_id = fields.Integer()
    user_obj = fields.Nested(
        UserSchema, exclude={'id'} 
    )

class PostSchema(dbSchema):
    title = fields.String()
    content = fields.String()
    date = fields.DateTime()
    tags = fields.List(
        fields.Nested(TagSchema),
        many=True
    )
    user_id = fields.Integer()
    user_obj = fields.Nested(
        UserSchema, exclude={'id'} 
    )
    replies = fields.Nested(
        ReplySchema,
        exclude={'id'},
        many=True
    )
