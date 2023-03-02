from flask import Flask, jsonify
import psycopg2


app = Flask(__name__)
connection = psycopg2.connect(user="user",
                              password="password",
                              host="db",
                              port="5432",
                              database="world_factbook")

connection.autocommit = True

@app.route("/")
def hello_world():
    return jsonify(hello="world")
