

import re


def to_coord(x, y):
    x = chr(ord("A") + x - 1)
    y = str(y)
    return x + y


def from_coord(coord):
    m = re.match(r"([A-Z]+)(\d+)", coord)
    x, y = m.group(1), m.group(2)
    return ord(x) - ord("A") + 1, int(y)
