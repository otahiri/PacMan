from pygame import Surface, surfarray

from src.render import Renderer


class ShakeInfo:
    def __init__(
        self,
        max_x: int,
        max_y: int,
        steps_x: int,
        steps_y: int,
        wait_time: int,
        max_cycles: int,
    ) -> None:
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

    def erase_frame(self, dest: Surface, target_id: int):
        shake_info = self.shake_objects.get(target_id, None)
        if not shake_info:
            return
        src = shake_info.last_frame
        frame_px = surfarray.pixels2d(src)
        eraser = Surface(frame_px.shape)
        eraser_px = surfarray.pixels2d(eraser)
        mask = frame_px != 0
        eraser_px[mask] = int(Renderer.BG, 16)
        del eraser_px
        del frame_px
        dest.blit(
            eraser,
            (
                self.shake_objects[target_id].last_x,
                self.shake_objects[target_id].last_y,
            ),
        )

    def del_shake(self, target_id: int) -> None:
        target = self.shake_objects.get(target_id, None)
        del target

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
        working_surface: Surface,
    ) -> Surface:
        shake_info = self.shake_objects.get(target_id, None)
        if not shake_info:
            working_surface.blit(target_frame, cords)
            shake_info = ShakeInfo(
                max_x,
                max_y,
                steps_x,
                steps_y,
                wait_time,
                max_cycles,
            )
            shake_info.last_frame = target_frame
            shake_info.last_x = cords[0]
            shake_info.last_y = cords[1]
            self.shake_objects[target_id] = shake_info
            return working_surface

        self.erase_frame(working_surface, target_id)
        shake_info.current_time += 1
        if shake_info.current_time >= shake_info.wait_time:
            shake_info.current_time = 0
            shake_info.accumelated_y += shake_info.steps_y
            shake_info.accumelated_x += shake_info.steps_x
            if (
                abs(shake_info.accumelated_y) >= shake_info.max_y
                and abs(shake_info.accumelated_x) >= shake_info.max_x
            ):
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

        working_surface.blit(
            target_frame,
            (shake_info.last_x, shake_info.last_y),
        )
        return working_surface
