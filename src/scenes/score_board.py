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
            "sa3d": "12000",
            "oussama": "11000",
            "zakaria": "9000",
            "rami": "600",
        }
        self.scores: list[tuple[Text, Text]] = []
        i = 0
        space = 50
        for name, score in data.items():
            y = height // 2 + i * 100
            self.scores.append(
                (
                    Text(name, (640 - space, y), "white"),
                    Text(score, (640 + space, y), "white"),
                )
            )
            i += 1

    def render_scene(self, renderer: Renderer) -> None:
        renderer.render(
            self.text.surf,
            self.text.get_pos(),
        )
        for name, score in self.scores:
            renderer.render(name.surf, name.get_pos("rightcenter"))
            renderer.render(score.surf, score.get_pos("leftcenter"))

    def handle_events(self, events: list[pygame.Event]) -> None | SceneName:
        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                return SceneName.MAIN_MENU
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return SceneName.MAIN_MENU
