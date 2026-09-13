from typing import Union

from src.parsing import GameConfig
from src.render import Renderer
from src import Player, Maze, Blinky, Pinky, Clyde, Inky
from src.enums import (
    ColorType,
    Direction,
    DisplayInfo,
    GhostState,
    PlayerState,
)
from mazegenerator import MazeGenerator
import pygame
from src.shake_object import Shake


class GameLogic:
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
        self.maze = Maze(MazeGenerator())
        self.game_config = game_config
        self.game_over = False
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
            (DisplayInfo.SCREEN_WIDTH.value - self.maze.max_x) // 2,
            (DisplayInfo.SCREEN_HEIGHT.value - self.maze.max_y) // 2,
        )
        self.player = Player(2, self.maze.cell_grid)
        self.blinky = Blinky(1, self.maze.cell_grid, [self.player])
        self.pinky = Pinky(1, self.maze.cell_grid, [self.player])
        self.clyde = Clyde(1, self.maze.cell_grid, [self.player])
        self.inky = Inky(1, self.maze.cell_grid, [self.player, self.blinky])
        self.mobs = [self.blinky, self.pinky, self.clyde, self.inky]
        self.working_surf = pygame.Surface(
            (self.maze.max_x + 64, self.maze.max_y + 64), pygame.SRCALPHA
        )
        self.maze_surf = self.maze.render_maze()
        self.working_surf.blit(self.maze_surf, (0, 0))
        self.maze.load_gums(self.working_surf)
        self.new_move = Direction.NONE

    def __set_hearts(self):
        if self.game_config.mode == "normal":
            self.hearts = 3
        elif self.game_config.mode == "hardcore":
            self.hearts = 1
        else:
            self.hearts = 3

    def handle_collision(self) -> None:
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

                victim.die()
                self.shake.del_shake(victim.id)
                return
        gum = self.maze.get_gum(p_x, p_y)
        if gum:
            if gum.is_super:
                self.global_mode = GhostState.FRIGHTENED
                self.change_mode()
            self.score += gum.score
            self.maze.set_gum(p_x, p_y)

    def get_score(self) -> int:
        return self.score

    def get_ghost_mode(self) -> GhostState:
        return self.global_mode

    def get_level(self) -> int:
        return self.level

    def set_global_mode(self, delta: float):
        if self.global_mode == GhostState.FRIGHTENED:
            self.super_gum_timer += delta
            if (
                self.super_gum_timer
                <= GameLogic.FRIGHTENED_DURATIONS[self.level - 1]
            ):
                return
            else:
                self.super_gum_timer = 0
                self.player.power = -self.player.power
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

    def reset_maze(self) -> None:
        for mob in self.mobs:
            self.shake.del_shake(mob.id)
            mob.reset_cords()
            self.change_frame(mob, 0)
            mob.state = self.global_mode
            mob.respawn_timer = 0
            mob.death_frame = 0
        self.working_surf.blit(self.maze_surf, (0, 0))
        self.player.reset_cords()
        self.change_frame(self.player, 0)
        self.player.dead = False
        self.player.death_frame = 0
        self.player.state = PlayerState.ALIVE
        self.death_timer = 0

    def change_mode(self):
        for mob in self.mobs:
            if mob.state == GhostState.RESPAWN:
                continue
            mob.state = self.global_mode

    def maze_engine(self, delta: float) -> pygame.Surface:

        if self.maze.get_gum_count() <= 0:
            self.level += 1
            if self.level > self.game_config.levels_number:
                self.game_over = True
            self.reset_maze()
            self.maze.set_gums()
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
        self.maze.load_gums(self.working_surf)
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
                self.reset_maze()

    def change_frame(
        self,
        character: Union[Player, Blinky],
        frame: int,
    ):
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
