from marshmallow import fields, validates, ValidationError
from ..extensions import ma
from ..models.team import Team
from .user_schema import UserSchema

class TeamSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Team
        load_instance=True
        fields = ("id", "name", "participants")

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True)
    participants = ma.Nested(UserSchema, many=True, exclude=("team_id",))

    @validates("name")
    def validate_unique_team_name(self, value, **kwargs):
        if Team.query.filter_by(name=value).first():
            raise ValidationError("Team name already exists")
        