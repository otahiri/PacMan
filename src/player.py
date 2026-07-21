import pygame
from src import Cell
from enum import Enum


class Direction(Enum):
    """represent each direction the player can face

    Attributes:
        NORTH: north direction
        EAST: east direction
        SOUTH: south direction
        WEST: west direction
    """

    NORTH = (0, -1, 0)
    EAST = (1, 0, 1)
    SOUTH = (0, 1, 2)
    WEST = (-1, 0, 3)


class Player:
    """player class

    Attributes:
        maze: the cell grid representing the maze
        speed: the movement speed of the player
        max_y: the maximum y cord the player can reach
        max_x: the maximum x cord the player can reach
        v_x: the visual x cord of the player inside the cell grid
        v_y: the visual y cord of the player inside the cell grid
        bit_y: the y cord inside the bit maze
        bit_x: the x cord inside the bit maze
        new_direction: the new chosen direction from the player input
        direction: the direction the player is facing
        empty_sprite: the empty sprite for the player to remove the old frame
        sprites: the list of sprite of the player
        frame: the current frame that passed between 0 and 60
    """

    def __init__(self, cord_x: int, cord_y: int,
                 maze: list[list[Cell]]) -> None:
        """constructor

        Args:
            cord_x: the cord x inside the bit maze
            cord_y: the cord y inside the bit maze
            maze: the cell grid
        """
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
        """get the current sprite of the player

        Args:
            frame: the current frame the game reach between 0 and 60

        Returns:
            surface with player sprite loaded
        """
        animation = self.sprites[self.direction.value[2]][self.frame]
        if frame % 10 == 0:
            self.frame = int(not self.frame)
        return animation

    def move(
        self, screen: pygame.Surface, frame: int, v_offset: tuple
    ) -> pygame.Surface:
        """move the player accoding to direction

        Args:
            screen: the surface the player fraw itself on
            frame: the current frame
            v_offset: the visual offset to

        Returns:
            a surface with the player drawn on it
        """
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
        """draw the player on screen with a v_offset

        Args:
            screen: the screen to draw the player on
            frame: the current frame
            v_offset: the visual offset to draw the player on

        Returns:
            the screen with player loaded on it
        """
        screen.blit(
            self.get_sprite(frame),
            (self.v_x + v_offset[0], self.v_y + v_offset[1])
        )
        return screen
