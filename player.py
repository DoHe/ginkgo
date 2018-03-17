import abc
import asyncio
import random

from cards import ActionCard
from constants import URBANIZE, BUILD_UP, PLAN, RESOURCE, TILE, LEFT, DOWN, RIGHT, UP, VICTORY_POINT, COLORS, RESET
from pieces import Space, Marker, Tile


class Player(abc.ABC):

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.hand = []
        self.cards = []
        self.tiles = []
        self.board = None
        self.resources = 0
        self.victory_points = 0
        self.last_card = None
        self.last_move = None

    @abc.abstractmethod
    async def plan_action(self):
        pass

    def action_executed(self, changes):
        for card in self.cards:
            if isinstance(card, ActionCard):
                changes.append(card.benefit(self.last_move))

        self._apply_changes(changes)

        if self.last_move == BUILD_UP:
            self.cards.append(self.last_card)

    def _apply_changes(self, changes):
        for amount, target in changes:
            if not amount:
                continue
            if target == VICTORY_POINT:
                self.victory_points += amount
            elif target == RESOURCE:
                self.resources += amount
            elif target == TILE:
                for _ in range(amount):
                    tile = self.game_controller.draw_tile()
                    if tile:
                        self.give_tile(tile)

    def give_tile(self, tile):
        tile.owner = self
        self.tiles.append(tile)

    def pay_for_move(self, move, card, extra):
        self.last_card = card
        self.last_move = move
        self.hand.remove(card)

        if move != PLAN:
            self.tiles.remove(extra['new_tile'])

        if move == URBANIZE:
            self.resources -= 1

        if move == BUILD_UP:
            self.resources -= self.board.get_tile(card.target)[0].resources + 1

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):
        return self.name < other.name

    def __str__(self):
        return "{}_{}_{}:\ntiles: {}\nresources: {}\nvictory points: {}\nhand: {}\ncards: {}".format(
            COLORS[self.color],
            self.name,
            COLORS[RESET],
            self.tiles,
            self.resources,
            self.victory_points,
            self.hand,
            self.cards
        )

    def __repr__(self):
        return self.__str__()

    def toJSON(self):
        return {
            'name': self.name,
            'color': self.color,
            'hand': self.hand,
            'cards': self.cards,
            'tiles': self.tiles,
            'resources': self.resources,
            'victory_points': self.victory_points,
            'is_web': isinstance(self, WebPlayer)
        }


class RandomPlayer(Player):
    possible_moves = [PLAN, BUILD_UP, URBANIZE]

    def __init__(self, name, color):
        super().__init__(name, color)

    async def plan_action(self):
        possible_moves = self.possible_moves[:]
        random.shuffle(self.hand)
        random.shuffle(possible_moves)
        random.shuffle(self.tiles)
        if not self.tiles:
            possible_moves = [PLAN]

        for move in possible_moves:
            for card in self.hand:
                if move == PLAN:
                    extra = self._extra_for_move(move, card, None)
                    if extra:
                        return self, move, card, extra
                else:
                    for tile in self.tiles:
                        extra = self._extra_for_move(move, card, tile)
                        if extra:
                            return self, move, card, extra

    def _extra_for_move(self, move, card, tile):
        if move == PLAN:
            return {
                'target_tile': card.target,
                'wish': random.choice((RESOURCE, TILE))
            }
        if move == BUILD_UP:
            target_tile, _, _ = self.board.get_tile(card.target)
            if isinstance(target_tile, Marker) or target_tile.resources >= self.resources:
                return None
            return {
                'target_tile': card.target,
                'new_tile': tile
            }
        if move == URBANIZE:
            if self.resources < 1:
                return None
            _, idx_x, idx_y = self.board.get_tile(card.target)
            neighbors = list(self.board.get_neighbors(idx_x, idx_y))
            random.shuffle(neighbors)
            for neighbor, neighbor_idx_x, neighbor_idx_y in neighbors:
                if isinstance(neighbor, Space):
                    if neighbor_idx_x < idx_x:
                        direction = LEFT
                    elif neighbor_idx_y < idx_y:
                        direction = UP
                    elif neighbor_idx_x > idx_x:
                        direction = RIGHT
                    elif neighbor_idx_y > idx_y:
                        direction = DOWN

                    return {
                        'marker': card.target,
                        'direction': direction,
                        'new_tile': tile
                    }

                return None


class WebPlayer(Player):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.receiver = None

    async def plan_action(self):
        self.receiver = asyncio.Future()
        await asyncio.wait([self.receiver])
        move = self.receiver.result()
        if move['cardTarget'].get('color') not in [None, 'undefined']:
            target = Tile(**move['cardTarget'])
        else:
            target = Marker(**move['cardTarget'])
        for card in self.hand:
            if card.target == target:
                break

        return self, move['kind'], card, move['extra']

    async def received_move(self, move):
        while self.receiver is None or self.receiver.done():
            await asyncio.sleep(0.1)
        self.receiver.set_result(move)
