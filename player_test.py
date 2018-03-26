import asynctest

from cards import Card
from constants import UP
from pieces import Tile, Marker
from player import WebPlayer

MARKER_A = Marker('A')
RED_1_TILE = Tile('red', 1)
RED_2_TILE = Tile('red', 2)


class WebPlayerTests(asynctest.TestCase):

    def setUp(self):
        self.player = WebPlayer(name='Test', color='red')
        self.player.hand = [Card(RED_1_TILE)]

    async def test_plan_action(self):
        for move, expected_kind, expected_card, expected_extra in [
            ({
                 'kind': 'plan',
                 'cardTarget': {'value': 1, 'color': 'red'},
                 'extra': {
                     'target_tile': {'value': 1, 'color': 'red'},
                     'wish': 'resource'
                 }
             }, 'plan', Card(RED_1_TILE), {'target_tile': RED_1_TILE, 'wish': 'resource'}),
            ({
                 'kind': 'build_up',
                 'cardTarget': {'value': 1, 'color': 'red'},
                 'extra': {
                     'target_tile': {'value': 1, 'color': 'red'},
                     'new_tile': {'value': 2, 'color': 'red'}
                 }
             }, 'build_up', Card(RED_1_TILE), {'target_tile': RED_1_TILE, 'new_tile': RED_2_TILE}),
            ({
                 'kind': 'urbanize',
                 'cardTarget': {'value': 'A'},
                 'extra': {
                     'marker': 'A',
                     'direction': 'up',
                     'new_tile': {'value': 2, 'color': 'red'}
                 }
             }, 'urbanize', Card(RED_1_TILE), {'marker': MARKER_A, 'new_tile': RED_2_TILE, 'direction': UP}),
        ]:
            with self.subTest(kind=expected_kind, card=expected_card):
                self.player.receiver.set_result(move)
                _, kind, card, extra = await self.player.plan_action()
                self.assertEqual(expected_kind, kind)
                self.assertEqual(expected_card, card)
                self.assertDictEqual(expected_extra, extra)
