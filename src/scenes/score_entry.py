import pygame
from src.enums import Asset, DisplayInfo, SceneName
from src.models import Scene, Text
from src.render import Renderer


class ScoreEntryScene(Scene):
    def __init__(self) -> None:
        print("initialize ScoreEntryScene")
        width, height = (
            DisplayInfo.SCREEN_WIDTH.value,
            DisplayInfo.SCREEN_HEIGHT.value,
        )

        self.text = Text("score entry", (width // 2, height // 4), "white")
        self.keyboard, self.keyboard_size = self.__get_keyboard_surface()

    def __get_keyboard_surface(self):

        spacing = 10
        scale = 5
        width = (Asset.LETTER_WIDTH.value + spacing) * scale
        height = (Asset.LETTER_HEIGHT.value + spacing) * scale
        size = (width * 10, height * 3)
        keyboard = pygame.Surface(size)

        i = 0
        x = 0
        y = 0
        line_count = 0
        # 26 alphabet
        for c in range(97, 123):
            if i % 10 == 0 and i != 0:
                line_count += 1
                y += height
                i = 0
                x = 0
                if line_count == 2:
                    x += width * 2
            text = Text(chr(c), (x, y), "white")
            keyboard.blit(text.surf, (x, y))
            x += width
            i += 1

        return (keyboard, size)

    def render_scene(self, renderer: Renderer) -> None:
        renderer.render(
            self.text.surf,
            self.text.get_pos(),
        )
        renderer.render(
            self.keyboard,
            Renderer.get_pos(
                (640, 640),
                self.keyboard_size,
            ),
        )

    def handle_events(self, events: list[pygame.Event]) -> None | SceneName:
        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                return SceneName.MAIN_MENU
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return SceneName.MAIN_MENU
