from flask import Blueprint
from ..contollers.teams_controller import (
    get_all_participants,
    get_all_team_components,
    add_participants_to_team
)

bp_participants = Blueprint("participants", __name__, url_prefix="/participants")

@bp_participants.route("/", methods=["GET"])
def get_participants():
    return get_all_participants()

@bp_participants.route("/<int:id>", methods=["GET"])
def get_team_components(id:int):
    return get_all_team_components(id)
    

@bp_participants.route("/", methods=["POST"])
def add_participants():
    return add_participants_to_team()
