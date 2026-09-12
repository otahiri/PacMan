from typing import Any
import pygame
from src.enums import AnchorPoint, ColorType, DisplayInfo, SceneName
from src.models import Scene, SceneTitle, Text
from src.render import Renderer


class ScoreboardScene(Scene):

    def __init__(self, scores: dict[str, int]) -> None:

        self.scores_list: list[tuple[Text, Text]] = []
        self.scores = scores
        self.__init_elements()

    def __init_elements(self):

        screen_width = DisplayInfo.SCREEN_WIDTH.value
        screen_height = DisplayInfo.SCREEN_HEIGHT.value

        padding = 200
        i = 0
        for name, score in self.scores.items():

            y = screen_height // 3 + i * 80
            self.scores_list.append(
                (
                    Text(name, (padding, y), ColorType.PRIMARY),
                    Text(
                        str(score),
                        (screen_width - padding, y),
                        ColorType.PRIMARY,
                    ),
                )
            )
            i += 1

        self.title = SceneTitle("score board")

    def __repr__(self) -> str:
        return "ScoreboardScene"

    def render_scene(self, renderer: Renderer) -> None:
        self.title.render(renderer)
        for name, score in self.scores_list:
            renderer.render(
                name.surf,
                Renderer.get_pos(name.pos, name.size, AnchorPoint.CENTER_LEFT),
            )
            renderer.render(
                score.surf,
                Renderer.get_pos(
                    score.pos, score.size, AnchorPoint.CENTER_RIGHT
                ),
            )

    def handle_events(self, events: list[pygame.Event]) -> dict[str, Any]:
        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                return {"pop": True, "next_scene": SceneName.MAIN_MENU}
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return {"pop": True, "next_scene": SceneName.MAIN_MENU}
        return {}
