import pygame
from src.scenes import MainMenuScene, Scene, ScoreboardScene, GameScene, ScoreEntryScene


class Screen:
    def __init__(self) -> None:

        self.height = 1280
        self.width = 1280
        self.screen: pygame.Surface = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.scenes: list[Scene] = [
            MainMenuScene(),
            GameScene(),
            ScoreEntryScene(),
            ScoreboardScene(),
        ]
        self.current_scene = 0

    def game_loop(self) -> None:

        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False

            self.scenes[self.current_scene].handle_events(events)
            self.screen.fill("black")
            self.scenes[self.current_scene].render_scene(self.screen)

            self.clock.tick(60)
            pygame.display.flip()
