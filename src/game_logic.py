import numpy
from src.render import Renderer

from src import Player, Maze, Blinky, Pinky, Clyde, Inky
from src.enums import Direction, DisplayInfo
from mazegenerator import MazeGenerator
import pygame
from webcolors import name_to_hex


class GameLogic:
    def __init__(
        self,
        scale: int,
    ) -> None:
        self.scale = scale
        self.maze = Maze(MazeGenerator(), scale)
        self.v_offset = (
            (DisplayInfo.SCREEN_WIDTH.value - self.maze.max_x) // 2,
            (DisplayInfo.SCREEN_HEIGHT.value - self.maze.max_y) // 2,
        )
        self.player = Player(2, scale, self.maze.cell_grid)
        self.blinky = Blinky(1, scale, self.maze.cell_grid, [self.player])
        self.pinky = Pinky(1, scale, self.maze.cell_grid, [self.player])
        self.clyde = Clyde(1, scale, self.maze.cell_grid, [self.player])
        self.inky = Inky(
            1, scale, self.maze.cell_grid, [self.player, self.blinky]
        )
        self.working_surf = pygame.Surface(
            (
                self.maze.max_x + 16 * self.scale,
                self.maze.max_y + 16 * self.scale,
            )
        )


    def maze_engine(self, frame: int, new_move: Direction) -> pygame.Surface:
        self.player.new_direction = new_move
        Renderer.fill(self.working_surf, "black")
        Renderer.custom_blit(
            self.working_surf, self.maze.render_maze(self.scale), (0, 0)
        )
        Renderer.custom_blit(
            self.working_surf,
            self.player.move(frame),
            (self.player.v_x, self.player.v_y),
        )
        Renderer.custom_blit(self.working_surf, self.blinky.move(frame), (self.blinky.v_x, self.blinky.v_y))
        Renderer.custom_blit(self.working_surf, self.pinky.move(frame), (self.pinky.v_x, self.pinky.v_y))
        Renderer.custom_blit(self.working_surf, self.clyde.move(frame), (self.clyde.v_x, self.clyde.v_y))
        Renderer.custom_blit(self.working_surf, self.inky.move(frame), (self.inky.v_x, self.inky.v_y))
        return self.working_surf
