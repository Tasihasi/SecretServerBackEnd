from .flask_app import create_app, db
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask, jsonify
import requests
import schedule, threading, time
from .flask_app.model import ManageDB  # Import ManageDB here to avoid circular imports

app = create_app()

def test_http():
    url = 'https://secretserverbackend-production.up.railway.app/secret/shsuqis'  # Replace with the actual URL

    try:
        # Make a GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Process the response if needed
            data = response.json()  # or response.text if expecting plain text
            return jsonify({'status': 'success', 'data': data}), 200
        else:
            return jsonify({'status': 'fail', 'message': f'Request failed with status code: {response.status_code}'}), response.status_code
    
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        return jsonify({'status': 'error', 'message': str(e)}), 500

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
    schedule.every(1).minutes.do(test_http)
