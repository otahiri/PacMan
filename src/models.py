from typing import Any
import pygame
from abc import ABC, abstractmethod
from src.enums import Asset, ColorType, DisplayInfo, SceneName
from src.render import Renderer


class Button:

    def __init__(self, name: str, pos: tuple[int, int]) -> None:
        self.name = name
        x, y = pos

        self.idel, self.hover, size = Renderer.get_button()

        self.width, self.height = size

        self.pos = (x - self.width // 2, y - self.height // 2)

        self.text = Text(name, pos, ColorType.SECONDARY)

    def is_collide(self, pos: tuple[int, int]) -> bool:
        my_x, my_y = self.pos
        target_x, target_y = pos
        is_inside_x = my_x <= target_x <= (my_x + self.width)
        is_inside_y = my_y <= target_y <= (my_y + self.height)
        return is_inside_x and is_inside_y


class Text:

    def __init__(
        self,
        label: str,
        pos: tuple[int, int],
        color_type: ColorType,
        anchor_point: str = "center",
    ) -> None:

        self.label = label
        self.pos = pos
        self.surf, self.size = Renderer.get_text(label, color_type)
        self.anchor_point = anchor_point


class LetterButton:

    def __init__(
        self,
        surf: pygame.Surface,
        letter: str,
        pos: tuple[int, int],
        size: tuple[int, int],
        place: tuple[int, int],
    ) -> None:
        self.surf = surf
        self.letter = letter
        self.pos = pos
        self.size = size
        self.place = place

    def is_collide(self, pos: tuple[int, int]) -> bool:

        width, height = self.size

        width *= 2
        height *= 2
        my_x, my_y = Renderer.get_pos(self.pos, (width, height))
        if self.letter == "E":
            width *= 3
        target_x, target_y = pos
        is_inside_x = my_x <= target_x <= (my_x + width)
        is_inside_y = my_y <= target_y <= (my_y + height)
        return is_inside_x and is_inside_y


class Cursor:
    def __init__(
        self,
    ) -> None:

        width = Asset.CURSOR_WIDTH.value
        height = Asset.CURSOR_WIDTH.value

        wide_width = Asset.CURSOR_WIDE_WIDTH.value
        wide_height = Asset.CURSOR_WIDE_HEIGHT.value

        self.wide_size = (wide_width, wide_height)
        self.size = (width, height)

        self.surf = Renderer.change_color(
            pygame.image.load(f"{Asset.CURSOR_PATH.value}.png"),
        )

        self.wide_surf = Renderer.change_color(
            pygame.image.load(f"{Asset.CURSOR_WIDE_PATH.value}.png"),
        )

        self.size = (width, height)

        wide_width = Asset.CURSOR_WIDE_WIDTH.value
        wide_height = Asset.CURSOR_WIDE_HEIGHT.value
        self.wide_size = (wide_width, wide_height)

        self.is_wide = False
        self.x = 0
        self.y = 0
        self.letter_hover = "0"


class NameFrame:
    def __init__(self) -> None:
        width, height = (
            Asset.NAME_FRAME_WIDTH.value,
            Asset.NAME_FRAME_HEIGHT.value,
        )
        self.surf = Renderer.change_color(
            pygame.image.load(f"{Asset.NAME_FRAME_PATH.value}.png"),
        )
        self.size = (width, height)
        self.pos = (
            DisplayInfo.SCREEN_WIDTH.value // 2,
            DisplayInfo.SCREEN_HEIGHT.value // 2,
        )

        self.name = ""
        self.text = Text(" ", self.pos, ColorType.PRIMARY)

    def update_name(self, letter: str) -> None:
        self.name += letter
        self.text = Text(self.name, self.pos, ColorType.PRIMARY)


class Scene(ABC):
    @abstractmethod
    def render_scene(self, renderer: Renderer) -> None: ...

    @abstractmethod
    def handle_events(self, events: list[pygame.Event]) -> dict[str, Any]: ...


class Corner:
    """corner object to decide the look of the corner connecting walls

    Attributes:
        bit: bit value for the corner representing the sides it has
    """

    def __init__(self) -> None:
        """constructor of the Corner class"""
        self.bit = 0


class Cell:
    """cell class that has all the attributes of the cell

    Attributes:
        bit_value: the bit value of the cell representing which  walls are open
        top_left: top left corner
        top_right: top right corner
        bottom_left: bottom left corner
        bottom_right: bottom right corner
    """

    def __init__(
        self, bit_value: int, corners: list[Corner], content: Any, cord: tuple
    ) -> None:
        """constructor of the Cell class

        Args:
            bit: bit value of the cell
            corners: list of corners surrounding the cell
        """
        self.bit_value = bit_value
        self.content: Gum | SuperGum | None = None
        self.top_left = corners[0]
        self.top_right = corners[1]
        self.bottom_left = corners[2]
        self.bottom_right = corners[3]
        self.update_corners()
        self.content = content
        self.cord = cord

    def update_corners(self) -> None:
        """mask the corner bit value according to the bit value of the cell
        top left corner will have an east side if the cell has a north wall
        and a south side if the cell has a west wall
        top right corner will have a west side if the cell has a north wall
        and a south side if the cell has an east wall
        bottom right corner will have north side if the cell has an east
        wall and a west side if the cell has a south wall
        bottom left corner  will have a north side if the cell has a west
        wall and an east side if the cell has a south wall
        """
        self.top_left.bit |= (1 & self.bit_value) << 1
        self.top_left.bit |= (8 & self.bit_value) >> 1
        self.top_right.bit |= (1 & self.bit_value) << 3
        self.top_right.bit |= (2 & self.bit_value) << 1
        self.bottom_right.bit |= (2 & self.bit_value) >> 1
        self.bottom_right.bit |= (4 & self.bit_value) << 1
        self.bottom_left.bit |= (4 & self.bit_value) >> 1
        self.bottom_left.bit |= (8 & self.bit_value) >> 3


class Character(ABC):
    def __init__(
        self,
        speed: int,
        scale: int,
        origin: tuple,
        maze: list[list[Cell]],
        anchors: list = [],
    ) -> None:
        self.id = 0
        self.maze = maze
        self.speed = speed
        self.scale = scale
        self.scaled_v_step_y = 32 * scale
        self.scaled_v_step_x = 32 * scale
        self.scaled_half_v_step_y = 16 * scale
        self.scaled_half_v_step_x = 16 * scale
        self.max_y = len(self.maze) * self.scaled_v_step_y
        self.max_x = len(self.maze[0]) * self.scaled_v_step_x
        self.origin = origin

    @abstractmethod
    def get_sprite(self, frame: int) -> pygame.Surface: ...

    @abstractmethod
    def move(self, frame: int) -> pygame.Surface: ...

    @abstractmethod
    def update_visual_cord(self) -> None: ...

    @abstractmethod
    def choose_direction(self) -> None: ...

    @abstractmethod
    def reset_cords(self) -> None: ...

    @abstractmethod
    def die(self) -> None: ...


class Gum:
    def __init__(
        self,
        score: int,
        cord: tuple,
        sprite: pygame.Surface,
        is_super: bool = False,
    ) -> None:
        self.is_super = is_super
        self.score = score
        self.cord = cord
        self.sprite = sprite


class SuperGum(Gum):
    def __init__(
        self, score: int, cord: tuple, sprite: pygame.Surface
    ) -> None:
        super().__init__(score, cord, sprite, True)
