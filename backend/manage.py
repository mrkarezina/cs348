from flask.cli import FlaskGroup
import os

from project import app, connection

cli = FlaskGroup(app)


@cli.command("create_static_tables")
def create_static_tables():
    cursor = connection.cursor()
    cursor.execute(open("utilities/drop_tables.sql", "r").read())
    print("Creating database...")
    cursor.execute(open("utilities/static_schema.sql", "r").read())
    connection.commit()
    print("Database created successfully")



# TODO: create separate function for dropping tables
@cli.command("create_stat_tables")
def create_stat_tables():
    cursor = connection.cursor()
    # TODO: do we have/how can we implement error checking on this?
    # TODO: DROP TABLES
    print("Creating database...")
    cursor.execute(open("utilities/stats_schema.sql", "r").read())
    connection.commit()
    print("Database created successfully")



@cli.command("populate_stat_tables")
def populate_stat_tables():
    # csv paths in psql container
    psql_fixed_data = "/var/lib/world_factbook/fixed_data/"
    psql_input_data = "/var/lib/world_factbook/input_data/"
    # csv path in web container
    web_input_data = "/usr/src/input_data/"
    print("Populating table...")
    cursor = connection.cursor()
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



@cli.command("create_recent_stat_tables")
def create_recent_stat_tables():
    web_input_data = "/usr/src/input_data/"
    cursor = connection.cursor()
    for filename in os.listdir(web_input_data):
        table_name=filename[:-4]
        # delete country recent statistic table if exists
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}_recent;")
        # create country recent statistic table
        cursor.execute(f"CREATE TABLE {table_name}_recent (LIKE {table_name} INCLUDING ALL);")
    connection.commit()



@cli.command("populate_recent_stat_tables")
def populate_recent_stat_tables():
    web_input_data = "/usr/src/input_data/"
    cursor = connection.cursor()
    for filename in os.listdir(web_input_data):
        cursor.execute(
            open("utilities/populate_recent_stat_table.sql", "r").read().format(
                    table_name=filename[:-4]
                )
        )
    connection.commit()




# TODO: create makefile script to automatically invoke create_db and populate_db


if __name__ == "__main__":
    cli()
