from typing import Any

import pygame
from src.enums import DisplayInfo, SceneName
from src.models import Scene, Text
from src.render import Renderer


class ScoreboardScene(Scene):
    def __init__(self) -> None:
        print("initialize ScoreboardScene")
        self.text = Text(
            "score board",
            (
                DisplayInfo.SCREEN_WIDTH.value // 2,
                DisplayInfo.SCREEN_HEIGHT.value // 6,
            ),
            "white",
        )

        self.scores: list[tuple[Text, Text]] = []

    def __set_scores(self, scores: dict[str, str]):

        self.scores.clear()
        padding = 200
        i = 0
        for name, score in scores.items():

            y = DisplayInfo.SCREEN_HEIGHT.value // 3 + i * 80
            self.scores.append(
                (
                    Text(name, (padding, y), "white"),
                    Text(
                        score,
                        (DisplayInfo.SCREEN_WIDTH.value - padding, y),
                        "white",
                    ),
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

    def get_scene_arguments(self, arguments: dict[str, Any]) -> None:
        scores = arguments.get("scores")
        if scores:
            self.__set_scores(scores)
            print("score updated")

    def handle_events(self, events: list[pygame.Event]) -> dict[str, Any]:
        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                return {"next_scene": SceneName.MAIN_MENU}
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return {"next_scene": SceneName.MAIN_MENU}
        return {"next_scene": None}
