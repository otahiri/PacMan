from numpy.testing import assert_
import pygame
from abc import ABC, abstractmethod
from src.enums import Asset, SceneName
from src.render import Renderer
from src.maze import Cell


class Button:

    def __init__(self, name: str, pos: tuple[int, int], scale: int) -> None:
        self.name = name
        x, y = pos

        self.idel, self.hover, size = Renderer.get_button(scale)

        self.width, self.height = size

        self.pos = (x - self.width // 2, y - self.height // 2)

        self.text = Text(name, pos, "black")

    def is_collide(self, pos: tuple[int, int]):
        my_x, my_y = self.pos
        target_x, target_y = pos
        is_inside_x = my_x <= target_x <= (my_x + self.width)
        is_inside_y = my_y <= target_y <= (my_y + self.height)
        return is_inside_x and is_inside_y


class Text:

    def __init__(self, text: str, pos: tuple[int, int], color: str) -> None:

        self.text = text
        self.surf, self.size = Renderer.get_text(text, 5, color)
        self.pos = pos


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

        # self.hover_width, self.hover_height = size
        # self.hover_width *= 2
        # self.hover_height *= 2
        # self.hover_surf = pygame.Surface((self.hover_width, self.hover_height))
        # self.hover_surf.fill("red")

    def is_collide(self, pos: tuple[int, int]):

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
        scale = 11
        self.surf = Renderer.scale_surface(
            pygame.image.load(f"{Asset.CURSOR_PATH.value}.png"),
            (Asset.CURSOR_WIDTH.value, Asset.CURSOR_HEIGHT.value),
            scale,
        )
        self.wide_surf = Renderer.scale_surface(
            pygame.image.load(f"{Asset.CURSOR_WIDE_PATH.value}.png"),
            (Asset.CURSOR_WIDE_WIDTH.value, Asset.CURSOR_WIDE_HEIGHT.value),
            scale,
        )

        width = Asset.CURSOR_WIDTH.value * scale
        height = Asset.CURSOR_WIDTH.value * scale
        self.size = (width, height)

        wide_width = Asset.CURSOR_WIDE_WIDTH.value * scale
        wide_height = Asset.CURSOR_WIDE_HEIGHT.value * scale
        self.wide_size = (wide_width, wide_height)

        self.is_wide = False
        self.x = 0
        self.y = 0


class Scene(ABC):

    @abstractmethod
    def render_scene(self, renderer: Renderer) -> None: ...

    @abstractmethod
    def handle_events(
        self, events: list[pygame.Event]
    ) -> None | SceneName: ...


class Character(ABC):
    @abstractmethod
    def __init__(
        self,
        speed: int,
        scale: int,
        maze: list[list[Cell]],
        anchors: list = [],
    ) -> None: ...

    @abstractmethod
    def get_sprite(self, frame: int) -> pygame.Surface: ...

    @abstractmethod
    def move(self, frame: int) -> pygame.Surface: ...

    @abstractmethod
    def update_visual_cord(self): ...

    @abstractmethod
    def choose_direction(self): ...

    @abstractmethod
    def set_cords(self) -> None: ...
