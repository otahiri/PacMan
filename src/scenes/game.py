import pygame
from pygame.event import Event
from src import Direction
from src.enums import DisplayInfo, SceneName
from mazegenerator import MazeGenerator
from src.models import Scene, Text
from src.render import Renderer
from src.game_logic import GameLogic


class GameScene(Scene):
    def __init__(self) -> None:

        scale = 2
        self.logical_maze = MazeGenerator()
        self.frame = 0
        self.game_logic = GameLogic(scale)
        self.new_move = Direction.NONE
        self.score = 112254
        self.text_gui = []
        for i, label in enumerate(["score", f"{self.score}"]):
            y = 75 * i
            self.text_gui.append(
                Text(label, (DisplayInfo.SCREEN_WIDTH.value // 2, y), "white")
            )
        self.running = True

    def render_scene(self, renderer: Renderer) -> None:
        renderer.render(
            self.game_logic.maze_engine(self.frame, self.new_move),
            self.game_logic.v_offset,
        )
        for text in self.text_gui:
            renderer.render(text.surf, text.get_pos("topcenter"))

    def handle_events(self, events: list[Event]) -> None | SceneName:
        self.frame = (self.frame + 1) % 60
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return SceneName.SCORE_ENTRY
                elif event.key in [pygame.K_w, pygame.K_UP]:
                    self.new_move = Direction.NORTH
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    self.new_move = Direction.SOUTH
                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    self.new_move = Direction.EAST
                elif event.key in [pygame.K_a, pygame.K_LEFT]:
                    self.new_move = Direction.WEST

            elif event.type == pygame.MOUSEBUTTONDOWN:
                return SceneName.SCORE_ENTRY
        return None
