from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from threading import Thread
from .model import ManageDB 

import schedule, time

# TODO if the expire date is 0 then it never expires 
# It dose not deletes when it expires 
# TODO implement the mimetype change
# TODO change the data type to datetime 

def job():
    print("this is job runner")
    ManageDB.ServerTick()

def scheduler_thread():
    print("running schedule")
    schedule.every(1).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler():
    scheduler = Thread(target=scheduler_thread)
    scheduler.daemon = True  # Ensures that the thread will exit when the main program exits
    scheduler.start()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config.from_object('app.config.Config')

    # Initialize the database with the app
    db.init_app(app)

    CORS(app)
     # Configure CORS to allow requests from the specific origin
    CORS(app, resources={r"/*": {"origins": "https://tasihasi.github.io"}})

    with app.app_context():
        from .controller.routes import main_blueprint

        app.register_blueprint(main_blueprint)

    print("starting schedueker in init")
    start_scheduler()

    return app
