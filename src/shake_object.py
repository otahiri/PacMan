from sys import int_info

import numpy
from pygame import Surface, surfarray
from typing import Union
from src.mobs import Blinky, Player

from src.render import Renderer


class ShakeInfo:
    def __init__(self, max_x: int, max_y: int, steps_x: int, steps_y: int, target_id: int, wait_time: int, max_cycles: int) -> None:
        self.max_x: int = max_x
        self.max_y: int = max_y
        self.steps_x: int = steps_x
        self.steps_y: int = steps_y
        self.accumelated_x = 0
        self.accumelated_y = 0
        self.cycles = 0
        self.max_cycles = max_cycles
        self.wait_time: int = wait_time
        self.current_idx = 0
        self.last_x = 0
        self.last_y = 0
        self.last_frame: Surface
        self.current_time: int = 0
        self.half = 0


class Shake:
    def __init__(self) -> None:
        self.shake_objects: dict = {}

    def erase_frame(self, scale, dest: Surface, target_id: int):
        shake_info = self.shake_objects[target_id]
        src = shake_info.last_frame
        dest_px = surfarray.pixels2d(dest)
        frame_px = surfarray.pixels2d(src)
        dest_dim = dest_px.shape
        start_x = max(0, shake_info.last_x)
        start_y = max(0, shake_info.last_y)
        end_x = start_x + 16 * scale
        end_y = start_y + 16 * scale
        max_x, max_y = dest_dim

        if (
            0 <= start_x <= max_x
            and 0 <= start_y <= max_y
            and 0 <= end_x <= max_x
            and 0 <= end_y <= max_y
        ):
            view_dest = dest_px[start_x:end_x, start_y:end_y]
            mask = frame_px != 0
            view_src = numpy.full_like(frame_px, 0)
            view_dest[mask] = view_src[mask]

        del dest_px
        del frame_px

    def apply_shake(
        self,
        max_x: int,
        max_y: int,
        steps_x: int,
        steps_y: int,
        max_cycles: int,
        wait_time: int,
        target_frame: Surface,
        target_id: int,
        cords: tuple,
        scale: int,
        working_surface: Surface
    ) -> Surface:
        shake_info = self.shake_objects.get(target_id, None)
        if not shake_info:
            Renderer.custom_blit(working_surface, target_frame, cords)
            shake_info = ShakeInfo(max_x, max_y, steps_x, steps_y, target_id, wait_time, max_cycles)
            shake_info.last_frame = target_frame
            shake_info.last_x = cords[0]
            shake_info.last_y = cords[1]
            self.shake_objects[target_id] = shake_info
            return working_surface

        self.erase_frame(scale, working_surface, target_id)
        shake_info.current_time += 1
        if shake_info.current_time >= shake_info.wait_time:
            shake_info.current_time = 0
            shake_info.accumelated_y += shake_info.steps_y
            shake_info.accumelated_x += shake_info.steps_x
            if abs(shake_info.accumelated_y) >= shake_info.max_y and abs(shake_info.accumelated_x) >= shake_info.max_x:
                shake_info.steps_x = -shake_info.steps_x
                shake_info.steps_y = -shake_info.steps_y
                shake_info.half += 1
                shake_info.cycles = shake_info.half // 2

            if shake_info.cycles >= shake_info.max_cycles:
                del self.shake_objects[target_id]
                return working_surface
        shake_info.last_x = cords[0] + shake_info.accumelated_x
        shake_info.last_y = cords[1] + shake_info.accumelated_y
        shake_info.last_frame = target_frame

        Renderer.custom_blit(working_surface, target_frame, (shake_info.last_x, shake_info.last_y))
        return working_surface
