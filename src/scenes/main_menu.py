import time
from typing import Any
import pygame
from src.enums import DisplayInfo, SceneName
from src.models import AnimatedBar, Button, Scene
from src.render import Renderer


class MainMenuScene(Scene):
    def __init__(self) -> None:

        self.buttons: list[Button] = []

        self.button_idx = 0
        self.__init_elements()
        self.last_time = time.perf_counter()
        self.animated_bar = AnimatedBar(
            "powered by otahiri and satifi", 200, 300
        )

    def __get_delta(self) -> float:

        current_time = time.perf_counter()
        delta = current_time - self.last_time
        self.last_time = current_time
        return delta

    def __init_elements(self):

        screen_width = DisplayInfo.SCREEN_WIDTH.value
        screen_height = DisplayInfo.SCREEN_HEIGHT.value

        x = screen_width // 2
        spacing = 120

        for i, label in enumerate(["play", "scores", "exit"]):

            y = screen_height // 2 + spacing * i
            self.buttons.append(Button(label, (x, y)))

    def __repr__(self) -> str:
        return "MainMenuScene"

    def render_scene(self, renderer: Renderer) -> None:

        for i, button in enumerate(self.buttons):

            if self.button_idx == i:
                renderer.render(button.surf, button.pos)
                renderer.render(
                    button.text_on.surf,
                    Renderer.get_pos(button.text_on.pos, button.text_on.size),
                )
            else:
                renderer.render(
                    button.text_off.surf,
                    Renderer.get_pos(
                        button.text_off.pos, button.text_off.size
                    ),
                )

        delta = self.__get_delta()
        self.animated_bar.render(renderer, delta)

    def __get_mouse_selected_button_idx(self) -> int | None:
        for i, button in enumerate(self.buttons):
            if button.is_collide(pygame.mouse.get_pos()):
                return i

    def __go_to_scene(self) -> dict[str, Any]:

        match self.button_idx:
            case 0:
                return {"next_scene": SceneName.GAME}
            case 1:
                return {"next_scene": SceneName.SCOREBOARD}
            case 2:
                pygame.quit()
                exit()
            case _:
                return {}

    def __handle_button_selection(self, direction: str):
        match direction:
            case "up":
                if self.button_idx == 0:
                    self.button_idx = len(self.buttons) - 1
                else:
                    self.button_idx -= 1
            case "down":
                if self.button_idx == len(self.buttons) - 1:
                    self.button_idx = 0
                else:
                    self.button_idx += 1

    def handle_events(self, events: list[pygame.Event]) -> dict[str, Any]:

        for event in events:
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_UP:
                        self.__handle_button_selection("up")

                    case pygame.K_DOWN:
                        self.__handle_button_selection("down")

                    case pygame.K_RETURN:
                        return self.__go_to_scene()

            elif event.type == pygame.MOUSEMOTION:
                new_button_idx = self.__get_mouse_selected_button_idx()
                if new_button_idx is not None:
                    self.button_idx = new_button_idx

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                new_button_idx = self.__get_mouse_selected_button_idx()

                if new_button_idx is not None:
                    self.button_idx = new_button_idx
                    return self.__go_to_scene()

        return {}
