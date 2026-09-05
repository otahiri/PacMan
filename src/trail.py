from typing import Any
import math
import numpy as np
from pygame import NOEVENT, Surface
import pygame
from pygame.version import PygameVersion

from src.render import Renderer


class TrailInfo:
    def __init__(
        self,
        trail_length: int,
        target_frame: Surface,
    ) -> None:
        self.trail_lenght: int = trail_length
        self.pixel_array: np.ndarray
        self.trail_list: list = []

    def set_correct_line(
        self, target_frame: Surface, direction: int, cord
    ) -> None:
        target_px = pygame.surfarray.array2d(target_frame)
        pixel_array = target_px
        x, y = cord
        width, height = target_px.shape
        match direction:
            case 0:
                pixel_array = target_px[:, [-1]]
                y += height
            case 1:
                pixel_array = target_px[[0], :]
            case 2:
                pixel_array = target_px[:, [0]]
            case 3:
                pixel_array = target_px[[-1], :]
                x += width
        self.trail_list.append((pixel_array, (x, y), self.trail_lenght))
        del target_px


class TrailManager:
    def __init__(self) -> None:
        self.trail_lookup: dict = {}

    def apply_trail(
        self,
        working_surf: Surface,
        target_id,
        target_frame,
        trail_lenght,
        direction,
        cord: tuple,
    ) -> None:
        trail = self.trail_lookup.get(target_id, None)
        if not trail:
            trail = TrailInfo(trail_lenght, target_frame)
            self.trail_lookup[target_id] = trail
        trail.set_correct_line(target_frame, direction, cord)
        new_list = []
        working_surf.blit(target_frame, cord)
        for s in trail.trail_list:
            pixel_array, cords, life_time = s
            working_surf.blit(
                self.make_slice(pixel_array, (life_time / trail.trail_lenght)),
                cords,
            )
            life_time -= 1
            if life_time <= 0:
                trail.trail_list.pop(trail.trail_list.index(s))
                continue
            new_list.append((pixel_array, cords, life_time))

        trail.trail_list = new_list

    def make_slice(self, pixel_array: np.ndarray, ratio: float) -> Surface:
        h, w = pixel_array.shape
        is_horizontal = w == 1
        lenght = h if is_horizontal else w
        current_lenght = int(math.floor(lenght * ratio))
        trim = (lenght - current_lenght) // 2
        new_surf = pygame.Surface(pixel_array.shape)
        new_surf.set_colorkey((0, 0, 0))
        Renderer.fill(new_surf, "black")
        new_surf_px = pygame.surfarray.pixels2d(new_surf)
        mask = pixel_array != 0
        if trim > 0:
            if is_horizontal:
                mask[:trim, :] = False
                mask[-trim:, :] = False
            else:
                mask[:, :trim] = False
                mask[:, -trim:] = False
        new_surf_px[mask] = pixel_array[mask]
        del new_surf_px
        return new_surf
