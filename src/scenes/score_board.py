import pygame
from src.enums import DisplayInfo, SceneName
from src.models import Scene, Text
from src.render import Renderer


class ScoreboardScene(Scene):
    def __init__(self) -> None:
        print("initialize ScoreboardScene")
        width = DisplayInfo.SCREEN_WIDTH.value
        height = DisplayInfo.SCREEN_HEIGHT.value

        self.text = Text("score board", (width // 2, height // 4), "white")
        data = {
            "saad": 123043,
            "oussama": 116232,
        }
        self.scores = []
        i = 0
        for name, score in data.items():
            y = height // 2 + i * 100
            self.scores.append(
                Text(name, (width // 2, y), "white"),
            )
            i += 1

    def render_scene(self, renderer: Renderer) -> None:
        renderer.render(
            self.text.surf,
            self.text.pos,
        )
        for name in self.scores:
            renderer.render(name.surf, name.pos)

    def handle_events(self, events: list[pygame.Event]) -> None | SceneName:
        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                return SceneName.MAIN_MENU
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return SceneName.MAIN_MENU
