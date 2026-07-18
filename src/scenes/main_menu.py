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

    def render_scene(self, screen) -> None:
        for button in self.buttons:
            is_sellected = button.rect.collidepoint(pygame.mouse.get_pos())
            thickness = 10
            if is_sellected:
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

            if event.type != pygame.MOUSEBUTTONDOWN:
                continue

            for button in self.buttons:

                if not button.rect.collidepoint(pygame.mouse.get_pos()):
                    continue

                match button.name:
                    case "Play":
                        return SceneName.GAME
                    case "Scores":
                        return SceneName.SCOREBOARD
                    case "Exit":
                        pygame.quit()
                        exit()
