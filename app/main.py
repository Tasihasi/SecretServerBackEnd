from .flask_app import create_app, db
# important to import db because gets circular import error 

app = create_app()

    

if __name__ == "__main__":
    app.run(debug=True)


    
