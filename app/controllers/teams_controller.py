from flask import request
from werkzeug.exceptions import Conflict, NotFound, BadRequest
from ..extensions import db
from ..models.team import Team
from ..models.user import User
from ..utils.response import success_response
from ..schemas.teams_schema import TeamSchema
from ..schemas.user_schema import UserSchema

teams_schema = TeamSchema(many=True)
team_schema = TeamSchema()
users_schemas = UserSchema(many=True)
user_schema = UserSchema()

def add_team():
    data = request.json
    print(data)
    team = team_schema.load(data)
    print(team)

    db.session.add(team)
    db.session.commit()
    return success_response(data=team_schema.dump(team), status=201)

def delete_team(id:int):
    team = Team.query.get_or_404(id)

    db.session.delete(team)
    db.session.commit()
    return success_response(data={"message": "Team deleted successfully."})

def update_team():
    data = request.json
    team = Team.query.get_or_404(data["id"])

    for k, v in data.items():
        if k in team.__dict__:
            setattr(team, k, v)

    db.session.commit()
    return success_response(data=team_schema.dump(team))


def get_team(id:int):
    team = Team.query.get_or_404(id)
    return success_response(data=team_schema.dump(team))
    

def get_all_teams():
    teams = Team.query.all()
    return success_response(data=teams_schema.dump(teams))

def get_all_participants():
    parts = User.query.all()
    users = users_schemas.dump(parts)

    return success_response(data=users)

def get_all_team_components(id:int):
    team = Team.query.get_or_404(id)
    users = users_schemas.dump(team.participants)

    return success_response(data=users)
