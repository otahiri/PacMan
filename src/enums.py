from enum import Enum, auto


class SceneName(Enum):
    MAIN_MENU = auto()
    GAME = auto()
    SCORE_ENTRY = auto()
    SCOREBOARD = auto()
    OPTIONS = auto()


class Asset(Enum):
    LETTER_PATH = "assets/letters"
    LETTER_WIDTH = 8
    LETTER_HEIGHT = 16
    LETTER_SPACING = 5
    BUTTON_WIDTH = 32
    BUTTON_HEIGHT = 11
    HART_WIDTH = 16
    HART_HEIGHT = 13


class DisplayInfo(Enum):
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 1280


class Direction(Enum):
    """represent each direction the player can face

    Attributes:
        NORTH: north direction
        EAST: east direction
        SOUTH: south direction
        WEST: west direction
    """

    NONE = (0, 0, 0)
    NORTH = (0, -1, 0)
    EAST = (1, 0, 1)
    SOUTH = (0, 1, 2)
    WEST = (-1, 0, 3)
