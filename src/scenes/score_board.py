import pygame
from src.enums import SceneName
from src.models import Scene


class ScoreboardScene(Scene):
    def __init__(self) -> None:
        print("initialize ScoreboardScene")

    def render_scene(self, renderer) -> None:
        # screen.blit(self.surf, (0, 0))
        pass

    def handle_events(self, events: list[pygame.Event]) -> None | SceneName:
        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                return SceneName.MAIN_MENU
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return SceneName.MAIN_MENU
