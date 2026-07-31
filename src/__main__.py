import pygame
import sys
from src.display import Screen
from src.parsing import Parser

Parser.parse()

pygame.init()
screen = Screen()
screen.game_loop()
