from flask import current_app, g
from app.extensions import db
from app.models.user import User
from app.schemas.user_schema import UserSchema
from app.utils.response import success_response
from ..extensions import auth
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
import datetime, jwt

user_schema = UserSchema()
users_schema = UserSchema(many=True)

def generate_jwt(username):
    payload = {
        "sub":username,
        "exp":dt.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
    }
    return jwt.encode(payload, current_app.config.get("SECRET_KEY"))

@auth.verify_token
def verify_user_token_jwt(token):
    """Valida o token JWT extraído do cabeçalho."""
    try:
        # Decodifica e valida a assinatura/expiração do token
        payload = jwt.decode(token, current_app.config.get("SECRET_KEY"), algorithms=['HS256', "MD5"])
        g.current_user = payload['sub']
        return g.current_user
    except jwt.ExpiredSignatureError:
        return None  # Token expirado
    except jwt.InvalidTokenError:
        return None  # Token inválido ou alterado

def listar_usuarios():
    usuarios = User.query.all()
    return success_response(users_schema.dump(usuarios))

def criar_usuario(data):
    dados_validados = user_schema.load(data)
    dados_validados["senha_hash"] = generate_password_hash(dados_validados.get("senha_hash"))
    novo_usuario = User(**dados_validados)

    db.session.add(novo_usuario)
    db.session.commit()
    
    return success_response(user_schema.dump(novo_usuario), 201)


def atualizar_usuario(id, data):
    usuario = User.query.get_or_404(id)
    dados_validados = user_schema.load(data, partial=True)
    print(dados_validados)
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

    return "", 204

def login_usuario(data):
    username = data.get("username")
    senha = data.get("senha")
    
    user = User.query.get(username=username).first()
    if user and check_password_hash(user.senha_hash, senha):
        token = generate_jwt(username)
        return success_response({
            "access_token":token
        }, 201)
