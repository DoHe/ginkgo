from quart import Quart, render_template, request

from constants import ORANGE, BLUE
from ginkgopolis import GameController
from player import RandomPlayer, WebPlayer
from server_helpers import json_response

app = Quart(__name__, static_url_path='/static')

PLAYERS = [RandomPlayer('John', ORANGE), WebPlayer('Lisa', BLUE)]
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


@app.route("/make_move/<player>", methods=['POST'])
async def make_move(player):
    move = await request.get_json()
    for p in PLAYERS:
        if player == p.name and isinstance(p, WebPlayer):
            await p.received_move(move)
            return "Move received", 200
    return "Player not found", 404


if __name__ == '__main__':
    app.run()
