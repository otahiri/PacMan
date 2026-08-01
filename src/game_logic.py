from typing import Union
import numpy
from src.render import Renderer
from src import Player, Maze, Blinky, Pinky, Clyde, Inky
from src.enums import Direction, DisplayInfo, PlayerState
from mazegenerator import MazeGenerator
import pygame


class GameLogic:
    def __init__(
        self,
        scale: int,
    ) -> None:
        self.scale = scale
        self.maze = Maze(MazeGenerator(), scale)
        self.game_over = False
        self.frame = 0
        self.accumulator = 0.0
        self.time_stamp = 0.0
        self.MS_PER_GRAME = 0.016
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
        self.working_surf = pygame.Surface(
            (
                self.maze.max_x + 32 * self.scale,
                self.maze.max_y + 32 * self.scale,
            )
        )
        Renderer.custom_blit(
            self.working_surf, self.maze.render_maze(self.scale), (0, 0)
        )
        self.maze.load_gums(self.working_surf)
        self.new_move = Direction.NONE

    def handle_collision(self) -> None:
        mobs = [self.blinky, self.pinky, self.inky, self.clyde]
        p_x, p_y = self.player.bit_x, self.player.bit_y
        for mob in mobs:
            if (
                abs(mob.v_x - self.player.v_x) < (8 * self.scale)
                and abs(mob.v_y - self.player.v_y) < (8 * self.scale)
                and not self.player.dead
            ):
                self.player.dead = True
                self.player.state = PlayerState.DEAD
                return
        gum = self.maze.get_gum(p_x, p_y)
        if gum:
            if gum.is_super:
                print("super")
            self.score += gum.score
            self.maze.set_gum(p_x, p_y)

    def get_score(self) -> int:
        return self.score

    def maze_engine(self, delta: float) -> pygame.Surface:
        self.time_stamp += delta
        self.accumulator += delta
        while self.accumulator > self.MS_PER_GRAME:
            self.frame += 1
            if not self.player.dead:
                self.alive_logic(self.frame)
                self.handle_collision()
            else:
                self.death_logic(self.frame)
            self.accumulator -= self.MS_PER_GRAME

        return self.working_surf

    def alive_logic(self, frame: int) -> None:
        self.player.new_direction = self.new_move
        self.maze.load_gums(self.working_surf)
        self.change_frame(self.working_surf, self.player, frame)
        self.change_frame(self.working_surf, self.blinky, frame)
        self.change_frame(self.working_surf, self.inky, frame)
        self.change_frame(self.working_surf, self.pinky, frame)
        self.change_frame(self.working_surf, self.clyde, frame)

    def death_logic(self, frame: int) -> None:
        self.new_move = Direction.NONE
        self.change_frame(self.working_surf, self.player, frame)
        self.change_frame(self.working_surf, self.blinky, frame)
        self.change_frame(self.working_surf, self.inky, frame)
        self.change_frame(self.working_surf, self.pinky, frame)
        self.change_frame(self.working_surf, self.clyde, frame)
        if self.player.death_frame >= 8:
            mobs: list[Union[Player, Blinky]] = [
                self.player,
                self.blinky,
                self.inky,
                self.pinky,
                self.clyde,
            ]
            for mob in mobs:
                mob.bit_x, mob.bit_y = mob.origin
                self.erase_frame(self.working_surf, mob)
                mob.reset_cords()
                self.change_frame(self.working_surf, mob, frame)
            self.player.dead = False
            self.hearts -= 1
            self.player.death_frame = 0
            self.player.state = PlayerState.ALIVE
        if self.hearts <= 0:
            self.game_over = True

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
        Renderer.custom_blit(
            self.working_surf,
            character.move(frame),
            (character.v_x, character.v_y),
        )
