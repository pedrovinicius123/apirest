from marshmallow import fields, validate

from app.extensions import ma
from app.models.user import User


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field(dump_only=True)
    idade = ma.auto_field(required=True, validate=validate.Range(min=1, max=130))
    nome = ma.auto_field(required=True)
    email = fields.Email(required=True)
    team_id = ma.auto_field(required=True)
    senha = fields.String(
        required=True,
        load_only=True,
        validate=validate.Length(min=6),
    )
    admin = ma.auto_field()
