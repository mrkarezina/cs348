from flask import Flask, jsonify, request
import psycopg2


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
    limit = request.args.get("limit")
    order_by = request.args.get("order_by")
    
    if order_by == "top":
        order_by = "DESC"
    elif order_by == "bottom":
        order_by = "ASC"
    
    cursor = connection.cursor()
    cursor.execute(f"SELECT country_id, value \
                   FROM {stat_name} \
                   ORDER BY value {order_by} \
                   LIMIT {limit};")
    connection.commit()
    data = cursor.fetchall()
    cursor.close()
    
    return jsonify(result=data)
