from enum import Enum


class BlockType(Enum):
    EMPTY = 0,
    UNBREAKABLE_WALL = 1,
    BREAKABLE_WALL = 2,
    TEMPORARY_WALL = 3,
    NO_BLOCK = 4
