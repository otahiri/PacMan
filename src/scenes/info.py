from typing import Any

import pygame

from src.enums import ColorType, DisplayInfo, SceneName
from src.models import Scene, Text
from src.render import Renderer


class InfoScene(Scene):
    def __init__(self) -> None:

        screen_width = DisplayInfo.SCREEN_WIDTH.value
        screen_height = DisplayInfo.SCREEN_HEIGHT.value

        self.text = Text(
            "instrucions",
            (
                DisplayInfo.SCREEN_WIDTH.value // 2,
                DisplayInfo.SCREEN_HEIGHT.value // 6,
            ),
            ColorType.PRIMARY,
        )

        self.body_text: list[Text] = []

        x = screen_width // 2
        y = screen_height // 2 - 300

        for text in [
            ("use arrow keys to navigait",),
            (
                "eat all gums to complete",
                "the level before the",
                "time ends with",
            ),
            ("getting touched by a ghost", "costs a life"),
            ("eat super gum to eat ghosts", "for a time"),
        ]:
            y += 80
            for line in text:
                y += 60
                self.body_text.append(
                    Text(
                        line,
                        (x, y),
                        ColorType.PRIMARY,
                    )
                )

    def __repr__(self) -> str:
        return "InfoScene"

    def render_scene(self, renderer: Renderer) -> None:
        renderer.render(
            self.text.surf, Renderer.get_pos(self.text.pos, self.text.size)
        )
        for text in self.body_text:
            renderer.render(
                text.surf,
                Renderer.get_pos(text.pos, text.size),
            )

    def handle_events(self, events: list[pygame.Event]) -> dict[str, Any]:
        for event in events:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return {"pop": True}
        return {}
