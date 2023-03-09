from flask import Flask, jsonify, request, make_response
import psycopg2, os


app = Flask(__name__)
connection = psycopg2.connect(user="user",
                              password="password",
                              host="db",
                              port="5432",
                              database="world_factbook")

# TODO: is this good practise/safe??
connection.autocommit = True

@app.route("/")
def hello_world():
    return jsonify(hello="world")


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

    
