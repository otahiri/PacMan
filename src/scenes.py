import pygame
from src.models import Button
from abc import ABC, abstractmethod


class Scene(ABC):

    @abstractmethod
    def render_scene(self, screen: pygame.Surface) -> None: ...


class MainMenuScene(Scene):
    def __init__(self) -> None:
        self.buttons = [
            Button(lable, (640, 150 * i + 640))
            for i, lable in enumerate(["Play", "Scores", "Exit"])
        ]

    def render_scene(self, screen) -> None:
        for button in self.buttons:
            screen.blit(button.surf, button.rect)
            screen.blit(button.text_surf, button.text_rect)


class ScoreboardScene(Scene):
    def __init__(self) -> None:
        f = pygame.font.Font(None, 100)
        self.surf = f.render("Score board", True, "white")

    def render_scene(self, screen) -> None:
        screen.blit(self.surf, (0, 0))


class GameScene(Scene):
    def __init__(self) -> None:
        f = pygame.font.Font(None, 100)
        self.surf = f.render("Game Here", True, "white")

    def render_scene(self, screen) -> None:
        screen.blit(self.surf, (0, 0))


class ScoreEntryScene(Scene):
    def __init__(self) -> None:
        f = pygame.font.Font(None, 100)
        self.surf = f.render("Score entry", True, "white")

    def render_scene(self, screen) -> None:
        screen.blit(self.surf, (0, 0))
