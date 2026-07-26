from src.enums import Direction
from src.models import Character
from src import Cell
import pygame

from src.render import Renderer


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

    def __init__(
        self, speed: int, scale: tuple[int, int], maze: list[list[Cell]]
    ) -> None:
        """constructor

        Args:
            cord_x: the cord x inside the bit maze
            cord_y: the cord y inside the bit maze
            maze: the cell grid
        """
        self.maze = maze
        self.scaled_v_step_y = 32 * scale[1]
        self.scaled_v_step_x = 32 * scale[0]
        self.scaled_half_v_step_y = 16 * scale[1]
        self.scaled_half_v_step_x = 16 * scale[0]
        self.speed = speed
        self.scale = scale
        self.max_y = len(self.maze) * self.scaled_v_step_y
        self.max_x = len(self.maze[0]) * self.scaled_v_step_x
        self.set_cords()
        self.new_direction = Direction.NORTH
        self.direction = self.new_direction
        # remember to change the dimensions of the sprite to 16 , 16 later after fixing the image dimensions
        base_sprite_one = Renderer.scale_surface(
            pygame.image.load("assets/player/pacman0.png"), (15, 15), scale
        )
        base_sprite_two = Renderer.scale_surface(
            pygame.image.load("assets/player/pacman1.png"), (15, 15), scale
        )
        self.empty_sprite = Renderer.scale_surface(
            pygame.image.load("assets/player/empty_sprite.png"),
            (15, 15),
            scale,
        )
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

    def set_cords(self) -> None:
        cord_x = len(self.maze) // 2
        cord_y = len(self.maze[0]) // 2
        self.origin = (cord_x, cord_y)
        self.v_x = cord_x * self.scaled_v_step_x + self.scaled_half_v_step_x
        self.v_y = cord_y * self.scaled_v_step_y + self.scaled_half_v_step_y
        self.bit_y = cord_y
        self.bit_x = cord_x

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

    def choose_direction(self):
        self.bit_y = self.v_y // (self.scaled_v_step_y)
        self.bit_x = self.v_x // (self.scaled_v_step_x)
        dx, dy, shift = self.new_direction.value
        if (1 << shift) & self.maze[self.bit_y][self.bit_x].hex_value == 0:
            self.direction = (
                self.new_direction if not self.dead else self.direction
            )

    def check_movability(self, is_centered: bool) -> bool:
        can_move = False
        dx, dy, shift = self.direction.value
        if is_centered:
            if (1 << shift) & self.maze[self.bit_y][
                self.bit_x
            ].hex_value == 0 and not self.dead:
                can_move = True
        else:
            can_move = True

        return can_move

    def update_visual_cord(self):
        dx, dy, shift = self.direction.value
        min_x = 0
        min_y = 0
        max_x = self.max_x
        max_y = self.max_y
        new_x = ((dx * self.speed) * self.scale[0]) + self.v_x
        new_y = ((dy * self.speed) * self.scale[1]) + self.v_y
        if min_y <= new_y < max_y and min_x <= new_x < max_x:
            self.v_x = new_x
            self.v_y = new_y

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
        if self.dead:
            return (
                self.get_sprite(frame),
                (self.v_x + v_offset[0], self.v_y + v_offset[1]),
            )
        is_centered = (
            self.v_x % (self.scaled_v_step_x) == self.scaled_half_v_step_x
            and self.v_y % (self.scaled_v_step_y) == self.scaled_half_v_step_y
        )
        if is_centered:
            self.choose_direction()
        dx, dy, shift = self.direction.value
        if self.check_movability(is_centered):
            self.update_visual_cord()
        return (
            self.get_sprite(frame),
            (self.v_x + v_offset[0], self.v_y + v_offset[1]),
        )


