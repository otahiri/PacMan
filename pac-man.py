import pygame
from src.main_game import MainGame
from src.parsing import Parser
import sys


if __name__ == "__main__":
    try:
        game_config = Parser.parse()
        pygame.init()
        pygame.display.set_caption('PacMan')
        screen = MainGame(game_config)
        screen.game_loop()
    except KeyboardInterrupt:
        print("program stopped by the user", file=sys.stderr)
