import pygame
from src.enums import SceneName
from src.models import Scene
from src.models import Button
from src.render import Renderer


class MainMenuScene(Scene):
    def __init__(self) -> None:
        print("initialize MainMenuScene")

        self.buttons: list[Button] = []

        for i, lable in enumerate(["play", "scores", "option", "exit"]):

            self.buttons.append(Button(lable, (10, 10)))

        self.button_idx = 0

    def render_scene(self, renderer: Renderer) -> None:
        spacing = 120

        x = renderer.screen_h // 2
        for i, button in enumerate(self.buttons):

            y = renderer.screen_w // 2 + i * spacing

            if self.button_idx == i:
                renderer.render(button.hover, (x, y), button.size)

            else:
                renderer.render(button.idel, (x, y), button.size)

            renderer.render(button.text.surf, (x, y), button.text.size)

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

            # elif event.type == pygame.MOUSEMOTION:

            #     for i, button in enumerate(self.buttons):
            #         if button.is_collide(pygame.mouse.get_pos()):
            #             self.button_idx = i

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return self.__go_to_scene()

    def __go_to_scene(self) -> None | SceneName:
        for i, button in enumerate(self.buttons):
            if i == self.button_idx:
                match button.name:
                    case "play":
                        return SceneName.GAME
                    case "scores":
                        return SceneName.SCOREBOARD
                    case "option":
                        return SceneName.OPTIONS
                    case "exit":
                        pygame.quit()
                        exit()
