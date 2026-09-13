"""render module is responsible for interacting with the main display
and load images and edit them
"""

import pygame
import numpy as np
from src.enums import AnchorPoint, Asset, ColorType, DisplayInfo


class Renderer:
    """Renderer class responsible for the graphics

    Attributes:
        colors: colors list containing background color and foreground color
        primary, secondary: chosen background and foreground colors
        LETTER: dictionary containing all lettters pre loaded
    """

    colors = [
        ("FFEDF6D6", "003E232C"),
        ("FFD3C9A1", "00323C39"),
        ("FFAFB0B0", "002E253D"),
        ("FFD7BCAD", "00452F47"),
    ]
    primary, secondary = colors[0]
    LETTER: dict = dict()

    def __init__(self, color_schema: int) -> None:
        """constructor for the Renderer class

        Args:
            color_schema: index for the chosen color theme
        """
        self.__window = pygame.display.set_mode(
            (DisplayInfo.SCREEN_WIDTH.value, DisplayInfo.SCREEN_HEIGHT.value),
            pygame.SRCALPHA,
        )

        if color_schema >= len(self.colors):
            color_schema = len(self.colors) - 1
        Renderer.primary, Renderer.secondary = Renderer.colors[color_schema]
        Renderer.LETTER = {
            c: pygame.image.load(
                f"{Asset.LETTER_PATH.value}/{c}.png"
            ).convert_alpha()
            for c in "0123456789abcdefghijklmnopqrstuvwxyz-E"
        }
        Renderer.LETTER[" "] = pygame.image.load(
            f"{Asset.LETTER_PATH.value}/space.png"
        )
        print("initialize Renderer")

    def clear(self) -> None:
        """clear main display"""
        Renderer.fill(self.__window, ColorType.SECONDARY)

    @staticmethod
    def load_image(img: str) -> pygame.Surface:
        """image loader

        Args:
            img: load image and call change color function

        Returns:
            suface object with image on it with correct colors
        """
        return Renderer.change_color(pygame.image.load(img).convert_alpha())

    @staticmethod
    def fill(dest: pygame.surface.Surface, color: ColorType) -> None:
        """fill dest surface with  chosen color

        Args:
            dest: surface to fill
            color_hex: hex value of color
        """
        color_hex = (
            Renderer.primary
            if color is ColorType.PRIMARY
            else Renderer.secondary
        )
        dest_px = pygame.surfarray.pixels2d(dest)
        dest_px.fill(int(color_hex, 16))
        del dest_px

    @classmethod
    def change_color(cls, source: pygame.surface.Surface) -> pygame.Surface:
        """change color of the surface to match the chosen color theme

        Args:
            source: suface with black and white

        Returns:
            new surface with appropriate colors
        """
        px = pygame.surfarray.pixels2d(source)
        result = pygame.Surface(px.shape, pygame.SRCALPHA)
        result_px = pygame.surfarray.pixels2d(result)
        mask = px == 4294967295
        dark_mask = px == 4278190080
        result_px[mask] = int(Renderer.primary, 16)
        result_px[dark_mask] = int(Renderer.secondary, 16)
        del result_px, px
        return result

    @classmethod
    def get_button(
        cls,
    ) -> tuple[pygame.Surface, tuple[int, int]]:
        """get button sprite

        Returns:
            tuple with surface and the size of the button
        """
        size = (Asset.BUTTON_WIDTH.value, Asset.BUTTON_HEIGHT.value)

        surf = Renderer.load_image(f"{Asset.BUTTON_PATH.value}.png")

        return (surf, size)

    @classmethod
    def get_pos(
        cls,
        pos: tuple[int, int],
        size: tuple[int, int],
        anchor: AnchorPoint = AnchorPoint.CENTER,
    ) -> tuple[int, int]:
        """get position offset for the

        Args:
            pos: current position
            size: size of the surface
            anchor: offset variable

        Returns:
            new offsetted position
        """
        x, y = pos
        width, height = size
        match anchor:
            case AnchorPoint.CENTER:
                return (x - width // 2, y - height // 2)
            case AnchorPoint.TOP_LEFT:
                return (x, y)
            case AnchorPoint.TOP_RIGHT:
                return (x - width, y)
            case AnchorPoint.BOTTOM_LEFT:
                return (x, y - height)
            case AnchorPoint.BOTTOM_RIGHT:
                return (x - width, y - height)
            case AnchorPoint.CENTER_LEFT:
                return (x, y - height // 2)
            case AnchorPoint.CENTER_RIGHT:
                return (x - width, y - height // 2)
            case AnchorPoint.TOP_CENTER:
                return (x - width // 2, y)
            case AnchorPoint.BOTTOM_CENTER:
                return (x - width // 2, y - height)

    @staticmethod
    def rotate_surf(surf: pygame.Surface, degree: int) -> pygame.Surface:
        surf_px = pygame.surfarray.pixels2d(surf)
        rotated_array = np.rot90(surf_px, degree)
        new_surf = pygame.Surface(rotated_array.shape, pygame.SRCALPHA)
        mask = rotated_array != int(Renderer.secondary, 16)
        new_surf_px = pygame.surfarray.pixels2d(new_surf)
        new_surf_px[mask] = rotated_array[mask]
        del new_surf_px
        del surf_px
        return new_surf

    def render(
        self,
        source: pygame.Surface,
        pos: tuple[int, int],
    ) -> None:
        self.__window.blit(source, pos)

    def update_window(self) -> None:
        pygame.display.flip()

    @classmethod
    def get_text(
        cls, text: str, color_type: ColorType
    ) -> tuple[pygame.Surface, tuple[int, int]]:
        """Build a surface by concatenating per-character sprite images.

        Args:
            text: Alphanumeric text to render using letter sprites.

        Returns:
            A tuple containing:
                - The rendered text surface.
                - The rendered surface size as (width, height).
        """
        bg_color, fg_color = (
            (int(Renderer.secondary, 16), int(Renderer.primary, 16))
            if color_type == ColorType.PRIMARY
            else (int(Renderer.primary, 16), int(Renderer.secondary, 16))
        )
        letter_width = Asset.LETTER_WIDTH.value
        letter_height = Asset.LETTER_HEIGHT.value
        letter_spacing = Asset.LETTER_SPACING.value

        spacing_width = letter_spacing * (len(text) - 1)

        surface_width = (letter_width) * len(text) + spacing_width
        surface_height = letter_height

        result_surface = pygame.Surface(
            (surface_width, letter_height), pygame.SRCALPHA
        )
        x_shift = 0

        for chr in text:
            if chr.isalnum() or chr == "-":
                letter_surface = Renderer.LETTER[chr]
                letter_surf_px = pygame.surfarray.pixels2d(letter_surface)
                letter = pygame.Surface(letter_surf_px.shape)
                letter_px = pygame.surfarray.pixels2d(letter)
                letter_px.fill(bg_color)
                mask = letter_surf_px == 4294967295
                letter_px[mask] = fg_color
                del letter_px, letter_surf_px
                result_surface.blit(letter, (x_shift, 0))
            x_shift += letter_width + letter_spacing

        return (result_surface, (surface_width, surface_height))
