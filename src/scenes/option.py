from typing import Any

import pygame
from src.enums import SceneName
from src.models import Scene, Text
from src.render import Renderer


class OptionsScene(Scene):
    def __init__(self) -> None:
        print("initialize OptionsScene")
        self.text = Text("options", (640, 640), "white")

    def render_scene(self, renderer: Renderer) -> None:
        renderer.render(
            self.text.surf, Renderer.get_pos(self.text.pos, self.text.size)
        )

    def get_scene_arguments(self, arguments: dict[str, Any]) -> None: ...

    def handle_events(self, events: list[pygame.Event]) -> dict[str, Any]:
        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                return {"next_scene": SceneName.MAIN_MENU}
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return {"next_scene": SceneName.MAIN_MENU}
        return {"next_scene": None}
