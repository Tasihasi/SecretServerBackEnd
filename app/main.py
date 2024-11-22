from .flask_app import create_app
import schedule, time
from .flask_app.model import ManageDB  # Import ManageDB here to avoid circular imports
from threading import Thread

app = create_app()


    

if __name__ == "__main__":
    print("Starting app")
    app.run(debug=True)


    
