from .gums import Gum, SuperGum
from typing import Any
import pygame
from mazegenerator import MazeGenerator


class Corner:
    """corner object to decide the look of the corner connecting walls

    Attributes:
        bit: bit value for the corner representing the sides it has
    """

    def __init__(self) -> None:
        """constructor of the Corner class"""
        self.bit = 0


class Cell:
    """cell class that has all the attributes of the cell

    Attributes:
        bit_value: the bit value of the cell representing which  walls are open
        top_left: top left corner
        top_right: top right corner
        bottom_left: bottom left corner
        bottom_right: bottom right corner
    """

    def __init__(self, bit_value: int, corners: list[Corner], content: Any, cord: tuple) -> None:
        """constructor of the Cell class

        Args:
            bit: bit value of the cell
            corners: list of corners surrounding the cell
        """
        self.bit_value = bit_value
        self.content: Any = None
        self.top_left = corners[0]
        self.top_right = corners[1]
        self.bottom_left = corners[2]
        self.bottom_right = corners[3]
        self.update_corners()
        self.content = content
        self.cord = cord

    def update_corners(self):
        """mask the corner bit value according to the bit value of the cell
        top left corner will have an east side if the cell has a north wall
        and a south side if the cell has a west wall
        top right corner will have a west side if the cell has a north wall
        and a south side if the cell has an east wall
        bottom right corner will have north side if the cell has an east
        wall and a west side if the cell has a south wall
        bottom left corner  will have a north side if the cell has a west
        wall and an east side if the cell has a south wall
        """
        self.top_left.bit |= (1 & self.bit_value) << 1
        self.top_left.bit |= (8 & self.bit_value) >> 1
        self.top_right.bit |= (1 & self.bit_value) << 3
        self.top_right.bit |= (2 & self.bit_value) << 1
        self.bottom_right.bit |= (2 & self.bit_value) >> 1
        self.bottom_right.bit |= (4 & self.bit_value) << 1
        self.bottom_left.bit |= (4 & self.bit_value) >> 1
        self.bottom_left.bit |= (8 & self.bit_value) >> 3


class Maze:
    """maze class containing all info about the map

    Attributes:
        max_x: the max x value of the maze
        max_y: the max y value of the maze
        v_offset: the visual offset to draw the maze to be in the center
        corner_images: every possible corner image
        maze: the object from the MazeGenerator model
        bit_maze: the bit maze from the maze
        wall_images: all possible wall images
        cell_grid: grid containing all cells
    """

    def __init__(self, maze: MazeGenerator, screen_size: tuple) -> None:
        """maze constructor

        Args:
            maze: the maze object
            screen_size: the current screen size
        """
        asset_path = "assets/walls/"
        self.max_x = maze._width * 32
        self.max_y = maze._height * 32
        self.v_offset = (
            (screen_size[0] - self.max_x) // 2,
            (screen_size[1] - self.max_x) // 2,
        )
        self.corner_images: dict = {}
        self.maze = maze
        self.bit_maze = maze.maze
        for i in range(16):
            self.corner_images[i] = pygame.image.load(
                f"{asset_path}{i}.png"
            ).convert_alpha()
        self.wall_images = [
            pygame.image.load(f"{asset_path}horizontanl_wall.png"),
            pygame.image.load(f"{asset_path}vertical_wall.png"),
        ]
        corner_grid = [
            [Corner() for _ in range(len(self.bit_maze) + 1)]
            for _ in range(len(self.bit_maze) + 1)
        ]
        self.cell_grid = [
            [
                Cell(
                    self.bit_maze[y][x],
                    [
                        corner_grid[y][x],
                        corner_grid[y][x + 1],
                        corner_grid[y + 1][x],
                        corner_grid[y + 1][x + 1],
                    ], None,
                    (x, y)
                )
                for x in range(len(self.bit_maze[0]))
            ]
            for y in range(len(self.bit_maze))
        ]
        self.set_gums()

    def set_gums(self) -> None:
        max_y = self.maze._height - 1
        max_x = self.maze._width - 1
        corners = [(0, 0), (max_x, 0), (0, max_y), (max_x, max_y)]
        for row in self.cell_grid:
            for cell in row:
                if cell.bit_value != 15:
                    gum = Gum(10, cell.cord) if cell.cord not in corners else SuperGum(100, cell.cord)
                    cell.content = gum

    def render_maze(self) -> pygame.Surface:
        """rendere the maze into a pygame surface

        Returns:
            surface with maze rendered on it
        """
        height = (self.maze._height * 32) + 32
        width = (self.maze._width * 32) + 32
        maze_surface = pygame.Surface((width, height))
        for y, row in enumerate(self.cell_grid):
            cord_y = y * 32
            for x, cell in enumerate(row):
                cord_x = x * 32
                maze_surface.blit(
                    self.corner_images[cell.top_left.bit], (cord_x, cord_y)
                )
                maze_surface.blit(
                    self.corner_images[cell.top_right.bit],
                    (cord_x + 32, cord_y)
                )
                maze_surface.blit(
                    self.corner_images[cell.bottom_left.bit],
                    (cord_x, cord_y + 32)
                )
                maze_surface.blit(
                    self.corner_images[cell.bottom_right.bit],
                    (cord_x + 32, cord_y + 32),
                )
                if cell.bit_value & 1:
                    maze_surface.blit(self.wall_images[0],
                                      (cord_x + 16, cord_y))
                if cell.bit_value & 2:
                    maze_surface.blit(self.wall_images[1],
                                      (cord_x + 32, cord_y + 16))
                if cell.bit_value & 4:
                    maze_surface.blit(self.wall_images[0],
                                      (cord_x + 16, cord_y + 32))
                if cell.bit_value & 8:
                    maze_surface.blit(self.wall_images[1],
                                      (cord_x, cord_y + 16))
                if cell.content:
                    maze_surface.blit(cell.content.sprite, (cord_x + 16, cord_y + 16))

        return maze_surface