class Blinky(Character):
    def __init__(
        self,
        speed: int,
        scale: tuple[int, int],
        maze: list[list[Cell]],
        anchors: list = [],
    ) -> None:
        """constructor

        Args:
            cord_x: the cord x inside the bit maze
            cord_y: the cord y inside the bit maze
            maze: the cell grid
        """
        self.origin = (0, 0)
        self.maze = maze
        self.speed = speed
        self.scaled_v_step_y = 32 * scale[1]
        self.scaled_v_step_x = 32 * scale[0]
        self.scaled_half_v_step_y = 16 * scale[1]
        self.scaled_half_v_step_x = 16 * scale[0]
        self.max_y = len(self.maze) * 32 * scale[1]
        self.max_x = len(self.maze[0]) * 32 * scale[0]
        self.new_direction = Direction.NORTH
        self.direction = self.new_direction
        self.scale = scale
        self.set_cords()
        self.player = anchors[0]
        base_sprite_one = Renderer.scale_surface(
            pygame.image.load("assets/player/pacman0.png"), (15, 15), scale
        )
        base_sprite_two = Renderer.scale_surface(
            pygame.image.load("assets/player/pacman1.png"), (15, 15), scale
        )
        self.empty_sprite = Renderer.scale_surface(
            pygame.image.load("assets/player/empty_sprite.png"),
            (15, 15),
            scale,
        )
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
        self.anchors: list = anchors

    def set_cords(self) -> None:
        x, y = self.origin
        self.v_x = x * self.scaled_v_step_x + self.scaled_half_v_step_x
        self.v_y = y * self.scaled_v_step_y + self.scaled_half_v_step_y
        self.bit_y = y
        self.bit_x = x

    def choose_target(self) -> tuple:
        return self.player.bit_x, self.player.bit_y

    def choose_direction(self):
        t_x, t_y = self.choose_target()
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

    def update_visual_cord(self):
        dx, dy, shift = self.direction.value
        min_x = 0
        min_y = 0
        max_x = self.max_x
        max_y = self.max_y
        new_x = ((dx * self.speed) * self.scale[0]) + self.v_x
        new_y = ((dy * self.speed) * self.scale[1]) + self.v_y
        if min_y <= new_y < max_y and min_x <= new_x < max_x:
            self.v_x = new_x
            self.v_y = new_y
            self.bit_x = self.v_x // (self.scaled_v_step_x)
            self.bit_y = self.v_y // (self.scaled_v_step_y)

    def check_movability(self, is_centered: bool) -> bool:
        can_move = False
        dx, dy, shift = self.direction.value
        if is_centered:
            if (1 << shift) & self.maze[self.bit_y][
                self.bit_x
            ].hex_value == 0 and not self.player.dead:
                can_move = True
        else:
            can_move = True

        return can_move

    def move(
        self,
        frame: int,
        v_offset: tuple,
    ) -> tuple[pygame.Surface, tuple[int, int]]:
        player = self.anchors[0]
        if (
            abs(self.v_x - player.v_x) < self.scaled_half_v_step_x
            and abs(self.v_y - player.v_y) < self.scaled_half_v_step_y
            and not player.dead
        ):
            player.dead = True
        is_centered = (
            self.v_x % (self.scaled_v_step_x) == self.scaled_half_v_step_x
            and self.v_y % (self.scaled_v_step_y) == self.scaled_half_v_step_y
        )
        if is_centered:
            self.choose_direction()
        dx, dy, shift = self.direction.value
        if self.check_movability(is_centered):
            self.update_visual_cord()
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
    def __init__(
        self,
        speed: int,
        scale: tuple[int, int],
        maze: list[list[Cell]],
        anchors: list,
    ) -> None:
        super().__init__(speed, scale, maze, anchors)
        self.origin = (0, len(maze[0]) - 1)
        self.set_cords()

    def choose_target(self) -> tuple:
        player = self.anchors[0]
        x = player.bit_x + (player.direction.value[0] * 4)
        y = player.bit_y + (player.direction.value[1] * 4)
        return x, y


class Clyde(Blinky):
    def __init__(
        self,
        speed: int,
        scale: tuple[int, int],
        maze: list[list[Cell]],
        anchors: list,
    ) -> None:
        super().__init__(speed, scale, maze, anchors)
        self.origin = (len(maze) - 1, len(maze[0]) - 1)
        self.set_cords()

    def choose_target(self) -> tuple:
        player = self.anchors[0]
        if abs(self.bit_x - player.bit_x) + abs(self.bit_y - player.bit_y) > 8:
            return (player.bit_x, player.bit_y)
        else:
            return (len(self.maze[0]) - 1, len(self.maze) - 1)


class Inky(Blinky):
    def __init__(
        self,
        speed: int,
        scale: tuple[int, int],
        maze: list[list[Cell]],
        anchors: list,
    ) -> None:
        super().__init__(speed, scale, maze, anchors)
        self.origin = (len(maze) - 1, 0)
        self.set_cords()

    def choose_target(self) -> tuple:
        player = self.anchors[0]
        blinky = self.anchors[1]
        blinky_x_distance = player.bit_x - blinky.bit_x
        blinky_y_distance = player.bit_y - blinky.bit_y
        return (
            player.bit_x + (player.direction.value[0] * 2) + blinky_x_distance,
            player.bit_y + (player.direction.value[1] * 2) + blinky_y_distance,
        )
