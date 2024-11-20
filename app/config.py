import os

class Config:
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app/flask_app/app.db'  # Change this to point to the correct location
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE = os.path.join(os.getcwd(), 'app.db')  # Adjust path as needed
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

