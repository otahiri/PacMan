import pygame
from src.enums import SceneName
from src.models import Scene, Text
from src.render import Renderer


class ScoreboardScene(Scene):
    def __init__(self) -> None:
        print("initialize ScoreboardScene")

        self.text = Text("score board", "white")
        data = {
            "sa3d": "12000",
            "oussama": "11000",
            "zakaria": "9000",
            "rami": "600",
        }
        self.scores: list[tuple[Text, Text]] = []
        for name, score in data.items():
            self.scores.append((Text(name, "white"), Text(score, "white")))

    def render_scene(self, renderer: Renderer) -> None:
        renderer.render(
            self.text.surf,
            (renderer.screen_w // 2, renderer.screen_h // 4),
            self.text.size,
        )
        i = 0
        spacing = 50
        for name, score in self.scores:
            y = renderer.screen_h // 2 + i * 100
            renderer.render(
                name.surf,
                (renderer.screen_w // 2 - spacing, y),
                name.size,
                "rightcenter",
            )
            renderer.render(
                score.surf,
                (renderer.screen_w // 2 + spacing, y),
                score.size,
                "leftcenter",
            )
            i += 1

    def handle_events(self, events: list[pygame.Event]) -> None | SceneName:
        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                return SceneName.MAIN_MENU
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return SceneName.MAIN_MENU
