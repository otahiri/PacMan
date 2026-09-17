"""Gameplay scene and pause-state logic.

This module contains the main game scene, including score/timer updates,
user input handling, pause controls, and scene transitions back to the
score-entry flow.
"""

from typing import Any
import pygame
import time
from pygame.event import Event
from src import Direction
from src.enums import AnchorPoint, Asset, ColorType, DisplayInfo, SceneName
from src.models import Button, Scene, SceneTitle, Text
from src.parsing import GameConfig
from src.render import Renderer
from src.game_logic import GameLogic


class GameScene(Scene):
    """Main game scene that owns gameplay, timers, and pause controls.

    Args:
        game_config: Parsed configuration for score and mode.
    """

    def __init__(self, game_config: GameConfig) -> None:

        self.game_config = game_config
        self.game_logic = GameLogic(game_config)

        self.game_over = False
        self.pause = False

        self.score = 0
        self.time_remaining = 0.0
        self.current_level = 10

        self.last_time = time.perf_counter()
        self.pause_buttons: list[Button] = []
        self.pause_button_idx = 0
        self.__init_elements()
        self.__set_timer()

    def __set_timer(self) -> None:
        """Set the timer according to the selected mode."""
        match self.game_config.mode:
            case "hardcore":
                self.time_remaining = 90
            case "normal":
                self.time_remaining = 120

    def __init_elements(self) -> None:
        """Build the HUD, pause buttons, labels, and other scene elements."""
        screen_width = DisplayInfo.SCREEN_WIDTH.value
        screen_height = DisplayInfo.SCREEN_HEIGHT.value

        for i, label in enumerate(["resume", "menu"]):

            new_button = Button(
                label, (200 + (screen_width - 400) * i, screen_height - 50)
            )

            if i == 0:
                new_button.switch_state()

            self.pause_buttons.append(new_button)

        self.pause_bar = SceneTitle("pause", "center")

        self.score_text = Text(
            "score",
            (screen_width // 2, 10),
            ColorType.PRIMARY,
            AnchorPoint.TOP_CENTER,
        )

        self.level_text = Text(
            f"level {self.game_logic.level}",
            (screen_width - 10, 10),
            ColorType.PRIMARY,
            AnchorPoint.TOP_RIGHT,
        )

        self.score_number = Text(
            str(self.score), (screen_width // 2, 100), ColorType.PRIMARY
        )
        self.time_text = Text(
            "time",
            (screen_width // 2, screen_height - 80),
            ColorType.PRIMARY,
            AnchorPoint.BOTTOM_CENTER,
        )

        self.time_value = Text(
            str(int(self.time_remaining)),
            (screen_width // 2, screen_height - 10),
            ColorType.PRIMARY,
            AnchorPoint.BOTTOM_CENTER,
        )

        self.heart = Renderer.load_image(f"{Asset.HEART_PATH.value}.png")

    def __get_delta(self) -> float:
        """Return the elapsed time since the last frame and refresh the timer.

        Returns:
            The time delta in seconds for the current frame update.
        """
        current_time = time.perf_counter()
        delta = current_time - self.last_time
        self.last_time = current_time
        return delta

    def __update_score(self) -> None:
        """Refresh the displayed score when the game logic has changed."""
        screen_width = DisplayInfo.SCREEN_WIDTH.value
        if self.score != self.game_logic.get_score():
            self.score = self.game_logic.get_score()
            self.score_number = Text(
                str(self.score), (screen_width // 2, 100), ColorType.PRIMARY
            )

    def __update_time(self, delta: float) -> None:
        """Advance the countdown timer unless
        the game is paused or in cheat mode.

        Args:
            delta: Elapsed time since the previous frame.
        """
        screen_width = DisplayInfo.SCREEN_WIDTH.value
        screen_height = DisplayInfo.SCREEN_HEIGHT.value

        if self.game_config.mode == "cheat" or self.pause:
            return

        self.time_remaining -= delta

        self.time_value = Text(
            str(int(self.time_remaining)),
            (screen_width // 2, screen_height - 10),
            ColorType.PRIMARY,
            AnchorPoint.BOTTOM_CENTER,
        )

    def __update_level(self) -> None:
        """Refresh the current level display when the game state changes."""
        screen_width = DisplayInfo.SCREEN_WIDTH.value

        if self.game_logic.level != self.current_level:
            self.current_level = self.game_logic.level

            self.level_text = Text(
                f"level {self.game_logic.level}",
                (screen_width - 10, 10),
                ColorType.PRIMARY,
                AnchorPoint.TOP_RIGHT,
            )

    def __render_text(self, renderer: Renderer) -> None:
        """Draw the HUD labels and score/time text.

        Args:
            renderer: Renderer instance used to blit the text.
        """
        if self.pause:
            self.pause_bar.render(renderer)
            for button in self.pause_buttons:
                button.render(renderer)

        renderer.render(
            self.level_text.surf,
            Renderer.get_pos(
                self.level_text.pos,
                self.level_text.size,
                self.level_text.anchor_point,
            ),
        )
        renderer.render(
            self.score_text.surf,
            Renderer.get_pos(
                self.score_text.pos,
                self.score_text.size,
                self.score_text.anchor_point,
            ),
        )
        renderer.render(
            self.score_number.surf,
            Renderer.get_pos(
                self.score_number.pos,
                self.score_number.size,
                self.score_number.anchor_point,
            ),
        )
        renderer.render(
            self.time_text.surf,
            Renderer.get_pos(
                self.time_text.pos,
                self.time_text.size,
                self.time_text.anchor_point,
            ),
        )

        renderer.render(
            self.time_value.surf,
            Renderer.get_pos(
                self.time_value.pos,
                self.time_value.size,
                self.time_value.anchor_point,
            ),
        )

    def __render_gui(self, renderer: Renderer, delta: float) -> None:
        """Update and draw the GUI panel for the current frame.

        Args:
            renderer: Renderer instance used for drawing.
            delta: Elapsed time in seconds since the last frame.
        """
        self.__update_time(delta)
        self.__render_text(renderer)
        self.__update_level()

        heart_width = Asset.HEART_WIDTH.value

        for i in range(self.game_logic.hearts):
            x = (heart_width + 2) * i
            y = 10
            renderer.render(self.heart, (x + 10, y))

    def render_scene(self, renderer: Renderer) -> None:
        """Render the game and GUI for the current frame.

        Args:
            renderer: Renderer used to draw the game scene.
        """
        if self.game_logic.reset_level:
            self.__set_timer()
            self.game_logic.reset_level = False

        self.__update_score()

        delta = self.__get_delta()

        renderer.render(
            self.game_logic.maze_engine(delta, self.pause),
            self.game_logic.v_offset,
        )
        self.__render_gui(renderer, delta)

    def __switch_pause_buttons(self) -> None:
        """Toggle the selected pause menu option between resume and menu."""
        self.pause_buttons[self.pause_button_idx].switch_state()
        self.pause_button_idx = 1 if self.pause_button_idx == 0 else 0
        self.pause_buttons[self.pause_button_idx].switch_state()

    def __handle_keydown(self, key: int) -> None:
        """Translate keyboard input into game movement or pause actions.

        Args:
            key: The key code produced by pygame.
        """
        if key in [pygame.K_w, pygame.K_UP]:
            self.game_logic.new_move = Direction.NORTH

        elif key in [pygame.K_s, pygame.K_DOWN]:
            self.game_logic.new_move = Direction.SOUTH

        elif key in [pygame.K_d, pygame.K_RIGHT]:
            if self.pause:
                self.__switch_pause_buttons()
            else:
                self.game_logic.new_move = Direction.EAST

        elif key in [pygame.K_a, pygame.K_LEFT]:
            if self.pause:
                self.__switch_pause_buttons()
            else:
                self.game_logic.new_move = Direction.WEST

        elif key in [pygame.K_n] and self.game_config.mode == "cheat":
            self.game_logic.maze_interface.gum_count = 0

        elif key in [pygame.K_ESCAPE]:
            self.pause = not self.pause

    def __leave_scene(self, scene: SceneName | None = None) -> dict[str, Any]:
        """Build a navigation that exits this scene.

        Args:
            scene: Optional destination scene to push after leaving.

        Returns:
            A dictionary with the exit instructions handled by `MainGame`.
        """
        return {
            "pop": True,
            "next_scene": scene,
            "score": self.score,
        }

    def handle_events(self, events: list[Event]) -> dict[str, Any]:
        """Process user input for movement, pause controls and mouse selection.

        Args:
            events: List of pygame events received for the current frame.

        Returns:
            A navigation instructions or empty dict if the scene stays active.
        """
        if self.game_logic.game_over:
            return self.__leave_scene(SceneName.SCORE_ENTRY)
        if self.time_remaining <= 0 and self.game_config.mode != "cheat":
            return self.__leave_scene(SceneName.SCORE_ENTRY)

        for event in events:

            if event.type == pygame.KEYDOWN:
                if self.pause:
                    if event.key == pygame.K_RETURN:
                        if self.pause_button_idx == 0:
                            self.pause = False
                        else:
                            return self.__leave_scene()

                self.__handle_keydown(event.key)

            elif event.type == pygame.MOUSEMOTION:
                if self.pause:
                    for i, button in enumerate(self.pause_buttons):
                        if button.is_collide(pygame.mouse.get_pos()):
                            if self.pause_button_idx != i:
                                self.__switch_pause_buttons()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self.pause:
                    return {}

                if self.pause_button_idx == 0:
                    self.pause = False
                else:
                    return self.__leave_scene()

        return {}
