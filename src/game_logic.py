from src import Player, Maze, Blinky, Pinky, Clyde, Inky
from src.enums import Direction
from mazegenerator import MazeGenerator
import pygame


class GameLogic:

    def __init__(
        self,
        scale: int,
        screen_w: int,
        screen_h: int,
    ) -> None:
        self.scale = scale
        self.maze = Maze(MazeGenerator(), scale)
        self.v_offset = (
            (screen_w - self.maze.max_x) // 2,
            (screen_h - self.maze.max_y) // 2,
        )
        self.player = Player(2, scale, self.maze.cell_grid)
        self.blinky = Blinky(1, scale, self.maze.cell_grid, [self.player])
        self.pinky = Pinky(1, scale, self.maze.cell_grid, [self.player])
        self.clyde = Clyde(1, scale, self.maze.cell_grid, [self.player])
        self.inky = Inky(
            1, scale, self.maze.cell_grid, [self.player, self.blinky]
        )
        self.maze_surf = self.maze.render_maze(scale).convert_alpha()
        self.working_surf = pygame.Surface(
            (
                self.maze.max_x + 16 * self.scale,
                self.maze.max_y + 16 * self.scale,
            )
        )

    def maze_engine(self, frame: int, new_move: Direction) -> pygame.Surface:
        self.player.new_direction = new_move
        self.working_surf.fill("black")
        self.working_surf.blit(self.maze_surf, (0, 0))
        self.working_surf.blit(
            self.player.move(frame), (self.player.v_x, self.player.v_y)
        )
        self.working_surf.blit(
            self.blinky.move(frame), (self.blinky.v_x, self.blinky.v_y)
        )
        self.working_surf.blit(
            self.pinky.move(frame), (self.pinky.v_x, self.pinky.v_y)
        )
        self.working_surf.blit(
            self.clyde.move(frame), (self.clyde.v_x, self.clyde.v_y)
        )
        self.working_surf.blit(
            self.inky.move(frame), (self.inky.v_x, self.inky.v_y)
        )
        return self.working_surf
