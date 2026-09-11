from typing import Any

import pygame
from src.enums import ColorType, DisplayInfo, SceneName
from src.models import Scene, Text
from src.render import Renderer


class ScoreboardScene(Scene):

    def __init__(self, scores: dict[str, int]) -> None:
        self.text = Text(
            "score board",
            (
                DisplayInfo.SCREEN_WIDTH.value // 2,
                DisplayInfo.SCREEN_HEIGHT.value // 6,
            ),
            ColorType.PRIMARY,
        )
        self.scores: list[tuple[Text, Text]] = []

        padding = 200
        i = 0
        for name, score in scores.items():

            y = DisplayInfo.SCREEN_HEIGHT.value // 3 + i * 80
            self.scores.append(
                (
                    Text(name, (padding, y), ColorType.PRIMARY),
                    Text(
                        str(score),
                        (DisplayInfo.SCREEN_WIDTH.value - padding, y),
                        ColorType.PRIMARY,
                    ),
                )
            )
            i += 1

    def __repr__(self) -> str:
        return "ScoreboardScene"

    def render_scene(self, renderer: Renderer) -> None:
        renderer.render(
            self.text.surf, Renderer.get_pos(self.text.pos, self.text.size)
        )
        for name, score in self.scores:
            renderer.render(
                name.surf, Renderer.get_pos(name.pos, name.size, "center_left")
            )
            renderer.render(
                score.surf,
                Renderer.get_pos(score.pos, score.size, "center_right"),
            )

    def handle_events(self, events: list[pygame.Event]) -> dict[str, Any]:
        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                return {"pop": True, "next_scene": SceneName.MAIN_MENU}
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return {"pop": True, "next_scene": SceneName.MAIN_MENU}
        return {}
