from flask import Flask, jsonify, request, make_response
import psycopg2, os


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
    
    cursor = connection.cursor()
    # database constraint ensures password is > 7 characters
    # and username is unique 
    cursor.execute(f"INSERT INTO users (username, password) \
                     VALUES ('{username}', '{password}');")
    cursor.close()
    
    return jsonify({"message": "User created successfully."})

# GET api/get-user?username={str}
# endpoint returns scores of games user played
@app.route("/api/get-user")
def get_user():
    username = request.args.get("username")
    
    cursor = connection.cursor()
    cursor.execute(f"SELECT score \
                        FROM games \
                        WHERE user_id = (SELECT id \
                                         FROM users \
                                            WHERE username = '{username}');") 
    data = cursor.fetchall()
    cursor.close()

    return jsonify(data)
