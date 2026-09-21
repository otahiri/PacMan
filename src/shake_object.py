"""the shake object model responsible to shift sprite from the center
to simulate shaking of bobbing
"""

from pygame import Surface


class ShakeInfo:
    """shake info class containing info about an object to shake

    Attributes:
        max_x: the maximum x steps to shift object with
        max_y: the maximum y steps to shift object with
        steps_x: the count of the steps to shift the object each time
        in the x cord
        steps_y: the count of the steps to shift the object each time
        in the y cord
        accumelated_x: the accumelated steps of the x cord
        accumelated_y: the accumelated steps of the y cord
        max_cycles: the maximum possible cycle of shifting the cords
        wait_time: the wait time before applying the next shift
        last_x: the last x cord
        last_y: the last y cord
        last_frame: the previous sprite
        current_time: the current time since the last shift
        accumelated_total: the total half cycle happend
    """

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
        self.max_cycles = max_cycles
        self.wait_time: int = wait_time
        self.last_x = 0
        self.last_y = 0
        self.last_frame: Surface
        self.current_time: int = 0
        self.accumelated_total = 0


class Shake:
    """shake sprite to simulate trigger effect or bobbing effect

    Attributes:
        shake_objects: the object handeling the shaking info
        last_x: the last x cord of the sprite
        last_y: the last y cord of the sprite
        last_frame: the last frame of the target
    """
    def __init__(self) -> None:
        self.shake_objects: dict = {}

    def del_shake(self, target_id: int) -> None:
        """delete the shake info of the target

        Args:
            target_id: the id of the target
        """
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
        """apply the offset each frame to stimulate the shake effect

        Args:
            max_x: the max x the sprite can get to
            max_y: the max y the sprite can get to
            steps_x: the shift x each frame takes
            steps_y: the shift y each frame takes
            max_cycles: the max cycle in total each shift takes
            wait_time: the wait time between shifts
            target_frame: the target frame to shift
            target_id: the target id for the target
            cords: the default cord of the target
            working_surface: the working surface to put the shifted frame on

        Returns:
            the working surface with the shifted sprite on it
        """
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
                shake_info.accumelated_total += 1

            if shake_info.accumelated_total // 2 >= shake_info.max_cycles:
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
