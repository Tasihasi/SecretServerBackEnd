from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime 
import click

# Create an instance of SQLAlchemy
db = SQLAlchemy()

def init_app(app):
    """
    Initialize the app with the database.
    - Bind the SQLAlchemy instance to the Flask app.
    - Register teardown and CLI commands if needed.
    """
    db.init_app(app)  # Bind SQLAlchemy to the Flask app

    # Create database tables if they don't exist (useful for local development)
    with app.app_context():
        db.create_all()

def init_db():
    """
    Manually initialize the database (usually for migrations).
    Not typically needed when using Flask-Migrate.
    """
    db.create_all()

# If you still want a CLI command for initializing the database (optional)

@click.command('init-db')
def init_db_command():
    """Command to initialize the database."""
    init_db()
    click.echo('Initialized the database.')
