import pygame
import time
from pygame.event import Event
from src import Direction
from src.enums import Asset, DisplayInfo, SceneName
from mazegenerator import MazeGenerator
from src.models import Scene, Text
from src.render import Renderer
from src.game_logic import GameLogic


class GameScene(Scene):
    def __init__(self) -> None:

        scale = 2
        self.logical_maze = MazeGenerator()
        self.game_logic = GameLogic(scale)
        self.text_gui = []
        for i, label in enumerate(["score", f"{self.game_logic.score}"]):
            y = 75 * i
            self.text_gui.append(
                Text(label, (DisplayInfo.SCREEN_WIDTH.value // 2, y), "white")
            )
        self.heart_surf = Renderer.scale_surface(
            pygame.image.load("assets/hart.png"),
            (Asset.HEART_WIDTH.value, Asset.HEART_HEIGHT.value),
            5,
        )
        self.last_time = time.perf_counter()

        self.running = True

    def render_scene(self, renderer: Renderer) -> None:
        current_time = time.perf_counter()
        delta = current_time - self.last_time
        self.last_time = current_time

        renderer.render(
            self.game_logic.maze_engine(delta),
            self.game_logic.v_offset,
        )
        for text in self.text_gui:
            renderer.render(text.surf, text.get_pos("topcenter"))
        for i in range(self.game_logic.hearts):
            renderer.render(
                self.heart_surf,
                (
                    (Asset.HEART_WIDTH.value + 2) * 5 * i,
                    DisplayInfo.SCREEN_HEIGHT.value
                    - (Asset.HEART_HEIGHT.value * 5 + 5),
                ),
            )

    def handle_events(self, events: list[Event]) -> None | SceneName:
        if self.game_logic.game_over:
            return SceneName.SCORE_ENTRY

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return SceneName.SCORE_ENTRY
                elif event.key in [pygame.K_w, pygame.K_UP]:
                    self.game_logic.new_move = Direction.NORTH
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    self.game_logic.new_move = Direction.SOUTH
                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    self.game_logic.new_move = Direction.EAST
                elif event.key in [pygame.K_a, pygame.K_LEFT]:
                    self.game_logic.new_move = Direction.WEST

            elif event.type == pygame.MOUSEBUTTONDOWN:
                return SceneName.SCORE_ENTRY
        return None
