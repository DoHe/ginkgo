from constants import DEFAULT, COLORS, RESET, GREEN


class Tile():

    def __init__(self, color, value, owner=None, resources=0):
        self.color = color
        self.value = value
        self.owner = owner
        self.resources = resources

    def __str__(self):
        owner_color = COLORS[DEFAULT]
        if self.owner is not None:
            owner_color = COLORS[self.owner.color]

        return '|{color}{number:02d}{reset}/{owner_color}{resources}{reset}|'.format(
            color=COLORS[self.color],
            number=self.value,
            owner_color=owner_color,
            resources=self.resources,
            reset=COLORS[RESET]
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.color == other.color and self.value == other.value

    def toJSON(self):
        owner_color = 'gray'
        if self.owner:
            owner_color = self.owner.color

        return {'name': 'tile', 'value': self.value, 'color': self.color, 'owner_color': owner_color,
                'resources': self.resources}


class Marker():
    color = GREEN

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '({} {}  {})'.format(COLORS[self.color], self.value, COLORS[RESET])

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return hasattr(other, 'value') and self.value == other.value

    def toJSON(self):
        return {'name': 'marker', 'value': self.value}


class Space():
    color = COLORS[DEFAULT]
    value = None

    def __str__(self):
        return '      '

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, Space)

    def toJSON(self):
        return {'name': 'space'}
