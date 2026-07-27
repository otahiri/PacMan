import pygame
from pygame.event import Event
from src import Player, Direction, Maze, Blinky, Pinky, Clyde, Inky, display
from src.enums import SceneName
from mazegenerator import MazeGenerator
from src.models import Scene
from src.render import Renderer


class GameScene(Scene):

    def __init__(self, screen_w: int, screen_h: int) -> None:
        self.logical_maze = MazeGenerator()
        scale = (
            screen_w // (self.logical_maze._height * 32 + 16),
            screen_h // (self.logical_maze._width * 32 + 16),
        )
        self.maze = Maze(screen_w, screen_h, self.logical_maze, scale)
        # self.player = Player(1, scale, self.maze.cell_grid)
        # self.blinky = Blinky(1, scale, self.maze.cell_grid, [self.player])
        # self.pinky = Pinky(1, scale, self.maze.cell_grid, [self.player])
        # self.clyde = Clyde(1, scale, self.maze.cell_grid, [self.player])
        # self.inky = Inky(
        #     1, scale, self.maze.cell_grid, [self.player, self.blinky]
        # )

        self.surf = self.maze.render_maze(scale)
        self.frame = 0

        self.running = True

    def render_scene(self, renderer: Renderer) -> None:
        # if renderer.is_window_changed():
        #     scale = (
        #         renderer.screen_w // (self.logical_maze._height * 32 + 16),
        #         renderer.screen_w // (self.logical_maze._width * 32 + 16),
        #     )
        #     self.maze = Maze(self.logical_maze, scale)
        #     self.player = Player(1, scale, self.maze.cell_grid)
        #     self.blinky = Blinky(1, scale, self.maze.cell_grid, [self.player])
        #     self.pinky = Pinky(1, scale, self.maze.cell_grid, [self.player])
        #     self.clyde = Clyde(1, scale, self.maze.cell_grid, [self.player])
        #     self.inky = Inky(
        #         1, scale, self.maze.cell_grid, [self.player, self.blinky]
        #     )

        #     self.surf = self.maze.render_maze(scale)
        # renderer.render(self.surf, self.maze.v_offset)
        renderer.render(
            self.surf,
            (renderer.screen_w, renderer.screen_h),
            (self.maze.max_x, self.maze.max_y),
            "center",
        )

        # renderer.render(*self.player.move(self.frame, self.maze.v_offset))
        # renderer.render(*self.blinky.move(self.frame, self.maze.v_offset))
        # renderer.render(*self.pinky.move(self.frame, self.maze.v_offset))
        # renderer.render(*self.clyde.move(self.frame, self.maze.v_offset))
        # renderer.render(*self.inky.move(self.frame, self.maze.v_offset))

    def handle_events(self, events: list[Event]) -> None | SceneName:
        self.frame = (self.frame + 1) % 60
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            # elif event.type == pygame.KEYDOWN:
            #     if event.key in [pygame.K_w, pygame.K_UP]:
            #         self.player.new_direction = Direction.NORTH
            #     elif event.key in [pygame.K_s, pygame.K_DOWN]:
            #         self.player.new_direction = Direction.SOUTH
            #     elif event.key in [pygame.K_d, pygame.K_RIGHT]:
            #         self.player.new_direction = Direction.EAST
            #     elif event.key in [pygame.K_a, pygame.K_LEFT]:
            #         self.player.new_direction = Direction.WEST
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return SceneName.SCORE_ENTRY
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return SceneName.SCORE_ENTRY
        return None
