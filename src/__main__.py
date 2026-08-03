import pygame
from src.main_game import MainGame
from src.parsing import Parser

game_config = Parser.parse()
pygame.init()
screen = MainGame(game_config)
screen.game_loop()
