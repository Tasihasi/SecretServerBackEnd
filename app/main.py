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
    ManageDB.ServerTick()
    logging.info("Job R")

def scheduler_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)
    

if __name__ == "__main__":
    logging.INFO("app running with big letters")
    logging.info("app running with small letters")
    print("maybe print please ")

    schedule.every(1).minutes.do(job)

     # Start scheduler in a separate thread
    scheduler_thread = threading.Thread(target=scheduler_thread, daemon=True)
    scheduler_thread.start()

    app.run(debug=True)
    
