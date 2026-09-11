from typing import Any
import pygame
import time
import math
from pygame.event import Event
from src import Direction
from src.enums import Asset, ColorType, DisplayInfo, SceneName
from mazegenerator import MazeGenerator
from src.models import Scene, Text
from src.render import Renderer
from src.game_logic import GameLogic


class GameScene(Scene):
    def __init__(self) -> None:

        scale = 2
        self.score = 0

        self.logical_maze = MazeGenerator()
        self.game_logic = GameLogic(scale)
        self.last_time = time.perf_counter()
        self.text_elements: list[Text] = []
        self.time_remaining: float = 15
        self.prev_time_remaining: float = self.time_remaining
        self.time_text = Text(
            f"time {self.time_remaining}",
            (DisplayInfo.SCREEN_WIDTH.value - 10, 10),
            ColorType.PRIMARY,
            "top_right",
        )

        self.__init_elements()

    def __init_elements(self):
        screen_width = DisplayInfo.SCREEN_WIDTH.value
        self.text_elements.append(
            Text(
                "score",
                (screen_width // 2, 10),
                ColorType.PRIMARY,
                "topcenter",
            )
        )
        self.text_elements.append(
            Text(
                str(self.score),
                (screen_width // 2, 75),
                ColorType.PRIMARY,
                "topcenter",
            )
        )
        self.heart = Renderer.change_color(
            pygame.image.load(f"{Asset.HEART_PATH.value}.png")
        )
        self.timer_bar = Renderer.change_color(
            pygame.image.load("assets/cursor_wide.png")
        )

    def __get_delta(self) -> float:

        current_time = time.perf_counter()
        delta = current_time - self.last_time
        self.time_remaining -= delta
        if self.time_remaining < 0:
            self.game_logic.game_over = True
        self.last_time = current_time
        return delta

    def __repr__(self) -> str:
        return "GameScene"

    def update_score(self) -> None:
        screen_width = DisplayInfo.SCREEN_WIDTH.value
        if self.score != self.game_logic.score:
            self.score = self.game_logic.score
            self.score_text = Text(
                str(self.score), (screen_width // 2, 75), ColorType.PRIMARY
            )

    def update_time(self) -> None:
        screen_width = DisplayInfo.SCREEN_WIDTH.value
        self.time_text = Text(
            str(math.ceil(self.time_remaining)),
            (
                screen_width
                - (
                    len(str(math.ceil(self.time_remaining)))
                    * Asset.LETTER_WIDTH.value
                ),
                32,
            ),
            ColorType.PRIMARY,
        )

    def __render_gui(self, renderer: Renderer) -> None:

        if (self.time_remaining < self.prev_time_remaining):
            self.update_time()
            self.prev_time_remaining = self.time_remaining
        for text in self.text_elements:
            renderer.render(
                text.surf,
                Renderer.get_pos(text.pos, text.size, text.anchor_point),
            )
        renderer.render(
            self.time_text.surf,
            Renderer.get_pos(
                self.time_text.pos,
                self.time_text.size,
                self.time_text.anchor_point,
            ),
        )
        heart_width = Asset.HEART_WIDTH.value

        for i in range(self.game_logic.hearts):
            x = (heart_width + 2) * i
            y = 10
            renderer.render(self.heart, (x + 10, y))
        # fix me later
        renderer.render(
            self.timer_bar,
            Renderer.get_pos(
                (1280 // 2, 1280),
                (
                    Asset.CURSOR_WIDE_WIDTH.value,
                    Asset.CURSOR_WIDE_HEIGHT.value,
                ),
                "bottomcenter",
            ),
        )

    def render_scene(self, renderer: Renderer) -> None:

        self.update_score()

        delta = self.__get_delta()

        renderer.render(
            self.game_logic.maze_engine(delta),
            self.game_logic.v_offset,
        )
        self.__render_gui(renderer)

    def __handle_player_moves(self, key: int) -> None:
        if key in [pygame.K_w, pygame.K_UP]:
            self.game_logic.new_move = Direction.NORTH

        elif key in [pygame.K_s, pygame.K_DOWN]:
            self.game_logic.new_move = Direction.SOUTH

        elif key in [pygame.K_d, pygame.K_RIGHT]:
            self.game_logic.new_move = Direction.EAST

        elif key in [pygame.K_a, pygame.K_LEFT]:
            self.game_logic.new_move = Direction.WEST

    def __leave_scene(self) -> dict[str, Any]:
        return {
            "pop": True,
            "next_scene": SceneName.SCORE_ENTRY,
            "score": self.score,
        }

    def handle_events(self, events: list[Event]) -> dict[str, Any]:
        if self.game_logic.game_over:
            return self.__leave_scene()

        for event in events:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    return self.__leave_scene()

                else:
                    self.__handle_player_moves(event.key)

        return {}
