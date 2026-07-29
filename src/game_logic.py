from typing import Union
import numpy
from src.render import Renderer
from src import Player, Maze, Blinky, Pinky, Clyde, Inky
from src.enums import Direction, DisplayInfo
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

    def maze_engine(self, frame: int, new_move: Direction) -> pygame.Surface:
        if not self.player.dead:
            self.player.new_direction = new_move
            self.maze.load_gums(self.working_surf)
            self.change_frame(self.working_surf, self.player, frame)
            self.change_frame(self.working_surf, self.blinky, frame)
            self.change_frame(self.working_surf, self.inky, frame)
            self.change_frame(self.working_surf, self.pinky, frame)
            self.change_frame(self.working_surf, self.clyde, frame)
        else:
            self.player.toggle_death()
            if self.player.lifes >= 0:
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
                    mob.set_cords()
                    self.change_frame(self.working_surf, mob, frame)
                self.player.dead = False
                self.player.lifes -= 1
            else:
                self.game_over = True
        return self.working_surf

    def erase_frame(
        self, dest: pygame.Surface, character: Union[Player, Blinky]
    ):
        char_frame = character.prev_sprite
        dest_px = pygame.surfarray.pixels2d(dest)
        frame_px = pygame.surfarray.pixels2d(char_frame)
        dest_dim = dest_px.shape
        start_x = max(0, character.v_x)
        start_y = max(0, character.v_y)
        end_x = start_x + 15 * self.scale
        end_y = start_y + 15 * self.scale
        max_x, max_y = dest_dim

        if (
            0 <= start_x < max_x
            and 0 <= start_y < max_y
            and 0 <= end_x < max_x
            and 0 <= end_y < max_y
        ):
            view_dest = dest_px[start_x:end_x, start_y:end_y]
            mask = frame_px == frame_px
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
