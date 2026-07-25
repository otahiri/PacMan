import pygame
from src import Cell
from src.enums import Direction


class Player:
    def __init__(
        self, cord_x: int, cord_y: int, maze: list[list[Cell]]
    ) -> None:
        self.maze = maze
        self.speed = 2
        self.max_y = len(self.maze) * 32
        self.max_x = len(self.maze[0]) * 32
        self.v_x = cord_x * 32 + 16
        self.v_y = cord_y * 32 + 16
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

    def get_sprite(self, frame: int) -> pygame.Surface:
        animation = self.sprites[self.direction.value[2]][self.frame]
        if frame % 10 == 0:
            self.frame = int(not self.frame)
        return animation

    def move(
        self, screen: pygame.Surface, frame: int, v_offset: tuple
    ) -> pygame.Surface:
        x, y = self.v_x, self.v_y
        is_centered = x % 32 == 16 and y % 32 == 16
        if is_centered:
            self.bit_y = y // 32
            self.bit_x = x // 32
            dx, dy, shift = self.new_direction.value
            if (1 << shift) & self.maze[self.bit_y][self.bit_x].hex_value == 0:
                self.direction = self.new_direction
        dx, dy, shift = self.direction.value
        can_move = False
        if is_centered:
            if (1 << shift) & self.maze[self.bit_y][self.bit_x].hex_value == 0:
                can_move = True
        else:
            can_move = True
        if can_move:
            min_x = 0
            min_y = 0
            max_x = self.max_x
            max_y = self.max_y
            new_x = (dx * self.speed) + x
            new_y = (dy * self.speed) + y
            if min_y <= new_y < max_y and min_x <= new_x < max_x:
                self.v_x = new_x
                self.v_y = new_y
        return self.draw_player(screen, frame, v_offset)

    def draw_player(
        self, screen: pygame.Surface, frame: int, v_offset: tuple
    ) -> pygame.Surface:
        screen.blit(
            self.get_sprite(frame),
            (self.v_x + v_offset[0], self.v_y + v_offset[1]),
        )
        return screen
