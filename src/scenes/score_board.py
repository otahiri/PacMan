import pygame
from src.enums import DisplayInfo, SceneName
from src.models import Scene, Text
from src.render import Renderer


class ScoreboardScene(Scene):
    def __init__(self, scores: dict[str, str]) -> None:
        print("initialize ScoreboardScene")
        width = DisplayInfo.SCREEN_WIDTH.value
        height = DisplayInfo.SCREEN_HEIGHT.value

        self.text = Text("score board", (width // 2, height // 6), "white")

        self.scores: list[tuple[Text, Text]] = []
        i = 0
        padding = 200
        for name, score in scores.items():
            y = height // 3 + i * 80
            self.scores.append(
                (
                    Text(name, (padding, y), "white"),
                    Text(score, (width - padding, y), "white"),
                )
            )
            i += 1

    def render_scene(self, renderer: Renderer) -> None:
        renderer.render(
            self.text.surf, Renderer.get_pos(self.text.pos, self.text.size)
        )
        for name, score in self.scores:
            renderer.render(
                name.surf, Renderer.get_pos(name.pos, name.size, "leftcenter")
            )
            renderer.render(
                score.surf,
                Renderer.get_pos(score.pos, score.size, "rightcenter"),
            )

    def handle_events(self, events: list[pygame.Event]) -> None | SceneName:
        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                return SceneName.MAIN_MENU
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return SceneName.MAIN_MENU
