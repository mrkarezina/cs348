from flask.cli import FlaskGroup
import os
import psycopg2

from project import app

cli = FlaskGroup(app)

connection = psycopg2.connect(user="hello_flask",
                              password="hello_flask",
                              host="db",
                              port="5432",
                              database="hello_flask_dev")

@cli.command("create_db")
def create_db():
    print("Creating database...")
    cursor = connection.cursor()
    cursor.execute(open("schema.sql", "r").read())
    print("Database created successfully")


# @cli.command("seed_db")
# def seed_db():
#     db.session.add(User(email="michael@mherman.org"))
#     db.session.commit()


if __name__ == "__main__":
    cli()
