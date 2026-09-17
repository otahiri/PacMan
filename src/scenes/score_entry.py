"""Scene for entering a player name and saving a new score."""

import json
import pygame
from typing import Any
from pathlib import Path
from src.parsing import Parser
from src.render import Renderer
from src.enums import ColorType, DisplayInfo
from src.models import (
    Keyboard,
    SceneTitle,
    NameFrame,
    Scene,
    Text,
)


class ScoreEntryScene(Scene):
    """Keyboard-based score entry form for saving a new result.

    Args:
        highscores_path: Path to the leaderboard JSON file.
        score: The score to save.
    """

    def __init__(self, highscores_path: Path, score: int) -> None:
        self.highscores_path = highscores_path
        self.score = score
        self.__init_elements()

    def __init_elements(self) -> None:
        """Build the title, score label, keyboard, and name frame."""
        screen_width = DisplayInfo.SCREEN_WIDTH.value
        screen_height = DisplayInfo.SCREEN_HEIGHT.value

        self.score_text = Text(
            f"your score is {self.score}",
            (screen_width // 2, screen_height // 2 - 200),
            ColorType.PRIMARY,
        )

        self.title = SceneTitle("score entry")
        self.keyboard = Keyboard()
        self.name_frame = NameFrame()

    def render_scene(self, renderer: Renderer) -> None:
        """Render the score entry screen.

        Args:
            renderer: Renderer used to draw the scene.
        """
        self.title.render(renderer)
        renderer.render(
            self.score_text.surf,
            Renderer.get_pos(self.score_text.pos, self.score_text.size),
        )

        renderer.render(
            self.name_frame.surf,
            Renderer.get_pos(self.name_frame.pos, self.name_frame.size),
        )
        renderer.render(
            self.name_frame.text.surf,
            Renderer.get_pos(
                self.name_frame.text.pos, self.name_frame.text.size
            ),
        )
        self.keyboard.render(renderer)

    def __update_cursor_pos(self) -> None:
        """Update the keyboard cursor with the currently hovered letter."""
        for button in self.keyboard.letters:
            if button.place == (
                self.keyboard.cursor.x,
                self.keyboard.cursor.y,
            ):
                self.keyboard.cursor.x, self.keyboard.cursor.y = button.place
                self.keyboard.cursor.is_wide = (
                    self.keyboard.cursor.y == 3 and self.keyboard.cursor.x >= 7
                )
                self.keyboard.cursor.letter_hover = button.letter

    def __move_cursor(self, key: int) -> None:
        """Move the keyboard cursor using the provided arrow-key input.

        Args:
            key: Pygame keyboard constant for the pressed key.
        """
        x = self.keyboard.cursor.x
        y = self.keyboard.cursor.y

        match (x, y, key):

            case (7, 3, pygame.K_UP):
                self.keyboard.cursor.x, self.keyboard.cursor.y = (9, 2)

            case (_, 3, pygame.K_DOWN):
                self.keyboard.cursor.x, self.keyboard.cursor.y = (
                    (9, 0) if x == 7 else (x, 0)
                )

            case (_, 2, pygame.K_DOWN) | (_, 0, pygame.K_UP):
                self.keyboard.cursor.x, self.keyboard.cursor.y = (
                    (7, 3) if x >= 7 else (x, 3)
                )

            case (9, _, pygame.K_RIGHT) | (7, 3, pygame.K_RIGHT):
                self.keyboard.cursor.x = 0

            case (0, _, pygame.K_LEFT):
                self.keyboard.cursor.x = 7 if y == 3 else 9

            case (_, _, pygame.K_RIGHT):
                self.keyboard.cursor.x += 1
            case (_, _, pygame.K_LEFT):
                self.keyboard.cursor.x -= 1
            case (_, _, pygame.K_UP):
                self.keyboard.cursor.y -= 1
            case (_, _, pygame.K_DOWN):
                self.keyboard.cursor.y += 1

        self.__update_cursor_pos()

    def __save_score(self) -> None:
        """Save the current score under the entered player name."""
        score, name = self.score, self.name_frame.name
        try:
            scores = json.loads(Parser.get_file_content(self.highscores_path))
            old_score = scores.get(name)

            if old_score and score <= old_score:
                return
            scores[name] = score

            with open(self.highscores_path, "w") as f:
                json.dump(scores, f, indent=4)

        except OSError as e:
            print("File:", self.highscores_path.absolute())
            print(f"Error: {e.strerror}")

    def __press_action(self) -> bool:
        """Apply the current keyboard selection as a letter or name save action.

        Returns:
            True when the save action is confirmed; otherwise False.
        """
        if self.keyboard.cursor.letter_hover == "E":
            if self.name_frame.name != "":
                self.__save_score()
                return True
            return False

        if len(self.name_frame.name) < 10:
            self.name_frame.update_name(self.keyboard.cursor.letter_hover)
            return False

        return False

    def __press_return(self) -> dict[str, Any]:
        """Handle the Enter key by saving the score if a valid name is ready.

        Returns:
            A dictionary with exit and new record when the score is
            saved; otherwise an empty dict.
        """
        if self.__press_action():
            return {
                "pop": True,
                "new_record": (self.name_frame.name, self.score),
            }
        return {}

    def __handle_mouse_motion(self) -> bool:
        """Update the cursor based on the mouse position over keyboard letters.

        Returns:
            True when the mouse is over a letter button; otherwise False.
        """
        for letter_button in self.keyboard.letters:
            if letter_button.is_collide(pygame.mouse.get_pos()):

                self.keyboard.cursor.x, self.keyboard.cursor.y = (
                    letter_button.place
                )
                self.keyboard.cursor.is_wide = (
                    self.keyboard.cursor.y == 3 and self.keyboard.cursor.x >= 7
                )
                self.keyboard.cursor.letter_hover = letter_button.letter
                return True

        return False

    def __handle_mouse_click(self) -> dict[str, Any]:
        """Handle a mouse click on the keyboard and save if a name is complete.

        Returns:
            A navigation instructions when the score is saved; otherwise an empty
            dict.
        """

        if not self.__handle_mouse_motion():
            return {}

        if self.__press_action():
            return {
                "pop": True,
                "new_record": (self.name_frame.name, self.score),
            }

        return {}

    def handle_events(self, events: list[pygame.Event]) -> dict[str, Any]:
        """Process keyboard and mouse input for the score entry scene.

        Args:
            events: Pygame events for the current frame.

        Returns:
            A dictionary with exit info or an empty dict.
        """
        for event in events:

            match event.type:
                case pygame.KEYDOWN:

                    if event.key == pygame.K_RETURN:
                        return self.__press_return()

                    else:
                        self.__move_cursor(event.key)

                case pygame.MOUSEMOTION:
                    self.__handle_mouse_motion()

                case pygame.MOUSEBUTTONDOWN:
                    if event.button != 1:
                        return {}
                    return self.__handle_mouse_click()

        return {}
