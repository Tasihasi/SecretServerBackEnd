from .flask_app import create_app, db
import schedule, time
from .flask_app.model import ManageDB  # Import ManageDB here to avoid circular imports
import logging

app = create_app()

# Initialize the scheduler after app creation
def job():
    ManageDB.ServerTick()
    

def scheduler_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)
    

if __name__ == "__main__":
    app.run(debug=True)
    schedule.every(1).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

    
