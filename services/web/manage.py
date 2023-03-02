from flask.cli import FlaskGroup
import os

from project import app, connection

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    cursor = connection.cursor()

    # TODO: do we have/how can we implement error checking on this?
    cursor.execute(open("utilities/drop_tables.sql", "r").read())

    print("Creating database...")
    cursor.execute(open("schema.sql", "r").read())
    connection.commit()
    print("Database created successfully")

# TODO: rewrite function to work on all files in /usr/src/app/data once population is fixed, esp region and country tables
@cli.command("populate_db")
def populate_db():

    cursor = connection.cursor()

    print("Populating table")

    # OPTION 1
    # with open("data/processed_population.csv", 'r') as f:
    #     next(f) # Skip the header row.
    #     cursor.copy_from(f, 'population', sep=',')


    # TODO: add appropriate volume to db service in docker-compose.yml so Postgres can find the correct csv file.
    # dev notes:
    # all files in services/web/data are meticulously generated by format_csv.py from data in the raw data directory. DO NOT touch this.
    # when running docker, this processed data in the services/web/data directory are copied into /usr/src/app within the container
    # all data is in the correct csv format to be directly imported to their appropriate tables
    # but when using OPTION 1 above that code sets a delimiter ',', which causes issues as there are commas within the data itself
    # so far the best option is to use OPTION 2, but this requires the DBMS to find the location of services/web/data.
    # I trust that this can be fixed by adding the appropriate volume to db service in docker-compose.yml so Postgres can find the correct csv file.

    # OPTION 2
    # cursor.execute(f"COPY population FROM 'data/processed_population.csv' CSV;")


    connection.commit()


# TODO: create makefile script to automatically invoke create_db and populate_db

# 


if __name__ == "__main__":
    cli()
