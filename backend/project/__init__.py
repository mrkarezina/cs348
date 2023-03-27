from flask import Flask, jsonify, request, make_response
import psycopg2, os
import uuid
from psycopg2 import errors
from psycopg2.errorcodes import UNIQUE_VIOLATION


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

# GET api/get-countries?stat_name={str}&limit={uint}&order_by{str}
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
    cursor.execute(f"SELECT country_id, value \
                     FROM {stat_name} \
                     ORDER BY value {order_by} \
                     LIMIT {limit};")
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
        cursor.execute(f"SELECT value \
                         FROM {stat} \
                         WHERE country_id = '{country_id}'")
        country_value = cursor.fetchone()
        data[stat] = country_value

    cursor.close()
    resp = make_response({country_id: data})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    
    return resp

    
# POST api/create-user {username: str, password: str}
# endpoint to create user storing their username and password
@app.route("/api/create-user", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    user_uuid = uuid.uuid4()
    
    if len(password) <= 7:
        return jsonify({"error": "Please ensure that your password is greater than 7 characters."})
    
    cursor = connection.cursor()

    try:
        cursor.execute(f"INSERT INTO users (user_id, username, password) \
                        VALUES ('{user_uuid}', '{username}', '{password}');")
    except errors.lookup(UNIQUE_VIOLATION):
        return jsonify({"error": f"{username} already exists, please use a different username."})
    
    cursor.close()
    
    return jsonify({"message": "User created successfully."})

# POST api/login-user {username: str, password: str}
# endpoint to login as user. If user exists and password is correct, return true, otherwise false
@app.route("/api/login-user", methods=["POST"])
def login_user():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    cursor = connection.cursor()

    cursor.execute(f"SELECT EXISTS (SELECT 1 FROM users WHERE username = '{username}' AND password = '{password}');")
    data = str(cursor.fetchone()[0])
    cursor.close()

    if data == 'False':
        return jsonify({"error": "Incorrect credentials."})
    else:
        return jsonify({"message": "Correct credentials."})
    
    
# GET api/get-user?username={str}
# endpoint returns array of scores corresponding to games user played
@app.route("/api/get-user-scores")
def get_user():
    username = request.args.get("username")
    
    cursor = connection.cursor()
    cursor.execute(f"SELECT score \
                        FROM games \
                        WHERE user_id = (SELECT user_id \
                                        FROM users \
                                        WHERE username = '{username}');") 
    data = cursor.fetchall()
    data = [score[0] for score in data]
    cursor.close()

    return jsonify(data)

# POST api/game-result {username: str, score: int}
# endpoint to store game result of a user
@app.route("/api/game-result", methods=["POST"])
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
    return jsonify({"message": "Game created successfully."})

# GET api/get-leaderboard
# endpoint returns top 10 scores
@app.route("/api/get-leaderboard")
def get_leaderboard():
    cursor = connection.cursor()
    cursor.execute(f"SELECT username, score \
                        FROM games \
                        JOIN users ON games.user_id = users.user_id \
                        ORDER BY score DESC \
                        LIMIT 10;") 
    data = cursor.fetchall()
    cursor.close()

    return jsonify(data)
