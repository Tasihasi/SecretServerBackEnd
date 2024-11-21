from .flask_app import create_app, db
from flask import Flask, jsonify
import schedule, threading, time
from .flask_app.model import ManageDB  # Import ManageDB here to avoid circular imports
import logging

app = create_app()

# Configure the logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# Initialize the scheduler after app creation
def job():
    raise RuntimeError ("Perhaps this will stop")
    ManageDB.ServerTick()
    

def scheduler_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)
    

if __name__ == "__main__":
    app.run(debug=True)
    schedule.every(1).minutes.do(job)

    while True:
        raise RuntimeError ("meeeghs")
        schedule.run_pending()
        time.sleep(1)

    
