"""Models and UI widgets used across the game.

This module contains small UI components and core game models such as
`Cell`, `Corner`, `Character`, `Gum` and related helper classes used by
the game scenes and renderer.
"""

from typing import Any
import pygame
from abc import ABC, abstractmethod
from src.enums import AnchorPoint, Asset, ColorType, DisplayInfo
from src.render import Renderer


class Button:
    """A clickable button composed of a background and text.

    Args:
        name: Button label.
        pos: (x, y) position for the button on screen.
    """

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
        """Return True if the given `pos` is inside the button bounds.

        Args:
            pos: Target (x, y) position to test.

        Returns:
            True when the point lies within the button.
        """
        my_x, my_y = self.pos
        target_x, target_y = pos
        is_inside_x = my_x <= target_x <= (my_x + self.width)
        is_inside_y = my_y <= target_y <= (my_y + self.height)
        return is_inside_x and is_inside_y

    def switch_state(self) -> None:
        """Toggle the internal `button_state` flag."""
        self.button_state = not self.button_state

    def render(self, renderer: Renderer) -> None:
        """Render the button using the provided `Renderer`.

        The method will draw either the `text_on` or `text_off` variant
        depending on the `button_state`.

        Args:
            renderer: Renderer instance used to blit surfaces.
        """
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
    """Renderable text containing sequence letters sprites.

    Args:
        label: The string to render.
        pos: Position to render the text.
        color_type: Color theme to use for the rendered text.
        anchor_point: Anchor used when computing the destination position.
    """

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
    """A title bar used by scenes to display a heading.

    Args:
        label: Title text to display.
        pos: Either 'top' or 'center' to position the title vertically.
        hide_top: When True, render a background strip.
    """

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
        """Draw the title bar and optional background to the display.

        Args:
            renderer: Renderer instance used to blit the surfaces.
        """
        if self.hide_top:
            renderer.render(self.bg, self.bg_pos)

        renderer.render(self.bar_surf, self.bar_pos)

        renderer.render(
            self.text.surf,
            Renderer.get_pos(self.text.pos, self.text.size),
        )


class AnimatedBar:
    """Animated text bar that scrolls horizontally across the screen.

    Args:
        label: Text label to display in the bar.
        gap: Distance between the two moving text copies.
        speed: Scroll speed of the animation.
    """

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
        """Reset the positions of animated text to the initial state."""
        screen_width = DisplayInfo.SCREEN_WIDTH.value

        self.x1 = screen_width + screen_width // 2
        self.x2 = self.x1 - self.text_width - self.gap

    def render(self, renderer: Renderer, delta: float) -> None:
        """Render the animated bar.

        Args:
            renderer: Renderer used to draw the bar and text.
            delta: Time delta used to compute movement.
        """
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
    """A single keyboard letter rendered as a button.

    Args:
        surf: Surface for the letter.
        letter: The character represented by this button.
        pos: Position to render the button.
        size: Size of the letter.
        place: Grid position inside the keyboard layout.
    """

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
        """Return True if the given `pos` collides with this letter button.

        Args:
            pos: Point to test in screen coordinates.

        Returns:
            True when the point is within the visual bounds of the button.
        """
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
    """On-screen keyboard composed of `LetterButton` items and cursor."""

    def __init__(self) -> None:
        self.letters: list[LetterButton] = []
        self.cursor = Cursor()
        self.__set_keyboard_letters()

    def __set_keyboard_letters(
        self,
    ) -> None:
        """Create and place `LetterButton` instances for the keyboard layout."""

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

    def render(self, renderer: Renderer) -> None:
        """Render keyboard (all letters) and the cursor onto the given renderer.

        Args:
            renderer: Renderer used to draw the keyboard.
        """
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
    """Visual cursor used by the on-screen keyboard."""

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
    """Container for the player's name input frame."""

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
        """Append `letter` to the current name and update the rendered text.

        Args:
            letter: Single character to append to the `name` string.
        """
        self.name += letter
        self.text = Text(self.name, self.pos, ColorType.PRIMARY)


class Scene(ABC):
    """Abstract base class for all game scenes.

    Subclasses define how a scene renders itself and how it responds to
    incoming events.
    """

    @abstractmethod
    def render_scene(self, renderer: Renderer) -> None:
        """Render the scene to the provided renderer.

        Args:
            renderer: Renderer used to display the scene.
        """
        ...

    @abstractmethod
    def handle_events(self, events: list[pygame.Event]) -> dict[str, Any]:
        """Handle a list of pygame events and return action data.

        Args:
            events: Events emitted by pygame for the current frame.

        Returns:
            Dictionary containing scene actions such as transitions or updates.
        """
        ...


class Corner:
    """corner object to decide the look of the corner connecting walls

    Attributes:
        bit: bit value for the corner representing the sides it has
    """

    def __init__(self) -> None:
        self.bit = 0


class Cell:
    """cell class that has all the attributes of the cell

    Args:
        bit: bit value of the cell
        corners: list of corners surrounding the cell

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
    """Abstract base class for all moving game characters.

    This includes the player and all ghosts, which share movement,
    animation and coordinate management methods.

    Args:
        speed: Movement speed in grid units.
        origin: Starting (x, y) coordinate for the character.
        maze: Cell grid used for navigation.
        anchors: Optional helper anchors or reference objects.
    """

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
    def get_sprite(self, frame: int) -> pygame.Surface:
        """Return the sprite for the current frame.

        Args:
            frame: Current animation frame index.

        Returns:
            The rendered sprite surface for this character.
        """
        ...

    @abstractmethod
    def move(self, frame: int) -> pygame.Surface:
        """Advance the character state and return its sprite.

        Args:
            frame: Current frame value used for animation timing.

        Returns:
            The sprite surface after updating the character position.
        """
        ...

    @abstractmethod
    def update_visual_cord(self) -> None:
        """Sync the visual position with the character's internal state."""
        ...

    @abstractmethod
    def choose_direction(self) -> None:
        """Choose the next movement direction based on the current state."""
        ...

    @abstractmethod
    def reset_cords(self) -> None:
        """Reset the character to its initial position and state."""
        ...

    @abstractmethod
    def die(self) -> None:
        """Trigger the character's death state."""
        ...


class Gum:
    """collectible item placed within the maze.

    Args:
        score: Points awarded when the gum is collected.
        cord: Grid coordinate of the gum.
        sprite: Surface used to render the gum.
        is_super: Whether this gum is a super-powered variant.
    """

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
    """Special collectible that temporarily frightens ghosts.

    Args:
        score: Points awarded when the super-gum is collected.
        cord: Grid coordinate of the super-gum.
        sprite: Surface used to render the super-gum.
    """

    def __init__(
        self, score: int, cord: tuple, sprite: pygame.Surface
    ) -> None:
        super().__init__(score, cord, sprite, True)
