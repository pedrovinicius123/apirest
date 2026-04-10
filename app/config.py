import os

BASE_DIR = os.path.curdir

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR}/app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
