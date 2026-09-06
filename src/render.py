import pygame
import numpy as np
from src.enums import Asset, DisplayInfo


class Renderer:
    COLOR_SCHEMES = [
        ("000000", "ffffff"),
        ("292b30", "cfab4a"),
        ("25342f", "01eb5f"),
        ("323c39", "d3c9a1"),
        ("1d0f44", "f44e38"),
        ("702963", "ffbf00"),
        ("10368f", "ff8e42"),
    ]
    BG: str = "000000"
    FG: str = "ffffff"

    def __init__(self, color_scheme_idx: int) -> None:
        try:
            Renderer.BG = Renderer.COLOR_SCHEMES[color_scheme_idx][0]
            Renderer.FG = Renderer.COLOR_SCHEMES[color_scheme_idx][1]
        except IndexError:
            pass

        self.__window: pygame.surface.Surface = pygame.display.set_mode(
            (DisplayInfo.SCREEN_WIDTH.value, DisplayInfo.SCREEN_HEIGHT.value),
        )

        print("initialize Renderer")

    def clear(self):
        self.fill(self.__window, Renderer.BG)

    @staticmethod
    def load_image(path: str) -> pygame.Surface:
        image = pygame.image.load(path).convert()
        image_px = pygame.surfarray.pixels2d(image)
        bg_mask = image_px == 0
        fg_mask = image_px != 0
        image_px[bg_mask] = int(Renderer.BG, 16)
        image_px[fg_mask] = int(Renderer.FG, 16)
        del image_px
        return image

    @staticmethod
    def fill(dest: pygame.Surface | pygame.surface.Surface, color: str):
        color_val = int(color, 16)
        dest_px = pygame.surfarray.pixels2d(dest)
        colored_rect = np.full_like(dest_px, color_val)
        mask = dest_px != color_val
        dest_px[mask] = colored_rect[mask]
        del colored_rect
        del dest_px

    def draw_debug(self):
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
    def get_button(
        cls, scale: int
    ) -> tuple[pygame.Surface, pygame.Surface, tuple[int, int]]:

        size = (Asset.BUTTON_WIDTH.value, Asset.BUTTON_HEIGHT.value)
        new_size = (
            Asset.BUTTON_WIDTH.value * scale,
            Asset.BUTTON_HEIGHT.value * scale,
        )

        idel = cls.scale_surface(
            pygame.image.load("assets/button/idel.png"), size, scale
        )
        hover = cls.scale_surface(
            pygame.image.load("assets/button/hover.png"), size, scale
        )
        return (idel, hover, new_size)

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
        Renderer.fill(new_surf, Renderer.BG)
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
    ):
        self.blit(self.__window, source, pos)

    @classmethod
    def scale_surface(
        cls,
        src_image: pygame.Surface | pygame.surface.Surface,
        size: tuple[int, int],
        scale: int,
        color: str | None = None,
    ) -> pygame.Surface:
        orig_w, orig_h = size
        new_w = orig_w * scale
        new_h = orig_h * scale

        scaled_surface = pygame.Surface((new_w, new_h), pygame.SRCALPHA)

        for y in range(new_h):
            for x in range(new_w):
                src_x = int(x * (orig_w / new_w))
                src_y = int(y * (orig_h / new_h))

                pixel_color = src_image.get_at((src_x, src_y))

                if pixel_color[3] == 0:  # skip transparent pixels
                    continue
                scaled_surface.set_at((x, y), color if color else pixel_color)

        return scaled_surface

    def update_window(self):
        pygame.display.flip()

    @staticmethod
    def blit(
        dest: pygame.Surface | pygame.surface.Surface,
        src: pygame.Surface | pygame.surface.Surface,
        cord: tuple,
    ) -> None:
        dest.blit(src, cord)

    @classmethod
    def get_text(
        cls, text: str, scale: int, color: str
    ) -> tuple[pygame.Surface, tuple[int, int]]:
        path = Asset.LETTER_PATH.value
        width = Asset.LETTER_WIDTH.value
        height = Asset.LETTER_HEIGHT.value
        surface_height = height * scale
        spacing_width = Asset.LETTER_SPACING.value * (len(text) - 1)
        surface_width = (width * scale) * len(text) + spacing_width
        new_surface = pygame.Surface(
            (surface_width, surface_height), pygame.SRCALPHA
        )
        x_shift = 0

        for c in text:
            if (c.isalpha() or c.isdigit()) and c != " ":
                letter_path = path + "/" + c + ".png"
                letter_surface = pygame.image.load(letter_path)
                scaled_letter = cls.scale_surface(
                    letter_surface, (width, height), scale, color
                )
                for y in range(height * scale):
                    for x in range(width * scale):
                        pixel_color = scaled_letter.get_at((x, y))
                        if pixel_color[3] > 0:
                            new_surface.set_at((x_shift + x, y), pixel_color)

            x_shift += width * scale + Asset.LETTER_SPACING.value

        return (new_surface, (surface_width, surface_height))
