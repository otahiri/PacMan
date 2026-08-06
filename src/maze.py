from src.models import Gum, SuperGum, Cell, Corner
from typing import Any, Union
import pygame
from mazegenerator import MazeGenerator
from src.render import Renderer


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

    def remove_gum(self, x: int, y: int) -> None:
        self.cell_grid[y][x].content = None

    def set_gums(self, scale) -> None:
        gum = Renderer.scale_surface(
            pygame.image.load("assets/gum.png"), (16, 16), scale
        )
        super_gum = Renderer.scale_surface(
            pygame.image.load("assets/super_gum.png"), (16, 16), scale
        )
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

    def load_gums(self, maze_surface) -> int:
        gum_count = 0
        for y, row in enumerate(self.cell_grid):
            cord_y = y * self.scaled_v_step_y
            for x, cell in enumerate(row):
                cord_x = x * self.scaled_v_step_x
                if cell.content:
                    gum_count += 1
                    Renderer.custom_blit(
                        maze_surface,
                        cell.content.sprite,
                        (
                            cord_x + self.scaled_half_v_step_x,
                            cord_y + self.scaled_half_v_step_y,
                        ),
                    )
        return gum_count
