from flask.cli import FlaskGroup
import os
import psycopg2

from project import app

cli = FlaskGroup(app)
class StatTableManager:
    def __init__(self):
        self.conn = psycopg2.connect(user="user",
                              password="password",
                              host="db",
                              port="5432",
                              database="world_factbook")        

    def check_tables_exist(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT EXISTS(SELECT * FROM pg_tables WHERE schemaname = 'public')")
        tables_exist = cursor.fetchone()[0]
        return tables_exist

    def create_static_tables(self):
        cursor = self.conn.cursor()
        cursor.execute(open("utilities/drop_static_tables.sql", "r").read())
        cursor.execute(open("utilities/static_schema.sql", "r").read())
        self.conn.commit()

    def create_stat_tables(self):
        web_input_data = "/usr/src/input_data/"
        cursor = self.conn.cursor()
        for filename in os.listdir(web_input_data):
            table_name = filename[:-4]
            cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        cursor.execute(open("utilities/stats_schema.sql", "r").read())
        self.conn.commit()

    def populate_static_tables(self):
        psql_fixed_data = "/var/lib/world_factbook/fixed_data/"
        cursor = self.conn.cursor()
        cursor.execute(
            open("utilities/populate_country_region.sql", "r").read(),
            (psql_fixed_data + "countries.csv", psql_fixed_data + "iso.csv")
        )
        self.conn.commit()

    def populate_stat_tables(self):
        psql_input_data = "/var/lib/world_factbook/input_data/"
        web_input_data = "/usr/src/input_data/"
        cursor = self.conn.cursor()
        for filename in os.listdir(web_input_data):
            cursor.execute(
                open("utilities/populate_stat_table.sql", "r").read().format(
                    table_name=filename[:-4],
                    csv=os.path.join(psql_input_data, filename)
                )
            )
        self.conn.commit()

    def create_recent_stat_tables(self):
        web_input_data = "/usr/src/input_data/"
        cursor = self.conn.cursor()
        for filename in os.listdir(web_input_data):
            table_name = filename[:-4]
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}_recent;")
            cursor.execute(f"CREATE TABLE {table_name}_recent (LIKE {table_name} INCLUDING ALL);")
        self.conn.commit()

    def populate_recent_stat_tables(self):
        web_input_data = "/usr/src/input_data/"
        cursor = self.conn.cursor()
        for filename in os.listdir(web_input_data):
            cursor.execute(
                open("utilities/populate_recent_stat_table.sql", "r").read().format(
                    table_name=filename[:-4]
                )
            )
        self.conn.commit()

    def auto_population(self):
        if self.check_tables_exist():
            print("SKIPPING DB INITIALIZATION: Tables already exist and are populated.")
        else:
            print("INITIALIZING DB: Tables do not exist. Executing scripts ...")
            self.create_static_tables()
            self.create_stat_tables()
            self.populate_static_tables()
            self.populate_stat_tables()
            self.create_recent_stat_tables()
            self.populate_recent_stat_tables()
            print("Tables created and populated successfully.")
    
    def update_stat_tables(self):
        self.create_stat_tables()
        self.create_recent_stat_tables()
        self.populate_stat_tables()
        self.populate_recent_stat_tables()


@cli.command("setup")
def setup():
    StatTableManager().auto_population()


@cli.command("update")
def update():
    StatTableManager().update_stat_tables()



if __name__ == "__main__":
    cli()
