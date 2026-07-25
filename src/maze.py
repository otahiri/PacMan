from typing import Any
import pygame
from mazegenerator import MazeGenerator

from src.enums import DisplayInfo


class Corner:
    """corner object to decide the look of the corner connecting walls

    Attributes:
        hex: hex value for the corner representing the sides it has
    """

    def __init__(self) -> None:
        """constructor of the Corner class"""
        self.hex = 0


class Cell:
    """cell class that has all the attributes of the cell

    Attributes:
        hex_value: the hex value of the cell representing which  walls are open
        top_left: top left corner
        top_right: top right corner
        bottom_left: bottom left corner
        bottom_right: bottom right corner
    """

    def __init__(self, hex: int, corners: list[Corner]) -> None:
        """constructor of the Cell class

        Args:
            hex: hex value of the cell
            corners: list of corners surrounding the cell
        """
        self.hex_value = hex
        self.content: Any = None
        self.top_left = corners[0]
        self.top_right = corners[1]
        self.bottom_left = corners[2]
        self.bottom_right = corners[3]
        self.update_corners()

    def update_corners(self) -> None:
        """mask the corner hex value according to the hex value of the cell
        top left corner will have an east side if the cell has a north wall
        and a south side if the cell has a west wall
        top right corner will have a west side if the cell has a north wall
        and a south side if the cell has an east wall
        bottom right corner will have north side if the cell has an east
        wall and a west side if the cell has a south wall
        bottom left corner  will have a north side if the cell has a west
        wall and an east side if the cell has a south wall
        """
        self.top_left.hex |= (1 & self.hex_value) << 1
        self.top_left.hex |= (8 & self.hex_value) >> 1
        self.top_right.hex |= (1 & self.hex_value) << 3
        self.top_right.hex |= (2 & self.hex_value) << 1
        self.bottom_right.hex |= (2 & self.hex_value) >> 1
        self.bottom_right.hex |= (4 & self.hex_value) << 1
        self.bottom_left.hex |= (4 & self.hex_value) >> 1
        self.bottom_left.hex |= (8 & self.hex_value) >> 3


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

    def __init__(self, maze: MazeGenerator) -> None:
        """maze constructor

        Args:
            maze: the maze object
            screen_size: the current screen size
        """
        asset_path = "assets/walls/"
        self.max_x = maze._width * 32
        self.max_y = maze._height * 32
        self.v_offset = (
            (DisplayInfo.SCREEN_WIDTH.value - self.max_x) // 2,
            (DisplayInfo.SCREEN_HEIGHT.value - self.max_x) // 2,
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
                    ],
                )
                for x in range(len(self.bit_maze[0]))
            ]
            for y in range(len(self.bit_maze))
        ]

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
                    self.corner_images[cell.top_left.hex], (cord_x, cord_y)
                )
                maze_surface.blit(
                    self.corner_images[cell.top_right.hex],
                    (cord_x + 32, cord_y),
                )
                maze_surface.blit(
                    self.corner_images[cell.bottom_left.hex],
                    (cord_x, cord_y + 32),
                )
                maze_surface.blit(
                    self.corner_images[cell.bottom_right.hex],
                    (cord_x + 32, cord_y + 32),
                )
                if cell.hex_value & 1:
                    maze_surface.blit(
                        self.wall_images[0], (cord_x + 16, cord_y)
                    )
                if cell.hex_value & 2:
                    maze_surface.blit(
                        self.wall_images[1], (cord_x + 32, cord_y + 16)
                    )
                if cell.hex_value & 4:
                    maze_surface.blit(
                        self.wall_images[0], (cord_x + 16, cord_y + 32)
                    )
                if cell.hex_value & 8:
                    maze_surface.blit(
                        self.wall_images[1], (cord_x, cord_y + 16)
                    )
        return maze_surface
