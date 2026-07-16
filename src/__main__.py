import pygame
from .display import Screen

try:
    pygame.init()
    game = Screen()
    game.game_loop()
except BaseException:
    pass
