import json
import pygame
from typing import Any
from pathlib import Path
from src.parsing import Parser
from src.render import Renderer
from src.enums import AnchorPoint, Asset, ColorType, DisplayInfo
from src.models import SceneTitle, Cursor, LetterButton, NameFrame, Scene, Text


class ScoreEntryScene(Scene):
    def __init__(self, heighscores_path: Path, score: int) -> None:
        self.heighscores_path = heighscores_path
        self.score = score
        self.__init_elements()

    def __init_elements(self) -> None:

        screen_width = DisplayInfo.SCREEN_WIDTH.value
        screen_height = DisplayInfo.SCREEN_HEIGHT.value

        self.score_text = Text(
            f"your score is {self.score}",
            (screen_width // 2, screen_height // 2 - 200),
            ColorType.PRIMARY,
        )

        self.title = SceneTitle("score entry")
        self.keyboard = self.__get_keyboard_letters()
        self.cursor = Cursor()
        self.name_frame = NameFrame()

    def __get_keyboard_letters(
        self,
    ) -> list[LetterButton]:
        keyboard = []

        spacing = 10

        letters_x = 10
        letters_y = 5

        spacing_width = spacing * 5
        spacing_height = spacing * 5

        letter_width = Asset.LETTER_WIDTH.value
        letter_height = Asset.LETTER_HEIGHT.value

        keyboard_width = letter_width * letters_x + (
            spacing_width * (letters_x - 1)
        )
        keyboard_height = letter_height * letters_y + spacing_height * (
            letters_y - 1
        )

        i = 0
        x = DisplayInfo.SCREEN_WIDTH.value // 2 - keyboard_width // 2
        y = DisplayInfo.SCREEN_HEIGHT.value - keyboard_height

        place_x = 0
        place_y = 0

        for c in "0123456789abcdefghijklmnopqrstuvwxyz E":
            if i % 10 == 0 and i != 0:
                y += spacing_height + letter_height
                i = 0
                x = DisplayInfo.SCREEN_WIDTH.value // 2 - keyboard_width // 2
                place_x = 0
                place_y += 1
            if c == "E":
                surf = Renderer.LETTER[c]
            else:
                surf = Renderer.LETTER[c]

            letter = LetterButton(
                surf,
                c,
                (x, y),
                (letter_width, letter_height),
                (place_x, place_y),
            )

            keyboard.append(letter)

            x += letter_width + spacing_width
            place_x += 1
            i += 1

        return keyboard

    def render_scene(self, renderer: Renderer) -> None:

        self.title.render(renderer)
        renderer.render(
            self.score_text.surf,
            Renderer.get_pos(self.score_text.pos, self.score_text.size),
        )

        renderer.render(
            self.name_frame.surf,
            Renderer.get_pos(self.name_frame.pos, self.name_frame.size),
        )
        if self.name_frame.name != "":
            renderer.render(
                self.name_frame.text.surf,
                Renderer.get_pos(
                    self.name_frame.text.pos, self.name_frame.text.size
                ),
            )

        for letter in self.keyboard:

            renderer.render(
                letter.surf, Renderer.get_pos(letter.pos, letter.size)
            )

            if (
                self.cursor.x == letter.place[0]
                and self.cursor.y == letter.place[1]
            ):
                if self.cursor.is_wide:
                    width, height = Renderer.get_pos(
                        letter.pos,
                        (self.cursor.wide_size),
                        AnchorPoint.CENTER_LEFT,
                    )
                    width -= letter.size[0]
                    renderer.render(self.cursor.wide_surf, (width, height))
                else:
                    renderer.render(
                        self.cursor.surf,
                        Renderer.get_pos(letter.pos, (self.cursor.size)),
                    )

    def __move_cursor(self, key: int):
        x = self.cursor.x
        y = self.cursor.y

        match (x, y, key):

            case (7, 3, pygame.K_UP):
                self.cursor.x, self.cursor.y = (9, 2)

            case (_, 3, pygame.K_DOWN):
                self.cursor.x, self.cursor.y = (9, 0) if x == 7 else (x, 0)

            case (_, 2, pygame.K_DOWN) | (_, 0, pygame.K_UP):
                self.cursor.x, self.cursor.y = (7, 3) if x >= 7 else (x, 3)

            case (9, _, pygame.K_RIGHT) | (7, 3, pygame.K_RIGHT):
                self.cursor.x = 0

            case (0, _, pygame.K_LEFT):
                self.cursor.x = 7 if y == 3 else 9

            case (_, _, pygame.K_RIGHT):
                self.cursor.x += 1
            case (_, _, pygame.K_LEFT):
                self.cursor.x -= 1
            case (_, _, pygame.K_UP):
                self.cursor.y -= 1
            case (_, _, pygame.K_DOWN):
                self.cursor.y += 1

        for button in self.keyboard:
            if button.place == (self.cursor.x, self.cursor.y):
                self.cursor.x, self.cursor.y = button.place
                self.cursor.is_wide = self.cursor.y == 3 and self.cursor.x >= 7
                self.cursor.letter_hover = button.letter

    def __save_score(self) -> None:
        score, name = self.score, self.name_frame.name
        try:
            scores = json.loads(Parser.get_file_content(self.heighscores_path))
            old_score = scores.get(name)

            if old_score and score <= old_score:
                return
            scores[name] = score

            with open(self.heighscores_path, "w") as f:
                json.dump(scores, f, indent=4)

            print(
                "Saved new score in",
                self.heighscores_path,
                "successfuly.",
            )

        except OSError as e:
            print("File:", self.heighscores_path.absolute())
            print(f"Error: {e.strerror}")

    def __press_action(self) -> bool:

        if self.cursor.letter_hover == "E":
            if self.name_frame.name != "":
                self.__save_score()
                return True
            return False

        if len(self.name_frame.name) < 10:
            self.name_frame.update_name(self.cursor.letter_hover)
            return False

        return False

    def __press_return(self) -> dict[str, Any]:

        if self.__press_action():
            return {
                "pop": True,
                "new_recorder": (self.name_frame.name, self.score),
            }
        return {}

    def __handle_mouse_motion(self) -> bool:
        for letter_button in self.keyboard:
            if letter_button.is_collide(pygame.mouse.get_pos()):

                self.cursor.x, self.cursor.y = letter_button.place
                self.cursor.is_wide = self.cursor.y == 3 and self.cursor.x >= 7
                self.cursor.letter_hover = letter_button.letter
                return True

        return False

    def __handle_mouse_click(self) -> dict[str, Any]:

        # check if mouse click on letter button
        if not self.__handle_mouse_motion():
            return {}

        if self.__press_action():
            return {
                "pop": True,
                "new_recorder": (self.name_frame.name, self.score),
            }

        return {}

    def handle_events(self, events: list[pygame.Event]) -> dict[str, Any]:
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
