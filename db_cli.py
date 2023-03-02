import glob
import csv
from pathlib import Path
from getpass import getpass
import sys

import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values
from psycopg2.errors import DuplicateDatabase

DB_NAME = 'WORLD_FACTBOOK'


# user = input('Enter database username (default postgres): ') or 'user'
user = 'user'

# database=
password = getpass('enter database password: ')
conn = psycopg2.connect(user=user,
                        password=password,
                        host='127.0.0.1',
                        port='5432')
conn.autocommit = True
cursor = conn.cursor()
try:
    cursor.execute(sql.SQL('CREATE DATABASE {}').format(sql.Identifier(DB_NAME)))
except DuplicateDatabase:
    pass
conn.close()
conn = psycopg2.connect(database=DB_NAME,
                        user=user,
                        password=password,
                        host='127.0.0.1',
                        port='5432')
conn.autocommit = True
cursor = conn.cursor()
print('Database Commands:')
print('init_db              : reset or initialize database to default')
print('population <country> : print row in database where name = <country>')
print('q')

while True:
    cmds = input('> ').split()
    if len(cmds) == 0 or cmds[0] == 'q':
        conn.close()
        sys.exit()
    elif cmds[0] == 'init_db' or cmds[0] == 'init-db':
        cursor.execute('DROP TABLE IF EXISTS population')
        sql = '''CREATE TABLE population(name varchar(56) NOT NULL, slug varchar(56) NOT NULL, population int NOT NULL, \
                                         date_of_information varchar(20), ranking int NOT NULL, region varchar(56))'''
        cursor.execute(sql)
        data = []
        with open('data/population.csv', 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for i, row in enumerate(spamreader):
                if i > 0:
                    row[2] = int(row[2].replace(',', ''))
                    data.append(row)

        sql2 = '''INSERT into population(name,slug, population,date_of_information,ranking,region) values %s'''
        execute_values(cursor, sql2, data, template=None, page_size=1000)
    elif cmds[0] == 'population':
        sql = '''SELECT * from population where UPPER(name) = %s'''
        cursor.execute(sql, (cmds[1].upper(),))
        print(cursor.fetchone())
