import os
from datetime import timedelta

BASE_DIR = os.path.curdir

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ["cookies"]  # Diz para o Flask usar cookies
    JWT_COOKIE_SECURE = False         # Mude para True em produção (HTTPS)
    JWT_ACCESS_COOKIE_PATH = "/"      # Torna o cookie acessível em todo o site
    JWT_COOKIE_CSRF_PROTECT = False
       
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR}/app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
