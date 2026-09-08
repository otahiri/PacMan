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
        self.id = 0
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
                    pygame.image.load(f"assets/player/alive/{i}.png"),
                    (16, 16),
                    scale,
                )
                for i in range(6)
            ]
        ]
        self.death_animation = [
            [
                Renderer.scale_surface(
                    pygame.image.load(f"assets/player/dead/{i}.png"),
                    (16, 16),
                    scale,
                )
                for i in range(11)
            ]
        ]
        for i in range(3):
            self.sprites.append(
                [Renderer.rotate_surf(s, i + 1) for s in self.sprites[0]]
            )
            self.death_animation.append(
                [
                    Renderer.rotate_surf(s, i + 1)
                    for s in self.death_animation[0]
                ]
            )

        self.frame = 0
        self.death_frame = 0
        self.dead = False
        self.score = 0
        self.prev_sprite = self.get_sprite(0)
        self.hover = 2

    def die(self) -> None:
        self.state = PlayerState.DEAD
        self.dead = True

    def reset_cords(self) -> None:
        """reset the cordination to the original point of the character"""
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
            sprite = self.sprites[self.direction.value[2]]
            animation = sprite[self.frame]
            if frame % 5 == 0:
                self.frame = (self.frame + 1) % len(sprite)
        else:
            animation = self.death_animation[self.direction.value[2]][
                self.death_frame
            ]
            if frame % 5 == 0:
                self.death_frame += 1
        return animation

    def choose_direction(self) -> None:
        """choose the new direction"""
        self.bit_y = self.v_y // (self.scaled_v_step_y)
        self.bit_x = self.v_x // (self.scaled_v_step_x)
        dx, dy, shift = self.new_direction.value
        if (1 << shift) & self.maze[self.bit_y][self.bit_x].bit_value == 0:
            self.direction = (
                self.new_direction if not self.dead else self.direction
            )

    def check_movability(self, is_centered: bool) -> bool:
        """check if the character can move or not depending on the surrounding
        walls and if the character is in the center of a cell or not

        Args:
            is_centered: is the character in the middle  of the cell

        Returns:
            bool representing if the character can change direction or not
        """
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

    def update_visual_cord(self) -> None:
        """update the visual cords"""
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
            sprite = self.get_sprite(frame)
            self.prev_sprite = sprite
            return sprite
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
    """the friendly ghost blinky

    Attributes:
        hover: the bobbing distance when moving
        steps: the steps of the bobbing
        accumelated_steps: the total steps accumelated
        state: the current state of the ghost
        power: the power of the character
        direction: the direction the character is moving towards
        scale: the scale multiplier of the visual maze
        sprites: the normal sprites of the character
        frightened_sprites: the frightened sprites of the character
        player: the player
        frame: the current frame of the animation
        anchors: the anchors used to choose direction
        prev_sprite: the previous sprite
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
            cord_x: the cord x inside the logical maze
            cord_y: the cord y inside the logical maze
            maze: the cell grid
        """
        super().__init__(
            speed,
            scale,
            (0, 0),
            maze,
            anchors,
        )
        self.id = 1
        self.hover = 4
        self.steps = 2
        self.accumelated_steps = 0
        self.state = GhostState.CHASE
        self.power = 0
        self.direction = Direction.NONE
        self.scale = scale
        self.sprites = [
            [
                Renderer.scale_surface(
                    pygame.image.load(
                        f"assets/mobs/moving/{d.name.lower()}/{i}.png"
                    ),
                    (16, 16),
                    scale,
                )
                for i in range(4)
            ]
            for d in Direction
            if d is not Direction.NONE
        ]
        self.frightened_sprites = [
            [
                Renderer.scale_surface(
                    pygame.image.load(
                        f"assets/mobs/frightened/{d.name.lower()}/{i}.png"
                    ),
                    (16, 16),
                    scale,
                )
                for i in range(4)
            ]
            for d in Direction
            if d is not Direction.NONE
        ]
        self.dead_sprite = [
            Renderer.scale_surface(
                pygame.image.load(f"assets/mobs/dead/{i}.png"),
                (16, 16),
                self.scale,
            )
            for i in range(6)
        ]
        self.reset_cords()
        self.player = anchors[0]
        self.frame = 0
        self.anchors: list = anchors
        self.prev_sprite = self.get_sprite(0)
        self.death_frame = 0
        self.respawn_timer = 0

    def reset_cords(self) -> None:
        """reset the cords of character to the origin"""
        self.direction = Direction.NONE
        x, y = self.origin
        self.v_x = x * self.scaled_v_step_x + self.scaled_half_v_step_x
        self.v_y = y * self.scaled_v_step_y + self.scaled_half_v_step_y
        self.bit_y = y
        self.bit_x = x

    def choose_target(self) -> tuple:
        """get the cords the player tile if in chase mode else cords
        of the corner
        Returns:
            return the bit cord of the chosen target
        """
        target = (
            (self.player.bit_x, self.player.bit_y)
            if self.state == GhostState.CHASE
            else self.origin
        )
        return target

    def choose_direction(self) -> None:
        """choose a direction depending on the target"""
        if self.state == GhostState.DEAD:
            t_x, t_y = self.origin
        else:
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

    def panic_direction(self) -> None:
        """direction algo when the ghost is in panic mode"""
        possible_directions = []
        for d in Direction:
            if d == Direction.NONE:
                continue
            dx, dy, shift = d.value
            if self.maze[self.bit_y][self.bit_x].bit_value & 1 << shift == 0:
                possible_directions.append(d)
        valid_direction = [
            d
            for d in possible_directions
            if self.direction.value[0] != -d.value[0]
            or self.direction.value[1] != -d.value[1]
        ]
        if valid_direction:
            possible_directions = valid_direction
        self.direction = random.choice(possible_directions)

    def die(self) -> None:
        self.state = GhostState.DEAD

    def update_visual_cord(self) -> None:
        """change the visual cords"""
        dx, dy, shift = self.direction.value
        min_x = 0
        min_y = 0
        max_x = self.max_x
        max_y = self.max_y
        new_x = ((dx * self.speed) * self.scale) + self.v_x
        new_y = ((dy * self.speed) * self.scale) + self.v_y
        if min_y <= new_y < max_y and min_x <= new_x < max_x:
            self.v_x = new_x
            self.v_y = new_y
            self.bit_x = self.v_x // (self.scaled_v_step_x)
            self.bit_y = self.v_y // (self.scaled_v_step_y)

    def check_movability(self, is_centered: bool) -> bool:
        """check if the character can move

        Args:
            is_centered: is the character in the middle of a cell

        Returns:
            bool representing if it is possible to change direction
        """
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
        """move the character to a chosen direction if it is possible

        Args:
            frame: the current frame of the game

        Returns:
            the appropriate sprite for the current direction and the mode
        """
        if self.state == GhostState.DEAD:
            sprite = self.dead_sprite[self.death_frame]
            if frame % 5 == 0:
                self.death_frame += 1
            if self.death_frame >= 6:
                self.death_frame = 0
                self.state = GhostState.RESPAWN
            self.prev_sprite = sprite
            return sprite
        if self.player.dead:
            return self.prev_sprite
        is_centered = (
            self.v_x % (self.scaled_v_step_x) == self.scaled_half_v_step_x
            and (self.v_y) % (self.scaled_v_step_y)
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
        if (
            self.bit_x,
            self.bit_y,
        ) == self.origin and self.state == GhostState.DEAD:
            self.state = GhostState.CHASE
        return sprite

    def get_sprite(self, frame: int) -> pygame.Surface:
        """get the current sprite of the player

        Args:
            frame: the current frame the game reach between 0 and 60

        Returns:
            surface with player sprite loaded
        """
        sprite = (
            self.frightened_sprites[self.direction.value[2]]
            if self.state == GhostState.FRIGHTENED
            or self.state == GhostState.DEAD
            else self.sprites[self.direction.value[2]]
        )
        animation = sprite[self.frame]
        if frame % 10 == 0:
            self.frame = (self.frame + 1) % len(sprite)
        return animation


class Pinky(Blinky):
    """the friendly ghost pinky

    Attributes:
        origin: the bottom right corner of the maze
    """

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
        self.id = 2
        self.death_frame = 0
        self.respawn_timer = 0

    def choose_target(
        self,
    ) -> tuple:
        """get the cord of the tile 4 steps infront of
        the player if in chase mode else the corner

        Returns:
            the tuple representing the cord of the target
        """
        player = self.anchors[0]
        x = player.bit_x + (player.direction.value[0] * 4)
        y = player.bit_y + (player.direction.value[1] * 4)
        target = (x, y) if self.state == GhostState.CHASE else self.origin
        return target


class Clyde(Blinky):
    """the friendly ghost clyde

    Attributes:
        origin: the bottom right of the maze
    """

    def __init__(
        self,
        speed: int,
        scale: int,
        maze: list[list[Cell]],
        anchors: list,
    ) -> None:
        """

        Args:
            speed: the speed of the ghost
            scale: the scale modifier of the size of the maze
            maze: the cell grid representing the maze
            anchors: the anchors used to choose the new direction
        """
        super().__init__(speed, scale, maze, anchors)
        self.origin = (len(maze) - 1, len(maze[0]) - 1)
        self.reset_cords()
        self.id = 3
        self.death_frame = 0
        self.respawn_timer = 0

    def choose_target(
        self,
    ) -> tuple:
        """get the cord of the player if the it is within
        8 tiles from clyde else the cord of the corner

        Returns:
            the cord of the chosen target
        """
        player = self.anchors[0]

        if (
            abs(self.bit_x - player.bit_x) + abs(self.bit_y - player.bit_y) > 8
            and self.state == GhostState.CHASE
        ):
            return (player.bit_x, player.bit_y)
        else:
            return self.origin


class Inky(Blinky):
    """your friendly ghost inky

    Attributes:
        origin: the top right corner of the maze
    """

    def __init__(
        self,
        speed: int,
        scale: int,
        maze: list[list[Cell]],
        anchors: list,
    ) -> None:
        super().__init__(speed, scale, maze, anchors)
        self.origin = (len(maze) - 1, 0)
        self.id = 4
        self.reset_cords()
        self.death_frame = 0
        self.respawn_timer = 0

    def choose_target(
        self,
    ) -> tuple:
        """the cords of tile 8 steps from blinky to the direction of the player
        if in chase mode else the cord of origin

        Returns:
            the cords of the chosen target
        """
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
