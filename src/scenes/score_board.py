import pygame
from src.enums import SceneName
from src.models import Scene


class ScoreboardScene(Scene):
    def __init__(self) -> None:
        f = pygame.font.Font(None, 100)
        self.surf = f.render("Score board", True, "white")

    def render_scene(self, screen) -> None:
        screen.blit(self.surf, (0, 0))

    def handle_events(self, events: list[pygame.Event]) -> None | SceneName:
        for event in events:

            if event.type != pygame.MOUSEBUTTONDOWN:
                continue
            return SceneName.MAIN_MENU
