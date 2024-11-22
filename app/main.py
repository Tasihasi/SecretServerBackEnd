from .flask_app import create_app
import schedule, time
from .flask_app.model import ManageDB  # Import ManageDB here to avoid circular imports
from threading import Thread

app = create_app()

# Initialize the scheduler after app creation
def job():
    print("this is job runner")
    ManageDB.ServerTick()
    

def scheduler_thread():
    print("running schedule")
    schedule.every(1).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
    

if __name__ == "__main__":
    print("Starting app")

    # Start the scheduler in a separate thread
    scheduler = Thread(target=scheduler_thread)
    scheduler.start()

    app.run(debug=True)


    
