import pygame
import numpy as np
from src.enums import Asset, ColorTheme, DisplayInfo
from webcolors import name_to_hex


class Renderer:
    def __init__(self) -> None:

        self.__window = pygame.display.set_mode(
            (DisplayInfo.SCREEN_WIDTH.value, DisplayInfo.SCREEN_HEIGHT.value),
        )
        print("initialize Renderer")

    def clear(self) -> None:
        secondary, primary = ColorTheme.ONE.value

        self.__window.fill(secondary)

    @staticmethod
    def custom_blit(
        dest: pygame.Surface,
        src: pygame.Surface,
        pos: tuple,
    ) -> None:
        dest_px = pygame.surfarray.pixels2d(dest)
        dest_dim = dest_px.shape
        src_px = pygame.surfarray.pixels2d(src)
        src_dim = src_px.shape
        start_x = max(0, pos[0])
        start_y = max(0, pos[1])
        end_x = min(pos[0] + src_dim[0], dest_dim[0])
        end_y = min(pos[1] + src_dim[1], dest_dim[1])
        src_start_x = start_x - pos[0]
        src_start_y = start_y - pos[1]
        src_end_x = src_start_x + (end_x - start_x)
        src_end_y = src_start_y + (end_y - start_y)
        if start_x < end_x and start_y < end_y:
            view_src = src_px[src_start_x:src_end_x, src_start_y:src_end_y]
            view_dest = dest_px[start_x:end_x, start_y:end_y]
            mask = view_src != 0
            view_dest[mask] = view_src[mask]

        del dest_px
        del src_px

    @staticmethod
    def fill(dest: pygame.Surface, color: str) -> None:
        color_hex = name_to_hex(color)[1:]
        dest_px = pygame.surfarray.pixels2d(dest)
        colored_rect = np.full_like(dest_px, color_hex)
        mask = dest_px != 0
        dest_px[mask] = colored_rect[mask]
        del colored_rect
        del dest_px

    def draw_debug(self) -> None:
        pygame.draw.line(
            self.__window,
            "red",
            (
                0,
                DisplayInfo.SCREEN_HEIGHT.value // 2,
            ),
            (
                DisplayInfo.SCREEN_WIDTH.value,
                DisplayInfo.SCREEN_HEIGHT.value // 2,
            ),
        )
        pygame.draw.line(
            self.__window,
            "red",
            (
                DisplayInfo.SCREEN_WIDTH.value // 2,
                0,
            ),
            (
                DisplayInfo.SCREEN_WIDTH.value // 2,
                DisplayInfo.SCREEN_HEIGHT.value,
            ),
        )

    @classmethod
    def change_color(
        cls, source: pygame.Surface, size: tuple[int, int]
    ) -> pygame.Surface:
        width, height = size
        result = pygame.Surface(
            size,
            pygame.SRCALPHA,
        )
        primary, secondary = ColorTheme.ONE.value
        for pixel_x in range(width):
            for pixel_y in range(height):
                r, g, b, a = source.get_at((pixel_x, pixel_y))
                if not a:
                    continue
                if (r + g + b) / 3 >= 128:
                    result.set_at(
                        (pixel_x, pixel_y),
                        secondary,
                    )
                else:
                    result.set_at((pixel_x, pixel_y), primary)
        return result

    @classmethod
    def get_button(
        cls,
    ) -> tuple[pygame.Surface, pygame.Surface, tuple[int, int]]:

        size = (Asset.BUTTON_WIDTH.value, Asset.BUTTON_HEIGHT.value)

        idel = pygame.image.load("assets/button/idel.png")
        idel = cls.change_color(idel, size)
        hover = pygame.image.load("assets/button/hover.png")
        hover = cls.change_color(hover, size)

        return (idel, hover, size)

    @classmethod
    def get_pos(
        cls,
        pos: tuple[int, int],
        size: tuple[int, int],
        anchor: str = "center",
    ) -> tuple[int, int]:

        x, y = pos
        width, height = size
        match anchor.lower():
            # Left anchors
            case "topleft" | "lefttop":
                return (x, y)
            case "centerleft" | "leftcenter":
                return (x, y - height // 2)
            case "bottomleft" | "leftbottom":  # includes your typo safeguard
                return (x, y - height)

            # Center anchors
            case "topcenter" | "centertop":
                return (x - width // 2, y)
            case "center":
                return (x - width // 2, y - height // 2)
            case "bottomcenter" | "centerbottom" | "bottomcenter":
                return (x - width // 2, y - height)

            # Right anchors
            case "topright":
                return (x - width, y)
            case "centerright" | "rightcenter":
                return (x - width, y - height // 2)
            case "bottomright" | "rightbottom":
                return (x - width, y - height)

            case _:
                raise ValueError(f"anchor value unknown {anchor}")

    @staticmethod
    def rotate_surf(surf: pygame.Surface, degree: int) -> pygame.Surface:
        surf_px = pygame.surfarray.pixels2d(surf)
        new_array = np.rot90(surf_px, degree)
        new_surf = pygame.Surface(new_array.shape)
        Renderer.fill(new_surf, "black")
        mask = new_array != 0
        new_surf_px = pygame.surfarray.pixels2d(new_surf)
        new_surf_px[mask] = new_array[mask]
        del new_surf_px
        del surf_px
        return new_surf

    def render(
        self,
        source: pygame.Surface,
        pos: tuple[int, int],
    ) -> None:
        self.__window.blit(source, pos)

    @classmethod
    def scale_surface(
        cls,
        src_image: pygame.Surface,
        size: tuple[int, int],
        scale: int,
        color: str | None = None,
    ) -> pygame.Surface:
        orig_w, orig_h = size
        new_w = orig_w * scale
        new_h = orig_h * scale

        scaled_surface = pygame.Surface((new_w, new_h), pygame.SRCALPHA)
        secondary, primary = ColorTheme.ONE.value

        for y in range(new_h):
            for x in range(new_w):
                src_x = int(x * (orig_w / new_w))
                src_y = int(y * (orig_h / new_h))

                r, g, b, a = src_image.get_at((src_x, src_y))

                if a == 0:  # skip transparent pixels
                    continue
                if (r + g + b) / 3 >= 128:
                    scaled_surface.set_at(
                        (x, y),
                        primary,
                    )
                else:
                    scaled_surface.set_at((x, y), secondary)

        return scaled_surface

    def update_window(self) -> None:
        pygame.display.flip()

    @classmethod
    def get_text(
        cls, text: str, primary_color: bool = True
    ) -> tuple[pygame.Surface, tuple[int, int]]:
        """Build a surface by concatenating per-character sprite images.

        Args:
            text: Alphanumeric text to render using letter sprites.

        Returns:
            A tuple containing:
                - The rendered text surface.
                - The rendered surface size as (width, height).
        """
        path = Asset.LETTER_PATH.value
        color = (
            ColorTheme.ONE.value[0]
            if primary_color
            else ColorTheme.ONE.value[1]
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

        for letter in text:
            if (letter.isalpha() or letter.isdigit()) and letter != " ":
                letter_path = path + "/" + letter + ".png"
                letter_surface = pygame.image.load(letter_path)

                # copy letter surf pixel by pixel to the dest surf
                for pixel_y in range(letter_height):
                    for pixel_x in range(letter_width):
                        _, _, _, alpha = letter_surface.get_at(
                            (pixel_x, pixel_y)
                        )
                        if not alpha:
                            continue

                        result_surface.set_at(
                            (x_shift + pixel_x, pixel_y),
                            color,
                        )

            x_shift += letter_width + letter_spacing

        return (result_surface, (surface_width, surface_height))
