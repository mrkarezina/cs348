from flask import Flask, jsonify, request, make_response
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

# GET api/get-countries?stat_name={str}&limit={uint}&order_by={str}
# list of top n/bottom n countries for x stat
@app.route("/api/get-countries")
def countries_stats():
    # TODO: error checking
    stat_name = request.args.get("stat_name")
    limit = request.args.get("limit", default=10)
    order_by = request.args.get("order_by", default="top")
    
    if order_by == "top":
        order_by = "DESC"
    elif order_by == "bottom":
        order_by = "ASC"
    
    cursor = connection.cursor()
    cursor.execute("SELECT country_id, value \
                     FROM %s \
                     ORDER BY value %s \
                     LIMIT %s;" % (stat_name, order_by, limit))
    data = cursor.fetchall()
    cursor.close()
    
    return jsonify(data)

# GET api/country-overview?country_id={str}
# Endpoint that return all of the stats associated with a country 
@app.route("/api/country-overview")
def country_overview():
    country_id = request.args.get("country_id")
    stats_list = []
    for filename in os.listdir("/usr/src/input_data/"):
        stats_list.append(filename[:-4])
    data = {}
    
    cursor = connection.cursor()
    for stat in stats_list:
        cursor.execute("SELECT value \
                        FROM %s \
                        WHERE country_id = '%s';" % (stat, country_id))
        country_value = cursor.fetchone()
        data[stat] = country_value

    cursor.close()
    resp = make_response({country_id: data})
    
    return resp

    
# POST api/create-user {username: str, password: str}
# endpoint to create user storing their username and password
@app.route("/api/create-user", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    user_uuid = uuid.uuid4()        
    
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO users (user_id, username, password) \
                        VALUES ('%s', '%s', '%s');" % (user_uuid, username, password))
    except UniqueViolation:
        return jsonify({"error": f"{username} already exists, please use a different username."})
    except CheckViolation:
        return jsonify({"error": "Please ensure that your password is greater than 7 characters."})

    
    cursor.close()

    resp = make_response({"message": "User created successfully."})

    return resp

# POST api/login-user {username: str, password: str}
# endpoint to login as user. If user exists and password is correct, return true, otherwise false
@app.route("/api/login-user", methods=["POST"])
def login_user():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    cursor = connection.cursor()

    cursor.execute("SELECT EXISTS (SELECT 1 FROM users WHERE username = '%s' AND password = '%s');" % (username, password))
    data = str(cursor.fetchone()[0])
    cursor.close()

    if data == 'False':
        return jsonify({"error": "Incorrect credentials."})
    else:
        return jsonify({"message": "Correct credentials."})
    

# GET api/get-user?username={str}
# endpoint returns array of scores corresponding to games user played
@app.route("/api/get-user")
def get_user():
    username = request.args.get("username")
    
    cursor = connection.cursor()
    cursor.execute("SELECT score \
                    FROM games \
                    WHERE user_id = (SELECT user_id \
                                    FROM users \
                                    WHERE username = '%s');" % username) 
    data = cursor.fetchall()
    data = [score[0] for score in data]
    cursor.close()

    return jsonify({"scores": data})

# GET api/game
# endpoint returns list of 5 random country and area tuples
# [(country_id, area), ...]
@app.route("/api/game")
def get_game():
    cursor = connection.cursor()

    cursor.execute("SELECT country_id, value \
                        FROM (SELECT id \
                                FROM country \
                                ORDER BY RANDOM() \
                                LIMIT 5) AS random_countries \
                        JOIN (SELECT country_id, value, date_of_info \
                                FROM Area \
                                ORDER BY date_of_info DESC) AS areas \
                        ON random_countries.id = areas.country_id \
                        GROUP BY country_id, value, date_of_info \
                        ORDER BY RANDOM();")

    data = cursor.fetchall()
    cursor.close()

    return jsonify(data)

# POST api/game {username: str, score: int}
# endpoint to store game result of a user
@app.route("/api/game", methods=["POST"])
def create_game():
    data = request.get_json()
    username = data["username"]
    score = data["score"]

    cursor = connection.cursor()
    cursor.execute("INSERT INTO games (user_id, score) \
                    VALUES ((SELECT user_id \
                            FROM users \
                            WHERE username = '%s'), %s);" % (username, score)) 
    cursor.close()
    return jsonify({"message": "Game created successfully."})

# GET api/get-leaderboard
# endpoint returns top 10 scores
@app.route("/api/get-leaderboard")
def get_leaderboard():
    cursor = connection.cursor()
    cursor.execute("SELECT username, score \
                    FROM games \
                    JOIN users ON games.user_id = users.user_id \
                    ORDER BY score DESC \
                    LIMIT 10;") 
    data = cursor.fetchall()
    cursor.close()

    resp = make_response(data)

    return resp

@app.after_request
def after_request_func(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response
