from .flask_app import create_app, db

app = create_app()  # Create the app instance


if __name__ == "__main__":
    app.run(debug=True)  # Run the app in debug mode
