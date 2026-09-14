import time
from typing import Any
import pygame
from src.enums import ColorType, DisplayInfo
from src.models import Scene, SceneTitle, Text
from src.render import Renderer


class InfoScene(Scene):
    def __init__(self) -> None:
        self.__init_elements()
        self.last_time = time.perf_counter()

    def __init_elements(self):
        screen_width = DisplayInfo.SCREEN_WIDTH.value
        screen_height = DisplayInfo.SCREEN_HEIGHT.value

        self.title = SceneTitle("instrucions", hide_top=True)
        self.body_text: list[Text] = []

        x = screen_width // 2
        y = screen_height // 2 - 400
        self.current_y = 0

        for text in [
            ("use arrow keys to navigait",),
            ("wins the level when all", "pacgums are eaten"),
            ("wins the game when all", "levels are completed"),
            ("getting touched by a ghost", "costs a life"),
            ("eat super gum to eat ghosts", "temporarily"),
        ]:
            y += 80
            for line in text:
                y += 60
                self.body_text.append(
                    Text(
                        line,
                        (x, y),
                        ColorType.PRIMARY,
                    )
                )

    def __get_delta(self):
        current_time = time.perf_counter()
        delta = current_time - self.last_time
        self.last_time = current_time
        return delta

    def __repr__(self) -> str:
        return "InfoScene"

    def render_scene(self, renderer: Renderer) -> None:

        for text in self.body_text:
            x, y = text.pos
            renderer.render(
                text.surf,
                Renderer.get_pos((x, y + int(self.current_y)), text.size),
            )
        self.title.render(renderer)

    def __handle_key_scroll(self, delta: float):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.current_y += delta * 300
        elif keys[pygame.K_DOWN]:
            self.current_y -= delta * 300

    def __handle_mouse_scroll(self, y_event: int, delta: float):

        if y_event == 1:
            self.current_y += delta * 300 * 50
        elif y_event == -1:
            self.current_y -= delta * 300 * 50

    def handle_events(self, events: list[pygame.Event]) -> dict[str, Any]:
        delta = self.__get_delta()
        self.__handle_key_scroll(delta)

        for event in events:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return {"pop": True}
            if event.type == pygame.MOUSEWHEEL:
                self.__handle_mouse_scroll(event.y, delta)

        return {}
