from enum import Enum, auto


class SceneName(Enum):
    MAIN_MENU = auto()
    GAME = auto()
    SCORE_ENTRY = auto()
    SCOREBOARD = auto()


class Asset(Enum):
    LETTER_PATH = "assets/letters"
    LETTER_WIDTH = 8
    LETTER_HEIGHT = 16
    LETTER_SPACING = 5


class DisplayInfo(Enum):
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 1280
