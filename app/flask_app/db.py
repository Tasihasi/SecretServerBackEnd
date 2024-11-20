import sqlite3
from datetime import datetime
import click
from flask import current_app, g

def get_db():
    """Returns a connection to the SQLite database."""
    print("Database path: ", current_app.config['DATABASE'])
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],  # Get the database from config
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row  # This allows us to access rows as dictionaries

    return g.db

def init_db():
    """Initializes the database by executing schema.sql."""
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))  # Execute the SQL commands from the schema file

@click.command('init-db')
def init_db_command():
    """Command to initialize the database."""
    init_db()
    click.echo('Initialized the database.')

sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())  # Registers timestamp conversion
)

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def close_db(e=None):
    """Closes the database connection."""
    db = g.pop('db', None)
    if db is not None:
        db.close()
