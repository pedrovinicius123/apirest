from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_httpauth import HTTPTokenAuth


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
login_manager= LoginManager()
auth = HTTPTokenAuth()
