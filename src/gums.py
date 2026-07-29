import pygame
from src.render import Renderer


class Gum:
    def __init__(self, score: int, cord: tuple, sprite: pygame.Surface) -> None:
        self.score = score
        self.cord = cord
        self.sprite = sprite


class SuperGum(Gum):
    def __init__(self, score: int, cord: tuple, sprite: pygame.Surface) -> None:
        super().__init__(score, cord, sprite)
