from flask import Flask, request, make_response
import psycopg2, os
import uuid
from psycopg2 import errors

UniqueViolation = errors.lookup('23505')
CheckViolation = errors.lookup('23514')

app = Flask(__name__, static_folder='../../build', static_url_path='/')
connection = psycopg2.connect(user="user",
                              password="password",
                              host="db",
                              port="5432",
                              database="world_factbook")

# TODO: is this good practise/safe??
connection.autocommit = True

@app.route("/")
def index():
   return app.send_static_file('index.html')


# GET api/country_rankings_by_stat?stat_name={str}&limit={uint}&order_by={str}&year={uint}
# list of top/bottom n countries for x stat
# order_by must be one of ASC or DESC
@app.route("/api/country_rankings_by_stat")
def country_rankings_by_stat():
    stat_name = request.args.get("stat_name")
    limit = request.args.get("limit", default=10)
    order_by = request.args.get("order_by", default="DESC")
    year = request.args.get("year")
    cursor = connection.cursor()
    try:
        if year:
            cursor.execute(
                f"SELECT country_id, value \
                FROM {stat_name} \
                WHERE date_of_info={year} \
                ORDER BY value {order_by} \
                LIMIT {limit};"
            )
        else:
            cursor.execute(
                f"SELECT country_id, value \
                FROM {stat_name}_recent \
                ORDER BY value {order_by} \
                LIMIT {limit};"
            )
        response = (cursor.fetchall(), 200)
    except psycopg2.Error as e:
        error = f"{type(e).__module__.removesuffix('.errors')}:{type(e).__name__}: {str(e).rstrip()}"
        response = (error, 400)
    cursor.close()
    return response


# GET api/country_stats?country_id={str}&year={uint}
# Endpoint that return all of the stats associated with a country
@app.route("/api/country_stats")
def country_stats():
    country_id = request.args.get("country_id")
    year = request.args.get("year")
    stats_list = []
    for filename in os.listdir("/usr/src/input_data/"):
        stats_list.append(filename[:-4])
    data = {}
    cursor = connection.cursor()
    try:
        for stat in stats_list:
            if year:
                cursor.execute(f"SELECT value \
                                FROM {stat} \
                                WHERE date_of_info={year} AND country_id = '{country_id}';")
            else:
                cursor.execute(f"SELECT value \
                                FROM {stat}_recent \
                                WHERE country_id = '{country_id}';")
            data[stat] = cursor.fetchone()
            resp = make_response({country_id: data})
            response = (resp, 200)
    except psycopg2.Error as e:
        error = f"{type(e).__module__.removesuffix('.errors')}:{type(e).__name__}: {str(e).rstrip()}"
        response = (error, 400)
    cursor.close()
    return response


# POST api/create_user {username: str, password: str}
# endpoint to create user storing their username and password
@app.route("/api/create_user", methods=["POST"])
def create_user():
    username, password = request.get_json()["username"], request.get_json()["password"]
    cursor = connection.cursor()
    response = ({"message": "User created successfully."}, 201)
    try:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
        cursor.execute(f"INSERT INTO users (username, password) \
                        VALUES ('{username}', crypt('{password}', gen_salt('bf', 8)));")
    except UniqueViolation:
        if connection: connection.rollback()
        response = ({"error": f"{username} already exists, please use a different username."}, 418)
    except CheckViolation:
        if connection: connection.rollback()
        response = ({"error": "Please ensure that your password is greater than 7 characters."}, 418)
    cursor.close()
    return response


# POST api/login_user {username: str, password: str}
# endpoint to login as user. If user exists and password is correct, return true, otherwise false
@app.route("/api/login_user", methods=["POST"])
def login_user():
    username, password = request.get_json()["username"], request.get_json()["password"]
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
        cursor.execute(
            f"SELECT EXISTS (SELECT 1 FROM users \
            WHERE username = '{username}' AND password = crypt('{password}', password));"
        )
        result = cursor.fetchone()[0]
        # Both outcomes are possible from a successful validaiton call, thus they both have response codes of 200
        message = {"message": "Correct credentials."} if result else {"error": "Incorrect credentials."}
        response = (message, 200)
    except psycopg2.Error as e:
        error = f"{type(e).__module__.removesuffix('.errors')}:{type(e).__name__}: {str(e).rstrip()}"
        response = (error, 400)
    cursor.close()
    return response


# GET api/user_scores?username={str}
# endpoint returns array of scores corresponding to games user played
@app.route("/api/user_scores")
def user_scores():
    username = request.args.get("username")
    cursor = connection.cursor()
    try:
        cursor.execute(
            f"SELECT score \
            FROM games \
            WHERE user_id = ( \
                SELECT user_id \
                FROM users \
                WHERE username = '{username}' \
            );"
        )
        data = cursor.fetchall()
        data = [score[0] for score in data]
        response = ({"scores": data}, 200)
    except psycopg2.Error as e:
        error = f"{type(e).__module__.removesuffix('.errors')}:{type(e).__name__}: {str(e).rstrip()}"
        response = (error, 400)
    cursor.close()
    return response


# TODO: fix up game related apis


# GET api/game?stat_name={str}
# endpoint returns list of 5 random country and area tuples
# [(country_id, area), ...]
@app.route("/api/game")
def get_game():
    stat_name = request.args.get("stat_name", default="Area")
    cursor = connection.cursor()
    try:
        cursor.execute(
            f"SELECT Country.name, Random_values.value \
            FROM ( \
                SELECT country_id, value \
                FROM {stat_name}_recent \
                ORDER BY RANDOM() \
                LIMIT 5 \
            ) AS Random_values\
            JOIN Country \
            ON Country.id = Random_values.country_id;"
        )
        data = cursor.fetchall()
        response = (data, 200)
    except psycopg2.Error as e:
        error = f"{type(e).__module__.removesuffix('.errors')}:{type(e).__name__}: {str(e).rstrip()}"
        response = (error, 400)
    cursor.close()
    return response


# POST api/game {username: str, score: int}
# endpoint to store game result of a user
@app.route("/api/game", methods=["POST"])
def create_game():
    data = request.get_json()
    username = data["username"]
    score = data["score"]

    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO games (user_id, score) \
                    VALUES ((SELECT user_id \
                            FROM users \
                            WHERE username = '{username}'), {score});") 
    cursor.close()
    return {"message": "Game created successfully."}

# GET api/get_leaderboard
# endpoint returns top 10 scores
@app.route("/api/get_leaderboard")
def get_leaderboard():
    cursor = connection.cursor()
    cursor.execute("SELECT username, score \
                    FROM games \
                    JOIN users ON games.user_id = users.user_id \
                    ORDER BY score DESC \
                    LIMIT 10;") 
    data = cursor.fetchall()
    cursor.close()
    return data


@app.after_request
def after_request_func(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response
