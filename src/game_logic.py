from typing import Union
import numpy
from src.render import Renderer
from src import Player, Maze, Blinky, Pinky, Clyde, Inky
from src.enums import Direction, DisplayInfo, GhostState, PlayerState
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

    def __init__(
        self,
        scale: int,
    ) -> None:
        self.scale = scale
        self.maze = Maze(MazeGenerator(), scale)
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
        self.hearts = 3
        self.v_offset = (
            (DisplayInfo.SCREEN_WIDTH.value - self.maze.max_x) // 2,
            (DisplayInfo.SCREEN_HEIGHT.value - self.maze.max_y) // 2,
        )
        self.player = Player(2, scale, self.maze.cell_grid)
        self.blinky = Blinky(1, scale, self.maze.cell_grid, [self.player])
        self.pinky = Pinky(1, scale, self.maze.cell_grid, [self.player])
        self.clyde = Clyde(1, scale, self.maze.cell_grid, [self.player])
        self.inky = Inky(
            1, scale, self.maze.cell_grid, [self.player, self.blinky]
        )
        self.mobs = [self.blinky, self.pinky, self.clyde, self.inky]
        self.working_surf = pygame.Surface(
            (
                self.maze.max_x + 32 * self.scale,
                self.maze.max_y + 32 * self.scale,
            )
        )
        self.maze_surf = self.maze.render_maze(self.scale)
        self.gum_count = self.maze.load_gums(self.working_surf)
        Renderer.custom_blit(self.working_surf, self.maze_surf, (0, 0))
        self.new_move = Direction.NONE

    def handle_collision(self) -> None:
        p_x, p_y = self.player.bit_x, self.player.bit_y
        for mob in self.mobs:
            if mob.state in [GhostState.DEAD, GhostState.RESPAWN]:
                continue
            if (
                abs(mob.v_x - self.player.v_x) < (8 * self.scale)
                and abs(mob.v_y - self.player.v_y) < (8 * self.scale)
                and not self.player.dead
            ):
                victim = (
                    mob if mob.state == GhostState.FRIGHTENED else self.player
                )
                victim.die()
                self.shake.erase_frame(
                    self.scale, self.working_surf, victim.id
                )
                self.shake.del_shake(victim.id)
                return
        gum = self.maze.get_gum(p_x, p_y)
        if gum:
            if gum.is_super:
                self.global_mode = GhostState.FRIGHTENED
                self.change_mode()
            self.score += gum.score
            self.maze.remove_gum(p_x, p_y)
            self.gum_count -= 1
            if not self.gum_count:
                self.level += 1
                self.reset_maze()
                self.maze.set_gums(self.scale)

    def get_score(self) -> int:
        return self.score

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
        for threshold, mode in waves:
            if self.time_stamp > threshold:
                new_mode = mode
            else:
                break

        if new_mode != self.global_mode:
            self.global_mode = new_mode
            self.change_mode()

    def reset_maze(self) -> None:
        Renderer.fill(self.working_surf, "black")
        Renderer.custom_blit(self.working_surf, self.maze_surf, (0, 0))
        for mob in self.mobs:
            self.shake.erase_frame(self.scale, self.working_surf, mob.id)
            self.shake.del_shake(mob.id)
            mob.reset_cords()
            self.change_frame(self.working_surf, mob, 0)
            mob.state = self.global_mode
            mob.respawn_timer = 0
            mob.death_frame = 0

        self.player.reset_cords()
        self.player.direction = Direction.NONE
        self.change_frame(self.working_surf, self.player, 0)
        self.player.dead = False
        self.hearts -= 1
        self.player.death_frame = 0
        self.player.state = PlayerState.ALIVE
        self.death_timer = 0

    def change_mode(self):
        for mob in self.mobs:
            if mob.state in [GhostState.RESPAWN, GhostState.DEAD]:
                continue
            mob.state = self.global_mode

    def maze_engine(self, delta: float) -> pygame.Surface:
        self.set_global_mode(delta)
        self.accumulator += delta
        while self.accumulator > self.MS_PER_FRAME:
            self.frame += 1
            if not self.player.dead:
                self.alive_logic(self.frame)
                self.handle_collision()
            else:
                self.death_logic(self.frame)
            self.accumulator -= self.MS_PER_FRAME
        return self.working_surf

    def alive_logic(self, frame: int) -> None:
        self.player.new_direction = self.new_move
        self.maze.load_gums(self.working_surf)
        self.change_frame(self.working_surf, self.player, frame)
        for mob in self.mobs:
            if mob.state == GhostState.RESPAWN:
                self.shake.erase_frame(self.scale, self.working_surf, mob.id)
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
                self.scale,
                self.working_surf,
            )

    def death_logic(self, frame: int) -> None:
        wait_timer = 60
        self.new_move = Direction.NONE
        if self.death_timer < wait_timer:
            if self.death_timer < 20:
                self.death_timer += 1
                return

            else:
                Renderer.fill(self.working_surf, "black")
                for mob in self.mobs:
                    self.shake.erase_frame(
                        self.scale, self.working_surf, mob.id
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
                    self.scale,
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
                self.scale,
                self.working_surf,
            )
            self.death_timer += 1
        else:
            self.change_frame(self.working_surf, self.player, frame)
            if self.player.death_frame >= 9:
                self.reset_maze()
                if self.hearts <= 0:
                    self.game_over = True
                    self.reset_maze()
                    self.maze.set_gums(self.scale)
                    self.hearts = 3
                    return

    def erase_frame(
        self, dest: pygame.Surface, character: Union[Player, Blinky]
    ):
        char_frame = character.prev_sprite
        dest_px = pygame.surfarray.pixels2d(dest)
        frame_px = pygame.surfarray.pixels2d(char_frame)
        dest_dim = dest_px.shape
        start_x = max(0, character.v_x)
        start_y = max(0, character.v_y)
        end_x = start_x + 16 * self.scale
        end_y = start_y + 16 * self.scale
        max_x, max_y = dest_dim

        if (
            0 <= start_x < max_x
            and 0 <= start_y < max_y
            and 0 <= end_x < max_x
            and 0 <= end_y < max_y
        ):
            view_dest = dest_px[start_x:end_x, start_y:end_y]
            mask = frame_px != 0
            view_src = numpy.full_like(frame_px, 0)
            view_dest[mask] = view_src[mask]

        del dest_px
        del frame_px

    def change_frame(
        self,
        dest: pygame.Surface,
        character: Union[Player, Blinky],
        frame: int,
    ):
        self.erase_frame(dest, character)
        if isinstance(character, Player):
            Renderer.custom_blit(
                self.working_surf,
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
                self.scale,
                self.working_surf,
            )
