import json
from pathlib import Path
import sys

import pygame
from typing import Any
from src.enums import Asset, DisplayInfo, SceneName
from src.models import Cursor, LetterButton, NameFrame, Scene, Text
from src.parsing import Parser
from src.render import Renderer


class ScoreEntryScene(Scene):
    def __init__(self, heighscores_path: Path) -> None:
        print("initialize ScoreEntryScene")
        width, height = (
            DisplayInfo.SCREEN_WIDTH.value,
            DisplayInfo.SCREEN_HEIGHT.value,
        )
        self.heighscores_path = heighscores_path
        self.text = Text("score entry", (width // 2, height // 6), "white")
        self.score: int = 0
        self.score_text = Text(
            "your score is 0", (width // 2, height // 2 - 200), "white"
        )

        self.keyboard = self.__get_keyboard_letters()
        self.cursor = Cursor()
        self.name_frame = NameFrame()

    def __get_keyboard_letters(
        self,
    ) -> list[LetterButton]:
        keyboard = []

        spacing = 10
        scale = 5

        letters_x = 10
        letters_y = 5

        spacing_width = spacing * scale
        spacing_height = spacing * scale

        letter_width = Asset.LETTER_WIDTH.value * scale
        letter_height = Asset.LETTER_HEIGHT.value * scale

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

            letter_path = f"{Asset.LETTER_PATH.value}/{c}.png"

            if c == " ":
                letter_path = f"{Asset.LETTER_PATH.value}/space.png"

            if c == "E":
                surf = Text("enter", (x, y), "white").surf
            else:
                surf = Renderer.scale_surface(
                    pygame.image.load(letter_path),
                    (Asset.LETTER_WIDTH.value, Asset.LETTER_HEIGHT.value),
                    scale,
                )
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

        renderer.render(
            self.text.surf,
            Renderer.get_pos(self.text.pos, self.text.size),
        )

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
                        letter.pos, (self.cursor.wide_size), "leftcenter"
                    )
                    width -= letter.size[0]
                    renderer.render(self.cursor.wide_surf, (width, height))
                else:
                    renderer.render(
                        self.cursor.surf,
                        Renderer.get_pos(letter.pos, (self.cursor.size)),
                    )

    def __move_cursor(self, direction: str):
        x = self.cursor.x
        y = self.cursor.y

        match (x, y, direction):

            case (7, 3, "up"):
                self.cursor.x, self.cursor.y = (9, 2)

            case (_, 3, "down"):
                self.cursor.x, self.cursor.y = (9, 0) if x == 7 else (x, 0)

            case (_, 2, "down") | (_, 0, "up"):
                self.cursor.x, self.cursor.y = (7, 3) if x >= 7 else (x, 3)

            case (9, _, "right") | (7, 3, "right"):
                self.cursor.x = 0

            case (0, _, "left"):
                self.cursor.x = 7 if y == 3 else 9

            case (_, _, "right"):
                self.cursor.x += 1
            case (_, _, "left"):
                self.cursor.x -= 1
            case (_, _, "up"):
                self.cursor.y -= 1
            case (_, _, "down"):
                self.cursor.y += 1

        for button in self.keyboard:
            if button.place == (self.cursor.x, self.cursor.y):
                self.cursor.x, self.cursor.y = button.place
                self.cursor.is_wide = self.cursor.y == 3 and self.cursor.x >= 7
                self.cursor.letter_hover = button.letter

    def __save_score(self):
        score, name = self.score, self.name_frame.name
        try:
            scores = json.loads(Parser.get_file_content(self.heighscores_path))
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
            self.__save_score()
            return True
        if len(self.name_frame.name) < 10:
            self.name_frame.update_name(self.cursor.letter_hover)
        return False

    def get_scene_arguments(self, arguments: dict[str, Any]) -> None:
        score = arguments.get("score")
        width, height = (
            DisplayInfo.SCREEN_WIDTH.value,
            DisplayInfo.SCREEN_HEIGHT.value,
        )
        if score:

            self.score = score
            self.score_text = Text(
                f"your score is {score}",
                (width // 2, height // 6 - 100),
                "white",
            )

    def handle_events(self, events: list[pygame.Event]) -> dict[str, Any]:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.__press_action():
                        return {"next_scene": SceneName.MAIN_MENU}

                elif event.key == pygame.K_RIGHT:
                    self.__move_cursor("right")

                elif event.key == pygame.K_LEFT:
                    self.__move_cursor("left")

                elif event.key == pygame.K_UP:
                    self.__move_cursor("up")
                elif event.key == pygame.K_DOWN:
                    self.__move_cursor("down")
            elif event.type == pygame.MOUSEMOTION:
                for button in self.keyboard:
                    if button.is_collide(pygame.mouse.get_pos()):
                        self.cursor.x, self.cursor.y = button.place
                        self.cursor.is_wide = (
                            self.cursor.y == 3 and self.cursor.x >= 7
                        )
                        self.cursor.letter_hover = button.letter

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.__press_action():
                    return {"next_scene": SceneName.MAIN_MENU}
        return {"next_scene": None}
