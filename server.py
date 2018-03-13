from quart import Quart, render_template

from constants import ORANGE, WHITE
from ginkgopolis import GameController
from player import RandomPlayer
from server_helpers import json_response

app = Quart(__name__, static_url_path='/static')

PLAYERS = [RandomPlayer('John', ORANGE), RandomPlayer('Amanda', WHITE)]
GAME_CONTROLLER = GameController(PLAYERS)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/board")
def board():
    return json_response(GAME_CONTROLLER.board, app)


@app.route("/play")
async def play():
    planned = await GAME_CONTROLLER.play_round()
    return json_response(planned, app)


if __name__ == '__main__':
    app.run()
