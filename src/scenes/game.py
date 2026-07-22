import pygame
from pygame.event import Event
from src import Player, Direction, Maze, Ghost
from src.enums import SceneName
from mazegenerator import MazeGenerator
from src.models import Scene


class GameScene(Scene):
    def __init__(self, width, height, screen: pygame.Surface) -> None:
        f = pygame.font.Font(None, 100)
        self.screen = screen
        self.logical_maze = MazeGenerator()
        self.maze = Maze(self.logical_maze, (width, height))
        self.player = Player(
            self.logical_maze._entryx,
            self.logical_maze._entryy,
            self.maze.cell_grid
        )
        self.ghost = Ghost(self.logical_maze._exitx, self.logical_maze._exity, self.maze.cell_grid)
        self.surf = self.maze.render_maze()
        self.frame = 0

        self.running = True

    def render_scene(self, screen) -> None:
        screen.blit(self.surf, self.maze.v_offset)
        self.player.move(screen, self.frame, self.maze.v_offset)
        self.ghost.move(screen, self.frame, self.maze.v_offset, self.player)

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
