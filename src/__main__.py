from enum import Enum
from os import setregid
import time
from typing import Any
import pygame
from mazegenerator.mazegenerator import MazeGenerator
from pygame.time import Clock


class Direction(Enum):
    NORTH = (0, -1, 0)
    EAST = (1, 0, 1)
    SOUTH = (0, 1, 2)
    WEST = (-1, 0, 3)


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

    def update_corners(self):
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


class Player:
    def __init__(
        self, cord_x: int, cord_y: int, maze: list[list[Cell]], v_offset: tuple
    ) -> None:
        self.v_offset = v_offset
        self.v_x = cord_x * 32 + v_offset[0] + 16
        self.v_y = cord_y * 32 + v_offset[1] + 16
        self.bit_y = cord_y
        self.bit_x = cord_x
        self.maze = maze
        self.max_y = (len(self.maze) * 32) + 400
        self.max_x = (len(self.maze[0]) * 32) + 400
        self.new_direction = Direction.NORTH
        self.direction = self.new_direction
        base_sprite_one = pygame.image.load("assets/player/pacman0.png")
        base_sprite_two = pygame.image.load("assets/player/pacman1.png")
        self.empty_sprite = pygame.image.load("assets/player/empty_sprite.png")
        self.sprites = [
            [
                pygame.transform.rotate(base_sprite_one, 90),
                pygame.transform.rotate(base_sprite_two, 90),
            ],
            [base_sprite_one, base_sprite_two],
            [
                pygame.transform.rotate(base_sprite_one, -90),
                pygame.transform.rotate(base_sprite_two, -90),
            ],
            [
                pygame.transform.rotate(base_sprite_one, -180),
                pygame.transform.rotate(base_sprite_two, -180),
            ],
        ]
        self.frame = 0

    def get_sprite(self, frame: int):
        animation = self.sprites[self.direction.value[2]][self.frame]
        if frame % 10 == 0:
            self.frame = int(not self.frame)
        return animation

    def move(self, screen: pygame.Surface, frame: int, speed: int):
        x, y = self.v_x, self.v_y
        is_centered = (x - 400) % 32 == 16 and (y - 400) % 32 == 16
        if is_centered:
            self.bit_y = (y - 400) // 32
            self.bit_x = (x - 400) // 32
            dx, dy, shift = self.new_direction.value
            if (1 << shift) & self.maze[self.bit_y][self.bit_x].hex_value == 0:
                self.direction = self.new_direction
        dx, dy, shift = self.direction.value
        can_move = False
        screen.blit(self.empty_sprite, (x, y))
        if is_centered:
            if (1 << shift) & self.maze[self.bit_y][self.bit_x].hex_value == 0:
                can_move = True
        else:
            can_move = True
        if can_move:
            new_x = (dx * speed) + x
            new_y = (dy * speed) + y
            if 0 <= new_y < self.max_y and 0 <= new_x < self.max_x:
                self.v_x = new_x
                self.v_y = new_y
        self.draw_player(screen, frame)

    def draw_player(self, screen: pygame.Surface, frame: int):
        screen.blit(self.get_sprite(frame), (self.v_x, self.v_y))
        pygame.display.update()


def draw_maze(
    maze: list[list[Cell]],
    corner_images: dict,
    wall_images: dict,
    screen: pygame.Surface,
):
    """rendering the map in pygame surface

    Args:
        maze: 2d array containing the cells
        corner_images: images of all possible corners pre-loaded
        wall_images: vertical and horzontal walls pre-loaded
        screen: surface of pygame
    """
    cord_y = 400
    for y in range(len(maze)):
        cord_x = 400
        for x in range(len(maze[0])):
            cell = maze[y][x]
            tl_corner = corner_images[cell.top_left.hex]
            screen.blit(tl_corner, (cord_x, cord_y))
            if cell.hex_value & 1:
                screen.blit(wall_images[0], (cord_x + 16, cord_y))
            tr_corner = corner_images[cell.top_right.hex]
            screen.blit(tr_corner, (cord_x + 32, cord_y))
            if cell.hex_value & 8:
                screen.blit(wall_images[1], (cord_x, cord_y + 16))
            if cell.hex_value & 2:
                screen.blit(wall_images[1], (cord_x + 32, cord_y + 16))
            bl_corner = corner_images[cell.bottom_left.hex]
            screen.blit(bl_corner, (cord_x, cord_y + 32))
            if cell.hex_value & 4:
                screen.blit(wall_images[0], (cord_x + 16, cord_y + 32))
            br_corner = corner_images[cell.bottom_right.hex]
            screen.blit(br_corner, (cord_x + 32, cord_y + 32))
            cord_x += 32
        cord_y += 32


def main():
    """main function"""
    pygame.init()
    asset_path = "assets/walls/"
    screen = pygame.display.set_mode((1400, 1400))
    maze = MazeGenerator()
    maze.generate()
    bit_maze = maze.maze
    corner_images = {}
    print(maze.maze)
    for i in range(16):
        corner_images[i] = pygame.image.load(f"{asset_path}{i}.png").convert_alpha()
    wall_images = {
        0: pygame.image.load(f"{asset_path}horizontanl_wall.png").convert_alpha(),
        1: pygame.image.load(f"{asset_path}vertical_wall.png").convert_alpha(),
    }
    corner_grid = [
        [Corner() for _ in range(len(bit_maze) + 1)] for _ in range(len(bit_maze) + 1)
    ]
    cell_grid = [
        [
            Cell(
                bit_maze[y][x],
                [
                    corner_grid[y][x],
                    corner_grid[y][x + 1],
                    corner_grid[y + 1][x],
                    corner_grid[y + 1][x + 1],
                ],
            )
            for x in range(len(bit_maze[0]))
        ]
        for y in range(len(bit_maze))
    ]
    player = Player(maze._entryx, maze._entryy, cell_grid, (400, 400))
    running = True
    frame = 0
    speed = 4
    screen.fill(pygame.Color(0, 0, 0))
    draw_maze(cell_grid, corner_images, wall_images, screen)
    pygame.display.update()
    player.draw_player(screen, frame)
    clock = pygame.time.Clock()
    while running:
        player.move(screen, frame, speed)
        pygame.display.update()
        for event in pygame.event.get():
            match event.type:

                case pygame.QUIT:
                    running = False
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_ESCAPE:
                            running = False
                        case pygame.K_UP | pygame.K_w:
                            player.new_direction = Direction.NORTH
                        case pygame.K_DOWN | pygame.K_s:
                            player.new_direction = Direction.SOUTH
                        case pygame.K_RIGHT | pygame.K_d:
                            player.new_direction = Direction.EAST
                        case pygame.K_LEFT | pygame.K_a:
                            player.new_direction = Direction.WEST
        clock.tick(1200)
        frame = (frame + 1) % 60


if __name__ == "__main__":
    main()
