import unittest
from unittest.mock import patch

import board
from constants import RED, YELLOW, BLUE, UP, RIGHT
from pieces import Tile, Marker, Space


class BoardTests(unittest.TestCase):

    def setUp(self):
        tiles = [Tile(RED, number) for number in range(1, 4)] + \
                [Tile(YELLOW, number) for number in range(1, 4)] + \
                [Tile(BLUE, number) for number in range(1, 4)]
        with patch(board.__name__ + '.TILES', tiles):
            self.board = board.Board()

    def test_get_tile(self):
        for search_tile, expected_x, expected_y in [
            (Tile(RED, 1), 2, 2),
            (Tile(RED, 2), 3, 2),
            (Tile(YELLOW, 2), 3, 3),
        ]:
            with self.subTest(color=search_tile.color, value=search_tile.value):
                tile, idx_x, idx_y = self.board.get_tile(search_tile)
                self.assertEqual(idx_x, expected_x)
                self.assertEqual(idx_y, expected_y)
                self.assertEqual(tile, search_tile)

    def test_get_neighbors(self):
        for search_tile, expected_neighbors in [
            (Tile(YELLOW, 2), [(Tile(YELLOW, 3), 4, 3), (Tile(YELLOW, 1), 2, 3),
                               (Tile(BLUE, 2), 3, 4), (Tile(RED, 2), 3, 2)]),
            (Tile(RED, 1), [(Tile(RED, 2), 3, 2), (Marker('L'), 1, 2),
                            (Tile(YELLOW, 1), 2, 3), (Marker('A'), 2, 1)]),
        ]:
            with self.subTest(color=search_tile.color, value=search_tile.value):
                _, idx_x, idx_y = self.board.get_tile(search_tile)
                neighbors = list(self.board.get_neighbors(idx_x, idx_y))
                self.assertListEqual(neighbors, expected_neighbors)

    def test_urbanize(self):
        self.board.urbanize(Marker('A'), UP, Tile(YELLOW, 1))
        self.board.urbanize(Marker('A'), UP, Tile(YELLOW, 1))
        self.board.urbanize(Marker('A'), UP, Tile(YELLOW, 1))
        self.assertListEqual(self.board.tiles[0], [Space()] * 7)
        self.board.urbanize(Marker('C'), RIGHT, Tile(YELLOW, 1))
        self.assertListEqual(self.board.tiles[0], [Space()] * 7)
        self.assertEqual(self.board.tiles[4][5], Marker('C'))
        self.assertEqual(self.board.tiles[3][5], Space())
        self.assertEqual(self.board.tiles[4][6], Space())


if __name__ == '__main__':
    unittest.main()
