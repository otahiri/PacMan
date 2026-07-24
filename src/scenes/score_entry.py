import pygame
from src.enums import SceneName
from src.models import Scene, Text
from src.render import Renderer


class ScoreEntryScene(Scene):
    def __init__(self) -> None:
        print("initialize ScoreEntryScene")
        self.text = Text("score entry", (640, 640), "white")

    def render_scene(self, renderer: Renderer) -> None:
        renderer.render(
            self.text.surf,
            self.text.get_pos(),
        )

    def handle_events(self, events: list[pygame.Event]) -> None | SceneName:
        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                return SceneName.MAIN_MENU
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return SceneName.MAIN_MENU
