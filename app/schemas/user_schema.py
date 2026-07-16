from marshmallow import fields, validate
from app.extensions import ma
from app.models.user import User


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        fields=("id", "nome", "idade", "email", "team_id", "senha_hash")
        

    id = ma.auto_field()
    idade = ma.auto_field(required=True, validate=validate.Range(min=1, max=130))
    nome = ma.auto_field(required=True)
    email = fields.Email(required=True)
    team_id = ma.auto_field(required=True)
    senha_hash = fields.String(
        required=True,
        load_only=True,
        validate=validate.Length(min=6),
    )
    admin = ma.auto_field()
