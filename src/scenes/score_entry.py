import pygame
from src.enums import SceneName
from src.models import Scene


class ScoreEntryScene(Scene):
    def __init__(self) -> None:
        f = pygame.font.Font(None, 100)
        self.surf = f.render("Score entry", True, "white")

    def render_scene(self, screen) -> None:
        screen.fill("black")
        screen.blit(self.surf, (0, 0))

    def handle_events(self, events: list[pygame.Event]) -> None | SceneName:
        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                return SceneName.MAIN_MENU
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return SceneName.MAIN_MENU
