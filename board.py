import random
import string
from pprint import pformat

from constants import UP, DOWN, LEFT, RIGHT, RED, YELLOW, BLUE, COLOR_TO_KIND, RESOURCE, VICTORY_POINT
from pieces import Space, Marker, Tile

MARKERS = [Marker(letter) for letter in string.ascii_uppercase[:12]]
TILES = [Tile(RED, number) for number in range(1, 4)] + \
        [Tile(YELLOW, number) for number in range(1, 4)] + \
        [Tile(BLUE, number) for number in range(1, 4)]
random.shuffle(TILES)


class Board():

    def __init__(self):
        self.tiles = [[], [], []]
        for idx, tile in enumerate(TILES):
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
        self.new_tiles = []

    def urbanize(self, marker, direction, new_tile):
        element, idx_x, idx_y = self.get_tile(marker)
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
        new_tile.resources = 1
        self.tiles[idx_y][idx_x] = new_tile
        self.new_tiles.append(new_tile)

        if move_y == 0:
            self.tiles.insert(0, [Space()] * len(self.tiles[1]))
        if move_y == len(self.tiles) - 1:
            self.tiles.append([Space()] * len(self.tiles[-1]))
        if move_x == 0:
            for row in self.tiles:
                row.insert(0, Space())
        if move_x == len(self.tiles[move_y]) - 1:
            current_row = self.tiles[move_y]
            current_row.append(Space())
            for other_row in (self.tiles[move_y - 1], self.tiles[move_y + 1]):
                if len(other_row) < len(current_row):
                    other_row.append(Space())

        changes = []
        for neighbor, neighbor_idx_x, neighbor_idx_y in self.get_neighbors(idx_x, idx_y):
            try:
                changes.append((max(1, neighbor.resources), COLOR_TO_KIND[neighbor.color]))
            except AttributeError:
                pass
        return changes

    def build_up(self, target_tile, new_tile):
        element, idx_x, idx_y = self.get_tile(target_tile)
        new_tile.resources = element.resources + 1
        self.tiles[idx_y][idx_x] = new_tile
        self.new_tiles.append(new_tile)

        changes = []
        if element.color != new_tile.color:
            changes.append((-1, RESOURCE))
        if element.value > new_tile.value:
            changes.append((new_tile.value - element.value, VICTORY_POINT))
        return changes

    def plan(self, target_tile, wish):
        if isinstance(target_tile, Marker):
            return [(1, wish)]
        element, _, _ = self.get_tile(target_tile)
        return [(max(1, element.resources), COLOR_TO_KIND[element.color])]

    def get_tile(self, tile):
        for idx_y, row in enumerate(self.tiles):
            for idx_x, element in enumerate(row):
                if element == tile:
                    return element, idx_x, idx_y

        raise ValueError('Tile {} does not exist'.format(tile))

    def get_neighbors(self, idx_x, idx_y):
        for neighbor_x_diff, neighbor_y_diff in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor_idx_x = idx_x + neighbor_x_diff
            neighbor_idx_y = idx_y + neighbor_y_diff
            yield self.tiles[neighbor_idx_y][neighbor_idx_x], neighbor_idx_x, neighbor_idx_y

    def json(self):
        return [[piece.json() for piece in row] for row in self.tiles]

    def __str__(self):
        return pformat(self.tiles, indent=4, width=400)

    def __repr__(self):
        return self.__str__()
