from flask import Blueprint
from ..contollers.teams_controller import (
    add_team,
    delete_team,
    update_team,
    get_team,
    get_all_teams,
    get_all_team_components
)

bp_teams = Blueprint("teams", __name__, url_prefix="/teams")

@bp_teams.route("/", methods=["GET"])
def get_all_teams():
    return get_all_teams()

@bp_teams.route("/", methods=["POST"])
def add_team_to_db():
    return add_team()

@bp_teams.route("/<int:id>/participants", methods=["GET"])
def get_team_participants(id:int):
    return get_all_team_components()

@bp_teams.route("/<int:id>", methods=["GET"])
def get_team_by_id(id:int):
    return get_team()

@bp_teams.route("/<int:id>", methods=["DELETE"])
def delete_team_by_id(id:int):
    return delete_team()

@bp_teams.route("/")
def update_team_id():
    return update_team()
