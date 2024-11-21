import os

class Config:
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE = os.getenv("DATABASE_URL")
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    