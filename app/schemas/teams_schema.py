from marshmallow import fields
from ..extensions import ma
from ..models.team import Team

class TeamSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Team

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True)
    participants = fields.Nested("UserSchema", only=("id", "nome"))
