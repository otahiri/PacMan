import pygame
from abc import ABC, abstractmethod
from src.enums import SceneName
from src.render import Renderer


class Button:

    def __init__(self, name: str, pos: tuple[int, int]) -> None:
        self.name = name
        self.x, self.y = pos
        idel, hover, width, height = Renderer.get_button()

        self.idel = Renderer.scale_surface(
            idel,
            (width, height),
            (width * 10, height * 10),
        )
        self.hover = Renderer.scale_surface(
            hover,
            (width, height),
            (width * 10, height * 10),
        )

        self.width = width * 10
        self.height = height * 10
        self.x -= self.width // 2

    def is_collide(self, pos: tuple[int, int]):
        x, y = pos
        is_inside_x = self.x <= x <= (self.x + self.width)
        is_inside_y = self.y <= y <= (self.y + self.height)
        return is_inside_x and is_inside_y


class Scene(ABC):

    @abstractmethod
    def render_scene(self, renderer: Renderer) -> None: ...

    @abstractmethod
    def handle_events(self, events: list[pygame.Event]) -> None | SceneName: ...
