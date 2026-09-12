import pygame
from src.enums import ColorType
from src.models import Gum, SuperGum, Cell, Corner
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

    def __init__(self, maze: MazeGenerator) -> None:
        """maze constructor

        Args:
            maze: the maze object
            screen_size: the current screen size
        """
        asset_path = "assets/walls/"
        self.v_step = 64
        self.half_v_step = 32
        self.max_x = maze._width * self.v_step
        self.max_y = maze._height * self.v_step
        self.maze = maze
        self.bit_maze = maze.maze
        self.corner_images = {
            i: Renderer.load_image(f"{asset_path}{i}.png") for i in range(16)
        }
        self.wall_images = [
            Renderer.load_image(f"{asset_path}horizontanl_wall.png"),
            Renderer.load_image(f"{asset_path}vertical_wall.png"),
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
        self.gum_count = 0
        self.set_gums()

    def get_gum_count(self) -> int:
        return self.gum_count

    def get_gum(self, x: int, y: int) -> Gum | SuperGum | None:
        return self.cell_grid[y][x].content

    def set_gum(self, x: int, y: int) -> None:
        self.cell_grid[y][x].content = None
        self.gum_count -= 1

    def set_gums(self) -> None:
        gum = Renderer.load_image("assets/gum.png")
        super_gum = Renderer.load_image("assets/super_gum.png")
        max_y = self.maze._height - 1
        max_x = self.maze._width - 1
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

    def render_maze(self) -> pygame.Surface:
        """render the maze into a pygame surface

        Returns:
            surface with maze rendered on it
        """
        height = (self.maze._height * self.v_step) + self.v_step
        width = (self.maze._width * self.v_step) + self.v_step
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

    def load_gums(self, maze_surface: pygame.Surface) -> None:
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
