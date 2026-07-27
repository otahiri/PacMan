import pygame
from abc import ABC, abstractmethod
from src.enums import SceneName
from src.render import Renderer
from src.maze import Cell


class Button:

    def __init__(self, name: str, scale: int) -> None:
        self.name = name

        self.idel, self.hover, self.size = Renderer.get_button(scale)

        self.width, self.height = self.size

        self.text = Text(name, "black")

    def is_collide(
        self, source_pos: tuple[int, int], target_pos: tuple[int, int]
    ):
        my_x, my_y = source_pos
        target_x, target_y = target_pos
        is_inside_x = my_x <= target_x <= (my_x + self.width)
        is_inside_y = my_y <= target_y <= (my_y + self.height)
        return is_inside_x and is_inside_y


class Text:

    def __init__(self, text: str, color: str) -> None:

        self.text = text
        self.surf, self.size = Renderer.get_text(text, 5, color)


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
