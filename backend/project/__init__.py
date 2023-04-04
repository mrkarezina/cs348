from flask import Flask, request, make_response
import psycopg2, os
import uuid
from psycopg2 import errors, sql
from psycopg2.extensions import AsIs, quote_ident

UniqueViolation = errors.lookup('23505')

app = Flask(__name__, static_folder='../../build', static_url_path='/')
connection = psycopg2.connect(user='user',
                              password='password',
                              host='db',
                              port='5432',
                              database='world_factbook')

# TODO: is this good practice/safe??
connection.autocommit = True

def format_error(e):
    return f'{type(e).__module__.removesuffix(".errors")}:{type(e).__name__}: {str(e).rstrip()}'

@app.get('/')
def index():
   return app.send_static_file('index.html')

# GET api/region_id?region={str}
@app.get('/api/region_id')
def region_id():
    region = request.args.get('region')
    cursor = connection.cursor()
    try:
        cursor.execute(
            'SELECT id \
             FROM Region \
             WHERE name = %s;',
            (region, )
        )
        response = (cursor.fetchall(), 200)
    except psycopg2.Error as e:
        error = format_error(e)
        response = (error, 400)
    cursor.close()
    return response


@app.get('/api/region_id')
def regions():
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT id, name FROM Region;')
        response = (cursor.fetchall(), 200)
    except psycopg2.Error as e:
        error = format_error(e)
        response = (error, 400)
    cursor.close()
    return response


# GET api/country_rankings_by_stat?stat_name={str}&limit={uint}&order_by={str}&year={uint}&region_id={str}
# list of top/bottom n countries for x stat
# order_by must be one of ASC or DESC
@app.get('/api/country_rankings_by_stat')
def country_rankings_by_stat():
    stat_name = request.args.get("stat_name")
    limit = request.args.get("limit", default=10)
    order_by = request.args.get("order_by", default="DESC")
    year = request.args.get("year", default="date_of_info")
    region_id = request.args.get("region_id", default="region_id")
    table_name = stat_name if year else stat_name.join("_recent")
    cursor = connection.cursor()
    try:
        query = sql.SQL("SELECT country_id, value \
                FROM {table_name} \
                JOIN Country ON Country.id={table_name}.country_id \
                WHERE date_of_info={year} AND region_id={region_id} \
                ORDER BY value {order_by} \
                LIMIT {limit};").format(
                    table_name=sql.SQL(table_name),
                    year=sql.SQL(year),
                    region_id=sql.SQL(region_id),
                    order_by=sql.SQL(order_by),
                    limit=sql.Literal(limit)
        )
        cursor.execute(query)
        response = (cursor.fetchall(), 200)
    except psycopg2.Error as e:
        error = f'{type(e).__module__.removesuffix(".errors")}:{type(e).__name__}: {str(e).rstrip()}'
        response = (error, 400)
    cursor.close()
    return response


# GET api/country_stats?country_id={str}&year={uint}
# Endpoint that return all of the stats associated with a country
@app.get('/api/country_stats')
def country_stats():
    country_id = request.args.get('country_id')
    year = request.args.get('year', default='date_of_info')
    stats_list = []
    for filename in os.listdir('/usr/src/input_data/'):
        stats_list.append(filename[:-4])
    data = {}
    cursor = connection.cursor()
    try:
        for stat in stats_list:
            table_name = stat if year else stat.join('_recent')
            query = 'SELECT value FROM %s WHERE country_id=%s AND date_of_info=%s;'
            cursor.execute(query, (AsIs(quote_ident(table_name, cursor)), country_id, year))
            data[stat] = cursor.fetchone()
        resp = make_response({country_id: data})
        response = (resp, 200)
    except psycopg2.Error as e:
        error = format_error(e)
        response = (error, 400)
    cursor.close()
    return response


# POST api/create_user {username: str, password: str}
# endpoint to create user storing their username and password
@app.post('/api/create_user')
def create_user():
    username, password = request.get_json()['username'], request.get_json()['password']
    cursor = connection.cursor()
    response = ({'message': 'User created successfully.'}, 201)
    try:
        cursor.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto;')
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, crypt(%s, gen_salt('bf', 8)));", (username, password))
    except UniqueViolation:
        if connection: connection.rollback()
        response = ({'error': f'{username} already exists, please use a different username.'}, 418)
    cursor.close()
    return response


# POST api/login_user {username: str, password: str}
# endpoint to login as user. If user exists and password is correct, return true, otherwise false
@app.post('/api/login_user')
def login_user():
    username, password = request.get_json()['username'], request.get_json()['password']
    cursor = connection.cursor()
    try:
        cursor.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto;')
        query = 'SELECT EXISTS (SELECT 1 FROM users \
                 WHERE username = %s AND password = crypt(%s, password));'
        cursor.execute(query, (username, password))
        result = cursor.fetchone()[0]
        # Both outcomes are possible from a successful validation call, thus they both have response codes of 200
        message = {'message': 'Correct credentials.'} if result else {'error': 'Incorrect credentials.'}
        response = (message, 200)
    except psycopg2.Error as e:
        error = format_error(e)
        response = (error, 400)
    cursor.close()
    return response


# GET api/user_scores?username={str}
# endpoint returns array of scores corresponding to games user played
@app.get('/api/user_scores')
def user_scores():
    username = request.args.get('username')
    cursor = connection.cursor()
    try:
        cursor.execute(
            'SELECT score \
             FROM games \
             WHERE user_id = ( \
                SELECT user_id \
                FROM users \
                WHERE username = %s \
             );',
            (username,)
        )
        data = cursor.fetchall()
        data = [score[0] for score in data]
        response = ({'scores': data}, 200)
    except psycopg2.Error as e:
        error = format_error(e)
        response = (error, 400)
    cursor.close()
    return response


# TODO: fix up game related apis
# TODO: figure out why (AsIs(quote_ident(table_name, cursor)) doesn't work


# GET api/game
# endpoint returns list of 5 random country and area tuples
# [(country_id, area), ...]
@app.get('/api/game')
def get_game():
    cursor = connection.cursor()
    try:
        cursor.execute(
            'SELECT Country.name, Random_values.value \
                FROM ( \
                    SELECT country_id, value \
                    FROM Area_recent \
                    ORDER BY RANDOM() \
                    LIMIT 5 \
                ) AS Random_values\
                JOIN Country \
                ON Country.id = Random_values.country_id;'
        )
        data = cursor.fetchall()
        response = (data, 200)
    except psycopg2.Error as e:
        error = format_error(e)
        response = (error, 400)
    cursor.close()
    return response

# POST api/game {username: str, score: int}
# endpoint to store game result of a user
@app.post('/api/game')
def create_game():
    data = request.get_json()
    username = data['username']
    score = data['score']

    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO games (user_id, score) \
                        VALUES ((SELECT user_id \
                                FROM users \
                                WHERE username = %s), %s);', (username, score))
        connection.commit()
        response = {'message': 'Game created successfully.'}
    except psycopg2.Error as e:
        error = format_error(e)
        response = {'error': error}
        connection.rollback()
    cursor.close()
    return {'message': 'Game created successfully.'}


# GET api/get_leaderboard
# endpoint returns top 10 players
@app.get('/api/get_leaderboard')
def get_leaderboard():
    cursor = connection.cursor()
    cursor.execute('SELECT username, MAX(score) \
                    FROM games \
                    NATURAL JOIN users \
                    GROUP BY username \
                    ORDER BY MAX(score) DESC \
                    LIMIT 10;')
    data = cursor.fetchall()
    cursor.close()
    return data


@app.after_request
def after_request_func(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response
