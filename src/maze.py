from .gums import Gum, SuperGum
from typing import Any, Union
import pygame
from mazegenerator import MazeGenerator
from src.render import Renderer


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

    def __init__(
        self, bit_value: int, corners: list[Corner], content: Any, cord: tuple
    ) -> None:
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
        corner_images: every possible corner image
        maze: the object from the MazeGenerator model
        bit_maze: the bit maze from the maze
        wall_images: all possible wall images
        cell_grid: grid containing all cells
    """

    def __init__(self, maze: MazeGenerator, scale: int) -> None:
        """maze constructor

        Args:
            maze: the maze object
            screen_size: the current screen size
        """
        asset_path = "assets/walls/"
        self.scaled_v_step_y = 32 * scale
        self.scaled_v_step_x = 32 * scale
        self.scaled_half_v_step_y = 16 * scale
        self.scaled_half_v_step_x = 16 * scale
        self.max_x = maze._width * self.scaled_v_step_x
        self.max_y = maze._height * self.scaled_v_step_y
        self.corner_images: dict = {}
        self.maze = maze
        self.bit_maze = maze.maze
        for i in range(16):
            self.corner_images[i] = Renderer.scale_surface(
                pygame.image.load(f"{asset_path}{i}.png"), (16, 16), scale
            )
        self.wall_images = [
            Renderer.scale_surface(
                pygame.image.load(f"{asset_path}horizontanl_wall.png"),
                (16, 16),
                scale,
            ),
            Renderer.scale_surface(
                pygame.image.load(f"{asset_path}vertical_wall.png"),
                (16, 16),
                scale,
            ),
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
                    None,
                    (x, y),
                )
                for x in range(len(self.bit_maze[0]))
            ]
            for y in range(len(self.bit_maze))
        ]
        self.set_gums(scale)

    def get_gum(self, x: int, y: int) -> Union[Gum, SuperGum]:
        return self.cell_grid[y][x].content

    def set_gum(self, x: int, y: int) -> None:
        self.cell_grid[y][x].content = None

    def set_gums(self, scale) -> None:
        gum = Renderer.scale_surface(pygame.image.load("assets/gum.png"), (16, 16), scale)
        super_gum = Renderer.scale_surface(pygame.image.load("assets/super_gum.png"), (16,16), scale)
        max_y = self.maze._height - 1
        max_x = self.maze._width - 1
        corners = [(0, 0), (max_x, 0), (0, max_y), (max_x, max_y)]
        for y, row in enumerate(self.cell_grid):
            for x, cell in enumerate(row):
                if (x, y) == (max_x // 2, max_y // 2):
                    continue
                if cell.bit_value != 15:
                    cell.content = (
                        Gum(10, cell.cord, gum)
                        if cell.cord not in corners
                        else SuperGum(100, cell.cord, super_gum)
                    )

    def render_maze(self, scale: int) -> pygame.Surface:
        """render the maze into a pygame surface

        Returns:
            surface with maze rendered on it
        """
        height = (
            self.maze._height * self.scaled_v_step_y
        ) + self.scaled_v_step_y
        width = (
            self.maze._width * self.scaled_v_step_x
        ) + self.scaled_v_step_x
        maze_surface = pygame.Surface((width, height))
        for y, row in enumerate(self.cell_grid):
            cord_y = y * self.scaled_v_step_y
            for x, cell in enumerate(row):
                cord_x = x * self.scaled_v_step_x
                Renderer.custom_blit(
                    maze_surface,
                    self.corner_images[cell.top_left.bit],
                    (cord_x, cord_y),
                )
                Renderer.custom_blit(
                    maze_surface,
                    self.corner_images[cell.top_right.bit],
                    (cord_x + self.scaled_v_step_x, cord_y),
                )
                Renderer.custom_blit(
                    maze_surface,
                    self.corner_images[cell.bottom_left.bit],
                    (cord_x, cord_y + self.scaled_v_step_y),
                )
                Renderer.custom_blit(
                    maze_surface,
                    self.corner_images[cell.bottom_right.bit],
                    (
                        cord_x + self.scaled_v_step_x,
                        cord_y + self.scaled_v_step_y,
                    ),
                )
                if cell.bit_value & 1:
                    Renderer.custom_blit(
                        maze_surface,
                        self.wall_images[0],
                        (cord_x + self.scaled_half_v_step_x, cord_y),
                    )
                if cell.bit_value & 2:
                    Renderer.custom_blit(
                        maze_surface,
                        self.wall_images[1],
                        (
                            cord_x + self.scaled_v_step_x,
                            cord_y + self.scaled_half_v_step_y,
                        ),
                    )
                if cell.bit_value & 4:
                    Renderer.custom_blit(
                        maze_surface,
                        self.wall_images[0],
                        (
                            cord_x + self.scaled_half_v_step_x,
                            cord_y + self.scaled_v_step_y,
                        ),
                    )
                if cell.bit_value & 8:
                    Renderer.custom_blit(
                        maze_surface,
                        self.wall_images[1],
                        (cord_x, cord_y + self.scaled_half_v_step_x),
                    )
        return maze_surface

    def load_gums(self, maze_surface) -> None:
        for y, row in enumerate(self.cell_grid):
            cord_y = y * self.scaled_v_step_y
            for x, cell in enumerate(row):
                cord_x = x * self.scaled_v_step_x
                if cell.content:
                    Renderer.custom_blit(
                        maze_surface,
                        cell.content.sprite,
                        (
                            cord_x + self.scaled_half_v_step_x,
                            cord_y + self.scaled_half_v_step_y,
                        ),
                    )
