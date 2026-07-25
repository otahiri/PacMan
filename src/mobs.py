from abc import ABC, abstractmethod
from src import Cell
import pygame

from src.enums import Direction


class Character(ABC):
    @abstractmethod
    def get_sprite(self, frame: int) -> pygame.Surface: ...


class Player(Character):
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

    def __init__(self, speed: int, maze: list[list[Cell]]) -> None:
        """constructor

        Args:
            cord_x: the cord x inside the bit maze
            cord_y: the cord y inside the bit maze
            maze: the cell grid
        """
        self.maze = maze
        cord_x = len(maze) // 2
        cord_y = len(maze[0]) // 2
        self.origin = (cord_x, cord_y)
        self.speed = speed
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
        self.dead = False
        self.death_time = 0

    def get_sprite(self, frame: int) -> pygame.Surface:
        """get the current sprite of the player

        Args:
            frame: the current frame the game reach between 0 and 60

        Returns:
            surface with player sprite loaded
        """
        animation = self.sprites[self.direction.value[2]][self.frame]
        if not self.dead:
            if frame % 10 == 0:
                self.frame = int(not self.frame)
        else:
            if frame % 10 == 0:
                if self.death_time < 10:
                    self.frame = int(not self.frame)
                    self.death_time += 1
        return animation

    def move(
        self, frame: int, v_offset: tuple
    ) -> tuple[pygame.Surface, tuple[int, int]]:
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
                self.direction = (
                    self.new_direction if not self.dead else self.direction
                )
        dx, dy, shift = self.direction.value
        can_move = False
        if is_centered:
            if (1 << shift) & self.maze[self.bit_y][
                self.bit_x
            ].hex_value == 0 and not self.dead:
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
        return (
            self.get_sprite(frame),
            (self.v_x + v_offset[0], self.v_y + v_offset[1]),
        )


class Blinky(Character):
    def __init__(self, speed: int, maze: list[list[Cell]]) -> None:
        """constructor

        Args:
            cord_x: the cord x inside the bit maze
            cord_y: the cord y inside the bit maze
            maze: the cell grid
        """
        self.origin = (0, 0)
        self.maze = maze
        self.set_cords()
        self.speed = speed
        self.max_y = len(self.maze) * 32
        self.max_x = len(self.maze[0]) * 32
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

    def set_cords(self) -> None:
        x, y = self.origin
        self.v_x = x * 32 + 16
        self.v_y = y * 32 + 16
        self.bit_y = y
        self.bit_x = x

    def choose_target(self, anchors: list) -> tuple:
        player = anchors.pop()
        return player.bit_x, player.bit_y

    def move(
        self,
        frame: int,
        v_offset: tuple,
        anchors: list,
    ) -> tuple[pygame.Surface, tuple[int, int]]:
        player = anchors[0]
        x, y = self.v_x, self.v_y
        if (
            abs(self.v_x - player.v_x) < 16
            and abs(self.v_y - player.v_y) < 16
            and not player.dead
        ):
            player.dead = True
            print("dead")
        is_centered = x % 32 == 16 and y % 32 == 16
        if is_centered:
            t_x, t_y = self.choose_target(anchors)
            possible_directions = []
            for direction in Direction:
                c_y = self.bit_y + direction.value[1]
                c_x = self.bit_x + direction.value[0]
                is_reverse = (
                    self.direction.value[0] == -direction.value[0]
                    and self.direction.value[1] == -direction.value[1]
                )
                if (
                    c_y < len(self.maze)
                    and c_x < len(self.maze[0])
                    and (
                        (1 << direction.value[2])
                        & self.maze[self.bit_y][self.bit_x].hex_value
                    )
                    == 0
                ):
                    possible_directions.append(
                        (
                            ((t_x - c_x) ** 2 + (t_y - c_y) ** 2),
                            direction,
                            is_reverse,
                        )
                    )

            if possible_directions:
                valid_direction = [d for d in possible_directions if not d[2]]
                if not valid_direction:
                    valid_direction = possible_directions
                valid_direction.sort(key=lambda x: x[0])
                self.direction = valid_direction[0][1]

        dx, dy, shift = self.direction.value
        can_move = False
        if is_centered:
            if (
                (1 << shift) & self.maze[self.bit_y][self.bit_x].hex_value
            ) == 0 and not player.dead:
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
                self.bit_x = self.v_x // 32
                self.bit_y = self.v_y // 32
        return (
            self.get_sprite(frame),
            (self.v_x + v_offset[0], self.v_y + v_offset[1]),
        )

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


class Pinky(Blinky):
    def __init__(self, speed: int, maze: list[list[Cell]]) -> None:
        super().__init__(speed, maze)
        self.origin = (0, len(maze[0]) - 1)
        self.set_cords()

    def choose_target(self, anchors: list) -> tuple:
        player = anchors.pop()
        x = player.bit_x + (player.direction.value[0] * 4)
        y = player.bit_y + (player.direction.value[1] * 4)
        return x, y


class Clyde(Blinky):
    def __init__(self, speed: int, maze: list[list[Cell]]) -> None:
        super().__init__(speed, maze)
        self.origin = (len(maze) - 1, len(maze[0]) - 1)
        self.set_cords()

    def choose_target(self, anchors: list) -> tuple:
        player = anchors.pop(0)
        if abs(self.bit_x - player.bit_x) + abs(self.bit_y - player.bit_y) > 8:
            return (player.bit_x, player.bit_y)
        else:
            return (len(self.maze[0]) - 1, len(self.maze) - 1)


class Inky(Blinky):
    def __init__(self, speed: int, maze: list[list[Cell]]) -> None:
        super().__init__(speed, maze)
        self.origin = (len(maze) - 1, 0)
        self.set_cords()

    def choose_target(self, anchors: list) -> tuple:
        player = anchors[0]
        blinky = anchors[1]
        blinky_x_distance = player.bit_x - blinky.bit_x
        blinky_y_distance = player.bit_y - blinky.bit_y
        return (
            player.bit_x + (player.direction.value[0] * 2) + blinky_x_distance,
            player.bit_y + (player.direction.value[1] * 2) + blinky_y_distance,
        )
