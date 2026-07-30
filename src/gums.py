import pygame


class Gum:
    def __init__(
        self,
        score: int,
        cord: tuple,
        sprite: pygame.Surface,
        is_super: bool = False,
    ) -> None:
        self.is_super = is_super
        self.score = score
        self.cord = cord
        self.sprite = sprite


class SuperGum(Gum):
    def __init__(
        self, score: int, cord: tuple, sprite: pygame.Surface
    ) -> None:
        super().__init__(score, cord, sprite, True)
