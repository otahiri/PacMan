import pygame
from src.models import Button
from abc import ABC, abstractmethod


class Scene(ABC):

    @abstractmethod
    def render_scene(self, screen: pygame.Surface) -> None: ...

    @abstractmethod
    def handle_events(self, events: list[pygame.Event]) -> None: ...


class MainMenuScene(Scene):
    def __init__(self) -> None:
        self.buttons = [
            Button(lable, (640, 150 * i + 640))
            for i, lable in enumerate(["Play", "Scores", "Exit"])
        ]

    def render_scene(self, screen) -> None:
        for button in self.buttons:
            is_sellected = button.rect.collidepoint(pygame.mouse.get_pos())
            thickness = 10
            if is_sellected:
                pygame.draw.rect(
                    screen,
                    "red",
                    button.rect.inflate(thickness * 2, thickness * 2),
                    thickness,
                )
            else:
                pygame.draw.rect(screen, "red", button.rect, 5)
            screen.blit(button.text_surf, button.text_rect)

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:

            if event.type != pygame.MOUSEBUTTONDOWN:
                continue

            for button in self.buttons:

                if not button.rect.collidepoint(pygame.mouse.get_pos()):
                    continue

                match button.name:
                    case "Play":
                        print("play")
                    case "Scores":
                        print("scores")
                    case "Exit":
                        pygame.quit()
                        exit()


class ScoreboardScene(Scene):
    def __init__(self) -> None:
        f = pygame.font.Font(None, 100)
        self.surf = f.render("Score board", True, "white")

    def render_scene(self, screen) -> None:
        screen.blit(self.surf, (0, 0))

    def handle_events(self, events: list[pygame.Event]) -> None: ...


class GameScene(Scene):
    def __init__(self) -> None:
        f = pygame.font.Font(None, 100)
        self.surf = f.render("Game Here", True, "white")

    def render_scene(self, screen) -> None:
        screen.blit(self.surf, (0, 0))

    def handle_events(self, events: list[pygame.Event]) -> None: ...


class ScoreEntryScene(Scene):
    def __init__(self) -> None:
        f = pygame.font.Font(None, 100)
        self.surf = f.render("Score entry", True, "white")

    def render_scene(self, screen) -> None:
        screen.blit(self.surf, (0, 0))

    def handle_events(self, events: list[pygame.Event]) -> None: ...
