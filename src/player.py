import pygame
from src import Cell
from enum import Enum


class Direction(Enum):
    NORTH = (0, -1, 0)
    EAST = (1, 0, 1)
    SOUTH = (0, 1, 2)
    WEST = (-1, 0, 3)


class Player:
    def __init__(
        self, cord_x: int, cord_y: int,
        maze: list[list[Cell]], v_offset: tuple
    ) -> None:
        self.maze = maze
        self.max_y = len(self.maze) * 32
        self.max_x = len(self.maze[0]) * 32
        self.v_offset = v_offset
        self.v_x = cord_x * 32 + self.v_offset[0] + 16
        self.v_y = cord_y * 32 + self.v_offset[1] + 16
        self.bit_y = cord_y
        self.bit_x = cord_x
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
        is_centered = (x - self.v_offset[0]) % 32 == 16 and (y - self.v_offset[1]) % 32 == 16
        if is_centered:
            self.bit_y = (y - self.v_offset[1]) // 32
            self.bit_x = (x - self.v_offset[0]) // 32
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
            min_x = self.v_offset[0]
            min_y = self.v_offset[1]
            max_x = self.v_offset[0] + self.max_x
            max_y = self.v_offset[1] + self.max_y
            new_x = (dx * speed) + x
            new_y = (dy * speed) + y
            if min_y <= new_y < max_y and min_x <= new_x < max_x:
                self.v_x = new_x
                self.v_y = new_y
        self.draw_player(screen, frame)

    def draw_player(self, screen: pygame.Surface, frame: int):
        screen.blit(self.get_sprite(frame), (self.v_x, self.v_y))
        pygame.display.update()
