from .flask_app import create_app, db
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask
from .model import ManageDB  # Import ManageDB here to avoid circular imports


app = create_app()


# Initialize the scheduler after app creation
def setup_scheduler():
    scheduler = BackgroundScheduler(daemon=True)

    # Add the job to the scheduler
    scheduler.add_job(
        ManageDB.ServerTick(),  # Function to run every minute
        trigger=IntervalTrigger(minutes=1),  # Interval for the job
        id='server_tick_job',  # Unique job ID
        name='Run ServerTick every minute',  # Optional job name
        replace_existing=True  # Replace job if it exists
    )

    # Start the scheduler
    scheduler.start()

# Call the scheduler setup function after app is created
setup_scheduler()

if __name__ == "__main__":
    app.run(debug=True)
