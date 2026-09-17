"""Main menu scene used to navigate to gameplay and other screens."""

import sys
import time
from typing import Any
import pygame
from src.enums import Asset, DisplayInfo, SceneName
from src.models import AnimatedBar, Button, Scene, SceneTitle
from src.render import Renderer


class MainMenuScene(Scene):
    """Main menu allowing access to play, score, info, and exit actions."""

    def __init__(self) -> None:

        self.buttons: list[Button] = []

        self.button_idx = 0
        self.__init_elements()
        self.last_time = time.perf_counter()
        self.animated_bar = AnimatedBar(
            "powered by otahiri- and satifi", 200, 300
        )

    def __get_delta(self) -> float:
        """Return the elapsed time since the previous frame.

        Returns:
            Time delta in seconds used for the animated menu bar.
        """
        current_time = time.perf_counter()
        delta = current_time - self.last_time
        self.last_time = current_time
        return delta

    def __init_elements(self) -> None:
        """Build the logo, title and menu buttons for the main menu."""
        screen_width = DisplayInfo.SCREEN_WIDTH.value
        screen_height = DisplayInfo.SCREEN_HEIGHT.value
        self.logo = Renderer.load_image(f"{Asset.LOGO_PATH.value}.png")

        self.title = SceneTitle("main menu")

        x = screen_width // 2
        spacing = 120

        for i, label in enumerate(["play", "scores", "info", "exit"]):

            y = screen_height // 2 + spacing * i
            new_button = Button(label, (x, y))
            if i == 0:
                new_button.switch_state()
            self.buttons.append(new_button)

    def render_scene(self, renderer: Renderer) -> None:
        """Render the menu title, logo, buttons and animated bar.

        Args:
            renderer: Renderer used to draw menu components.
        """
        self.title.render(renderer)
        renderer.render(self.logo, (0, 300))
        for button in self.buttons:
            button.render(renderer)

        delta = self.__get_delta()
        self.animated_bar.render(renderer, delta)

    def __get_mouse_selected_button_idx(self) -> int | None:
        """Return the hovered menu button index, if any.

        Returns:
            The selected button index or `None` when the mouse is not over a
            button.
        """
        for i, button in enumerate(self.buttons):
            if button.is_collide(pygame.mouse.get_pos()):
                return i
        return None

    def __go_to_scene(self) -> dict[str, Any]:
        """Create the scene-navigation instructions
        for the current menu selection.

        Returns:
            A dictionary describing the next scene or action.
        """

        match self.button_idx:
            case 0:
                return {"next_scene": SceneName.GAME}
            case 1:
                return {"next_scene": SceneName.SCOREBOARD}
            case 2:
                return {"next_scene": SceneName.INFO}
            case 3:
                pygame.quit()
                sys.exit(0)
            case _:
                return {}

    def __handle_button_selection(self, direction: str) -> None:
        """Move the button menu up or down.

        Args:
            direction: Either "up" or "down" to change the active button.
        """
        self.buttons[self.button_idx].switch_state()
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
        self.buttons[self.button_idx].switch_state()

    def handle_events(self, events: list[pygame.Event]) -> dict[str, Any]:
        """Process keyboard and mouse events for the menu screen.

        Args:
            events: Pygame events received for the current frame.

        Returns:
            A dictionary with the exit instructions or an empty dict.
        """
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

                    self.buttons[self.button_idx].switch_state()
                    self.button_idx = new_button_idx
                    self.buttons[self.button_idx].switch_state()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                new_button_idx = self.__get_mouse_selected_button_idx()

                if new_button_idx is not None:
                    self.buttons[self.button_idx].switch_state()
                    self.button_idx = new_button_idx
                    self.buttons[self.button_idx].switch_state()

                    return self.__go_to_scene()

        return {}
