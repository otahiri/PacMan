import pygame
from pygame.event import Event
from src import Player, Direction, Maze, Blinky, Pinky, Clyde, Inky
from src.enums import SceneName
from mazegenerator import MazeGenerator
from src.models import Scene
from src.render import Renderer


class GameScene(Scene):
    def __init__(self, width, height, screen: pygame.Surface) -> None:
        self.screen = screen
        self.logical_maze = MazeGenerator()
        self.maze = Maze(self.logical_maze, (width, height))
        self.player = Player(2, self.maze.cell_grid)
        self.blinky = Blinky(1, self.maze.cell_grid)
        self.pinky = Pinky(1, self.maze.cell_grid)
        self.clyde = Clyde(1, self.maze.cell_grid)

        self.inky = Inky(1, self.maze.cell_grid)

        self.surf = self.maze.render_maze()
        self.frame = 0

        self.running = True

    def render_scene(self, renderer: Renderer) -> None:
        renderer.window.fill("black")
        renderer.window.blit(self.surf, self.maze.v_offset)
        self.player.move(renderer.window, self.frame, self.maze.v_offset)
        self.blinky.move(
            renderer.window, self.frame, self.maze.v_offset, [self.player]
        )
        self.pinky.move(
            renderer.window, self.frame, self.maze.v_offset, [self.player]
        )
        self.clyde.move(
            renderer.window, self.frame, self.maze.v_offset, [self.player]
        )
        self.inky.move(
            renderer.window,
            self.frame,
            self.maze.v_offset,
            [self.player, self.blinky],
        )

    def handle_events(self, events: list[Event]) -> None | SceneName:
        self.frame = (self.frame + 1) % 60
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_UP]:
                    self.player.new_direction = Direction.NORTH
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    self.player.new_direction = Direction.SOUTH
                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    self.player.new_direction = Direction.EAST
                elif event.key in [pygame.K_a, pygame.K_LEFT]:
                    self.player.new_direction = Direction.WEST
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return SceneName.SCORE_ENTRY
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return SceneName.SCORE_ENTRY
        return None
