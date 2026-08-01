from os import stat
import random

from src.enums import Direction, PlayerState, GhostState
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
        self,
        speed: int,
        scale: int,
        maze: list[list[Cell]],
        anchors: list = [],
    ) -> None:
        """constructor

        Args:
            cord_x: the cord x inside the bit maze
            cord_y: the cord y inside the bit maze
            maze: the cell grid
        """
        super().__init__(
            speed,
            scale,
            (len(maze) // 2, len(maze[0]) // 2),
            maze,
            anchors,
        )
        self.lifes = 3
        self.power = -1
        cord_x = len(self.maze) // 2
        cord_y = len(self.maze[0]) // 2
        self.origin = (cord_x, cord_y)
        self.reset_cords()
        self.new_direction = Direction.NORTH
        self.direction = self.new_direction
        self.state = PlayerState.ALIVE
        self.sprites = [
            [
                Renderer.scale_surface(
                    pygame.image.load(
                        f"assets/player/alive/{d.name.lower()}/{i}.png"
                    ),
                    (16, 16),
                    scale,
                )
                for i in range(3)
            ]
            for d in Direction
            if d is not Direction.NONE
        ]
        self.death_animation = [
            [
                Renderer.scale_surface(
                    pygame.image.load(
                        f"assets/player/dead/{d.name.lower()}/{i}.png"
                    ),
                    (16, 16),
                    scale,
                )
                for i in range(9)
            ]
            for d in Direction
            if d is not Direction.NONE
        ]
        self.frame = 0
        self.death_frame = 0
        self.dead = False
        self.score = 0
        self.prev_sprite = self.get_sprite(0)
        self.hover = 2

    def reset_cords(self) -> None:
        self.v_x = (
            self.origin[0] * self.scaled_v_step_x + self.scaled_half_v_step_x
        )
        self.v_y = (
            self.origin[1] * self.scaled_v_step_y + self.scaled_half_v_step_y
        )
        self.bit_y = self.origin[1]
        self.bit_x = self.origin[0]

    def get_sprite(self, frame: int) -> pygame.Surface:
        """get the current sprite of the player

        Args:
            frame: the current frame the game reach between 0 and 60

        Returns:
            surface with player sprite loaded
        """
        if not self.dead:
            animation = self.sprites[self.direction.value[2]][self.frame]
            if frame % 10 == 0:
                self.frame = (self.frame + 1) % 3
        else:
            animation = self.death_animation[self.direction.value[2]][
                self.death_frame
            ]
            if frame % 10 == 0:
                self.death_frame += 1
        return animation

    def choose_direction(self):
        self.bit_y = self.v_y // (self.scaled_v_step_y)
        self.bit_x = self.v_x // (self.scaled_v_step_x)
        dx, dy, shift = self.new_direction.value
        if (1 << shift) & self.maze[self.bit_y][self.bit_x].bit_value == 0:
            self.direction = (
                self.new_direction if not self.dead else self.direction
            )

    def check_movability(self, is_centered: bool) -> bool:
        can_move = False
        dx, dy, shift = self.direction.value
        if is_centered:
            if (1 << shift) & self.maze[self.bit_y][
                self.bit_x
            ].bit_value == 0 and not self.dead:
                can_move = True
        else:
            can_move = True

        return can_move

    def update_visual_cord(self):
        dx, dy, shift = self.direction.value
        max_x = self.max_x
        max_y = self.max_y
        new_x = ((dx * self.speed) * self.scale) + self.v_x
        new_y = ((dy * self.speed) * self.scale) + self.v_y
        if 0 <= new_y < max_y and 0 <= new_x < max_x:
            self.v_x = new_x
            self.v_y = new_y

    def move(self, frame: int) -> pygame.Surface:
        """move the player accoding to direction

        Args:
            screen: the surface the player fraw itself on
            frame: the current frame
            v_offset: the visual offset to

        Returns:
            a surface with the player drawn on it
        """
        if self.dead:
            return self.get_sprite(frame)
        is_centered = (
            self.v_x % (self.scaled_v_step_x) == self.scaled_half_v_step_x
            and self.v_y % (self.scaled_v_step_y) == self.scaled_half_v_step_y
        )
        if is_centered:
            self.choose_direction()
        dx, dy, shift = self.direction.value
        if self.check_movability(is_centered):
            self.update_visual_cord()
        sprite = self.get_sprite(frame)
        self.prev_sprite = sprite
        return sprite


class Blinky(Character):
    def __init__(
        self,
        speed: int,
        scale: int,
        maze: list[list[Cell]],
        anchors: list = [],
    ) -> None:
        """constructor

        Args:
            cord_x: the cord x inside the bit maze
            cord_y: the cord y inside the bit maze
            maze: the cell grid
        """
        super().__init__(
            speed,
            scale,
            (0, 0),
            maze,
            anchors,
        )
        self.hover = 4
        self.steps = 2
        self.accumelated_steps = 0
        self.state = GhostState.CHASE
        self.power = 0
        self.new_direction = Direction.NORTH
        self.direction = self.new_direction
        self.scale = scale
        self.sprites = [
            [
                Renderer.scale_surface(
                    pygame.image.load(f"assets/mobs/{d.name.lower()}/{i}.png"),
                    (16, 16),
                    scale,
                )
                for i in range(4)
            ]
            for d in Direction
            if d is not Direction.NONE
        ]
        self.frightened_sprites = [
            Renderer.scale_surface(
                pygame.image.load(f"assets/mobs/frightened/{i}.png"),
                (16, 16),
                scale,
            )
            for i in range(4)
        ]
        self.reset_cords()
        self.player = anchors[0]
        self.frame = 0
        self.anchors: list = anchors
        self.prev_sprite = self.get_sprite(0)
        self.can_move = True

    def reset_cords(self):
        self.direction = Direction.NONE
        self.new_direction = Direction.NONE
        x, y = self.origin
        self.v_x = x * self.scaled_v_step_x + self.scaled_half_v_step_x
        self.v_y = y * self.scaled_v_step_y + self.scaled_half_v_step_y
        self.static_v_y = self.v_y
        self.bit_y = y
        self.bit_x = x

    def choose_target(self) -> tuple:
        target = (
            (self.player.bit_x, self.player.bit_y)
            if self.state == GhostState.CHASE
            else self.origin
        )
        return target

    def choose_direction(self):
        t_x, t_y = self.choose_target()
        possible_directions = []
        for direction in Direction:
            if direction.name == "NONE":
                continue
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
                    & self.maze[self.bit_y][self.bit_x].bit_value
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

    def panic_direction(self):
        possible_directions = [d for d in Direction if self.direction.value[0] != -d.value[0] and self.direction.value[1] != -d.value[1] and d != Direction.NONE]
        self.direction = random.choice(possible_directions)

    def update_visual_cord(self):
        dx, dy, shift = self.direction.value
        min_x = 0
        min_y = 0
        max_x = self.max_x
        max_y = self.max_y
        new_x = ((dx * self.speed) * self.scale) + self.v_x
        new_y = ((dy * self.speed) * self.scale) + self.static_v_y
        if min_y <= new_y < max_y and min_x <= new_x < max_x:
            self.v_x = new_x
            self.static_v_y = new_y
            self.v_y = self.static_v_y + self.accumelated_steps
            self.bit_x = self.v_x // (self.scaled_v_step_x)
            self.bit_y = self.static_v_y // (self.scaled_v_step_y)

    def check_movability(self, is_centered: bool) -> bool:
        can_move = False
        dx, dy, shift = self.direction.value
        if is_centered:
            if (1 << shift) & self.maze[self.bit_y][
                self.bit_x
            ].bit_value == 0 and not self.player.dead:
                can_move = True
        else:
            can_move = True
        return can_move

    def move(self, frame: int) -> pygame.Surface:
        if self.player.dead:
            return self.prev_sprite
        player = self.anchors[0]
        if (
            abs(self.v_x - player.v_x) < self.scaled_half_v_step_x
            and abs(self.static_v_y - player.v_y) < self.scaled_half_v_step_y
            and not player.dead
        ):
            player.dead = True
            player.state = PlayerState.DEAD
        is_centered = (
            self.v_x % (self.scaled_v_step_x) == self.scaled_half_v_step_x
            and (self.static_v_y) % (self.scaled_v_step_y)
            == self.scaled_half_v_step_y
        )
        if is_centered:
            if self.state == GhostState.FRIGHTENED:
                self.panic_direction()
            else:
                self.choose_direction()
        dx, dy, shift = self.direction.value
        if self.check_movability(is_centered):
            self.update_visual_cord()
        sprite = self.get_sprite(frame)
        self.prev_sprite = sprite
        return sprite

    def get_sprite(self, frame: int) -> pygame.Surface:
        """get the current sprite of the player

        Args:
            frame: the current frame the game reach between 0 and 60

        Returns:
            surface with player sprite loaded
        """
        sprite = self.frightened_sprites if self.state == GhostState.FRIGHTENED else self.sprites[self.direction.value[2]]
        animation = sprite[self.frame]
        if frame % 2 == 0:
            self.accumelated_steps += self.steps
            if self.accumelated_steps >= self.hover * self.scale:
                self.steps = -1
            elif self.accumelated_steps <= -self.hover * self.scale:
                self.steps = 1
        if frame % 10 == 0:
            self.frame = (self.frame + 1) % 4
        return animation


class Pinky(Blinky):
    def __init__(
        self,
        speed: int,
        scale: int,
        maze: list[list[Cell]],
        anchors: list,
    ) -> None:
        super().__init__(speed, scale, maze, anchors)
        self.origin = (0, len(maze[0]) - 1)
        self.reset_cords()

    def choose_target(self, ) -> tuple:
        player = self.anchors[0]
        x = player.bit_x + (player.direction.value[0] * 4)
        y = player.bit_y + (player.direction.value[1] * 4)
        target = (x, y) if self.state == GhostState.CHASE else self.origin
        return target


class Clyde(Blinky):
    def __init__(
        self,
        speed: int,
        scale: int,
        maze: list[list[Cell]],
        anchors: list,
    ) -> None:
        super().__init__(speed, scale, maze, anchors)
        self.origin = (len(maze) - 1, len(maze[0]) - 1)
        self.reset_cords()

    def choose_target(self, ) -> tuple:
        player = self.anchors[0]

        if (
            abs(self.bit_x - player.bit_x) + abs(self.bit_y - player.bit_y) > 8
            and self.state == GhostState.CHASE
        ):
            return (player.bit_x, player.bit_y)
        else:
            return self.origin


class Inky(Blinky):
    def __init__(
        self,
        speed: int,
        scale: int,
        maze: list[list[Cell]],
        anchors: list,
    ) -> None:
        super().__init__(speed, scale, maze, anchors)
        self.origin = (len(maze) - 1, 0)
        self.reset_cords()

    def choose_target(self, ) -> tuple:
        player = self.anchors[0]
        blinky = self.anchors[1]
        blinky_x_distance = player.bit_x - blinky.bit_x
        blinky_y_distance = player.bit_y - blinky.bit_y
        target = (
            (
                player.bit_x
                + (player.direction.value[0] * 2)
                + blinky_x_distance,
                player.bit_y
                + (player.direction.value[1] * 2)
                + blinky_y_distance,
            )
            if self.state == GhostState.CHASE
            else self.origin
        )
        return target
