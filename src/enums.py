"""Enum definitions shared across the game.

This module centralizes names used by scenes, display settings, movement
logic, asset paths and ghost/game state transitions.
"""

from enum import Enum, auto


class SceneName(Enum):
    """Available game scenes.

    Enum values represent the scene transitions.
    """

    MAIN_MENU = auto()
    GAME = auto()
    SCORE_ENTRY = auto()
    SCOREBOARD = auto()
    INFO = auto()


class GhostState(Enum):
    """Possible states for each ghost entity.

    The state determines chase logic, frightened behavior, death handling,
    and respawn timing.
    """

    CHASE = auto()
    SCATTER = auto()
    FRIGHTENED = auto()
    DEAD = auto()
    RESPAWN = auto()


class ColorType(Enum):
    """Theme colors used by the renderer and scene elements."""

    PRIMARY = auto()
    SECONDARY = auto()


class AnchorPoint(Enum):
    """Enumeration of anchor positions for UI layout and text placement.

    These values control how surfaces are aligned relative to a given point.
    """

    TOP_LEFT = auto()
    TOP_CENTER = auto()
    TOP_RIGHT = auto()

    CENTER_LEFT = auto()
    CENTER = auto()
    CENTER_RIGHT = auto()

    BOTTOM_LEFT = auto()
    BOTTOM_CENTER = auto()
    BOTTOM_RIGHT = auto()


class Asset(Enum):
    """Filesystem asset paths and pixel dimensions used by the game.

    Values include both the asset directory names and the sprite sizes used
    for rendering UI and maze elements.
    """

    LETTER_PATH = "assets/letters"
    CURSOR_PATH = "assets/cursor"

    CURSOR_WIDE_PATH = "assets/cursor_wide"
    NAME_FRAME_PATH = "assets/name_frame"

    HEART_PATH = "assets/heart"
    BUTTON_PATH = "assets/button"

    LOGO_PATH = "assets/logo"

    LETTER_WIDTH = 40
    LETTER_HEIGHT = 40

    LETTER_SPACING = 5

    BUTTON_WIDTH = 320
    BUTTON_HEIGHT = 80

    HEART_WIDTH = 80
    HEART_HEIGHT = 65

    CURSOR_WIDTH = 88
    CURSOR_HEIGHT = 88

    CURSOR_WIDE_WIDTH = 264
    CURSOR_WIDE_HEIGHT = 88

    NAME_FRAME_WIDTH = 500
    NAME_FRAME_HEIGHT = 80


class DisplayInfo(Enum):
    """Screen geometry used throughout the game."""

    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 1280


class Direction(Enum):
    """Directions used by movement and maze traversal."""

    NONE = (0, 0, 0)
    NORTH = (0, -1, 0)
    EAST = (1, 0, 1)
    SOUTH = (0, 1, 2)
    WEST = (-1, 0, 3)
