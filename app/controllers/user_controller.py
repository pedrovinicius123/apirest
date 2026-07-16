from flask import jsonify
from app.extensions import db
from app.models.user import User
from app.schemas.user_schema import UserSchema
from app.utils.response import error_response, success_response
from ..extensions import auth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, set_access_cookies

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@auth.user_identity_loader
def load_user_identity(user):
    if hasattr(user, "id"):
        return str(user.id)
    return str(user)

@auth.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=int(identity)).one_or_none()

def listar_usuarios():
    usuarios = User.query.all()
    return success_response(users_schema.dump(usuarios))

def mostrar_usuario(id:int):
    user = User.query.get_or_404(id)
    return success_response({k:v for k,v in user.__dict__.items() if k in ["id", "nome", "idade", "email", "admin"]})

def _build_auth_response(user, status_code=200):
    token = create_access_token(identity=str(user.id))
    payload = {
        "success": True,
        "data": {
            **user_schema.dump(user),
            "access_token": token,
        },
    }
    response = jsonify(payload)
    response.status_code = status_code
    set_access_cookies(response, token)
    return response


def criar_usuario(data):
    dados_validados = user_schema.load(data)
    dados_validados["senha_hash"] = generate_password_hash(dados_validados.get("senha_hash"))
    novo_usuario = User(**dados_validados)

    if not User.query.filter_by(email=novo_usuario.email).first():
        db.session.add(novo_usuario)
        db.session.commit()

    return _build_auth_response(novo_usuario, 201)

def atualizar_usuario(id, data):
    usuario = User.query.get_or_404(id)
    dados_validados = user_schema.load(data, partial=True)
    sh = dados_validados.get("senha_hash")
    if sh:
        dados_validados["senha_hash"] = generate_password_hash(sh)

    for campo, valor in dados_validados.items():
        setattr(usuario, campo, valor)

    db.session.commit()
    return success_response(user_schema.dump(usuario))


def deletar_usuario(id):
    usuario = User.query.get_or_404(id)

    db.session.delete(usuario)
    db.session.commit()

    return success_response(
        {
            "msg": "User deleted"
        }
    )

def login_usuario(data):
    username = data.get("nome")
    senha = data.get("senha_hash")

    user = User.query.filter_by(nome=username).first()
    if user and check_password_hash(user.senha_hash, senha):
        return _build_auth_response(user, 201)

    return error_response("Credenciais invalidas", 401)
