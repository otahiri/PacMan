from typing import Any
import pygame
import time
from pygame.event import Event
from src import Direction
from src.enums import AnchorPoint, Asset, ColorType, DisplayInfo, SceneName
from src.models import Scene, SceneTitle, Text
from src.parsing import GameConfig
from src.render import Renderer
from src.game_logic import GameLogic


class GameScene(Scene):
    def __init__(self, game_config: GameConfig) -> None:

        self.game_config = game_config
        self.game_logic = GameLogic(game_config)

        self.game_over = False
        self.pause = False

        self.score = 0
        self.time_remaining = 1.0
        self.current_level = 10

        self.last_time = time.perf_counter()

        self.__init_elements()
        self.__set_timer()

    def __set_timer(self):

        match self.game_config.mode:
            case "hardcore":
                self.time_remaining = 90
            case "normal":
                self.time_remaining = 120

    def __init_elements(self):
        screen_width = DisplayInfo.SCREEN_WIDTH.value
        screen_height = DisplayInfo.SCREEN_HEIGHT.value

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

        self.heart = Renderer.change_color(
            pygame.image.load(f"{Asset.HEART_PATH.value}.png")
        )

    def __get_delta(self) -> float:

        current_time = time.perf_counter()
        delta = current_time - self.last_time
        self.last_time = current_time
        return delta

    def __repr__(self) -> str:
        return "GameScene"

    def __update_score(self) -> None:
        screen_width = DisplayInfo.SCREEN_WIDTH.value
        if self.score != self.game_logic.get_score():
            self.score = self.game_logic.get_score()
            self.score_number = Text(
                str(self.score), (screen_width // 2, 100), ColorType.PRIMARY
            )

    def __update_time(self, delta: float):
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

    def __update_level(self):
        screen_width = DisplayInfo.SCREEN_WIDTH.value

        if self.game_logic.level != self.current_level:
            self.current_level = self.game_logic.level

            self.level_text = Text(
                f"level {self.game_logic.level}",
                (screen_width - 10, 10),
                ColorType.PRIMARY,
                AnchorPoint.TOP_RIGHT,
            )

    def __render_text(self, renderer: Renderer):
        if self.pause:
            self.pause_bar.render(renderer)

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
        self.__update_time(delta)
        self.__render_text(renderer)
        self.__update_level()

        heart_width = Asset.HEART_WIDTH.value

        for i in range(self.game_logic.hearts):
            x = (heart_width + 2) * i
            y = 10
            renderer.render(self.heart, (x + 10, y))

    def render_scene(self, renderer: Renderer) -> None:
        if self.game_logic.reset_level:
            self.time_remaining = 200
            self.prev_time_remaining = 200
            self.game_logic.reset_level = False

        self.__update_score()

        delta = self.__get_delta()

        renderer.render(
            self.game_logic.maze_engine(delta, self.pause),
            self.game_logic.v_offset,
        )
        self.__render_gui(renderer, delta)

    def __handle_keydown(self, key: int) -> None:
        if key in [pygame.K_w, pygame.K_UP]:
            self.game_logic.new_move = Direction.NORTH

        elif key in [pygame.K_s, pygame.K_DOWN]:
            self.game_logic.new_move = Direction.SOUTH

        elif key in [pygame.K_d, pygame.K_RIGHT]:
            self.game_logic.new_move = Direction.EAST

        elif key in [pygame.K_a, pygame.K_LEFT]:
            self.game_logic.new_move = Direction.WEST

        elif key in [pygame.K_n] and self.game_config.mode == "cheat":
            self.game_logic.maze_interface.gum_count = 0
            self.__set_timer()

        elif key in [pygame.K_ESCAPE]:
            self.pause = not self.pause

    def __leave_scene(self) -> dict[str, Any]:
        return {
            "pop": True,
            "next_scene": SceneName.SCORE_ENTRY,
            "score": self.score,
        }

    def handle_events(self, events: list[Event]) -> dict[str, Any]:

        if self.game_logic.game_over:
            return self.__leave_scene()
        if self.time_remaining <= 0 and self.game_config.mode != "cheat":
            return self.__leave_scene()

        for event in events:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return self.__leave_scene()
                else:
                    self.__handle_keydown(event.key)

        return {}
