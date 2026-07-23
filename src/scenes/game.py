import pygame
from pygame.event import Event
from src import Player, Direction, Maze, Blinky, Pinky, Clyde, Inky
from src.enums import SceneName
from mazegenerator import MazeGenerator
from src.maze import Cell
from src.models import Scene


class GameScene(Scene):
    def __init__(self, width, height, screen: pygame.Surface) -> None:
        f = pygame.font.Font(None, 100)
        self.screen = screen
        self.logical_maze = MazeGenerator()
        self.maze = Maze(self.logical_maze, (width, height))
        self.player = Player(2, self.maze.cell_grid)
        self.blinky = Blinky(2, self.maze.cell_grid)
        self.pinky = Pinky(2, self.maze.cell_grid)
        self.clyde = Clyde(2, self.maze.cell_grid)

        self.inky = Inky(2, self.maze.cell_grid)

        self.surf = self.maze.render_maze()
        self.frame = 0
        self.erase = pygame.image.load("assets/player/empty_sprite.png")

        self.running = True

    def render_scene(self, screen) -> None:
        screen.fill("black")
        screen.blit(self.surf, self.maze.v_offset)
        self.player.move(screen, self.frame, self.maze.v_offset)
        self.blinky.move(screen, self.frame, self.maze.v_offset, [self.player])
        self.pinky.move(screen, self.frame, self.maze.v_offset, [self.player])
        self.clyde.move(screen, self.frame, self.maze.v_offset, [self.player])
        self.inky.move(
            screen, self.frame, self.maze.v_offset, [self.player, self.blinky]
        )
        for row in self.maze.cell_grid:
            for cell in row:
                if not cell.content:
                    x, y = cell.cord
                    screen.blit(self.erase, (x * 32 + 16 + self.maze.v_offset[0], y * 32 + 16 + self.maze.v_offset[1]))
                    if (x, y) == (self.player.bit_x, self.player.bit_y):
                        self.player.draw_player(screen, self.frame, self.maze.v_offset)


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
