import pygame
from src.enums import Asset, DisplayInfo, SceneName
from src.models import Cursor, LetterButton, Scene, Text
from src.render import Renderer


class ScoreEntryScene(Scene):
    def __init__(self) -> None:
        print("initialize ScoreEntryScene")
        width, height = (
            DisplayInfo.SCREEN_WIDTH.value,
            DisplayInfo.SCREEN_HEIGHT.value,
        )

        self.text = Text("score entry", (width // 2, height // 4), "white")
        self.keyboard = self.__get_keyboard_letters()
        self.cursor = Cursor()

    def __get_keyboard_letters(
        self,
    ) -> list[LetterButton]:
        keyboard = []

        spacing = 10
        scale = 5

        letters_x = 10
        letters_y = 3

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
        y = DisplayInfo.SCREEN_HEIGHT.value // 2 - keyboard_height // 2

        place_x = 0
        place_y = 0

        line_count = 0

        for c in range(97, 123):
            if i % 10 == 0 and i != 0:
                line_count += 1
                y += spacing_height + letter_height
                i = 0
                x = DisplayInfo.SCREEN_WIDTH.value // 2 - keyboard_width // 2
                place_x = 0
                place_y += 1
                if line_count == 2:
                    x += (letter_width + spacing_width) * 2
                    place_x = 2
            surf = Renderer.scale_surface(
                pygame.image.load(f"{Asset.LETTER_PATH.value}/{chr(c)}.png"),
                (Asset.LETTER_WIDTH.value, Asset.LETTER_HEIGHT.value),
                scale,
            )
            letter = LetterButton(
                surf,
                chr(c),
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

        for letter in self.keyboard:
            # renderer.render(
            #     letter.hover_surf,
            #     Renderer.get_pos(letter.pos, (letter.w, letter.h)),
            # )
            renderer.render(
                letter.surf, Renderer.get_pos(letter.pos, letter.size)
            )

            if (
                self.cursor.x == letter.place[0]
                and self.cursor.y == letter.place[1]
            ):
                renderer.render(
                    self.cursor.surf,
                    Renderer.get_pos(letter.pos, (self.cursor.size)),
                )

    def __move_cursor(self, direction: str):
        match (self.cursor.x, self.cursor.y, direction):

            case (7, 2, "right"):
                self.cursor.x, self.cursor.y = (0, 0)
            case (9, 1, "right"):
                self.cursor.x, self.cursor.y = (2, 2)
            case (9, 0, "right"):
                self.cursor.x, self.cursor.y = (0, 1)

            case (0, 1, "left"):
                self.cursor.x, self.cursor.y = (9, 0)
            case (2, 2, "left"):
                self.cursor.x, self.cursor.y = (9, 1)
            case (0, 0, "left"):
                self.cursor.x, self.cursor.y = (7, 2)

            case (_, 0, "up") | (_, 1, "down"):
                if self.cursor.x >= 7:
                    self.cursor.x = 7
                elif self.cursor.x <= 2:
                    self.cursor.x = 2
                self.cursor.y = 2

            case (_, 2, "down"):
                self.cursor.y = 0

            case (_, _, "right"):
                self.cursor.x += 1
            case (_, _, "left"):
                self.cursor.x -= 1
            case (_, _, "up"):
                self.cursor.y -= 1
            case (_, _, "down"):
                self.cursor.y += 1

    def handle_events(self, events: list[pygame.Event]) -> None | SceneName:
        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                return SceneName.MAIN_MENU
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return SceneName.MAIN_MENU
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
