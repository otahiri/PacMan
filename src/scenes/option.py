from typing import Any

import pygame
from src.enums import ColorType, SceneName
from src.models import Scene, Text
from src.render import Renderer


class OptionsScene(Scene):
    def __init__(self) -> None:
        self.text = Text("options", (640, 640), ColorType.PRIMARY)

    def __repr__(self) -> str:
        return "OptionsScene"

    def render_scene(self, renderer: Renderer) -> None:
        renderer.render(
            self.text.surf, Renderer.get_pos(self.text.pos, self.text.size)
        )

    def handle_events(self, events: list[pygame.Event]) -> dict[str, Any]:
        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                return {"pop": True, "next_scene": SceneName.MAIN_MENU}
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return {"pop": True, "next_scene": SceneName.MAIN_MENU}
        return {"pop": False, "next_scene": None}
