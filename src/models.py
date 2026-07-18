import pygame
from abc import ABC, abstractmethod
from src.enums import SceneName


class Button:

    def __init__(self, name: str, pos: tuple[int, int]) -> None:
        self.name = name
        font = pygame.font.Font(None, 100)
        self.text_surf = font.render(name, True, "white")
        self.text_rect = self.text_surf.get_rect(center=pos)
        self.pos = pos
        self.surf = pygame.surface.Surface((300, 100))
        self.surf.fill("red")
        self.rect = self.surf.get_rect(center=pos)


class Scene(ABC):

    @abstractmethod
    def render_scene(self, screen: pygame.Surface) -> None: ...

    @abstractmethod
    def handle_events(self, events: list[pygame.Event]) -> None | SceneName: ...
