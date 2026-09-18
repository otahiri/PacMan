import sys

import pygame
from src.main_game import MainGame
from src.parsing import Parser

if __name__ == "__main__":
    game_config = Parser.parse()
    pygame.init()
    pygame.display.set_caption("Pac-Meh")
    screen = MainGame(game_config)
    screen.game_loop()
# except Exception as p:
#     print(p)
# except KeyboardInterrupt:
#     print("program stopped by the user", file=sys.stderr)
