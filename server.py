from flask import Flask, render_template, jsonify

from constants import ORANGE, WHITE
from ginkgopolis import GameController
from player import RandomPlayer

app = Flask(__name__, static_url_path='/static')


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/board")
def board():
    john = RandomPlayer('John', ORANGE)
    amanda = RandomPlayer('Amanda', WHITE)
    game_controller = GameController([john, amanda])
    print(game_controller.board.json())
    return jsonify(game_controller.board.json())
