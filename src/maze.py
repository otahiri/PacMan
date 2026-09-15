"""the maze model responsible for anything related to the maze generation"""

import pygame
from src.enums import ColorType
from src.models import Gum, SuperGum, Cell, Corner
from mazegenerator import MazeGenerator
from src.render import Renderer


class MazeInterface:
    """maze class resposible for constructing the maze

    Attributes:
        v_step: one visual step
        half_v_step: half visual step
        max_x: maximum x a character can get to
        max_y: maximum y a character can get to
        maze: result from the MazeGenerator model
        bit_maze: list containing integer to show which wall is up
        corner_images: all possible corner sprite
        wall_images: vertical and horizontal walls
        cell_grid: list of all the cell of the maze
        gum_count: number of gums in the maze
    """

    def __init__(self) -> None:
        """
            maze object constructor
        Args:
            maze: maze object created by MazeGenerator
        """
        self.maze_generator = MazeGenerator(seed=67)
        asset_path = "assets/walls/"
        self.v_step = 64
        self.half_v_step = 32
        self.max_x = self.maze_generator._width * self.v_step
        self.max_y = self.maze_generator._height * self.v_step
        self.bit_maze = self.maze_generator.maze
        self.corner_images = {
            i: Renderer.load_image(f"{asset_path}{i}.png") for i in range(16)
        }
        self.wall_images = [
            Renderer.load_image(f"{asset_path}horizontanl_wall.png"),
            Renderer.load_image(f"{asset_path}vertical_wall.png"),
        ]
        self.cell_grid: list[list[Cell]] = []
        self.construct_grid()
        self.gum_count = 0
        self.set_maze_content()

    def get_gum_count(self) -> int:
        """return the number of gums left in the maze

        Returns:
            the count of gum
        """
        return self.gum_count

    def get_content(self, x: int, y: int) -> Gum | None:
        """get content of cell at x, y

        Args:
            x: x cord inside the grid
            y: y cord inside the grid

        Returns:
            content of the cell
        """
        return self.cell_grid[y][x].content

    def set_content(self, x: int, y: int) -> None:
        """set cell content

        Args:
            x: x cord inside the grid
            y: y cord inside the grid
        """
        self.cell_grid[y][x].content = None
        self.gum_count -= 1

    def set_maze_content(self) -> None:
        """set the content of each cell"""
        gum = Renderer.load_image("assets/gum.png")
        super_gum = Renderer.load_image("assets/super_gum.png")
        max_y = self.maze_generator._height - 1
        max_x = self.maze_generator._width - 1
        corners = [(0, 0), (max_x, 0), (0, max_y), (max_x, max_y)]
        for y, row in enumerate(self.cell_grid):
            for x, cell in enumerate(row):
                if (x, y) == (max_x // 2, max_y // 2):
                    continue
                if cell.bit_value != 15:
                    self.gum_count += 1
                    cell.content = (
                        Gum(10, cell.cord, gum)
                        if cell.cord not in corners
                        else SuperGum(100, cell.cord, super_gum)
                    )

    def construct_grid(self) -> None:
        """constructe the cell grind representing the maze"""
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

    def render_maze(self) -> pygame.Surface:
        """render the maze on a surface

        Returns:
            the result surface with maze on it
        """
        height = (self.maze_generator._height * self.v_step) + self.v_step
        width = (self.maze_generator._width * self.v_step) + self.v_step
        maze_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        Renderer.fill(maze_surface, ColorType.SECONDARY)
        for y, row in enumerate(self.cell_grid):
            cord_y = y * self.v_step
            for x, cell in enumerate(row):
                cord_x = x * self.v_step
                maze_surface.blit(
                    self.corner_images[cell.top_left.bit],
                    (cord_x, cord_y),
                )
                maze_surface.blit(
                    self.corner_images[cell.top_right.bit],
                    (cord_x + self.v_step, cord_y),
                )
                maze_surface.blit(
                    self.corner_images[cell.bottom_left.bit],
                    (cord_x, cord_y + self.v_step),
                )
                maze_surface.blit(
                    self.corner_images[cell.bottom_right.bit],
                    (
                        cord_x + self.v_step,
                        cord_y + self.v_step,
                    ),
                )
                if cell.bit_value & 1:
                    maze_surface.blit(
                        self.wall_images[0],
                        (cord_x + self.half_v_step, cord_y),
                    )
                if cell.bit_value & 2:
                    maze_surface.blit(
                        self.wall_images[1],
                        (
                            cord_x + self.v_step,
                            cord_y + self.half_v_step,
                        ),
                    )
                if cell.bit_value & 4:
                    maze_surface.blit(
                        self.wall_images[0],
                        (
                            cord_x + self.half_v_step,
                            cord_y + self.v_step,
                        ),
                    )
                if cell.bit_value & 8:
                    maze_surface.blit(
                        self.wall_images[1],
                        (cord_x, cord_y + self.half_v_step),
                    )
        return maze_surface

    def render_gums(self, maze_surface: pygame.Surface) -> None:
        """
        render gums on the maze surface
        Args:
            maze_surface: result maze surface
        """
        for y, row in enumerate(self.cell_grid):
            cord_y = y * self.v_step
            for x, cell in enumerate(row):
                cord_x = x * self.v_step
                if cell.content:
                    maze_surface.blit(
                        cell.content.sprite,
                        (
                            cord_x + self.half_v_step,
                            cord_y + self.half_v_step,
                        ),
                    )

    def reset_maze(self):
        """generate  new maze after level finish"""
        self.maze_generator.generate(-10)
        self.bit_maze = self.maze_generator.maze
        self.construct_grid()
        self.set_maze_content()
