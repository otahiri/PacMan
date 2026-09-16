from typing import Any
import pygame
from abc import ABC, abstractmethod
from src.enums import AnchorPoint, Asset, ColorType, DisplayInfo
from src.render import Renderer


class Button:

    def __init__(self, name: str, pos: tuple[int, int]) -> None:
        self.name = name
        x, y = pos

        self.surf, size = Renderer.get_button()

        self.width, self.height = size

        self.pos = (x - self.width // 2, y - self.height // 2)

        self.text_on = Text(name, pos, ColorType.SECONDARY)
        self.text_off = Text(name, pos, ColorType.PRIMARY)
        self.button_state = False

    def is_collide(self, pos: tuple[int, int]) -> bool:
        my_x, my_y = self.pos
        target_x, target_y = pos
        is_inside_x = my_x <= target_x <= (my_x + self.width)
        is_inside_y = my_y <= target_y <= (my_y + self.height)
        return is_inside_x and is_inside_y

    def switch_state(self) -> None:
        self.button_state = not self.button_state

    def render(self, renderer: Renderer) -> None:

        if self.button_state is True:
            renderer.render(self.surf, self.pos)
            renderer.render(
                self.text_on.surf,
                Renderer.get_pos(self.text_on.pos, self.text_on.size),
            )
        else:
            renderer.render(
                self.text_off.surf,
                Renderer.get_pos(self.text_off.pos, self.text_off.size),
            )


class Text:

    def __init__(
        self,
        label: str,
        pos: tuple[int, int],
        color_type: ColorType,
        anchor_point: AnchorPoint = AnchorPoint.CENTER,
    ) -> None:

        self.label = label
        self.pos = pos
        self.surf, self.size = Renderer.get_text(label, color_type)
        self.anchor_point = anchor_point


class SceneTitle:

    def __init__(
        self, label: str, pos: str = "top", hide_top: bool = False
    ) -> None:

        screen_width = DisplayInfo.SCREEN_WIDTH.value
        screen_height = DisplayInfo.SCREEN_HEIGHT.value
        self.hide_top = hide_top
        y_pos = 0

        if pos == "top":
            y_pos = screen_height // 6

        elif pos == "center":
            y_pos = screen_height // 2

        self.text = Text(
            label,
            (screen_width // 2, y_pos),
            ColorType.SECONDARY,
        )

        bar_size = (screen_width, 60)

        self.bar_surf = pygame.Surface(bar_size)
        Renderer.fill(self.bar_surf, ColorType.PRIMARY)
        self.bar_pos = Renderer.get_pos(
            (0, y_pos), bar_size, AnchorPoint.CENTER_LEFT
        )

        if hide_top:
            bg_size = (screen_width, y_pos)
            self.bg = pygame.Surface(bg_size)
            Renderer.fill(self.bg, ColorType.SECONDARY)
            self.bg_pos = Renderer.get_pos(
                (0, y_pos), bg_size, AnchorPoint.BOTTOM_LEFT
            )

    def render(self, renderer: Renderer) -> None:
        if self.hide_top:
            renderer.render(self.bg, self.bg_pos)

        renderer.render(self.bar_surf, self.bar_pos)

        renderer.render(
            self.text.surf,
            Renderer.get_pos(self.text.pos, self.text.size),
        )


class AnimatedBar:
    def __init__(self, label: str, gap: int, speed: int) -> None:
        screen_width = DisplayInfo.SCREEN_WIDTH.value
        screen_height = DisplayInfo.SCREEN_HEIGHT.value
        self.y_pos = screen_height - 10
        self.speed = speed
        self.gap = gap
        self.x1: float = screen_width + screen_width // 2

        self.y = self.y_pos

        self.text = Text(
            label,
            (self.x1, self.y_pos - 10),
            ColorType.SECONDARY,
            AnchorPoint.BOTTOM_RIGHT,
        )

        self.bar = pygame.Surface((screen_width, 60))
        Renderer.fill(self.bar, ColorType.PRIMARY)
        self.bar_pos = (0, self.y_pos - Asset.LETTER_HEIGHT.value - 10)

        self.text_width = self.text.size[0]
        self.x2: float = self.x1 - self.text_width - self.gap

    def reset_pos(self) -> None:
        screen_width = DisplayInfo.SCREEN_WIDTH.value

        self.x1 = screen_width + screen_width // 2
        self.x2 = self.x1 - self.text_width - self.gap

    def render(self, renderer: Renderer, delta: float) -> None:
        self.x1 -= delta * self.speed
        if self.x1 + self.gap <= 0:
            self.x1 = self.x2 + self.text_width + self.gap

        self.x2 -= delta * self.speed

        if self.x2 + self.gap <= 0:
            self.x2 = self.x1 + self.text_width + self.gap

        renderer.render(
            self.bar,
            self.bar_pos,
        )
        renderer.render(
            self.text.surf,
            Renderer.get_pos(
                (int(self.x1), self.y),
                self.text.size,
                self.text.anchor_point,
            ),
        )

        renderer.render(
            self.text.surf,
            Renderer.get_pos(
                (int(self.x2), self.y),
                self.text.size,
                self.text.anchor_point,
            ),
        )


class LetterButton:

    def __init__(
        self,
        surf: pygame.Surface,
        letter: str,
        pos: tuple[int, int],
        size: tuple[int, int],
        place: tuple[int, int],
    ) -> None:
        self.surf = Renderer.change_color(surf)
        self.letter = letter
        self.pos = pos
        self.size = size
        self.place = place

    def is_collide(self, pos: tuple[int, int]) -> bool:

        width, height = self.size

        width *= 2
        height *= 2
        my_x, my_y = Renderer.get_pos(self.pos, (width, height))
        if self.letter == "E":
            width *= 3
        target_x, target_y = pos
        is_inside_x = my_x <= target_x <= (my_x + width)
        is_inside_y = my_y <= target_y <= (my_y + height)
        return is_inside_x and is_inside_y


class Keyboard:
    def __init__(self) -> None:

        self.letters: list[LetterButton] = []
        self.cursor = Cursor()
        self.__set_keyboard_letters()

    def __set_keyboard_letters(
        self,
    ) -> None:

        screen_width = DisplayInfo.SCREEN_WIDTH.value
        screen_height = DisplayInfo.SCREEN_HEIGHT.value

        spacing = 50

        letters_x_number = 10
        letters_y_number = 4

        letter_width = Asset.LETTER_WIDTH.value
        letter_height = Asset.LETTER_HEIGHT.value

        # calculate all letters plus the spaces between theme minus the last space
        keyboard_width = (letter_width * (letters_x_number - 1)) + (
            spacing * (letters_x_number - 1)
        )
        keyboard_height = (letter_height * (letters_y_number - 1)) + (
            spacing * (letters_y_number - 1)
        )

        # x, y pos for keyboard that will init the x, y pos
        keyboard_x = screen_width // 2 - keyboard_width // 2
        keyboard_y = screen_height - keyboard_height - 100

        place_x = 0
        place_y = 0

        letter_x = keyboard_x
        letter_y = keyboard_y

        for letter_idx, letter in enumerate(
            "0123456789abcdefghijklmnopqrstuvwxyz E"
        ):
            # when finish each 10 letters go to next line
            if letter_idx % 10 == 0 and letter_idx != 0:
                letter_y += spacing + letter_height
                letter_x = keyboard_x
                place_x = 0
                place_y += 1

            surf = Renderer.LETTER[letter]

            letter = LetterButton(
                surf,
                letter,
                (letter_x, letter_y),
                (letter_width, letter_height),
                (place_x, place_y),
            )

            self.letters.append(letter)

            letter_x += letter_width + spacing
            place_x += 1

    def render(self, renderer: Renderer):
        for letter in self.letters:

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


class Cursor:
    def __init__(
        self,
    ) -> None:

        width = Asset.CURSOR_WIDTH.value
        height = Asset.CURSOR_WIDTH.value

        wide_width = Asset.CURSOR_WIDE_WIDTH.value
        wide_height = Asset.CURSOR_WIDE_HEIGHT.value

        self.wide_size = (wide_width, wide_height)
        self.size = (width, height)

        self.surf = Renderer.load_image(f"{Asset.CURSOR_PATH.value}.png")

        self.wide_surf = Renderer.load_image(
            f"{Asset.CURSOR_WIDE_PATH.value}.png"
        )

        self.size = (width, height)

        wide_width = Asset.CURSOR_WIDE_WIDTH.value
        wide_height = Asset.CURSOR_WIDE_HEIGHT.value
        self.wide_size = (wide_width, wide_height)

        self.is_wide = False
        self.x = 0
        self.y = 0
        self.letter_hover = "0"


class NameFrame:
    def __init__(self) -> None:
        width, height = (
            Asset.NAME_FRAME_WIDTH.value,
            Asset.NAME_FRAME_HEIGHT.value,
        )
        self.surf = Renderer.change_color(
            pygame.image.load(f"{Asset.NAME_FRAME_PATH.value}.png")
        )
        self.size = (width, height)
        self.pos = (
            DisplayInfo.SCREEN_WIDTH.value // 2,
            DisplayInfo.SCREEN_HEIGHT.value // 2,
        )

        self.name = ""
        self.text = Text(" ", self.pos, ColorType.PRIMARY)

    def update_name(self, letter: str) -> None:
        self.name += letter
        self.text = Text(self.name, self.pos, ColorType.PRIMARY)


class Scene(ABC):
    @abstractmethod
    def render_scene(self, renderer: Renderer) -> None: ...

    @abstractmethod
    def handle_events(self, events: list[pygame.Event]) -> dict[str, Any]: ...


class Corner:
    """corner object to decide the look of the corner connecting walls

    Attributes:
        bit: bit value for the corner representing the sides it has
    """

    def __init__(self) -> None:
        """constructor of the Corner class"""
        self.bit = 0


class Cell:
    """cell class that has all the attributes of the cell

    Attributes:
        bit_value: the bit value of the cell representing which  walls are open
        top_left: top left corner
        top_right: top right corner
        bottom_left: bottom left corner
        bottom_right: bottom right corner
    """

    def __init__(
        self, bit_value: int, corners: list[Corner], content: Any, cord: tuple
    ) -> None:
        """constructor of the Cell class

        Args:
            bit: bit value of the cell
            corners: list of corners surrounding the cell
        """
        self.bit_value = bit_value
        self.content: Gum | SuperGum | None = None
        self.top_left = corners[0]
        self.top_right = corners[1]
        self.bottom_left = corners[2]
        self.bottom_right = corners[3]
        self.update_corners()
        self.content = content
        self.cord = cord

    def update_corners(self) -> None:
        """mask the corner bit value according to the bit value of the cell
        top left corner will have an east side if the cell has a north wall
        and a south side if the cell has a west wall
        top right corner will have a west side if the cell has a north wall
        and a south side if the cell has an east wall
        bottom right corner will have north side if the cell has an east
        wall and a west side if the cell has a south wall
        bottom left corner  will have a north side if the cell has a west
        wall and an east side if the cell has a south wall
        """
        self.top_left.bit |= (1 & self.bit_value) << 1
        self.top_left.bit |= (8 & self.bit_value) >> 1
        self.top_right.bit |= (1 & self.bit_value) << 3
        self.top_right.bit |= (2 & self.bit_value) << 1
        self.bottom_right.bit |= (2 & self.bit_value) >> 1
        self.bottom_right.bit |= (4 & self.bit_value) << 1
        self.bottom_left.bit |= (4 & self.bit_value) >> 1
        self.bottom_left.bit |= (8 & self.bit_value) >> 3


class Character(ABC):
    def __init__(
        self,
        speed: int,
        origin: tuple,
        maze: list[list[Cell]],
        anchors: list = [],
    ) -> None:
        self.id = 0
        self.maze = maze
        self.speed = speed
        self.v_step = 64
        self.half_v_step = 32
        self.max_y = len(self.maze) * self.v_step
        self.max_x = len(self.maze[0]) * self.v_step
        self.origin = origin

    @abstractmethod
    def get_sprite(self, frame: int) -> pygame.Surface: ...

    @abstractmethod
    def move(self, frame: int) -> pygame.Surface: ...

    @abstractmethod
    def update_visual_cord(self) -> None: ...

    @abstractmethod
    def choose_direction(self) -> None: ...

    @abstractmethod
    def reset_cords(self) -> None: ...

    @abstractmethod
    def die(self) -> None: ...


class Gum:
    def __init__(
        self,
        score: int,
        cord: tuple,
        sprite: pygame.Surface,
        is_super: bool = False,
    ) -> None:
        self.is_super = is_super
        self.score = score
        self.cord = cord
        self.sprite = sprite


class SuperGum(Gum):
    def __init__(
        self, score: int, cord: tuple, sprite: pygame.Surface
    ) -> None:
        super().__init__(score, cord, sprite, True)
