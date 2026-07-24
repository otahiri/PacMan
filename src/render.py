import pygame
from src.enums import Asset, DisplayInfo


class Renderer:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode(
            (DisplayInfo.SCREEN_WIDTH.value, DisplayInfo.SCREEN_HEIGHT.value),
        )
        print("initialize Renderer")

    def clear(self):
        self.window.fill((0, 0, 0))

    def draw_debug(self):
        pygame.draw.line(
            self.window,
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
            self.window,
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

        idel = cls.__scale_surface(
            pygame.image.load("assets/button/idel.png"), size, scale
        )
        hover = cls.__scale_surface(
            pygame.image.load("assets/button/hover.png"), size, scale
        )
        return (idel, hover, new_size)

    def render(self, source, pos):
        self.window.blit(source, pos)

    @classmethod
    def __scale_surface(
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

        for y in range(new_h):
            for x in range(new_w):
                src_x = int(x * (orig_w / new_w))
                src_y = int(y * (orig_h / new_h))

                pixel_color = src_image.get_at((src_x, src_y))

                if pixel_color.a == 0:  # skip transparent pixels
                    continue
                scaled_surface.set_at((x, y), color if color else pixel_color)

        return scaled_surface

    def update_window(self):
        pygame.display.flip()

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
            if c.isalpha() and c != " ":
                letter_path = path + "/" + c + ".png"
                letter_surface = pygame.image.load(letter_path)
                scaled_letter = cls.__scale_surface(
                    letter_surface, (width, height), scale, color
                )

                for y in range(height * scale):
                    for x in range(width * scale):
                        pixel_color = scaled_letter.get_at((x, y))
                        if pixel_color.a > 0:
                            new_surface.set_at((x_shift + x, y), pixel_color)

            x_shift += width * scale + Asset.LETTER_SPACING.value

        return (new_surface, (surface_width, surface_height))
