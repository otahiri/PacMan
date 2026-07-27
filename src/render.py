import pygame
from src.enums import Asset


class Renderer:
    def __init__(self, screen_w: int, screen_h: int) -> None:
        self.__window = pygame.display.set_mode(
            (screen_w, screen_h),
            pygame.RESIZABLE,
        )
        print("initialize Renderer")

        # self.old_screen_w = screen_w
        # self.old_screen_h = screen_h

        self.screen_w = screen_w
        self.screen_h = screen_h

    def clear(self):
        self.__window.fill((0, 0, 0))

    # def is_window_changed(self):
    #     h_changed = self.old_screen_h != self.screen_h
    #     w_changed = self.old_screen_w != self.screen_w
    #     return h_changed or w_changed

    def get_resolution(self):
        return self.screen_w, self.screen_h

    def set_new_resolution(self, w: int, h: int):
        self.screen_w, self.screen_h = w, h

    def draw_debug(self):
        pygame.draw.line(
            self.__window,
            "red",
            (0, self.screen_h // 2),
            (self.screen_w, self.screen_h // 2),
        )
        pygame.draw.line(
            self.__window,
            "red",
            (self.screen_w // 2, 0),
            (self.screen_w // 2, self.screen_h),
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

    def get_pos(
        self,
        pos: tuple[int, int],
        size: tuple[int, int],
        anchor: str,
    ) -> tuple[int, int]:

        x, y = pos
        width, height = size
        match anchor.lower():
            # Left anchors
            case "topleft" | "lefttop":
                return (x, y)
            case "centerleft" | "leftcenter":
                return (x, y - height // 2)
            case "bottomleft" | "buttomleft":  # includes your typo safeguard
                return (x, y - height)

            # Center anchors
            case "topcenter" | "centertop":
                return (x - width // 2, y)
            case "center":
                return (x - width // 2, y - height // 2)
            case "bottomcenter" | "centerbottom" | "buttomcenter":
                return (x - width // 2, y - height)

            # Right anchors
            case "topright":
                return (x - width, y)
            case "centerright" | "rightcenter":
                return (x - width, y - height // 2)
            case "bottomright" | "buttomright":
                return (x - width, y - height)

            case _:
                raise ValueError(f"anchor value unknown {anchor}")

    def render(
        self,
        source: pygame.Surface,
        pos: tuple[int, int],
        size: tuple[int, int],
        anchor: str = "center",
    ):
        pos = self.get_pos(pos, size, anchor)
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
        # self.screen_w, self.screen_h = self.old_screen_w, self.old_screen_h
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
            if (c.isalpha() or c.isdigit()) and c != " ":
                letter_path = path + "/" + c + ".png"
                letter_surface = pygame.image.load(letter_path)
                scaled_letter = cls.scale_surface(
                    letter_surface, (width, height), scale, color
                )

                for y in range(height * scale):
                    for x in range(width * scale):
                        pixel_color = scaled_letter.get_at((x, y))
                        if pixel_color.a > 0:
                            new_surface.set_at((x_shift + x, y), pixel_color)

            x_shift += width * scale + Asset.LETTER_SPACING.value

        return (new_surface, (surface_width, surface_height))
