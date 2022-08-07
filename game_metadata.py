from enum import Enum
from typing import NamedTuple


class Move(NamedTuple):
    col: int
    row: int


class Player(int, Enum):
    player_1 = 1
    player_2 = 2


class BoardEntries(int, Enum):
    X_entry = 1
    O_entry = -1
    Blank = 0
