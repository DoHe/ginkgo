import asyncio
import random

from board import Board, MARKERS, TILES
from cards import MarkerCard, card_factory, Planter, Scientist, Architect, Mechanic, Clerk
from constants import RED, YELLOW, BLUE, ORANGE, WHITE, VICTORY_POINT, RESOURCE, TILE, BUILD_UP
from pieces import Tile
from player import RandomPlayer


class GameController():

    def __init__(self, players):
        self.heroes = [
            [Planter(), Scientist(), Architect()],
            [Mechanic(), Clerk(), Architect()]
        ]
        self.tile_pool = [Tile(RED, number) for number in range(4, 21)] + \
                         [Tile(YELLOW, number) for number in range(4, 21)] + \
                         [Tile(BLUE, number) for number in range(4, 21)]
        self.draw_pile = [MarkerCard(marker) for marker in MARKERS] + \
                         [card_factory(tile) for tile in TILES]
        self.discard_pile = []
        for _set in (self.tile_pool, self.draw_pile, self.heroes):
            random.shuffle(_set)
        self.board = Board()
        self.players = players
        for player, heroes in zip(self.players, self.heroes):
            player.board = self.board
            player.game_controller = self
            player.cards = heroes
            for hero in heroes:
                for starter in hero.starting:
                    if starter == VICTORY_POINT:
                        player.victory_points += 1
                    elif starter == RESOURCE:
                        player.resources += 1
                    elif starter == TILE:
                        player.give_tile(self.draw_tile())
        self.draw_cards()
        self.first_player = random.randrange(len(self.players) + 1)

    async def play_round(self):
        actions = await asyncio.wait([player.plan_action() for player in self.players])
        planned_actions = {}
        for action in actions[0]:
            player, kind, card, extra = action.result()
            player.pay_for_move(kind, card, extra)
            if kind != BUILD_UP:
                self.discard_pile.append(card)
            planned_actions[player] = (kind, extra)
        self._execute_planned_actions(planned_actions)
        self.prepare_next_round()
        print(self.board)
        print("Discarded cards: {}".format(self.discard_pile))
        print("Cards to draw: {}".format(len(self.draw_pile)))
        print("Tiles left: {}".format(len(self.tile_pool)))
        print()
        for player in self.players:
            print(player)
            print()
        print("======================================")
        return {player.name: action for player, action in planned_actions.items()}

    def _execute_planned_actions(self, planned_actions):
        for player in (self.players[self.first_player:] + self.players[:self.first_player]):
            kind, extra = planned_actions[player]
            print("{}'s move: {} ({})".format(player.name, kind, extra))
            changes = getattr(self.board, kind.lower())(**extra)
            player.action_executed(changes)

    def prepare_next_round(self):
        self.rotate_hands()
        self.draw_cards()

    def rotate_hands(self):
        hands = []
        for player in self.players:
            hands.append(player.hand)
        for idx, hand in enumerate(hands):
            self.players[(idx + 1) % len(self.players)].hand = hand

    def draw_cards(self):
        for player in self.players:
            while len(player.hand) < 4:
                player.hand.append(self.draw_pile.pop())
                if not self.draw_pile:
                    self.refresh_draw_pile()

    def draw_tile(self):
        try:
            return self.tile_pool.pop()
        except IndexError:
            return None

    def refresh_draw_pile(self):
        self.draw_pile = self.discard_pile[:]
        self.discard_pile = []
        while self.board.new_tiles:
            new_tile = self.board.new_tiles.pop()
            self.draw_pile.append(card_factory(new_tile))
        random.shuffle(self.draw_pile)

    def game_over(self):
        return not self.tile_pool


async def main():
    john = RandomPlayer('John', ORANGE)
    amanda = RandomPlayer('Amanda', WHITE)
    game_controller = GameController([john, amanda])
    while not game_controller.game_over():
        await game_controller.play_round()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
