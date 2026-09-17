"""Instructions scene used to display game rules and controls."""

import time
from typing import Any
import pygame
from src.enums import ColorType, DisplayInfo
from src.models import Scene, SceneTitle, Text
from src.render import Renderer


class InfoScene(Scene):
    """Scrolling instructions screen with gameplay help text."""

    def __init__(self) -> None:

        self.__init_elements()
        self.last_time = time.perf_counter()

    def __init_elements(self) -> None:
        """Build the instruction text and title for the scene."""
        screen_width = DisplayInfo.SCREEN_WIDTH.value
        screen_height = DisplayInfo.SCREEN_HEIGHT.value

        self.title = SceneTitle("instrucions", hide_top=True)
        self.body_text: list[Text] = []

        x = screen_width // 2
        y = screen_height // 2 - 400
        self.current_y = 0.0

        for text in [
            (
                "use wasd or arrow keys to",
                "navigait through the maze",
            ),
            ("wins the level when all", "pacgums are eaten"),
            ("wins the game when all", "levels are completed"),
            (
                "each level has a time limit",
                "120 in normal mode",
                "90 in hardcore mode",
            ),
            ("getting touched by a ghost", "costs a life"),
            ("eating a pacgum increases", "the score by 10"),
            (
                "eating a super pacgum",
                "increases the score by 100",
                "and makes ghosts edible for",
                "a short time",
            ),
            (
                "eating an edible ghost",
                "increases the score by 100",
            ),
            ("your goal is to achive", "the maximum score"),
            ("ghosts respawn to their", "corner after a while", "when eaten"),
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

    def __get_delta(self) -> float:
        """Return elapsed time since the last frame.

        Returns:
            Time delta in seconds for smooth scroll movement.
        """
        current_time = time.perf_counter()
        delta = current_time - self.last_time
        self.last_time = current_time
        return delta

    def render_scene(self, renderer: Renderer) -> None:
        """Render the instruction text and title.

        Args:
            renderer: Renderer used to draw the scene.
        """
        for text in self.body_text:
            x, y = text.pos
            renderer.render(
                text.surf,
                Renderer.get_pos((x, y + int(self.current_y)), text.size),
            )
        self.title.render(renderer)

    def __handle_key_scroll(self, delta: float) -> None:
        """Scroll the instructions using keyboard input.

        Args:
            delta: Elapsed time since the last frame.
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.current_y += delta * 300
        elif keys[pygame.K_DOWN]:
            self.current_y -= delta * 300

    def __handle_mouse_scroll(self, y_event: int, delta: float) -> None:
        """Scroll the instructions using mouse wheel events.

        Args:
            y_event: Wheel event direction value.
            delta: Elapsed time since the last frame.
        """
        if y_event == 1:
            self.current_y += delta * 300 * 50
        elif y_event == -1:
            self.current_y -= delta * 300 * 50

    def handle_events(self, events: list[pygame.Event]) -> dict[str, Any]:
        """Handle key, mouse wheel, and click events for the info scene.

        Args:
            events: List of pygame events to process.

        Returns:
            A dictionary with a `pop` action or an empty dict if the scene
            stays active.
        """
        delta = self.__get_delta()
        self.__handle_key_scroll(delta)

        for event in events:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return {"pop": True}

            elif event.type == pygame.MOUSEWHEEL:
                self.__handle_mouse_scroll(event.y, delta)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return {"pop": True}
        return {}
