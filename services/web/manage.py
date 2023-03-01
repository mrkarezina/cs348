from flask.cli import FlaskGroup
import os

from project import app, connection

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    cursor = connection.cursor()
    cursor.execute(open("drop_tables.sql", "r").read())
    print("Creating database...")
    cursor.execute(open("schema.sql", "r").read())
    connection.commit()
    print("Database created successfully")



if __name__ == "__main__":
    cli()
