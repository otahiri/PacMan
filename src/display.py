import pygame

pygame.init()


class Button:

    def __init__(self, name: str, pos: tuple[int, int]) -> None:
        self.name = name
        font = pygame.font.Font(None, 100)
        self.text_surf = font.render(name, True, "white")
        self.text_rect = self.text_surf.get_rect(center=pos)
        self.pos = pos
        self.surf = pygame.surface.Surface((300, 100))
        self.surf.fill("red")
        self.rect = self.surf.get_rect(center=pos)

    def in_rage(self, pos: tuple[int, int]) -> bool:
        x, y = pos
        if (
            x >= self.rect.topleft[0]
            and x <= self.rect.topright[0]
            and y >= self.rect.topleft[1]
            and y <= self.rect.bottomleft[1]
        ):
            return True
        return False


class Screen:
    def __init__(self) -> None:

        self.height = 1280
        self.width = 1280
        self.screen: pygame.Surface = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.buttons = [
            Button(lable, (640, 150 * i + 640))
            for i, lable in enumerate(["Start", "Scores", "Exit"])
        ]

    def __handle_mouse_click(self) -> None:
        for b in self.buttons:
            if b.in_rage(pygame.mouse.get_pos()):
                match b.name:
                    case "Exit":
                        pygame.quit()
                        exit()

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
            self.__draw_main_menu()
            self.clock.tick(60)
            pygame.display.flip()

    def __draw_main_menu(self) -> None:
        pos = 400
        for button in self.buttons:
            pos += 200
            self.screen.blit(button.surf, button.rect)
            self.screen.blit(button.text_surf, button.text_rect)
