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
    cursor.execute(open("utilities/schema.sql", "r").read())
    connection.commit()
    print("Database created successfully")

# TODO: rewrite function to work on all files in /usr/src/app/data once population is fixed, esp region and country tables
@cli.command("populate_db")
def populate_db():

    cursor = connection.cursor()

    print("Populating table...")

    psql_fixed_data = "/var/lib/world_factbook/fixed_data/"
    psql_input_data = "/var/lib/world_factbook/input_data/"
    web_input_data = "/usr/src/input_data/"

    # populate Region and Country tables
    cursor.execute(
        open("utilities/populate_country_region.sql", "r").read(),
        (psql_fixed_data+"countries.csv", psql_fixed_data+"iso.csv")
    )

    # populate country statistic tables
    for filename in os.listdir(web_input_data):
        cursor.execute(
            open("utilities/populate_stat_table.sql", "r").read().format(
                table_name=filename[:-4],
                csv=os.path.join(psql_input_data, filename)
            )
        )

    connection.commit()
    print("Database populated successfully")


# TODO: create makefile script to automatically invoke create_db and populate_db


if __name__ == "__main__":
    cli()
