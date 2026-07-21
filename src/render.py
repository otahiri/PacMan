import pygame


class Renderer:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode((1280, 1280))
        print("initialize Renderer")

    def clear(self):
        self.window.fill("black")

    @classmethod
    def get_button(cls):
        size = (32, 11)
        new_size = (32 * 10, 11 * 10)

        idel = cls.__scale_surface(
            pygame.image.load("assets/button/idel.png"), size, new_size
        )
        hover = cls.__scale_surface(
            pygame.image.load("assets/button/hover.png"), size, new_size
        )
        return (idel, hover, new_size)

    def render(self, source, pos):
        self.window.blit(source, pos)

    @classmethod
    def __scale_surface(cls, src_image, size, new_size):
        orig_w, orig_h = size
        new_w, new_h = new_size

        scaled_surface = pygame.Surface((new_w, new_h))

        for y in range(new_h):
            for x in range(new_w):
                src_x = int(x * (orig_w / new_w))
                src_y = int(y * (orig_h / new_h))

                color = src_image.get_at((src_x, src_y))
                scaled_surface.set_at((x, y), color)

        return scaled_surface

    def update_window(self):
        pygame.display.flip()

    @classmethod
    def get_text(cls, text):
        result = []
        for c in text:
            result.append(
                cls.__scale_surface(
                    pygame.image.load(f"assets/letters/{c}.png"),
                    (8, 16),
                    (8 * 5, 16 * 5),
                )
            )
        return result
