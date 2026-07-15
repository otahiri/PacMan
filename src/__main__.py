from .display import Screen

try:
    game = Screen()
    game.game_loop()
except BaseException:
    pass
