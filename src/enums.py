from enum import Enum, auto


class SceneName(Enum):
    MAIN_MENU = auto()
    GAME = auto()
    SCORE_ENTRY = auto()
    SCOREBOARD = auto()


class PlayerState(Enum):
    ALIVE = auto()
    DEAD = auto()


class GhostState(Enum):
    CHASE = auto()
    SCATTER = auto()
    FRIGHTENED = auto()
    DEAD = auto()
    RESPAWN = auto()


class ColorType(Enum):
    PRIMARY = auto()
    SECONDARY = auto()


class Asset(Enum):
    LETTER_PATH = "assets/letters"
    CURSOR_PATH = "assets/cursor"

    CURSOR_WIDE_PATH = "assets/cursor_wide"
    NAME_FRAME_PATH = "assets/name_frame"

    HEART_PATH = "assets/heart"

    LETTER_WIDTH = 40
    LETTER_HEIGHT = 40

    LETTER_SPACING = 5

    BUTTON_WIDTH = 320
    BUTTON_HEIGHT = 110

    HEART_WIDTH = 80
    HEART_HEIGHT = 65

    CURSOR_WIDTH = 88
    CURSOR_HEIGHT = 88

    CURSOR_WIDE_WIDTH = 264
    CURSOR_WIDE_HEIGHT = 88

    NAME_FRAME_WIDTH = 500
    NAME_FRAME_HEIGHT = 80


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
