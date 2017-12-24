

import random

from errors import NotPlaceableError, ValidationError
import util


class Board:
    SIZE = (11, 11)
    def __init__(self, ships=None):
        self.ships = ships or {
            # size: amount
            4: 1,
            3: 2,
            2: 3,
            1: 4,
        }
        self._board = {
            util.to_coord(x, y): None
            for x in range(1, self.SIZE[0])
            for y in range(1, self.SIZE[1])
        }

    def fill_randomly(self):
        possible = [(x, y) for x in range(1, self.SIZE[0]) for y in range(1, self.SIZE[1])]
        for size, amount in self.ships.items():
            choices = possible[:]
            random.shuffle(choices)
            for i in range(amount):
                for x, y in choices:
                    for direction in ('x', 'y'):
                        if direction == 'x':
                            ex = x + size - 1
                            ey = y
                        else:
                            ex = x
                            ey = y + size - 1
                        sequence = [util.to_coord(xi, yi) for xi in range(x, ex+1) for yi in range(y, ey+1)]
                        if all([self.can_place(coord) for coord in sequence]):
                            for coord in sequence:
                                self.place(coord)
                                xi, yi = util.from_coord(coord)
                                choices.remove((xi, yi))
                                possible.remove((xi, yi))
                            break
                    else:  # no success adding ship
                        continue
                    break  # success adding ship
                else:
                    raise NotPlaceableError("Board not big enough to place all ships")

    def place(self, coord):
        """Place ship at coord"""
        x, y = util.from_coord(coord)
        if x > 0 and y > 0 and x <= self.SIZE[0] and y <= self.SIZE[1]:
            self._board[coord] = True
        else:
            raise NotPlaceableError(f"Coord {coord} out of bounds {self.SIZE}")

    def is_ship(self, coord):
        return self._board.get(coord, False)

    def unknowns(self):
        for coord, is_ship in self._board.items():
            if is_ship is None:
                yield coord

    def get_ships(self):
        return [coord for coord, is_ship in self._board.items() if is_ship]

    def can_place(self, coord):
        x, y = util.from_coord(coord)
        if not (0 < x < self.SIZE[0] and 0 < y < self.SIZE[1]):
            return False
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                 if self.is_ship(util.to_coord(i, j)):
                     return False
        return True

    def validate(self):
        placed = [coord for coord, is_ship in self._board.items() if is_ship]
        sequences = []
        for coord in placed:
            x, y = util.from_coord(coord)
            for sequence in sequences:
                if len(set([x for x, y in sequence] + [x])) == 1:  # if x is the same
                    ys = sorted([y for x, y in sequence] + [y])
                    if ys == list(range(ys[0], ys[-1]+1)):
                        sequence.append((x, y))
                        break
                elif len(set([y for x, y in sequence] + [y])) == 1:  # if y is the same
                    xs = sorted([x for x, y in sequence] + [x])
                    if xs == list(range(xs[0], xs[-1]+1)):
                        sequence.append((x, y))
                        break
            else:
                sequences.append([(x, y)])

        ships = {}
        for sequence in sequences:
            size = len(sequence)
            try:
                ships[size] += 1
            except KeyError:
                ships[size] = 1

        if ships != self.ships:
            raise ValidationError(f"Got ships count {ships}, expected {self.ships}")