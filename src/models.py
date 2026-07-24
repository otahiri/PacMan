import pygame
from abc import ABC, abstractmethod
from src.enums import SceneName
from src.render import Renderer


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
        self.surf, size = Renderer.get_text(text, 5, color)
        self.width, self.height = size

        x, y = pos
        self.pos = (x - self.width // 2, y - self.height // 2)


class Scene(ABC):

    @abstractmethod
    def render_scene(self, renderer: Renderer) -> None: ...

    @abstractmethod
    def handle_events(
        self, events: list[pygame.Event]
    ) -> None | SceneName: ...
