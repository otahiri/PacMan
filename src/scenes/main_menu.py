import pygame
from src.enums import SceneName
from src.models import Scene
from src.models import Button


class MainMenuScene(Scene):
    def __init__(self) -> None:
        self.buttons = [
            Button(lable, (640, 150 * i + 640))
            for i, lable in enumerate(["Play", "Scores", "Exit"])
        ]
        self.button_idx = 0

    def render_scene(self, screen) -> None:
        for i, button in enumerate(self.buttons):
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                self.button_idx = i
            thickness = 10
            if i == self.button_idx:
                pygame.draw.rect(
                    screen,
                    "red",
                    button.rect.inflate(thickness * 2, thickness * 2),
                    thickness,
                )
            else:
                pygame.draw.rect(screen, "red", button.rect, 5)
            screen.blit(button.text_surf, button.text_rect)

    def handle_events(self, events: list[pygame.Event]) -> None | SceneName:
        for event in events:
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_UP:
                        if self.button_idx == 0:
                            self.button_idx = len(self.buttons) - 1
                        else:
                            self.button_idx -= 1

                    case pygame.K_DOWN:
                        if self.button_idx == len(self.buttons) - 1:
                            self.button_idx = 0
                        else:
                            self.button_idx += 1
                    case pygame.K_RETURN:
                        return self.__go_to_scene()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                return self.__go_to_scene()

    def __go_to_scene(self) -> None | SceneName:
        for i, button in enumerate(self.buttons):
            if button.rect.collidepoint(pygame.mouse.get_pos()) or i == self.button_idx:
                match button.name:
                    case "Play":
                        return SceneName.GAME
                    case "Scores":
                        return SceneName.SCOREBOARD
                    case "Exit":
                        pygame.quit()
                        exit()
