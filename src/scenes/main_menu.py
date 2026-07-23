import pygame
from src.enums import DisplayInfo, SceneName
from src.models import Scene, Text
from src.models import Button


class MainMenuScene(Scene):
    def __init__(self) -> None:
        print("initialize MainMenuScene")
        self.buttons = []

        x = DisplayInfo.SCREEN_WIDTH.value // 2

        for i, lable in enumerate(["Play", "Scores", "Exit"]):

            y = DisplayInfo.SCREEN_HEIGHT.value // 2 + 150 * i

            self.buttons.append(Button(lable, (x, y)))

        self.button_idx = 0

        self.text = Text("hello")

    def render_scene(self, renderer) -> None:
        for i, button in enumerate(self.buttons):

            if self.button_idx == i:
                renderer.render(button.hover, (button.x, button.y))

            else:
                renderer.render(button.idel, (button.x, button.y))
        self.text.render(
            renderer,
            (
                DisplayInfo.SCREEN_WIDTH.value // 2,
                DisplayInfo.SCREEN_HEIGHT.value // 2,
            ),
        )

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

            elif event.type == pygame.MOUSEMOTION:

                for i, button in enumerate(self.buttons):
                    if button.is_collide(pygame.mouse.get_pos()):
                        self.button_idx = i

            elif event.type == pygame.MOUSEBUTTONDOWN:
                return self.__go_to_scene()

    def __go_to_scene(self) -> None | SceneName:
        for i, button in enumerate(self.buttons):
            if i == self.button_idx:
                match button.name:
                    case "Play":
                        return SceneName.GAME
                    case "Scores":
                        return SceneName.SCOREBOARD
                    case "Exit":
                        pygame.quit()
                        exit()
