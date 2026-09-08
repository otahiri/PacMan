import math
import numpy as np
import pygame
from src.render import Renderer


class TrailInfo:
    def __init__(
        self,
        trail_length: int,
        target_frame: pygame.Surface,
    ) -> None:
        self.trail_lenght: int = trail_length
        self.pixel_array: np.ndarray
        self.trail_list: list = []

    def set_correct_line(
        self, target_frame: pygame.Surface, direction: int, cord
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



