import random
import string
from pprint import pformat

from cards import MarkerCard, card_factory, Planter, Scientist, Architect, Mechanic, Clerk
from constants import RED, YELLOW, BLUE, UP, DOWN, LEFT, RIGHT, ORANGE, WHITE
from pieces import Tile, Marker, Space

MARKERS = [Marker(letter) for letter in string.ascii_uppercase[:12]]

TILES = [Tile(RED, number) for number in range(4, 21)] + \
        [Tile(YELLOW, number) for number in range(4, 21)] + \
        [Tile(BLUE, number) for number in range(4, 21)]

STARTING_TILES = [Tile(RED, number) for number in range(1, 4)] + \
                 [Tile(YELLOW, number) for number in range(1, 4)] + \
                 [Tile(BLUE, number) for number in range(1, 4)]

DRAW_PILE = [MarkerCard(marker) for marker in MARKERS] + \
            [card_factory(tile) for tile in STARTING_TILES]

CARD_POOL = [card_factory(tile) for tile in TILES]

HEROES = [
    [Planter(), Scientist(), Architect()],
    [Mechanic(), Clerk(), Architect()]
]


class Player():

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.hand = []
        self.cards = []
        self.tiles = []

    def __eq__(self, other):
        return self.name == other.name


class Board():

    def __init__(self):
        self.tiles = [[], [], []]
        for idx, tile in enumerate(random.sample(STARTING_TILES, len(STARTING_TILES))):
            self.tiles[idx // 3].append(tile)
        self.tiles.insert(0, [Space()] * 2 + MARKERS[:3] + [Space()])
        self.tiles.append([Space()] * 2 + list(reversed(MARKERS[6:9])) + [Space()])
        for idx, letter in enumerate(MARKERS[3:6]):
            self.tiles[idx + 1].extend([letter, Space()])
        for idx, letter in enumerate(reversed(MARKERS[9:])):
            self.tiles[idx + 1].insert(0, letter)
            self.tiles[idx + 1].insert(0, Space())
        self.tiles.insert(0, [Space()] * 5)
        self.tiles.append([Space()] * 5)

    def urbanize(self, marker, direction, tile):
        for idx_y, row in enumerate(self.tiles):
            for idx_x, element in enumerate(row):
                if element == marker:
                    if direction == UP:
                        move_x, move_y = idx_x, idx_y - 1
                    elif direction == DOWN:
                        move_x, move_y = idx_x, idx_y + 1
                    elif direction == LEFT:
                        move_x, move_y = idx_x - 1, idx_y
                    elif direction == RIGHT:
                        move_x, move_y = idx_x + 1, idx_y
                    else:
                        raise ValueError('Wrong direction type')
                    target = self.tiles[move_y][move_x]
                    if not isinstance(target, Space):
                        raise ValueError('Illegal target: {}'.format(target))
                    self.tiles[move_y][move_x] = element
                    tile.resources = 1
                    self.tiles[idx_y][idx_x] = tile
                    return

        raise ValueError('Marker {} does not exist'.format(marker))

    def build_up(self, target_tile, new_tile):
        for idx_y, row in enumerate(self.tiles):
            for idx_x, element in enumerate(row):
                if element == target_tile:
                    new_tile.resources = element.resources + 1
                    self.tiles[idx_y][idx_x] = new_tile
                    return

        raise ValueError('Tile {} does not exist').format(target_tile)

    def __str__(self):
        return pformat(self.tiles, indent=4, width=200)

    def __repr__(self):
        return self.__str__()


class GameController():

    def __init__(self, players):
        self.tiles = [Tile(RED, number) for number in range(4, 21)] + \
                     [Tile(YELLOW, number) for number in range(4, 21)] + \
                     [Tile(BLUE, number) for number in range(4, 21)]
        random.shuffle(self.tiles)
        self.players = players
        self.board = Board()


if __name__ == '__main__':
    john = Player('John', ORANGE)
    amanda = Player('Amanda', WHITE)
    game_controller = GameController([john, amanda])
    board = game_controller.board
    print(board)
    board.urbanize(Marker('A'), UP, Tile(YELLOW, 5, john))
    print(board)
    board.build_up(Tile(RED, 1), Tile(BLUE, 5, john))
    print(board)
    board.build_up(Tile(BLUE, 5), Tile(YELLOW, 10, amanda))
    print(board)
