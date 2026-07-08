from flask import Blueprint, jsonify, request
from app.controllers.message_controller import listar_mensagens_por_usuario
from app.controllers.user_controller import (
    atualizar_usuario,
    criar_usuario,
    deletar_usuario,
    listar_usuarios,
    login_usuario,
    mostrar_usuario
)
from flask_jwt_extended import jwt_required, unset_jwt_cookies
users_bp = Blueprint("users", __name__)

@users_bp.route("/", methods=["GET"])
def get_users():
    response, status = listar_usuarios()
    return jsonify(response), status

@users_bp.route("/<int:id>", methods=["GET"])
def get_user(id:int):
    response, status = mostrar_usuario(id)
    return jsonify(response), status

@users_bp.route("/login", methods=["POST"])
def login_user():
    data = request.json
    return login_usuario(data)

@users_bp.route("/logout", methods=["POST"])
def logout_user():
    response = jsonify({"success": True, "message": "Logout realizado"})
    unset_jwt_cookies(response)
    return response
    
@users_bp.route("/", methods=["POST"])
def post_user():
    data = request.get_json()
    return criar_usuario(data)

@users_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def patch_user(id):
    data = request.get_json()
    response, status = atualizar_usuario(id, data)
    return jsonify(response), status

@users_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    response, status = deletar_usuario(id)
    if status == 204:
        return "", 204
    return jsonify(response), status

@users_bp.route("/<int:user_id>/messages", methods=["GET"])
def get_user_messages(user_id):
    response, status = listar_mensagens_por_usuario(user_id)
    return jsonify(response), status
