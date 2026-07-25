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
        self.surf = self.maze.render_maze()
        self.player = Player(2, self.maze.cell_grid, self.surf)
        self.blinky = Blinky(1, self.maze.cell_grid, self.maze.v_offset)
        self.pinky = Pinky(1, self.maze.cell_grid, self.maze.v_offset)
        self.clyde = Clyde(1, self.maze.cell_grid, self.maze.v_offset)

        self.inky = Inky(1, self.maze.cell_grid, self.maze.v_offset)

        self.frame = 0
        self.erase = pygame.image.load("assets/player/empty_sprite.png")

        self.running = True

    def render_scene(self, screen) -> None:
        if self.player.dead:
            self.blinky.set_cords()
            self.inky.set_cords()
            self.pinky.set_cords()
            self.clyde.set_cords()
            self.player.set_cords()
            self.player.dead = False
            self.player.direction = Direction.NONE
            self.player.new_direction = Direction.NONE
            return
        screen.blit(self.surf, self.maze.v_offset)
        self.surf = self.player.move(screen, self.frame, self.maze.v_offset, self.maze)
        self.blinky.move(screen, self.frame, self.maze.v_offset, [self.player])
        self.pinky.move(screen, self.frame, self.maze.v_offset, [self.player])
        self.clyde.move(screen, self.frame, self.maze.v_offset, [self.player])
        self.inky.move(
            screen, self.frame, self.maze.v_offset, [self.player, self.blinky]
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
