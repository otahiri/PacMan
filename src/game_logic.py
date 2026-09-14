"""game logic module handle all the game logics for
characters consumables and maze
"""

from typing import Union

from src.parsing import GameConfig
from src.render import Renderer
from src import Player, MazeInterface, Blinky, Pinky, Clyde, Inky
from src.enums import (
    ColorType,
    Direction,
    DisplayInfo,
    GhostState,
)
import pygame
from src.shake_object import Shake


class GameLogic:
    """the main game logic class that handles everything that happens
    inside the game

    Attributes:
        FRIGHTENED_DURATIONS: the super gum duration according to the wave
        WAVES_AFTER_FIFTH: scatter / chase timing post wave 5
        WAVES_BEFORE_FIFTH: scatter / chase timing pre wave 5
        maze: the maze object handling maze logic
        game_config: game config object containing the options extracted
        from the config file
        game_over: boolean flag to show if the game is over
        shake: shake object responsible for shaking sprites
        frame: current frame of the game
        level: the current level
        death_timer: duration passed since the start of the death animation
        accumulator: the accumulated ms from last frame
        time_stamp: current time stamp
        super_gum_timer: the duration passed since the consumtion of
        the super gum
        global_mode: current global ghost mode
        MS_PER_FRAME: ms each frame spans
        score: current player score
        hearts: current heart left the player has
        v_offset: visual offset to paint sprite in the correct position
        player: player object
        blinky: blinky ghost object
        pinky: pinky ghost object
        clyde: clyde ghost object
        inky: inky ghost object
        mobs: list containing all ghosts
        working_surf: surface to paint the actual game
        maze_surf: preloaded maze surface
        new_move: player next move
    """

    FRIGHTENED_DURATIONS = (
        6.0,
        5.0,
        4.0,
        3.0,
        2.0,
        5.0,
        2.0,
        1.0,
        1.0,
        5.0,
        2.0,
        1.0,
        1.0,
        3.0,
        1.0,
        1.0,
        0.0,
        1.0,
        0.0,
    )
    WAVES_AFTER_FIFTH = [
        (0, GhostState.SCATTER),
        (5, GhostState.CHASE),
        (25, GhostState.SCATTER),
        (30, GhostState.CHASE),
        (50, GhostState.SCATTER),
        (55, GhostState.CHASE),
    ]
    WAVES_BEFORE_FIFTH = [
        (0, GhostState.SCATTER),
        (7, GhostState.CHASE),
        (27, GhostState.SCATTER),
        (34, GhostState.CHASE),
        (54, GhostState.SCATTER),
        (61, GhostState.CHASE),
    ]

    def __init__(self, game_config: GameConfig) -> None:
        """game logic constructor

        Args:
            game_config: game config object containing info extracted
            from config file
        """
        self.maze_interface = MazeInterface()
        self.game_config = game_config
        self.game_over = False
        self.reset_level = False
        self.shake = Shake()
        self.frame = 0
        self.level = 1
        self.death_timer = 0
        self.accumulator = 0.0
        self.time_stamp = 0.0
        self.super_gum_timer = 0.0

        self.global_mode = GhostState.SCATTER
        self.MS_PER_FRAME = 0.016
        self.score = 0
        self.hearts = 0
        self.__set_hearts()
        self.v_offset = (
            (DisplayInfo.SCREEN_WIDTH.value - self.maze_interface.max_x) // 2,
            (DisplayInfo.SCREEN_HEIGHT.value - self.maze_interface.max_y) // 2,
        )
        self.player = Player(2, self.maze_interface.cell_grid)
        self.blinky = Blinky(1, self.maze_interface.cell_grid, [self.player])
        self.pinky = Pinky(1, self.maze_interface.cell_grid, [self.player])
        self.clyde = Clyde(1, self.maze_interface.cell_grid, [self.player])
        self.inky = Inky(
            1, self.maze_interface.cell_grid, [self.player, self.blinky]
        )
        self.mobs = [self.blinky, self.pinky, self.clyde, self.inky]
        self.working_surf = pygame.Surface(
            (self.maze_interface.max_x + 64, self.maze_interface.max_y + 64),
            pygame.SRCALPHA,
        )
        self.maze_surf = self.maze_interface.render_maze()
        self.working_surf.blit(self.maze_surf, (0, 0))
        self.maze_interface.render_gums(self.working_surf)
        self.new_move = Direction.NONE

    def __set_hearts(self):
        """set heart count according to mode"""
        if self.game_config.mode == "normal":
            self.hearts = 3
        elif self.game_config.mode == "hardcore":
            self.hearts = 1
        else:
            self.hearts = 3

    def handle_collision(self) -> None:
        """handle player collisions with other object"""
        p_x, p_y = self.player.bit_x, self.player.bit_y
        for mob in self.mobs:
            if mob.state in [GhostState.DEAD, GhostState.RESPAWN]:
                continue
            if (
                abs(mob.v_x - self.player.v_x) < 16
                and abs(mob.v_y - self.player.v_y) < 16
                and not self.player.dead
            ):
                victim = (
                    mob if mob.state == GhostState.FRIGHTENED else self.player
                )
                if (
                    isinstance(victim, Player)
                    and self.game_config.mode == "cheat"
                ):
                    continue
                elif isinstance(victim, Blinky):
                    self.score += 200

                victim.die()
                self.shake.del_shake(victim.id)
                return
        gum = self.maze_interface.get_content(p_x, p_y)
        if gum:
            if gum.is_super:
                self.global_mode = GhostState.FRIGHTENED
                self.change_mode()
            self.score += gum.score
            self.maze_interface.set_content(p_x, p_y)
            print(self.maze_interface.get_gum_count())

    def get_score(self) -> int:
        """get current score

        Returns:
            current score
        """
        return self.score

    def get_ghost_mode(self) -> GhostState:
        """get the ghosts global mode

        Returns:
            ghost global mode
        """
        return self.global_mode

    def get_level(self) -> int:
        """get current level

        Returns:
            the current level
        """
        return self.level

    def set_global_mode(self, delta: float):
        """set global mode according to the current wave

        Args:
            delta: current delta time
        """
        if self.global_mode == GhostState.FRIGHTENED:
            self.super_gum_timer += delta
            if (
                self.super_gum_timer
                <= GameLogic.FRIGHTENED_DURATIONS[self.level - 1]
            ):
                return
            else:
                self.super_gum_timer = 0
        self.time_stamp += delta
        waves = (
            GameLogic.WAVES_BEFORE_FIFTH
            if self.level < 5
            else GameLogic.WAVES_AFTER_FIFTH
        )
        new_mode = waves[0][1]
        for thresh_hold, mode in waves:
            if self.time_stamp > thresh_hold:
                new_mode = mode
            else:
                break

        if new_mode != self.global_mode:
            self.global_mode = new_mode
            self.change_mode()

    def death_reset(self) -> None:
        """reset the maze and characters"""
        self.reset_characters()
        self.working_surf.blit(self.maze_surf, (0, 0))

    def reset_game(self) -> None:
        """reset the game when next level is triggered"""
        self.time_stamp = 0.0
        self.maze_interface.reset_maze()
        self.death_logic(self.frame)
        self.maze_interface.render_gums(self.working_surf)
        self.reset_characters()
        self.maze_surf = self.maze_interface.render_maze()

    def reset_characters(self) -> None:
        """reset the characters to their original cords"""
        self.player.reset_cords()
        self.player.maze = self.maze_interface.cell_grid
        self.change_frame(self.player, self.frame)
        self.player.dead = False
        self.player.death_frame = 0
        self.death_timer = 0
        for mob in self.mobs:
            mob.maze = self.maze_interface.cell_grid
            self.shake.del_shake(mob.id)
            mob.reset_cords()
            self.change_frame(mob, 0)
            mob.state = self.global_mode
            mob.respawn_timer = 0
            mob.death_frame = 0
            mob.state = self.global_mode

    def change_mode(self):
        """change the mode of all ghost to the current global mode unless
        they are in respawn"""
        for mob in self.mobs:
            if mob.state == GhostState.RESPAWN:
                continue
            mob.state = self.global_mode

    def render_pause(self) -> pygame.Surface:
        """render paused scene

        Returns:
            working_surf surface with paused game on it
        """
        self.maze_interface.render_gums(self.working_surf)
        self.working_surf.blit(self.maze_surf, (0, 0))
        for mob in self.mobs:
            mob_shake = self.shake.shake_objects[mob.id]
            self.working_surf.blit(
                mob_shake.last_frame, (mob_shake.last_x, mob_shake.last_y)
            )
        self.working_surf.blit(
            self.player.prev_sprite, (self.player.v_x, self.player.v_y)
        )
        return self.working_surf

    def maze_engine(self, delta: float, pause: bool) -> pygame.Surface:
        """main engine behind the game logic

        Args:
            delta: the current delta time
            pause: is game in pause state

        Returns:
            the constructed surface
        """
        if pause:
            return self.render_pause()
        if self.maze_interface.get_gum_count() <= 0:
            Renderer.fill(self.working_surf, ColorType.SECONDARY)
            self.level += 1
            self.reset_level = True
            self.reset_game()
            if self.level > 10:
                self.game_over = True
            return self.working_surf
        self.set_global_mode(delta)
        self.accumulator += delta
        while self.accumulator > self.MS_PER_FRAME:
            Renderer.fill(self.working_surf, ColorType.SECONDARY)
            self.frame += 1
            if not self.player.dead:
                self.working_surf.blit(self.maze_surf, (0, 0))
                self.alive_logic(self.frame)
                self.handle_collision()
            else:
                self.death_logic(self.frame)
            self.accumulator -= self.MS_PER_FRAME
        return self.working_surf

    def alive_logic(self, frame: int) -> None:
        """apply logic when the player is alive

        Args:
            frame: current frame of the game
        """
        self.maze_interface.render_gums(self.working_surf)
        self.player.new_direction = self.new_move
        self.change_frame(self.player, frame)
        for mob in self.mobs:
            if mob.state == GhostState.RESPAWN:
                mob.reset_cords()
                if frame % 60 == 0:
                    mob.respawn_timer += 1
                    if mob.respawn_timer >= 10:
                        mob.respawn_timer = 0
                        mob.state = self.global_mode
                continue
            self.shake.apply_shake(
                4,
                4,
                2,
                2,
                100,
                4,
                mob.move(frame),
                mob.id,
                (mob.v_x, mob.v_y),
                self.working_surf,
            )

    def death_logic(self, frame: int) -> None:
        """apply logic of when the player is dead

        Args:
            frame: current frame of the game
        """
        wait_timer = 60
        self.new_move = Direction.NONE
        if self.death_timer < wait_timer:
            if self.death_timer < 20:
                self.working_surf.blit(
                    self.player.prev_sprite, (self.player.v_x, self.player.v_y)
                )
                self.death_timer += 1
                return

            else:
                Renderer.fill(self.working_surf, ColorType.SECONDARY)
                self.shake.apply_shake(
                    2,
                    0,
                    2,
                    0,
                    4,
                    1,
                    self.player.prev_sprite,
                    self.player.id,
                    (self.player.v_x, self.player.v_y),
                    self.working_surf,
                )
            self.shake.apply_shake(
                2,
                0,
                2,
                0,
                4,
                1,
                self.player.prev_sprite,
                self.player.id,
                (self.player.v_x, self.player.v_y),
                self.working_surf,
            )
            self.death_timer += 1
        else:
            if self.hearts <= 0:
                self.game_over = True
                return
            self.change_frame(self.player, frame)
            if self.player.death_frame >= 9:
                self.hearts -= 1
                self.death_reset()

    def change_frame(
        self,
        character: Union[Player, Blinky],
        frame: int,
    ):
        """change the position of the sprite of character

        Args:
            character: either player of ghost object
            frame: current frame of the game
        """
        if isinstance(character, Player):
            self.working_surf.blit(
                character.move(frame),
                (character.v_x, character.v_y),
            )
        else:

            self.shake.apply_shake(
                4,
                4,
                2,
                2,
                100,
                4,
                character.move(frame),
                character.id,
                (character.v_x, character.v_y),
                self.working_surf,
            )
