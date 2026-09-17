"""Scoreboard scene showing the highest saved player scores."""

from typing import Any
import pygame
from src.enums import AnchorPoint, ColorType, DisplayInfo, SceneName
from src.models import Scene, SceneTitle, Text
from src.render import Renderer


class ScoreboardScene(Scene):
    """Scene that displays the top scored players in a leaderboard layout.

    Args:
        scores: Dict of players name and score value.
    """

    def __init__(self, scores: dict[str, int]) -> None:

        self.scores_list: list[tuple[Text, Text]] = []
        self.scores = scores
        self.__init_elements()

    def __init_elements(self) -> None:
        """Create the title and text rows used in the scoreboard display."""
        screen_width = DisplayInfo.SCREEN_WIDTH.value
        screen_height = DisplayInfo.SCREEN_HEIGHT.value

        padding = 150
        i = 0
        for name, score in self.scores.items():

            y = screen_height // 3 + i * 80
            self.scores_list.append(
                (
                    Text(
                        name,
                        (padding, y),
                        ColorType.PRIMARY,
                        AnchorPoint.CENTER_LEFT,
                    ),
                    Text(
                        str(score),
                        (screen_width - padding, y),
                        ColorType.PRIMARY,
                        AnchorPoint.CENTER_RIGHT,
                    ),
                )
            )
            i += 1

        self.title = SceneTitle("score board")

    def render_scene(self, renderer: Renderer) -> None:
        """Render the title and each name and score.

        Args:
            renderer: Renderer used to blit the scoreboard.
        """
        self.title.render(renderer)
        for name, score in self.scores_list:
            renderer.render(
                name.surf,
                Renderer.get_pos(name.pos, name.size, name.anchor_point),
            )
            renderer.render(
                score.surf,
                Renderer.get_pos(score.pos, score.size, score.anchor_point),
            )

    def handle_events(self, events: list[pygame.Event]) -> dict[str, Any]:
        """Handle close actions for the scoreboard.

        Args:
            events: Pygame events to inspect for exit input.

        Returns:
            A dictionary with `pop` action or an empty dict.
        """
        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return {"pop": True}
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return {"pop": True}

        return {}
