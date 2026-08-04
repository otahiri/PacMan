from enum import Enum, auto


class SceneName(Enum):
    MAIN_MENU = auto()
    GAME = auto()
    SCORE_ENTRY = auto()
    SCOREBOARD = auto()
    OPTIONS = auto()


class PlayerState(Enum):
    ALIVE = auto()
    DEAD = auto()


class GhostState(Enum):
    CHASE = auto()
    SCATTER = auto()
    FRIGHTENED = auto()
    DEAD = auto()
    RESPAWN = auto()


class Asset(Enum):
    LETTER_PATH = "assets/letters"
    CURSOR_PATH = "assets/cursor"
    CURSOR_WIDE_PATH = "assets/cursor_wide"
    NAME_FRAME_PATH = "assets/name_frame"

    LETTER_WIDTH = 8
    LETTER_HEIGHT = 8

    LETTER_SPACING = 5

    BUTTON_WIDTH = 32
    BUTTON_HEIGHT = 11

    HEART_WIDTH = 16
    HEART_HEIGHT = 13

    CURSOR_WIDTH = 8
    CURSOR_HEIGHT = 8

    CURSOR_WIDE_WIDTH = 24
    CURSOR_WIDE_HEIGHT = 8

    NAME_FRAME_WIDTH = 50
    NAME_FRAME_HEIGHT = 8


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
