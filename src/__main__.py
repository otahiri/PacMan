import pygame
from src.display import Screen
from src.parsing import Parser

Parser.parse()
exit()
pygame.init()
screen = Screen()
screen.game_loop()
