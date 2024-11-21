from .flask_app import create_app, db
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask
import schedule, threading, time
from .flask_app.model import ManageDB  # Import ManageDB here to avoid circular imports

app = create_app()


# Initialize the scheduler after app creation
def job():
    ManageDB.ServerTick()

def scheduler_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)
    

if __name__ == "__main__":

     # Start scheduler in a separate thread
    scheduler_thread = threading.Thread(target=scheduler_thread, daemon=True)
    scheduler_thread.start()

    app.run(debug=True)
    schedule.every(1).minutes.do(job)