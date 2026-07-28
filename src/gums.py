import pygame


class Gum:
    def __init__(self, score: int, cord: tuple) -> None:
        self.score = score
        self.cord = cord
        self.sprite = pygame.image.load("assets/gum.png")


class SuperGum(Gum):
    def __init__(self, score: int, cord: tuple) -> None:
        super().__init__(score, cord)
        self.sprite = pygame.image.load("assets/super_gum.png")
