import pygame
from src.models import Button


class Screen:
    def __init__(self) -> None:

        self.height = 1280
        self.width = 1280
        self.screen: pygame.Surface = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.main_menu_buttons = [
            Button(lable, (640, 150 * i + 640))
            for i, lable in enumerate(["Start", "Scores", "Exit"])
        ]
        self.score_entry_buttons = [
            Button(lable, (640, 150 * i + 640))
            for i, lable in enumerate(["Enter your name"])
        ]
        self.current_scene = "main_menu"

    def __handle_mouse_click(self) -> None:
        buttons: list[Button] = []
        if self.current_scene == "main_menu":
            buttons = self.main_menu_buttons
        if self.current_scene == "score_entry":
            buttons = self.score_entry_buttons

        for b in buttons:
            if b.in_rage(pygame.mouse.get_pos()):
                match b.name:
                    case "Exit":
                        pygame.quit()
                        exit()
                    case "Enter your name":
                        self.current_scene = "main_menu"
                    case "Scores":
                        self.current_scene = "score_entry"

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
            if self.current_scene == "main_menu":
                self.__draw_main_menu()
            elif self.current_scene == "score_entry":
                self.__draw_score_entry()
            self.clock.tick(60)
            pygame.display.flip()

    def __draw_main_menu(self) -> None:
        for button in self.main_menu_buttons:
            self.screen.blit(button.surf, button.rect)
            self.screen.blit(button.text_surf, button.text_rect)

    def __draw_score_entry(self) -> None:
        for button in self.score_entry_buttons:
            self.screen.blit(button.surf, button.rect)
            self.screen.blit(button.text_surf, button.text_rect)
