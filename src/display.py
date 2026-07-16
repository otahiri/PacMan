import pygame
from src.scenes import MainMenuScene, ScoreboardScene, GameScene, ScoreEntryScene


class Screen:
    def __init__(self) -> None:

        self.height = 1280
        self.width = 1280
        self.screen: pygame.Surface = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.scenes = [
            MainMenuScene(),
            GameScene(),
            ScoreEntryScene(),
            ScoreboardScene(),
        ]
        self.current_scene = 0

    def __handle_mouse_click(self) -> None:

        if self.current_scene == 0:
            for button in self.scenes[0].buttons:
                if button.in_rage(pygame.mouse.get_pos()):
                    match button.name:
                        case "Exit":
                            pygame.quit()
                            exit()
                        case "Play":
                            self.current_scene = 1
                        case "Scores":
                            self.current_scene = 3

        elif self.current_scene == 1:
            self.current_scene = 2

        elif self.current_scene == 3 or self.current_scene == 2:
            self.current_scene = 0

    def game_loop(self) -> None:

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.__handle_mouse_click()

            self.screen.fill("black")
            self.scenes[self.current_scene].render_scene(self.screen)
            self.clock.tick(60)
            pygame.display.flip()
