import pygame
from abc import ABC, abstractmethod
from src.enums import SceneName
from src.render import Renderer


class Button:

    def __init__(self, name: str, pos: tuple[int, int]) -> None:
        self.name = name
        self.x, self.y = pos
        self.idel, self.hover, size = Renderer.get_button()
        self.width, self.height = size
        self.x -= self.width // 2

    def is_collide(self, pos: tuple[int, int]):
        x, y = pos
        is_inside_x = self.x <= x <= (self.x + self.width)
        is_inside_y = self.y <= y <= (self.y + self.height)
        return is_inside_x and is_inside_y


class Text:
    def __init__(self, text: str) -> None:

        self.text = text
        self.surf, size = Renderer.get_text(text, 5)
        self.width, self.height = size

    def render(self, renderer: Renderer, pos: tuple[int, int]):
        width, height = pos
        width -= self.width // 2
        height -= self.height // 2

        renderer.window.blit(self.surf, (width, height))


class Scene(ABC):

    @abstractmethod
    def render_scene(self, renderer: Renderer) -> None: ...

    @abstractmethod
    def handle_events(
        self, events: list[pygame.Event]
    ) -> None | SceneName: ...
