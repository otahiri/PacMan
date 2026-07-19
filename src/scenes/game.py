import pygame
from pygame.event import Event
from src import Player, Direction, Maze
from src.enums import SceneName
from mazegenerator import MazeGenerator
from src.models import Scene


class GameScene(Scene):
    def __init__(self, width, height, screen: pygame.Surface) -> None:
        f = pygame.font.Font(None, 100)
        self.screen = screen
        self.logical_maze = MazeGenerator()
        self.maze =  Maze(self.logical_maze, (width, height))
        self.player = Player(self.logical_maze._entryx, self.logical_maze._entryy, self.maze.cell_grid)
        self.surf = self.maze.render_maze()

        self.running = True

    def render_scene(self, screen) -> None:
        screen.blit(self.surf, (0, 0))

    def handle_events(self, events: list[Event]) -> None | SceneName:
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_UP]:
                    self.player.direction = Direction.NORTH
                    return None
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    self.player.direction = Direction.SOUTH
                    return None
                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    self.player.direction = Direction.EAST
                    return None
                elif event.key in [pygame.K_a, pygame.K_LEFT]:
                    self.player.direction = Direction.WEST
                    return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                return SceneName.SCORE_ENTRY
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return SceneName.SCORE_ENTRY
        return None
