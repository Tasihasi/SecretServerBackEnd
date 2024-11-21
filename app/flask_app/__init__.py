from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# TODO if the expire date is 0 then it never expires 
# TODO implement the mimetype change
# TODO how to implement the time manager?

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config.from_object('app.config.Config')

    # Initialize the database with the app
    db.init_app(app)

    CORS(app)

    with app.app_context():
        from .controller.routes import main_blueprint

        app.register_blueprint(main_blueprint)


    return app
