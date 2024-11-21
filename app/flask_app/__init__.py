from flask import Flask
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask_sqlalchemy import SQLAlchemy
#from .model import ManageDB
#from . import db

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

    # Set up the scheduler to run the task every minute
    """
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(
        ManageDB.ServerTick(),  # This is the function you want to run
        trigger=IntervalTrigger(minutes=1),  # The interval to run it
        id='server_tick_job',  # Job ID (can be any unique string)
        name='Run ServerTick every minute',  # Job name (optional)
        replace_existing=True  # Replace the job if it already exists
    )
    """
    #scheduler.start()

    with app.app_context():
        from .controller.routes import main_blueprint

        app.register_blueprint(main_blueprint)


    return app
