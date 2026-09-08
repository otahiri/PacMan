from typing import Any

import pygame
import time
from pygame.event import Event
from src import Direction
from src.enums import Asset, DisplayInfo, SceneName
from mazegenerator import MazeGenerator
from src.models import Heart, Scene, Text
from src.render import Renderer
from src.game_logic import GameLogic


class GameScene(Scene):
    def __init__(self) -> None:

        scale = 2
        self.score = 0
        self.screen_w = DisplayInfo.SCREEN_WIDTH.value
        self.logical_maze = MazeGenerator()
        self.game_logic = GameLogic(scale)
        self.title_text = Text("score", (self.screen_w // 2, 10), False)
        self.score_text = Text(
            str(self.score), (self.screen_w // 2, 75), False
        )
        self.heart = Heart()
        self.last_time = time.perf_counter()

        self.running = True

    def __repr__(self) -> str:
        return "GameScene"

    def update_score(self) -> None:
        self.score_text = Text(
            str(self.score), (self.screen_w // 2, 75), False
        )

    def render_scene(self, renderer: Renderer) -> None:
        if self.score != self.game_logic.score:
            self.score = self.game_logic.score
            self.update_score()

        current_time = time.perf_counter()
        delta = current_time - self.last_time
        self.last_time = current_time

        renderer.render(
            self.game_logic.maze_engine(delta),
            self.game_logic.v_offset,
        )

        renderer.render(
            self.title_text.surf,
            Renderer.get_pos(
                self.title_text.pos, self.title_text.size, "topcenter"
            ),
        )
        renderer.render(
            self.score_text.surf,
            Renderer.get_pos(
                self.score_text.pos, self.score_text.size, "topcenter"
            ),
        )
        for i in range(self.game_logic.hearts):
            x = (Asset.HEART_WIDTH.value + 2) * i
            y = 0
            renderer.render(self.heart.surf, (x, y))

    def handle_events(self, events: list[Event]) -> dict[str, Any]:
        if self.game_logic.game_over:
            return {
                "pop": True,
                "next_scene": SceneName.SCORE_ENTRY,
                "score": self.score,
            }

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return {
                        "pop": True,
                        "next_scene": SceneName.SCORE_ENTRY,
                        "score": self.score,
                    }

                elif event.key in [pygame.K_w, pygame.K_UP]:
                    self.game_logic.new_move = Direction.NORTH
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    self.game_logic.new_move = Direction.SOUTH
                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    self.game_logic.new_move = Direction.EAST
                elif event.key in [pygame.K_a, pygame.K_LEFT]:
                    self.game_logic.new_move = Direction.WEST

            elif event.type == pygame.MOUSEBUTTONDOWN:
                return {
                    "pop": True,
                    "next_scene": SceneName.SCORE_ENTRY,
                    "score": self.score,
                }
        return {"pop": False, "next_scene": None}
