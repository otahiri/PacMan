import pygame

from src.enums import Asset, DisplayInfo


class Renderer:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode(
            (DisplayInfo.SCREEN_WIDTH.value, DisplayInfo.SCREEN_HEIGHT.value)
        )
        print("initialize Renderer")

    def clear(self):
        self.window.fill("black")

    @classmethod
    def get_button(cls):
        size = (32, 11)
        new_size = (32 * 10, 11 * 10)

        idel = cls.__scale_surface(
            pygame.image.load("assets/button/idel.png"), size, 10
        )
        hover = cls.__scale_surface(
            pygame.image.load("assets/button/hover.png"), size, 10
        )
        return (idel, hover, new_size)

    def render(self, source, pos):
        self.window.blit(source, pos)

    @classmethod
    def __scale_surface(
        cls, src_image: pygame.Surface, size: tuple[int, int], scale: int
    ):
        orig_w, orig_h = size
        new_w = orig_w * scale
        new_h = orig_h * scale

        scaled_surface = pygame.Surface((new_w, new_h))
        for y in range(new_h):
            for x in range(new_w):
                src_x = int(x * (orig_w / new_w))
                src_y = int(y * (orig_h / new_h))

                color = src_image.get_at((src_x, src_y))
                if color == pygame.Color(255, 255, 255, 255):
                    scaled_surface.set_at((x, y), color)
                else:
                    pass

        return scaled_surface

    def update_window(self):
        pygame.display.flip()

    @classmethod
    def get_text(
        cls, text: str, scale: int
    ) -> tuple[pygame.Surface, tuple[int, int]]:

        path = Asset.LETTER_PATH.value
        width = Asset.LETTER_WIDTH.value
        height = Asset.LETTER_HEIGHT.value
        surface_height = height * scale
        spacing_width = Asset.LETTER_SPACING.value * (len(text) - 1)
        surface_width = (width * scale) * len(text) + spacing_width
        new_surface = pygame.Surface((surface_width, surface_height))

        x_pos = 0
        for c in text:
            if c.isalpha() and c != " ":
                letter_path = path + "/" + c + ".png"
                letter_surface = pygame.image.load(letter_path)
                scaled_letter = cls.__scale_surface(
                    letter_surface, (width, height), scale
                )
                new_surface.blit(
                    scaled_letter,
                    (x_pos, 0),
                )

            x_pos += width * scale + Asset.LETTER_SPACING.value

        return (new_surface, (surface_width, surface_height))
