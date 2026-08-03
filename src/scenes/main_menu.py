from typing import Any

import pygame
from src.enums import DisplayInfo, SceneName
from src.models import Scene
from src.models import Button
from src.render import Renderer


class MainMenuScene(Scene):
    def __init__(self) -> None:
        print("initialize MainMenuScene")

        self.buttons: list[Button] = []

        x = DisplayInfo.SCREEN_WIDTH.value // 2
        spacing = 120
        scale = 10

        for i, lable in enumerate(["play", "scores", "option", "exit"]):

            y = DisplayInfo.SCREEN_HEIGHT.value // 2 + spacing * i
            self.buttons.append(Button(lable, (x, y), scale))

        self.button_idx = 0

    def render_scene(self, renderer: Renderer) -> None:
        for i, button in enumerate(self.buttons):

            if self.button_idx == i:
                renderer.render(button.hover, button.pos)
            else:
                renderer.render(button.idel, button.pos)

            renderer.render(
                button.text.surf,
                Renderer.get_pos(button.text.pos, button.text.size),
            )

    def get_scene_arguments(self, arguments: dict[str, Any]) -> None: ...

    def handle_events(self, events: list[pygame.Event]) -> dict[str, Any]:

        for event in events:
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_UP:
                        if self.button_idx == 0:
                            self.button_idx = len(self.buttons) - 1
                        else:
                            self.button_idx -= 1

                    case pygame.K_DOWN:
                        if self.button_idx == len(self.buttons) - 1:
                            self.button_idx = 0
                        else:
                            self.button_idx += 1
                    case pygame.K_RETURN:
                        return self.__go_to_scene()

            elif event.type == pygame.MOUSEMOTION:

                for i, button in enumerate(self.buttons):
                    if button.is_collide(pygame.mouse.get_pos()):
                        self.button_idx = i

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return self.__go_to_scene()
        return {"next_scene": None}

    def __go_to_scene(self) -> dict[str, Any]:
        for i, button in enumerate(self.buttons):
            if i == self.button_idx:
                match button.name:
                    case "play":
                        return {"next_scene": SceneName.GAME}
                    case "scores":
                        return {"next_scene": SceneName.SCOREBOARD}
                    case "option":
                        return {"next_scene": SceneName.OPTIONS}
                    case "exit":
                        pygame.quit()
                        exit()
        return {"next_scene": None}
