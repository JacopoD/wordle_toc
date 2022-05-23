from flask import Flask
from game.wordle import solve
from flask import request
from flask import jsonify

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/solution", methods=['GET'])
def solution():
    args = request.args
    response = jsonify(solve(args["key"]))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
