from constants import VICTORY_POINT, RED, RESOURCE, TILE, BLUE, YELLOW, PLAN, URBANIZE, BUILD_UP, COLORS, RESET
from pieces import Tile


class Card:

    def __init__(self, target):
        self.target = target

    def __str__(self):
        return '/{}{}{}\\'.format(COLORS[self.target.color], self.target.value, COLORS[RESET])

    def __repr__(self):
        return self.__str__()


class ActionCard(Card):

    def __init__(self, target):
        super().__init__(target)
        self.action = PLAN
        if self.target.value in [2, 5, 8]:
            self.action = URBANIZE
        elif self.target.value in [3, 6, 9]:
            self.action = BUILD_UP

    def benefit(self, action):
        if action != self.action:
            return (0, None)

        kind = VICTORY_POINT
        if self.target.color == RED:
            kind = RESOURCE
        elif self.target.color == BLUE:
            kind = TILE

        amount = 1
        if self.target.value >= 7:
            amount = 2

        return (amount, kind)


def _matching_tiles(board, player, condition):
    matches = []
    for row in board:
        for tile in row:
            if tile.owner == player:
                if condition(tile):
                    matches.append(tile)
    return matches


class ColorEndgameCard(Card):

    def __init__(self, target):
        super().__init__(target)

    def benefit(self, board, player):
        if self.target.number == 10 or self.target.number == 13:
            color = self.target.color
        elif self.target.number == 11:
            color = RED if self.target.color != RED else YELLOW
        elif self.target.number == 12:
            color = BLUE if self.target.color != BLUE else YELLOW

        matching_tiles = _matching_tiles(board, player, lambda tile: tile.color == color)
        amount = sum(len(tile.resources) for tile in matching_tiles)
        return (amount, VICTORY_POINT)


class HeightEndgameCard(Card):

    def __init__(self, target):
        super().__init__(target)

    def benefit(self, board, player):
        condition = lambda tile: tile.resources <= 2
        per_tile = 1
        if self.target.number == 15:
            condition = lambda tile: tile.resources >= 3
            per_tile = 3

        amount = len(_matching_tiles(board, player, condition))
        return (amount * per_tile, VICTORY_POINT)


class CardEndgameCard(Card):

    def __init__(self, target):
        super().__init__(target)

    def benefit(self, player):
        action = None
        if self.target.number == 16:
            action = PLAN
        elif self.target.number == 17:
            action = URBANIZE
        elif self.target.number == 18:
            action = BUILD_UP

        if action:
            condition = lambda card: card.action == action
        else:
            condition = lambda card: card.target.color == self.target.color

        amount = len([card for card in player.cards if condition(card)])
        return (amount * 2, VICTORY_POINT)


class ConditionlessEndgameCard(Card):
    def __init__(self, target):
        super().__init__(target)

    def benefit(self):
        return (9, VICTORY_POINT)


class MarkerCard(Card):
    def __init__(self, target):
        super().__init__(target)


def card_factory(target):
    if target.value <= 9:
        cardClass = ActionCard
    elif target.value <= 13:
        cardClass = ColorEndgameCard
    elif target.value <= 15:
        cardClass = HeightEndgameCard
    elif target.value <= 19:
        cardClass = CardEndgameCard
    else:
        cardClass = ConditionlessEndgameCard

    return cardClass(target)


class HeroCard(ActionCard):

    def __init__(self):
        self.target = Tile(self.color, -1)


class Scientist(HeroCard):
    color = BLUE
    action = BUILD_UP
    starting = [RESOURCE]


class Planter(HeroCard):
    color = RED
    action = URBANIZE
    starting = [RESOURCE, VICTORY_POINT, TILE]


class Architect(HeroCard):
    color = YELLOW
    action = BUILD_UP
    starting = [RESOURCE, RESOURCE, VICTORY_POINT, TILE]


class Clerk(HeroCard):
    color = BLUE
    action = PLAN
    starting = [RESOURCE, RESOURCE, VICTORY_POINT]


class Mechanic(HeroCard):
    color = RED
    action = BUILD_UP
    starting = [TILE]
